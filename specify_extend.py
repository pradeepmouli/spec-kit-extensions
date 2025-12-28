#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "httpx",
# ]
# ///
"""
specify-extend - Installation tool for spec-kit-extensions

Works alongside GitHub spec-kit's `specify init` command.
Detects agent configuration and mirrors the installation.

Usage:
    python specify_extend.py --all
    python specify_extend.py bugfix modify refactor
    python specify_extend.py --agent claude --all
    python specify_extend.py --dry-run --all
    python specify_extend.py --all --github-integration

Or install globally:
    uv tool install --from specify_extend.py specify-extend
    specify-extend --all
    specify-extend --all --github-integration
"""

import os
import sys
import shutil
import subprocess
import tempfile
import zipfile
import re
from pathlib import Path
from typing import Optional, List, Tuple
from enum import Enum
from datetime import datetime, timezone

import typer
import httpx
import ssl
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

__version__ = "1.5.5"

# Initialize Rich console
console = Console()

# Set up SSL context for HTTPS requests
ssl_context = ssl.create_default_context()

# Set up HTTPS client for GitHub API requests with SSL verification
client = httpx.Client(follow_redirects=True, verify=ssl_context)

# Constants
GITHUB_REPO_OWNER = "pradeepmouli"
GITHUB_REPO_NAME = "spec-kit-extensions"
GITHUB_REPO = f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
GITHUB_API_BASE = "https://api.github.com"

# Workflow extensions: Create workflow directories with specs, plans, and tasks
WORKFLOW_EXTENSIONS = ["baseline", "bugfix", "enhance", "modify", "refactor", "hotfix", "deprecate", "cleanup"]

# Command extensions: Provide commands without creating workflow directories
COMMAND_EXTENSIONS = ["review", "incorporate"]

# All available extensions for validation and documentation
AVAILABLE_EXTENSIONS = WORKFLOW_EXTENSIONS + COMMAND_EXTENSIONS

# Detection thresholds for workflow selection content
MIN_SECTION_HEADERS = 2  # Minimum section headers to detect existing workflow content
MIN_WORKFLOW_COMMANDS = 3  # Minimum workflow commands to detect existing workflow content

# Section header patterns for parsing constitutions
ROMAN_NUMERAL_PATTERN = r'^###\s+([IVXLCDM]+)\.'
NUMERIC_SECTION_PATTERN = r'^###\s+(\d+)\.'

# Markdown formatting constants
HEADER_PREFIX_LENGTH = 3  # Length of '## ' prefix
SECTION_SEPARATOR = '\n\n'  # Separator between constitution sections

# Agent configuration based on spec-kit AGENTS.md
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/commands",
        "file_extension": "md",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/commands",
        "file_extension": "toml",
        "requires_cli": True,
    },
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/agents",
        "file_extension": "md",
        "requires_cli": False,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor/commands",
        "file_extension": "md",
        "requires_cli": True,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/commands",
        "file_extension": "toml",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/commands",
        "file_extension": "md",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/commands",
        "file_extension": "md",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf/workflows",
        "file_extension": "md",
        "requires_cli": False,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".q/commands",
        "file_extension": "md",
        "requires_cli": True,
    },
    "manual": {
        "name": "Manual/Generic",
        "folder": None,
        "file_extension": None,
        "requires_cli": False,
    },
}


def _github_token(cli_token: str | None = None) -> str | None:
    """Return GitHub token from CLI arg, GH_TOKEN, or GITHUB_TOKEN env vars."""
    return (
        cli_token
        or os.getenv("GH_TOKEN", "").strip()
        or os.getenv("GITHUB_TOKEN", "").strip()
    ) or None


def _github_auth_headers(cli_token: str | None = None) -> dict:
    """Return Authorization header dict only when a non-empty token exists."""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


def _parse_rate_limit_headers(headers: httpx.Headers) -> dict:
    """Extract and parse GitHub rate-limit headers."""
    info = {}

    # Standard GitHub rate-limit headers
    if "X-RateLimit-Limit" in headers:
        info["limit"] = headers.get("X-RateLimit-Limit")
    if "X-RateLimit-Remaining" in headers:
        info["remaining"] = headers.get("X-RateLimit-Remaining")
    if "X-RateLimit-Reset" in headers:
        reset_epoch = int(headers.get("X-RateLimit-Reset", "0"))
        if reset_epoch:
            reset_time = datetime.fromtimestamp(reset_epoch, tz=timezone.utc)
            info["reset_epoch"] = reset_epoch
            info["reset_local"] = reset_time.astimezone()

    # Retry-After header (for 429 responses)
    if "Retry-After" in headers:
        info["retry_after_seconds"] = headers.get("Retry-After")

    return info


def _format_rate_limit_error(status_code: int, headers: httpx.Headers, url: str) -> str:
    """Format a user-friendly error message with rate-limit information."""
    rate_info = _parse_rate_limit_headers(headers)

    lines = [f"GitHub API returned status {status_code} for {url}"]
    lines.append("")

    if rate_info:
        lines.append("[bold]Rate Limit Information:[/bold]")
        if "limit" in rate_info:
            lines.append(f"  • Rate Limit: {rate_info['limit']} requests/hour")
        if "remaining" in rate_info:
            lines.append(f"  • Remaining: {rate_info['remaining']}")
        if "reset_local" in rate_info:
            reset_str = rate_info["reset_local"].strftime("%Y-%m-%d %H:%M:%S %Z")
            lines.append(f"  • Resets at: {reset_str}")
        if "retry_after_seconds" in rate_info:
            lines.append(f"  • Retry after: {rate_info['retry_after_seconds']} seconds")
        lines.append("")

    # Add troubleshooting guidance
    lines.append("[bold]Troubleshooting Tips:[/bold]")
    lines.append("  • If you're on a shared CI or corporate environment, you may be rate-limited.")
    lines.append("  • Consider using a GitHub token via --github-token or the GH_TOKEN/GITHUB_TOKEN")
    lines.append("    environment variable to increase rate limits.")
    lines.append("  • Authenticated requests have a limit of 5,000/hour vs 60/hour for unauthenticated.")

    return "\n".join(lines)


class Agent(str, Enum):
    """Supported AI agents"""
    claude = "claude"
    gemini = "gemini"
    copilot = "copilot"
    cursor = "cursor-agent"
    qwen = "qwen"
    opencode = "opencode"
    codex = "codex"
    windsurf = "windsurf"
    q = "q"
    manual = "manual"


app = typer.Typer(
    name="specify-extend",
    help="Installation tool for spec-kit-extensions that detects your existing spec-kit installation and mirrors the agent configuration.",
    add_completion=False,
)


def get_script_name(extension: str) -> str:
    """Get the script name for an extension (handles special cases)"""
    if extension == "modify":
        return "create-modification.sh"
    return f"create-{extension}.sh"


def get_powershell_script_name(extension: str) -> str:
    """Get the PowerShell script name for an extension (handles special cases)"""
    if extension == "modify":
        return "create-modification.ps1"
    return f"create-{extension}.ps1"


def is_workflow_extension(extension: str) -> bool:
    """Check if an extension is a workflow extension.

    Workflow extensions create workflow directories with specs, plans, and tasks.
    Command extensions provide commands without creating workflow structures.
    """
    return extension in WORKFLOW_EXTENSIONS


def is_command_extension(extension: str) -> bool:
    """Check if an extension is a command-only extension (not a workflow)."""
    return extension in COMMAND_EXTENSIONS


def roman_to_int(roman: str) -> int:
    """Convert Roman numeral to integer

    Returns 0 for invalid or malformed Roman numerals to handle
    real-world constitution headers gracefully. This intentionally
    allows malformed Roman numerals (e.g., 'IXI') and returns a
    best-effort conversion, as we're parsing user content that may
    not follow strict Roman numeral rules.
    """
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    prev_value = 0

    for char in reversed(roman.upper()):
        value = roman_values.get(char, 0)
        if value == 0:
            # Invalid character, return 0 to skip this header
            return 0
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total


def int_to_roman(num: int) -> str:
    """Convert integer to Roman numeral

    Args:
        num: Positive integer to convert

    Returns:
        Roman numeral representation

    Raises:
        ValueError: If num is less than or equal to 0
    """
    if num <= 0:
        raise ValueError(f"Cannot convert {num} to Roman numeral (must be positive)")

    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]

    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1

    return roman_num


def parse_constitution_sections(content: str) -> Tuple[Optional[str], Optional[int]]:
    """Parse constitution to find the highest section number and numbering style.

    Args:
        content: Constitution file content with section headers in the format
                '### N. Title' where N is either a Roman numeral or number

    Returns:
        Tuple of (numbering_style, highest_number)
        numbering_style can be: 'roman', 'numeric', or None
        highest_number is the integer value of the highest section found

    Note:
        - Section headers with malformed Roman numerals (e.g., "IIV", "VVV") will be
          silently skipped and not counted. Only valid Roman numerals are considered.
        - If a constitution contains BOTH Roman and numeric section headers (mixed styles),
          the function returns the style with non-zero sections, preferring Roman numerals
          if both are present. Mixed numbering styles in a single document would be unusual
          and may indicate inconsistent formatting.
    """
    highest_roman = 0
    highest_numeric = 0

    for line in content.split('\n'):
        # Check for Roman numerals
        roman_match = re.match(ROMAN_NUMERAL_PATTERN, line.strip())
        if roman_match:
            roman_value = roman_to_int(roman_match.group(1))
            # Only count valid Roman numerals (non-zero values)
            if roman_value > 0:
                highest_roman = max(highest_roman, roman_value)

        # Check for numeric
        numeric_match = re.match(NUMERIC_SECTION_PATTERN, line.strip())
        if numeric_match:
            numeric_value = int(numeric_match.group(1))
            highest_numeric = max(highest_numeric, numeric_value)

    # Determine which style was used
    if highest_roman > 0:
        return ('roman', highest_roman)
    elif highest_numeric > 0:
        return ('numeric', highest_numeric)
    else:
        return (None, None)


def format_template_with_sections(template_content: str, numbering_style: Optional[str], start_number: int) -> str:
    """
    Format the template content with proper section numbering.

    Args:
        template_content: The raw template content
        numbering_style: 'roman', 'numeric', or None
        start_number: The starting number for the first section

    Returns:
        Formatted template with section numbers
    """
    if not numbering_style:
        # No existing numbering, just return as-is
        return template_content

    lines = template_content.split('\n')
    result = []
    current_section = start_number

    for line in lines:
        # Check if this is exactly a ## header (not ### or ####)
        stripped = line.strip()
        # Must start with '## ' and the character after '## ' must not be '#'
        if stripped.startswith('## ') and len(stripped) > HEADER_PREFIX_LENGTH and stripped[HEADER_PREFIX_LENGTH] != '#':
            # Extract the section title (remove '## ')
            title = stripped[HEADER_PREFIX_LENGTH:]

            # Format the section number
            if numbering_style == 'roman':
                section_num = int_to_roman(current_section)
            else:  # numeric
                section_num = str(current_section)

            # Create the new line with section number
            result.append(f"### {section_num}. {title}")
            current_section += 1
        else:
            result.append(line)

    return '\n'.join(result)


def detect_existing_workflows(content: str) -> set:
    """Detect which extension workflows are already documented in constitution

    Returns a set of workflow names that have quality gate sections in the constitution.
    """
    existing_workflows = set()

    # Look for quality gate sections for each workflow
    workflow_patterns = {
        'baseline': r'\*\*Baseline\*\*:',
        'bugfix': r'\*\*Bug\s*Fix(es)?\*\*:',
        'modify': r'\*\*Modif(y|ication(s)?)\*\*:',
        'refactor': r'\*\*Refactor(ing)?\*\*:',
        'hotfix': r'\*\*Hotfix(es)?\*\*:',
        'deprecate': r'\*\*Deprecat(e|ion)\*\*:',
        'cleanup': r'\*\*Cleanup\*\*:',
        'review': r'\*\*Review\*\*:'
    }

    for workflow, pattern in workflow_patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            existing_workflows.add(workflow)

    return existing_workflows


def detect_workflow_selection_section(content: str) -> bool:
    """Check if the constitution already contains workflow selection content

    Returns True if both section header and workflow command thresholds are met,
    indicating existing workflow content.

    Uses regex patterns to match section headers specifically (not just text mentions)
    and configurable thresholds to reduce false positives.
    """
    # Look for specific section headers using regex to match actual headers
    # Pattern matches ## or ### headers containing these terms
    section_patterns = [
        r'^##\s+.*Workflow Selection',
        r'^##\s+.*Development Workflow',
        r'^##\s+.*Quality Gates by Workflow'
    ]

    # Look for workflow command patterns in their expected context
    # Match them as list items, in tables, or in backticks
    workflow_patterns = [
        r'`/baseline[^`]*`',
        r'`/bugfix[^`]*`',
        r'`/modify[^`]*`',
        r'`/refactor[^`]*`',
        r'`/hotfix[^`]*`',
        r'`/deprecate[^`]*`'
    ]

    # Check if we have the main section headers
    has_sections = 0
    for pattern in section_patterns:
        if re.search(pattern, content, re.MULTILINE):
            has_sections += 1

    # Check if we have workflow commands in expected format
    workflow_commands_found = set()
    for pattern in workflow_patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            # Extract which workflow this is
            workflow_name = re.search(r'/(baseline|bugfix|modify|refactor|hotfix|deprecate)', pattern)
            if workflow_name:
                workflow_commands_found.add(workflow_name.group(1))
    has_workflows = len(workflow_commands_found)

    # Return True if both thresholds are met
    return has_sections >= MIN_SECTION_HEADERS and has_workflows >= MIN_WORKFLOW_COMMANDS


def detect_agent(repo_root: Path) -> str:
    """Detect which AI agent is configured by examining project structure"""

    # Check for Claude Code
    if (repo_root / ".claude" / "commands").exists():
        return "claude"

    # Check for GitHub Copilot
    if (repo_root / ".github" / "agents").exists() or (repo_root / ".github" / "copilot-instructions.md").exists():
        return "copilot"

    # Check for Cursor
    if (repo_root / ".cursor" / "commands").exists() or (repo_root / ".cursorrules").exists():
        return "cursor-agent"

    # Check for Windsurf
    if (repo_root / ".windsurf").exists():
        return "windsurf"

    # Check for Gemini
    if (repo_root / ".gemini" / "commands").exists():
        return "gemini"

    # Check for Qwen
    if (repo_root / ".qwen" / "commands").exists():
        return "qwen"

    # Check for opencode
    if (repo_root / ".opencode" / "commands").exists():
        return "opencode"

    # Check for Codex
    if (repo_root / ".codex" / "commands").exists():
        return "codex"

    # Check for Amazon Q
    if (repo_root / ".q" / "commands").exists():
        return "q"

    # Default to manual
    return "manual"


def get_repo_root() -> Path:
    """Get the repository root directory"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        path_str = result.stdout.strip()

        # On Windows with Git Bash, git returns Unix-style paths like /c/Users/...
        # Convert these to Windows format (C:/Users/...) for Python's Path
        if sys.platform == "win32":
            # Normalize backslashes to forward slashes first
            path_str = path_str.replace('\\', '/')

            # Match /c, /d, /c/... or /d/... etc. (Git Bash format)
            match = re.match(r'^/([a-zA-Z])(/.*)?$', path_str)
            if match:
                drive = match.group(1).upper()
                rest = match.group(2) or "/"
                path_str = f"{drive}:{rest}"

        return Path(path_str)
    except subprocess.CalledProcessError:
        return Path.cwd()


def validate_speckit_installation(repo_root: Path) -> bool:
    """Validate that spec-kit is installed"""
    specify_dir = repo_root / ".specify"

    if not specify_dir.exists():
        console.print(
            "[red]✗[/red] No .specify directory found. Please run 'specify init' first.",
            style="bold"
        )
        return False

    if not (specify_dir / "scripts").exists():
        console.print(
            "[yellow]⚠[/yellow] .specify/scripts directory not found - this might be a minimal installation",
            style="yellow"
        )

    console.print(
        f"[green]✓[/green] Found spec-kit installation at {specify_dir}",
        style="green"
    )
    return True


def download_latest_release(temp_dir: Path, github_token: str = None) -> Optional[Path]:
    """Download the latest template release from GitHub

    Fetches the latest templates-v* tag from the repository, as templates
    are now versioned separately from the CLI tool.
    """

    with console.status("[bold blue]Downloading latest extensions...") as status:
        try:
            # Get all tags to find latest templates-v* tag
            url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/tags"
            response = client.get(
                url,
                timeout=30,
                headers=_github_auth_headers(github_token),
            )

            if response.status_code != 200:
                error_msg = _format_rate_limit_error(response.status_code, response.headers, url)
                console.print(Panel(error_msg, title="GitHub API Error", border_style="red"))
                return None

            try:
                tags_data = response.json()
            except ValueError as je:
                console.print(f"[red]Failed to parse tags JSON:[/red] {je}")
                return None

            # Find latest templates-v* tag
            template_tags = [tag for tag in tags_data if tag["name"].startswith("templates-v")]

            if not template_tags:
                console.print("[red]No template tags found (looking for templates-v* pattern)[/red]")
                return None

            # Get the first one (GitHub returns tags in reverse chronological order)
            tag_name = template_tags[0]["name"]

            console.print(f"[blue]ℹ[/blue] Latest template version: {tag_name}")

            # Download zipball
            zipball_url = f"https://github.com/{GITHUB_REPO}/archive/refs/tags/{tag_name}.zip"

            status.update(f"[bold blue]Downloading {tag_name}...")
            response = client.get(
                zipball_url,
                timeout=60,
                headers=_github_auth_headers(github_token),
            )

            if response.status_code != 200:
                error_msg = _format_rate_limit_error(response.status_code, response.headers, zipball_url)
                console.print(Panel(error_msg, title="Download Error", border_style="red"))
                return None

            # Save and extract
            zip_path = temp_dir / "extensions.zip"
            with open(zip_path, "wb") as f:
                f.write(response.content)

            status.update("[bold blue]Extracting files...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # Find extracted directory
            extracted_dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
            if extracted_dirs:
                return extracted_dirs[0]

            return None

        except httpx.HTTPError as e:
            console.print(f"[red]✗[/red] Failed to download: {e}", style="red")
            return None
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {e}", style="red")
            return None


def read_enabled_conf(repo_root: Path) -> set:
    """Read enabled.conf and return set of enabled workflow names

    Args:
        repo_root: Root directory of the repository

    Returns:
        Set of enabled workflow names (without comments/blank lines)
    """
    enabled_conf = repo_root / ".specify" / "extensions" / "enabled.conf"

    if not enabled_conf.exists():
        return set()

    enabled = set()
    content = enabled_conf.read_text()

    for line in content.split('\n'):
        line = line.strip()
        # Skip comments and empty lines
        if line and not line.startswith('#'):
            enabled.add(line)

    return enabled


def update_enabled_conf(
    repo_root: Path,
    workflows_to_enable: set,
    dry_run: bool = False
) -> None:
    """Update enabled.conf with specified workflows

    Args:
        repo_root: Root directory of the repository
        workflows_to_enable: Set of workflow names to mark as enabled
        dry_run: Whether to perform a dry run
    """
    enabled_conf = repo_root / ".specify" / "extensions" / "enabled.conf"

    if not enabled_conf.exists():
        if not dry_run:
            enabled_conf.parent.mkdir(parents=True, exist_ok=True)
            # Create with header
            content = """# Extension Workflows Configuration
# Uncomment workflows you want to enable
# Comment out a line to disable that workflow extension\n\n# Extension Workflows\n"""
            enabled_conf.write_text(content)

    # Read current content preserving comments
    if enabled_conf.exists():
        lines = enabled_conf.read_text().split('\n')
    else:
        lines = []

    # Build new content
    new_lines = []
    seen_workflows = set()

    # Process existing lines
    for line in lines:
        stripped = line.strip()

        # Keep comments and empty lines
        if not stripped or stripped.startswith('#'):
            new_lines.append(line)
            continue

        # Check if this is a workflow line
        workflow_name = stripped
        seen_workflows.add(workflow_name)

        # Enable or disable based on workflows_to_enable
        if workflow_name in workflows_to_enable:
            new_lines.append(workflow_name)
        else:
            # Comment out disabled workflows
            new_lines.append(f"# {workflow_name}")

    # Add new workflows that weren't in the file
    new_workflows = workflows_to_enable - seen_workflows
    if new_workflows:
        if new_lines and new_lines[-1].strip():  # Add blank line if needed
            new_lines.append('')
        for workflow in sorted(new_workflows):
            new_lines.append(workflow)

    if not dry_run:
        enabled_conf.write_text('\n'.join(new_lines) + '\n')
        console.print(f"[green]✓[/green] Updated enabled.conf")
    else:
        console.print("  [dim]Would update enabled.conf[/dim]")


def prompt_for_workflows(
    available: List[str],
    currently_enabled: set,
    installed: set
) -> set:
    """Interactively prompt user to select which workflows to enable

    Args:
        available: List of all available workflows
        currently_enabled: Set of currently enabled workflows
        installed: Set of workflows being installed this session

    Returns:
        Set of workflows the user wants to enable
    """
    from rich.prompt import Confirm, Prompt
    from rich.table import Table

    # Identify new workflows (available but not currently enabled)
    new_workflows = set(available) - currently_enabled

    if not new_workflows:
        # No new workflows, just return currently enabled ones plus installed
        return currently_enabled | installed

    console.print("\n[bold yellow]New workflows detected![/bold yellow]")
    console.print(f"Currently enabled: {', '.join(sorted(currently_enabled)) or 'none'}")
    console.print(f"New available: {', '.join(sorted(new_workflows))}\n")

    # Build table showing workflow info
    table = Table(title="Available Workflows")
    table.add_column("Workflow", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Description", style="dim")

    workflow_descriptions = {
        "baseline": "Establish project baseline and track changes",
        "bugfix": "Bug remediation with regression tests",
        "modify": "Modify existing features with impact analysis",
        "refactor": "Improve code quality while preserving behavior",
        "hotfix": "Emergency production fixes",
        "deprecate": "Planned feature sunset with phased rollout",
        "cleanup": "Validate and reorganize spec-kit artifacts",
        "review": "Review completed implementation work"
    }

    for workflow in sorted(available):
        status = "✓ Enabled" if workflow in currently_enabled else "○ New"
        desc = workflow_descriptions.get(workflow, "Extension workflow")
        table.add_row(workflow, status, desc)

    console.print(table)
    console.print()

    # Ask user what to do
    choice = Prompt.ask(
        "[bold]Enable new workflows?[/bold]",
        choices=["all", "select", "none", "current"],
        default="all"
    )

    if choice == "all":
        # Enable all available workflows
        return set(available)
    elif choice == "none":
        # Keep only currently enabled workflows
        return currently_enabled
    elif choice == "current":
        # Keep currently enabled + install what's being installed this session
        return currently_enabled | installed
    else:  # select
        # Let user pick individual workflows
        selected = currently_enabled.copy()
        console.print("\n[bold]Select new workflows to enable:[/bold]")
        for workflow in sorted(new_workflows):
            desc = workflow_descriptions.get(workflow, "Extension workflow")
            if Confirm.ask(f"  Enable [cyan]{workflow}[/cyan]? ({desc})", default=True):
                selected.add(workflow)
        return selected


def install_extension_files(
    repo_root: Path,
    source_dir: Path,
    extensions: List[str],
    dry_run: bool = False,
    install_powershell: bool = False,
) -> None:
    """Install extension workflow templates and scripts"""

    console.print("[blue]ℹ[/blue] Installing extension files...")

    extensions_dir = repo_root / ".specify" / "extensions"
    scripts_dir = repo_root / ".specify" / "scripts" / "bash"
    powershell_scripts_dir = repo_root / ".specify" / "scripts" / "powershell"

    if not dry_run:
        extensions_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir.mkdir(parents=True, exist_ok=True)
        if install_powershell:
            powershell_scripts_dir.mkdir(parents=True, exist_ok=True)

    # Copy extension base files
    source_extensions = source_dir / "extensions"
    if source_extensions.exists():
        for file in ["README.md", "enabled.conf"]:
            source_file = source_extensions / file
            if source_file.exists():
                if not dry_run:
                    shutil.copy(source_file, extensions_dir / file)
                console.print(f"  [dim]→ {file}[/dim]")

    # Copy workflow directories
    workflows_dir = extensions_dir / "workflows"
    if not dry_run:
        workflows_dir.mkdir(exist_ok=True)

    for ext in extensions:
        # Only workflow extensions have workflow directories
        if not is_workflow_extension(ext):
            continue

        source_workflow = source_extensions / "workflows" / ext
        if source_workflow.exists():
            if not dry_run:
                dest_workflow = workflows_dir / ext
                if dest_workflow.exists():
                    shutil.rmtree(dest_workflow)
                shutil.copytree(source_workflow, dest_workflow)
            console.print(f"[green]✓[/green] Copied {ext} workflow templates")
        else:
            console.print(f"[yellow]⚠[/yellow] Workflow directory for {ext} not found")

    # Copy scripts based on selected script type (consistent with spec-kit behavior)
    if install_powershell:
        # Install PowerShell scripts only
        source_powershell_scripts = source_dir / "scripts" / "powershell"
        if source_powershell_scripts.exists():
            for ext in extensions:
                # Only workflow extensions have create scripts
                if not is_workflow_extension(ext):
                    continue

                script_name = get_powershell_script_name(ext)
                source_script = source_powershell_scripts / script_name

                if source_script.exists():
                    if not dry_run:
                        dest_script = powershell_scripts_dir / script_name
                        shutil.copy(source_script, dest_script)
                    console.print(f"[green]✓[/green] Copied {script_name} script")
                else:
                    console.print(f"[yellow]⚠[/yellow] Script {script_name} not found")
    else:
        # Install bash scripts only
        source_scripts = source_dir / "scripts"
        if source_scripts.exists():
            for ext in extensions:
                # Only workflow extensions have create scripts
                if not is_workflow_extension(ext):
                    continue

                script_name = get_script_name(ext)
                source_script = source_scripts / script_name

                if source_script.exists():
                    if not dry_run:
                        dest_script = scripts_dir / script_name
                        shutil.copy(source_script, dest_script)
                        dest_script.chmod(0o755)  # Make executable
                    console.print(f"[green]✓[/green] Copied {script_name} script")
                else:
                    console.print(f"[yellow]⚠[/yellow] Script {script_name} not found")


def install_agent_commands(
    repo_root: Path,
    source_dir: Path,
    agent: str,
    extensions: List[str],
    dry_run: bool = False,
    link: bool = False,
    install_powershell: bool = False,
) -> None:
    """Install agent-specific command files"""

    agent_info = AGENT_CONFIG.get(agent, AGENT_CONFIG["manual"])
    agent_name = agent_info["name"]

    if agent == "manual":
        console.print(f"[blue]ℹ[/blue] Installing for manual/generic agent setup...")
        console.print("  [dim]To use extensions, run bash scripts directly:[/dim]")
        console.print("  [dim].specify/scripts/bash/create-bugfix.sh \"description\"[/dim]")
        if install_powershell:
            console.print("  [dim]PowerShell scripts are also installed:[/dim]")
            console.print("  [dim].specify/scripts/powershell/create-bugfix.ps1 \"description\"[/dim]")
        return

    console.print(f"[blue]ℹ[/blue] Installing {agent_name} commands...")

    folder = agent_info["folder"]
    file_ext = agent_info["file_extension"]

    if not folder:
        return

    if link and os.name == "nt":
        console.print(
            "[yellow]⚠[/yellow] Symlink mode requested on Windows; falling back to copy"
        )
        link = False
    if link and install_powershell:
        console.print(
            "[yellow]⚠[/yellow] Symlink mode requested with PowerShell script selection; "
            "falling back to copy so command scripts can reference .ps1 workflows"
        )
        link = False

    # Check if this agent needs TOML files (not yet supported)
    if file_ext == "toml":
        console.print(
            f"[yellow]⚠[/yellow] {agent_name} requires TOML command files (not yet implemented)"
        )
        console.print("  [dim]Will install markdown files as fallback[/dim]")

    commands_dir = repo_root / folder

    if not dry_run:
        commands_dir.mkdir(parents=True, exist_ok=True)

    source_commands = source_dir / "commands"

    for ext in extensions:
        # Try new naming convention first (speckit.*), fallback to old (specify.*)
        source_file = source_commands / f"speckit.{ext}.md"
        if not source_file.exists():
            source_file = source_commands / f"specify.{ext}.md"

        # For Copilot, append .agent suffix to the filename
        if agent == "copilot":
            dest_filename = f"speckit.{ext}.agent.{file_ext or 'md'}"
        else:
            dest_filename = f"speckit.{ext}.{file_ext or 'md'}"

        dest_file = commands_dir / dest_filename

        def install_file(src: Path, dest: Path) -> None:
            if link:
                if dest.exists() or dest.is_symlink():
                    dest.unlink()
                dest.symlink_to(src)
            else:
                shutil.copy(src, dest)

        if source_file.exists():
            if not dry_run:
                if install_powershell:
                    content = source_file.read_text()
                    # Replace bash script paths with PowerShell paths
                    content = content.replace(
                        ".specify/scripts/bash/", ".specify/scripts/powershell/"
                    )
                    # Only replace `.sh` when it appears as a file extension (word boundary)
                    content = re.sub(r"\.sh\b", ".ps1", content)
                    dest_file.write_text(content)
                else:
                    install_file(source_file, dest_file)

                # For GitHub Copilot, also create a prompt file that points to the agent
                if agent == "copilot":
                    prompts_dir = repo_root / ".github" / "prompts"
                    prompts_dir.mkdir(parents=True, exist_ok=True)
                    prompt_file = prompts_dir / f"speckit.{ext}.prompt.md"
                    # Prompt file is just a pointer to the agent file
                    prompt_content = f"---\nagent: speckit.{ext}\n---\n"
                    prompt_file.write_text(prompt_content)
                    console.print(f"[green]✓[/green] Installed /speckit.{ext} agent and prompt")
                else:
                    console.print(f"[green]✓[/green] Installed /speckit.{ext} command")
            else:
                if agent == "copilot":
                    console.print(f"[green]✓[/green] Installed /speckit.{ext} agent and prompt")
                else:
                    console.print(f"[green]✓[/green] Installed /speckit.{ext} command")
        else:
            console.print(f"[yellow]⚠[/yellow] Command file for {ext} not found")


def create_constitution_enhance_command(
    repo_root: Path,
    source_dir: Path,
    agent: str,
    dry_run: bool = False,
) -> None:
    """Create a one-time-use command to LLM-enhance constitution update"""

    agent_info = AGENT_CONFIG.get(agent, AGENT_CONFIG["manual"])
    agent_name = agent_info["name"]

    if agent == "manual":
        console.print(
            "[yellow]⚠[/yellow] LLM-enhance requires an AI agent configuration. "
            "Falling back to standard constitution update."
        )
        return

    console.print(f"[blue]ℹ[/blue] Creating one-time constitution enhancement prompt...")

    # Read the constitution template
    template_file = source_dir / "docs" / "constitution-template.md"
    if not template_file.exists():
        console.print("[yellow]⚠[/yellow] Constitution template not found")
        return

    template_content = template_file.read_text()

    # Determine file locations based on agent
    folder = agent_info["folder"]
    file_ext = agent_info["file_extension"]

    if not folder:
        console.print(
            "[yellow]⚠[/yellow] LLM-enhance not supported for this agent. "
            "Falling back to standard constitution update."
        )
        return

    # For GitHub Copilot, create both agent and prompt files
    if agent == "copilot":
        agent_dir = repo_root / ".github" / "agents"
        prompt_dir = repo_root / ".github" / "prompts"
        agent_file = agent_dir / "speckit.enhance-constitution.md"
        prompt_file = prompt_dir / "speckit.enhance-constitution.prompt.md"
        file_location = ".github/prompts/speckit.enhance-constitution.prompt.md (and .github/agents/speckit.enhance-constitution.md)"
    else:
        # For other agents, use their command directories
        prompt_dir = repo_root / folder
        prompt_file = prompt_dir / f"speckit.enhance-constitution.{file_ext or 'md'}"
        agent_file = None
        file_location = f"{folder}/speckit.enhance-constitution.{file_ext or 'md'}"

    # Create the one-time prompt content
    # For GitHub Copilot, we use a simpler format without frontmatter
    if agent == "copilot":
        command_content = f"""# Constitution Enhancement (One-Time Use)

**IMPORTANT**: This is a one-time prompt. After using it, delete this file to prevent accidental re-use.

## Your Task

You are enhancing the project's constitution file (`.specify/memory/constitution.md`) with workflow-specific quality gates.

### Steps:

1. **Read the current constitution**: `.specify/memory/constitution.md`
2. **Review the template below**: Contains workflow selection guidelines and quality gates
3. **Intelligently merge the content**:
   - Preserve all existing constitution content
   - Add missing workflow selection guidance
   - Add missing quality gates for each workflow type
   - Match the existing writing style, tone, and section numbering
   - Avoid duplicating content that already exists
   - Ensure smooth integration without jarring transitions

4. **Self-destruct**: After updating the constitution, DELETE both files
   - Prompt: `.github/prompts/speckit.enhance-constitution.prompt.md`
   - Agent: `.github/agents/speckit.enhance-constitution.md`
   - This prevents accidental re-use

## Template Content to Integrate

```markdown
{template_content}
```

## Important Notes

- **Preserve existing content**: Don't remove or significantly alter existing constitution sections
- **Match style**: Adapt template language to match existing constitution's tone
- **Section numbering**: Continue existing numbering scheme (Roman numerals, numeric, or none)
- **No duplication**: If workflow guidance already exists, enhance rather than duplicate
- **One-time only**: This prompt deletes itself after use to prevent confusion

---

**After completion**: Verify that `.specify/memory/constitution.md` contains both the original content and the new workflow quality gates, properly integrated.
"""
    else:
        # For other agents (Claude, Cursor, etc.), use command format with frontmatter
        command_content = f"""---
name: speckit.enhance-constitution
description: One-time command to enhance constitution with workflow quality gates using LLM intelligence
handoffs:
  - speckit.plan
  - speckit.tasks
---

# Constitution Enhancement (One-Time Use)

You are enhancing the project's constitution file (`.specify/memory/constitution.md`) with workflow-specific quality gates.

## Your Task

1. **Read the current constitution**: `.specify/memory/constitution.md`
2. **Review the template below**: Contains workflow selection guidelines and quality gates
3. **Intelligently merge**: Use `/specify.constitution` to:
   - Preserve all existing constitution content
   - Add missing workflow selection guidance
   - Add missing quality gates for each workflow type
   - Match the existing writing style, tone, and section numbering
   - Avoid duplicating content that already exists
   - Ensure smooth integration without jarring transitions

4. **Self-destruct**: After updating the constitution, DELETE this command file
   - Location: `{file_location}`
   - This prevents accidental re-use

## Template Content to Integrate

```markdown
{template_content}
```

## Instructions

1. First, run `/specify.constitution` with instructions to merge the above template content intelligently
2. Review the updated constitution to ensure quality
3. Then delete this command file: `{file_location}`

## Important Notes

- **Preserve existing content**: Don't remove or significantly alter existing constitution sections
- **Match style**: Adapt template language to match existing constitution's tone
- **Section numbering**: Continue existing numbering scheme (Roman numerals, numeric, or none)
- **No duplication**: If workflow guidance already exists, enhance rather than duplicate
- **One-time only**: This command deletes itself after use to prevent confusion

---

**After completion**: Verify that `.specify/memory/constitution.md` contains both the original content and the new workflow quality gates, properly integrated.
"""

    if not dry_run:
        prompt_dir.mkdir(parents=True, exist_ok=True)
        prompt_file.write_text(command_content)

        # For Copilot, also create the agent file
        if agent == "copilot":
            agent_dir.mkdir(parents=True, exist_ok=True)
            agent_file.write_text(command_content)
            console.print(f"[green]✓[/green] Created constitution enhancement agent and prompt")
            console.print(f"[blue]ℹ[/blue] Reference the prompt in GitHub Copilot Chat or use as an agent")
        else:
            console.print(f"[green]✓[/green] Created /speckit.enhance-constitution command")
            console.print(f"[blue]ℹ[/blue] Run this command to intelligently merge constitution updates")
        console.print(f"[dim]  Location: {file_location}[/dim]")
        console.print(f"[yellow]⚠[/yellow] This will self-destruct after use")
    else:
        console.print(f"  [dim]Would create {file_location}[/dim]")


def update_constitution(
    repo_root: Path,
    source_dir: Path,
    agent: str = "manual",
    dry_run: bool = False,
    llm_enhance: bool = False,
) -> None:
    """Update constitution with quality gates, intelligently numbering sections

    Args:
        repo_root: Root directory of the repository
        source_dir: Source directory containing templates
        agent: Detected agent type
        dry_run: Whether to perform a dry run
        llm_enhance: If True, create one-time LLM enhancement command instead of direct update
    """

    if llm_enhance:
        create_constitution_enhance_command(repo_root, source_dir, agent, dry_run)
        return

    console.print("[blue]ℹ[/blue] Updating constitution with quality gates...")

    constitution_file = repo_root / ".specify" / "memory" / "constitution.md"

    if not dry_run:
        constitution_file.parent.mkdir(parents=True, exist_ok=True)

        # Read template content
        template_file = source_dir / "docs" / "constitution-template.md"
        if not template_file.exists():
            console.print("[yellow]⚠[/yellow] Constitution template not found")
            return

        template_content = template_file.read_text()
        is_new_file = not constitution_file.exists()

        # Check if already has quality gates
        if constitution_file.exists():
            content = constitution_file.read_text()

            # Check which workflows are already documented
            existing_workflows = detect_existing_workflows(content)

            # Check if workflow selection section exists
            has_selection_section = detect_workflow_selection_section(content)

            # If all major workflows are present, skip update
            major_workflows = {'baseline', 'bugfix', 'modify', 'refactor', 'hotfix', 'deprecate'}
            if has_selection_section and major_workflows.issubset(existing_workflows):
                console.print(
                    "[yellow]⚠[/yellow] Constitution already contains all workflow quality gates"
                )
                return

            # If we have some workflows but not all, inform about what's missing
            if existing_workflows:
                missing = major_workflows - existing_workflows
                if missing:
                    console.print(
                        f"[blue]ℹ[/blue] Found existing workflows: {', '.join(sorted(existing_workflows))}"
                    )
                    console.print(
                        f"[blue]ℹ[/blue] Adding missing workflows: {', '.join(sorted(missing))}"
                    )

            # Parse existing constitution to find section numbering
            numbering_style, highest_number = parse_constitution_sections(content)

            # Check for malformed Roman numerals case
            if numbering_style == 'roman' and highest_number == 0:
                # Malformed Roman numerals detected, fall back to no numbering
                formatted_template = template_content
                console.print("[yellow]⚠[/yellow] Detected malformed Roman numerals, using template as-is")
            elif numbering_style and highest_number:
                # Found existing numbered sections, continue the numbering
                next_number = highest_number + 1
                try:
                    formatted_template = format_template_with_sections(
                        template_content,
                        numbering_style,
                        next_number
                    )
                    console.print(
                        f"[blue]ℹ[/blue] Detected {numbering_style} numbering, adding sections starting at "
                        f"{int_to_roman(next_number) if numbering_style == 'roman' else next_number}"
                    )
                except ValueError as e:
                    # Handle edge case where int_to_roman might fail
                    console.print(f"[yellow]⚠[/yellow] Error formatting sections: {e}, using template as-is")
                    formatted_template = template_content
            else:
                # No existing numbering found, use template as-is
                formatted_template = template_content
                console.print("[blue]ℹ[/blue] No section numbering detected, using template as-is")
        else:
            # New constitution file - no numbering, no leading newlines
            formatted_template = template_content
            console.print("[blue]ℹ[/blue] Creating new constitution file")

        # Append formatted template to constitution
        with open(constitution_file, "a") as f:
            # Only add separator for existing files
            if not is_new_file:
                f.write(SECTION_SEPARATOR)
            f.write(formatted_template)

        console.print("[green]✓[/green] Constitution updated with quality gates")
    else:
        console.print("  [dim]Would update constitution.md[/dim]")


def patch_common_sh(repo_root: Path, dry_run: bool = False) -> None:
    """Patch spec-kit's common.sh to support extension branch patterns

    Modifies check_feature_branch() to accept both standard spec-kit patterns (###-)
    and extension patterns (bugfix/###-, modify/###^###-, refactor/###-, hotfix/###-, deprecate/###-)

    Args:
        repo_root: Root directory of the repository
        dry_run: Whether to perform a dry run
    """
    console.print("[blue]ℹ[/blue] Patching common.sh for extension branch support...")

    common_sh = repo_root / ".specify" / "scripts" / "bash" / "common.sh"

    if not common_sh.exists():
        console.print("[yellow]⚠[/yellow] common.sh not found, skipping patch")
        return

    if not dry_run:
        content = common_sh.read_text()

        # Check if already patched AND up-to-date
        if "check_feature_branch_old()" in content:
            # Check if patch includes all workflow patterns (enhance, cleanup, baseline)
            if '"^enhance/[0-9]{3}-"' in content and '"^cleanup/[0-9]{3}-"' in content and '"^baseline/[0-9]{3}-"' in content:
                console.print("[blue]ℹ[/blue] common.sh already patched with latest patterns")
                return
            else:
                console.print("[yellow]⚠[/yellow] common.sh has outdated patch, updating...")
                # Restore from backup or remove old patched function
                if (common_sh.parent / "common.sh.backup").exists():
                    backup_file = common_sh.parent / "common.sh.backup"
                    content = backup_file.read_text()
                    console.print(f"  [dim]Restored from backup: {backup_file}[/dim]")
                else:
                    # Remove the old patched function by restoring check_feature_branch_old
                    content = content.replace("check_feature_branch_old()", "check_feature_branch()", 1)
                    # Find and remove the extended check_feature_branch function
                    import re
                    pattern = r'\n# Extended branch validation supporting spec-kit-extensions\ncheck_feature_branch\(\) \{.*?\n\}'
                    content = re.sub(pattern, '', content, flags=re.DOTALL)
                    console.print("  [dim]Removed old patched function[/dim]")

        # New function to append at the end
        # Supports both parameterized and non-parameterized signatures
        new_function = '''
# Extended branch validation supporting spec-kit-extensions
check_feature_branch() {
    # Support both parameterized and non-parameterized calls
    local branch="${1:-}"
    local has_git_repo="${2:-}"

    # If branch not provided as parameter, get current branch
    if [[ -z "$branch" ]]; then
        if git rev-parse --git-dir > /dev/null 2>&1; then
            branch=$(git branch --show-current)
            has_git_repo="true"
        else
            return 0
        fi
    fi

    # For non-git repos, skip validation if explicitly specified
    if [[ "$has_git_repo" != "true" && -n "$has_git_repo" ]]; then
        echo "[specify] Warning: Git repository not detected; skipped branch validation" >&2
        return 0
    fi

    # Extension branch patterns (spec-kit-extensions)
    local extension_patterns=(
        "^baseline/[0-9]{3}-"
        "^bugfix/[0-9]{3}-"
        "^enhance/[0-9]{3}-"
        "^modify/[0-9]{3}\\^[0-9]{3}-"
        "^refactor/[0-9]{3}-"
        "^hotfix/[0-9]{3}-"
        "^deprecate/[0-9]{3}-"
        "^cleanup/[0-9]{3}-"
    )

    # Check extension patterns first
    for pattern in "${extension_patterns[@]}"; do
        if [[ "$branch" =~ $pattern ]]; then
            return 0
        fi
    done

    # Check standard spec-kit pattern (###-)
    if [[ "$branch" =~ ^[0-9]{3}- ]]; then
        return 0
    fi

    # No match - show helpful error
    echo "ERROR: Not on a feature branch. Current branch: $branch" >&2
    echo "Feature branches must follow one of these patterns:" >&2
    echo "  Standard:    ###-description (e.g., 001-add-user-authentication)" >&2
    echo "  Baseline:    baseline/###-description" >&2
    echo "  Bugfix:      bugfix/###-description" >&2
    echo "  Enhance:     enhance/###-description" >&2
    echo "  Modify:      modify/###^###-description" >&2
    echo "  Refactor:    refactor/###-description" >&2
    echo "  Hotfix:      hotfix/###-description" >&2
    echo "  Deprecate:   deprecate/###-description" >&2
    echo "  Cleanup:     cleanup/###-description" >&2
    return 1
}'''

        if "check_feature_branch()" in content:
            # Create backup
            backup_file = common_sh.with_suffix('.sh.backup')
            backup_file.write_text(content)

            # Rename original to check_feature_branch_old
            patched_content = content.replace(
                "check_feature_branch()",
                "check_feature_branch_old()",
                1  # Only replace the first occurrence (the function definition)
            )

            # Append new function to the end
            patched_content += new_function

            common_sh.write_text(patched_content)

            console.print("[green]✓[/green] common.sh patched to support extension branch patterns")
            console.print("  [dim]Original function renamed to check_feature_branch_old()[/dim]")
            console.print("  [dim]New check_feature_branch() appended at end[/dim]")
            console.print(f"  [dim]Backup saved to: {backup_file}[/dim]")
        else:
            console.print("[yellow]⚠[/yellow] check_feature_branch() function not found")
            console.print("  [dim]Manual patching required[/dim]")
    else:
        console.print("  [dim]Would patch common.sh for extension branch support[/dim]")


def patch_update_agent_context_sh(repo_root: Path, dry_run: bool = False) -> None:
    """Patch spec-kit's update-agent-context.sh to prefer AGENTS.md via a compatibility shim.

    Spec-kit ships a script that generates/updates agent context files from plan.md.
    Today it may write Copilot instructions to `.github/agents/copilot-instructions.md`.

    With new Copilot guidance, `AGENTS.md` can be used as the canonical repo instructions.
    For compatibility with other Copilot surfaces, we keep a `.github/copilot-instructions.md`
    shim that points to `AGENTS.md`.

    This patch rewrites the COPILOT file target to `.github/copilot-instructions.md`.
    (It does not replace/rename spec-kit's script; it only adjusts where it writes.)
    """

    script_path = repo_root / "scripts" / "bash" / "update-agent-context.sh"
    if not script_path.exists():
        return

    console.print("[blue]ℹ[/blue] Patching update-agent-context.sh for AGENTS.md-first Copilot instructions...")

    content = script_path.read_text()

    # If it already targets the shim location, we're done.
    if 'COPILOT_FILE="$REPO_ROOT/.github/copilot-instructions.md"' in content:
        console.print("[blue]ℹ[/blue] update-agent-context.sh already patched")
        return

    # Only patch if we find the known upstream assignment.
    old = 'COPILOT_FILE="$REPO_ROOT/.github/agents/copilot-instructions.md"'
    new = 'COPILOT_FILE="$REPO_ROOT/.github/copilot-instructions.md"'

    if old not in content:
        console.print("[yellow]⚠[/yellow] update-agent-context.sh COPILOT_FILE pattern not found; skipping patch")
        return

    patched = content.replace(old, new, 1)

    if not dry_run:
        backup_file = script_path.with_suffix(script_path.suffix + ".backup")
        backup_file.write_text(content)
        script_path.write_text(patched)
        console.print("[green]✓[/green] update-agent-context.sh patched")
        console.print("  [dim]Copilot instructions now written to .github/copilot-instructions.md[/dim]")
        console.print("  [dim]Backup saved to: %s[/dim]" % backup_file)
    else:
        console.print("  [dim]Would patch update-agent-context.sh COPILOT_FILE path[/dim]")


def install_github_integration(
    repo_root: Path,
    source_dir: Path,
    dry_run: bool = False,
    non_interactive: bool = False,
) -> None:
    """Install optional GitHub workflows, PR template, issue templates, and code review integration"""

    # Source .github directory from downloaded release
    source_github = source_dir / ".github"

    if not source_github.exists():
        console.print("[yellow]⚠[/yellow] .github directory not found in release")
        return

    # Define available features with descriptions
    github_features = {
        "review-enforcement": {
            "name": "Review Enforcement Workflow",
            "description": "Automatically requires code reviews before merging spec-kit branches",
            "files": {
                "workflows": ["spec-kit-review-required.yml"],
            },
        },
        "review-reminder": {
            "name": "Review Reminder Workflow",
            "description": "Auto-comments on PRs with review instructions",
            "files": {
                "workflows": ["spec-kit-review-reminder.yml"],
            },
        },
        "review-helper": {
            "name": "Review Helper Workflow",
            "description": "Manual tools to check review status and validate branches",
            "files": {
                "workflows": ["spec-kit-review-helper.yml"],
            },
        },
        "pr-template": {
            "name": "Pull Request Template",
            "description": "Structured PR template with review checklist",
            "files": {
                "root": ["pull_request_template.md"],
            },
        },
        "issue-templates": {
            "name": "Issue Templates",
            "description": "9 structured issue templates for all workflow types",
            "files": {
                "directories": ["ISSUE_TEMPLATE"],
            },
        },
        "copilot-config": {
            "name": "GitHub Copilot Configuration",
            "description": "Copilot instructions and PR review configuration example",
            "files": {
                "root": ["copilot-instructions.md", "copilot.yml.example"],
            },
        },
        "codeowners": {
            "name": "CODEOWNERS Template",
            "description": "Example configuration for automatic reviewer assignment",
            "files": {
                "root": ["CODEOWNERS.example"],
            },
        },
        "documentation": {
            "name": "Documentation",
            "description": "Complete documentation for GitHub integration",
            "files": {
                "root": ["README.md"],
            },
        },
    }

    # Prompt user to select features (unless non-interactive)
    if non_interactive:
        # Install all features
        features_to_install = list(github_features.keys())
    else:
        console.print("\n[bold]GitHub Integration Features:[/bold]\n")

        for key, feature in github_features.items():
            console.print(f"  [cyan]{key:20}[/cyan] - {feature['description']}")

        console.print("\n[dim]Enter feature keys to install (comma-separated) or 'all' for everything:[/dim]")
        console.print("[dim]Example: review-enforcement,pr-template,issue-templates[/dim]")

        user_input = input("\nFeatures to install [all]: ").strip()

        if not user_input or user_input.lower() == "all":
            features_to_install = list(github_features.keys())
        else:
            features_to_install = [f.strip() for f in user_input.split(",")]
            # Validate feature keys
            invalid = [f for f in features_to_install if f not in github_features]
            if invalid:
                console.print(f"[red]✗[/red] Invalid feature(s): {', '.join(invalid)}")
                console.print(f"[dim]Available: {', '.join(github_features.keys())}[/dim]")
                return

    if not features_to_install:
        console.print("[yellow]⚠[/yellow] No features selected. Skipping GitHub integration.")
        return

    console.print(f"\n[blue]ℹ[/blue] Installing GitHub integration features: {', '.join(features_to_install)}\n")

    github_dir = repo_root / ".github"

    if not dry_run:
        github_dir.mkdir(parents=True, exist_ok=True)

    # Collect all files to install from selected features
    files_by_type = {"workflows": [], "root": [], "directories": []}

    for feature_key in features_to_install:
        feature = github_features[feature_key]
        for file_type, files in feature["files"].items():
            files_by_type[file_type].extend(files)

    # Remove duplicates
    for file_type in files_by_type:
        files_by_type[file_type] = list(set(files_by_type[file_type]))

    # Install workflow files
    if files_by_type["workflows"]:
        workflows_dir = github_dir / "workflows"
        if not dry_run:
            workflows_dir.mkdir(parents=True, exist_ok=True)

        for workflow in files_by_type["workflows"]:
            source_file = source_github / "workflows" / workflow
            if source_file.exists():
                if not dry_run:
                    shutil.copy(source_file, workflows_dir / workflow)
                console.print(f"[green]✓[/green] Installed workflow: {workflow}")
            else:
                console.print(f"[yellow]⚠[/yellow] Workflow {workflow} not found")

    # Install root .github files
    if files_by_type["root"]:
        for file in files_by_type["root"]:
            source_file = source_github / file
            if source_file.exists():
                if not dry_run:
                    shutil.copy(source_file, github_dir / file)
                console.print(f"[green]✓[/green] Installed: {file}")
            else:
                console.print(f"[yellow]⚠[/yellow] File {file} not found")

    # Install directories
    if files_by_type["directories"]:
        for directory in files_by_type["directories"]:
            source_directory = source_github / directory
            if source_directory.exists():
                dest_directory = github_dir / directory
                if not dry_run:
                    if dest_directory.exists():
                        shutil.rmtree(dest_directory)
                    shutil.copytree(source_directory, dest_directory)
                console.print(f"[green]✓[/green] Installed directory: {directory}")
            else:
                console.print(f"[yellow]⚠[/yellow] Directory {directory} not found")

    console.print("\n[bold green]✓ GitHub integration installed![/bold green]")
    console.print("\n[dim]Installed features:[/dim]")
    for feature_key in features_to_install:
        console.print(f"  [dim]✓ {github_features[feature_key]['name']}[/dim]")

    console.print("\n[bold cyan]Next steps:[/bold cyan]")
    console.print("  1. Review .github/README.md for complete documentation")
    if "codeowners" in features_to_install:
        console.print("  2. Customize .github/CODEOWNERS.example and rename to CODEOWNERS")
    console.print("  3. Commit and push the .github/ directory")
    console.print("\n  [dim]See .github/README.md for detailed usage instructions[/dim]")


@app.callback(invoke_without_command=True)
def main(
    extensions: List[str] = typer.Argument(
        None,
        help="Extensions to install (bugfix, modify, refactor, hotfix, deprecate)",
    ),
    all: bool = typer.Option(
        False,
        "--all",
        help="Install all available extensions",
    ),
    agent: Optional[Agent] = typer.Option(
        None,
        "--agent",
        help="Force specific agent (claude, copilot, cursor-agent, etc.)",
    ),
    agents: Optional[str] = typer.Option(
        None,
        "--agents",
        help=(
            "Install for multiple agents (comma-separated). "
            "Example: --agents claude,copilot,cursor-agent"
        ),
    ),
    link: bool = typer.Option(
        False,
        "--link",
        help=(
            "Opt-in: create symlinks for agent command files instead of copying. "
            "May be less portable on Windows/ZIP releases."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be installed without installing",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version",
    ),
    list_extensions: bool = typer.Option(
        False,
        "--list",
        help="List available extensions",
    ),
    llm_enhance: bool = typer.Option(
        True,
        "--llm-enhance/--no-llm-enhance",
        help="Create one-time command for LLM-enhanced constitution update (uses /specify.constitution)",
    ),
    enable: Optional[str] = typer.Option(
        None,
        "--enable",
        help="Comma-separated list of workflows to enable in enabled.conf (e.g., --enable bugfix,modify,refactor)",
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--no-interactive",
        help="Prompt to select which new workflows to enable (default: enabled)",
    ),
    github_token: str = typer.Option(
        None,
        "--github-token",
        help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)",
    ),
    script_type: Optional[str] = typer.Option(
        None,
        "--script",
        help="Script type to install: sh (bash) or ps (PowerShell)",
    ),
    github_integration: bool = typer.Option(
        False,
        "--github-integration",
        help="Install optional GitHub workflows, PR template, issue templates, and code review integration",
    ),
) -> None:
    """
    Installation tool for spec-kit-extensions that detects your existing
    spec-kit installation and mirrors the agent configuration.
    """

    # Handle --version
    if version:
        console.print(f"specify-extend version {__version__}")
        raise typer.Exit(0)

    # Handle --list
    if list_extensions:
        console.print("\n[bold]Available Extensions:[/bold]\n")

        extension_info = {
            "baseline": ("Establish project baseline and track all changes", "Document project comprehensively"),
            "bugfix": ("Bug remediation with regression-test-first approach", "Write regression test BEFORE fix"),
            "modify": ("Modify existing features with automatic impact analysis", "Review impact analysis before changes"),
            "refactor": ("Improve code quality while preserving behavior", "Tests pass after EVERY incremental change"),
            "hotfix": ("Emergency production fixes with expedited process", "Post-mortem required within 48 hours"),
            "deprecate": ("Planned feature sunset with 3-phase rollout", "Follow 3-phase sunset process"),
            "cleanup": ("Validate and reorganize spec-kit artifacts", "Maintain consistent structure"),
        }

        for ext, (desc, gate) in extension_info.items():
            console.print(f"  [cyan]{ext:12}[/cyan] - {desc}")
            console.print(f"               [dim]Quality Gate: {gate}[/dim]\n")

        console.print("[dim]Use: specify-extend [extension names...] or specify-extend --all[/dim]")
        raise typer.Exit(0)

    # Determine extensions to install
    if all:
        extensions_to_install = AVAILABLE_EXTENSIONS.copy()
    elif extensions:
        # Validate extensions
        invalid = [e for e in extensions if e not in AVAILABLE_EXTENSIONS]
        if invalid:
            console.print(
                f"[red]✗[/red] Invalid extension(s): {', '.join(invalid)}",
                style="red bold"
            )
            console.print(f"[dim]Available: {', '.join(AVAILABLE_EXTENSIONS)}[/dim]")
            raise typer.Exit(1)
        extensions_to_install = extensions
    else:
        console.print(
            "[red]✗[/red] No extensions specified. Use --all or specify extension names.",
            style="red bold"
        )
        console.print("\n[dim]Examples:[/dim]")
        console.print("  [dim]specify-extend --all[/dim]")
        console.print("  [dim]specify-extend bugfix modify refactor[/dim]")
        raise typer.Exit(1)

    # Get repository root
    repo_root = get_repo_root()

    # Validate spec-kit installation
    if not validate_speckit_installation(repo_root):
        raise typer.Exit(1)

    # Resolve target agents
    resolved_agents: List[str]

    if agent and agents:
        console.print("[red]✗[/red] Use either --agent or --agents, not both", style="red bold")
        raise typer.Exit(1)

    if agents:
        requested = [a.strip() for a in agents.split(",") if a.strip()]
        if not requested:
            console.print("[red]✗[/red] --agents provided but empty", style="red bold")
            raise typer.Exit(1)
        invalid = [a for a in requested if a not in AGENT_CONFIG]
        if invalid:
            console.print(
                f"[red]✗[/red] Invalid agent(s): {', '.join(invalid)}",
                style="red bold",
            )
            console.print(f"[dim]Available: {', '.join(sorted(AGENT_CONFIG.keys()))}[/dim]")
            raise typer.Exit(1)
        resolved_agents = requested
        console.print(f"[blue]ℹ[/blue] Installing for agents: {', '.join(resolved_agents)}")
    elif agent:
        resolved_agents = [agent.value]
        console.print(f"[blue]ℹ[/blue] Using forced agent: {resolved_agents[0]}")
    else:
        detected_agent = detect_agent(repo_root)
        resolved_agents = [detected_agent]
        console.print(f"[blue]ℹ[/blue] Detected agent: {detected_agent}")

    # Dry run summary
    if dry_run:
        console.print("\n[bold yellow]DRY RUN - Would install:[/bold yellow]")
        console.print(f"  Repository: {repo_root}")
        console.print(f"  Agents: {', '.join(resolved_agents)}")
        console.print(f"  Extensions: {', '.join(extensions_to_install)}")
        console.print(f"  Link mode: {'symlink' if link else 'copy'}")
        if github_integration:
            console.print(f"  GitHub integration: yes (interactive)" if interactive else "  GitHub integration: yes (all features)")
        raise typer.Exit(0)

    # Handle workflow enabling
    currently_enabled = read_enabled_conf(repo_root)
    workflows_to_enable = set()

    if enable:
        # User explicitly specified workflows to enable
        workflows_to_enable = set(enable.split(','))
        invalid = [w for w in workflows_to_enable if w not in AVAILABLE_EXTENSIONS]
        if invalid:
            console.print(f"[red]✗[/red] Invalid workflows: {', '.join(invalid)}")
            console.print(f"[dim]Available: {', '.join(AVAILABLE_EXTENSIONS)}[/dim]")
            raise typer.Exit(1)
    elif interactive and not dry_run:
        # Interactive mode: prompt for new workflows
        workflows_to_enable = prompt_for_workflows(
            AVAILABLE_EXTENSIONS,
            currently_enabled,
            set(extensions_to_install)
        )
    else:
        # Non-interactive: enable what's being installed + keep current
        workflows_to_enable = currently_enabled | set(extensions_to_install)

    # Download latest release
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        source_dir = download_latest_release(temp_path, github_token)

        if not source_dir:
            console.print(
                "[red]✗[/red] Failed to download extensions. Installation aborted.",
                style="red bold"
            )
            raise typer.Exit(1)

        # Install files
        console.print(f"\n[bold]Installing extensions:[/bold] {', '.join(extensions_to_install)}")
        console.print(f"[bold]Configured for:[/bold] {', '.join(resolved_agents)}\n")

        # Default the script type only once we reach installation. At this point,
        # agent resolution and related checks have already completed, so it's safe
        # to fall back to "sh" if the user did not explicitly pass --script.
        selected_script = script_type or "sh"
        if selected_script not in {"sh", "ps"}:
            console.print(
                f"[red]Error:[/red] Invalid --script option '{selected_script}'. Must be 'sh' or 'ps'."
            )
            raise typer.Exit(1)

        install_extension_files(
            repo_root,
            source_dir,
            extensions_to_install,
            dry_run,
            install_powershell=selected_script == "ps",
        )
        for target_agent in resolved_agents:
            install_agent_commands(
                repo_root,
                source_dir,
                target_agent,
                extensions_to_install,
                dry_run,
                link=link,
                install_powershell=selected_script == "ps",
            )

        # Constitution update is repo-level; use the first agent for formatting conventions
        update_constitution(repo_root, source_dir, resolved_agents[0], dry_run, llm_enhance)
        patch_common_sh(repo_root, dry_run)
        patch_update_agent_context_sh(repo_root, dry_run)

        # Install GitHub integration if requested
        if github_integration:
            install_github_integration(
                repo_root,
                source_dir,
                dry_run=dry_run,
                non_interactive=(not interactive),
            )

    # Update enabled.conf with selected workflows
    if workflows_to_enable and not dry_run:
        update_enabled_conf(repo_root, workflows_to_enable, dry_run)
        console.print(f"[blue]ℹ[/blue] Enabled workflows: {', '.join(sorted(workflows_to_enable))}\n")

    # Success message
    console.print("\n" + "━" * 60)
    console.print("[bold green]✓ spec-kit-extensions installed successfully![/bold green]")
    console.print("━" * 60 + "\n")

    console.print(f"[blue]ℹ[/blue] Installed extensions: {', '.join(extensions_to_install)}")
    console.print(f"[blue]ℹ[/blue] Configured for: {', '.join(resolved_agents)}\n")

    # Next steps
    console.print("[bold]Next steps:[/bold]")
    primary_agent = resolved_agents[0]
    agent_info = AGENT_CONFIG.get(primary_agent, AGENT_CONFIG["manual"])
    agent_name = agent_info["name"]

    if llm_enhance and primary_agent != "manual":
        if primary_agent == "copilot":
            console.print("  [bold yellow]1. Reference the constitution enhancement prompt[/bold yellow]")
            console.print("     [dim]In Copilot Chat, reference .github/prompts/speckit.enhance-constitution.md[/dim]")
            console.print("     [dim]This uses LLM intelligence to merge quality gates into your existing constitution[/dim]")
            console.print("     [dim]Delete both .github/prompts/ and .github/agents/ files after use[/dim]")
        else:
            console.print("  [bold yellow]1. Run /speckit.enhance-constitution to update your constitution[/bold yellow]")
            console.print("     [dim]This uses LLM intelligence to merge quality gates into your existing constitution[/dim]")
            console.print("     [dim]The command will self-destruct after use[/dim]")
        console.print("  2. Try a workflow command after constitution is updated")
        console.print("  3. Read the docs: .specify/extensions/README.md")
    elif primary_agent == "claude":
        console.print("  1. Try a command: /speckit.bugfix \"test bug\"")
        console.print("  2. Read the docs: .specify/extensions/README.md")
    elif primary_agent == "copilot":
        console.print("  1. Reload VS Code or restart Copilot")
        console.print("  2. Use in Copilot Chat: @workspace /speckit.bugfix \"test bug\"")
        console.print("  3. Read the docs: .specify/extensions/README.md")
    elif primary_agent == "cursor-agent":
        console.print("  1. Ask Cursor: /speckit.bugfix \"test bug\"")
        console.print("  2. Read the docs: .specify/extensions/README.md")
    else:
        console.print("  1. Run: .specify/scripts/bash/create-bugfix.sh \"test bug\"")
        console.print("  2. Ask your AI agent to implement following the generated files")
        console.print("  3. Read the docs: .specify/extensions/README.md")

    console.print()


if __name__ == "__main__":
    app()
