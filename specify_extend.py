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

Or install globally:
    uv tool install --from specify_extend.py specify-extend
    specify-extend --all
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

import typer
import httpx
import ssl
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

__version__ = "1.1.1"

# Set up HTTPS client for GitHub API requests
client = httpx.Client(follow_redirects=True)

# Initialize Rich console
console = Console()

# Constants
GITHUB_REPO_OWNER = "pradeepmouli"
GITHUB_REPO_NAME = "spec-kit-extensions"
GITHUB_REPO = f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
GITHUB_API_BASE = "https://api.github.com"

AVAILABLE_EXTENSIONS = ["bugfix", "modify", "refactor", "hotfix", "deprecate"]

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
            workflow_name = re.search(r'/(bugfix|modify|refactor|hotfix|deprecate)', pattern)
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
        return Path(result.stdout.strip())
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


def download_latest_release(temp_dir: Path) -> Optional[Path]:
    """Download the latest release from GitHub"""

    with console.status("[bold blue]Downloading latest extensions...") as status:
        try:
            # Get latest release info
            url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/releases/latest"
            response = client.get(url)
            response.raise_for_status()

            release_data = response.json()
            tag_name = release_data["tag_name"]

            console.print(f"[blue]ℹ[/blue] Latest version: {tag_name}")

            # Download zipball
            zipball_url = f"https://github.com/{GITHUB_REPO}/archive/refs/tags/{tag_name}.zip"

            status.update(f"[bold blue]Downloading {tag_name}...")
            response = client.get(zipball_url)
            response.raise_for_status()

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


def install_extension_files(
    repo_root: Path,
    source_dir: Path,
    extensions: List[str],
    dry_run: bool = False,
) -> None:
    """Install extension workflow templates and scripts"""

    console.print("[blue]ℹ[/blue] Installing extension files...")

    extensions_dir = repo_root / ".specify" / "extensions"
    scripts_dir = repo_root / ".specify" / "scripts" / "bash"

    if not dry_run:
        extensions_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir.mkdir(parents=True, exist_ok=True)

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

    # Copy bash scripts
    source_scripts = source_dir / "scripts"
    if source_scripts.exists():
        for ext in extensions:
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
) -> None:
    """Install agent-specific command files"""

    agent_info = AGENT_CONFIG.get(agent, AGENT_CONFIG["manual"])
    agent_name = agent_info["name"]

    if agent == "manual":
        console.print(f"[blue]ℹ[/blue] Installing for manual/generic agent setup...")
        console.print("  [dim]To use extensions, run bash scripts directly:[/dim]")
        console.print("  [dim].specify/scripts/bash/create-bugfix.sh \"description\"[/dim]")
        return

    console.print(f"[blue]ℹ[/blue] Installing {agent_name} commands...")

    folder = agent_info["folder"]
    file_ext = agent_info["file_extension"]

    if not folder:
        return

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
        # For now, we only have markdown files
        source_file = source_commands / f"speckit.{ext}.md"
        dest_file = commands_dir / f"speckit.{ext}.{file_ext or 'md'}"

        if source_file.exists():
            if not dry_run:
                shutil.copy(source_file, dest_file)

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

            # Check if workflow selection content already exists
            if detect_workflow_selection_section(content):
                console.print(
                    "[yellow]⚠[/yellow] Constitution already contains workflow selection and quality gates"
                )
                return

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


@app.command()
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
        False,
        "--llm-enhance",
        help="Create one-time command for LLM-enhanced constitution update (uses /specify.constitution)",
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
            "bugfix": ("Bug remediation with regression-test-first approach", "Write regression test BEFORE fix"),
            "modify": ("Modify existing features with automatic impact analysis", "Review impact analysis before changes"),
            "refactor": ("Improve code quality while preserving behavior", "Tests pass after EVERY incremental change"),
            "hotfix": ("Emergency production fixes with expedited process", "Post-mortem required within 48 hours"),
            "deprecate": ("Planned feature sunset with 3-phase rollout", "Follow 3-phase sunset process"),
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

    # Detect or use forced agent
    if agent:
        detected_agent = agent.value
        console.print(f"[blue]ℹ[/blue] Using forced agent: {detected_agent}")
    else:
        detected_agent = detect_agent(repo_root)
        console.print(f"[blue]ℹ[/blue] Detected agent: {detected_agent}")

    # Dry run summary
    if dry_run:
        console.print("\n[bold yellow]DRY RUN - Would install:[/bold yellow]")
        console.print(f"  Repository: {repo_root}")
        console.print(f"  Agent: {detected_agent}")
        console.print(f"  Extensions: {', '.join(extensions_to_install)}")
        raise typer.Exit(0)

    # Download latest release
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        source_dir = download_latest_release(temp_path)

        if not source_dir:
            console.print(
                "[red]✗[/red] Failed to download extensions. Installation aborted.",
                style="red bold"
            )
            raise typer.Exit(1)

        # Install files
        console.print(f"\n[bold]Installing extensions:[/bold] {', '.join(extensions_to_install)}")
        console.print(f"[bold]Configured for:[/bold] {detected_agent}\n")

        install_extension_files(repo_root, source_dir, extensions_to_install, dry_run)
        install_agent_commands(repo_root, source_dir, detected_agent, extensions_to_install, dry_run)
        update_constitution(repo_root, source_dir, detected_agent, dry_run, llm_enhance)

    # Success message
    console.print("\n" + "━" * 60)
    console.print("[bold green]✓ spec-kit-extensions installed successfully![/bold green]")
    console.print("━" * 60 + "\n")

    console.print(f"[blue]ℹ[/blue] Installed extensions: {', '.join(extensions_to_install)}")
    console.print(f"[blue]ℹ[/blue] Configured for: {detected_agent}\n")

    # Next steps
    console.print("[bold]Next steps:[/bold]")
    agent_info = AGENT_CONFIG.get(detected_agent, AGENT_CONFIG["manual"])
    agent_name = agent_info["name"]

    if llm_enhance and detected_agent != "manual":
        if detected_agent == "copilot":
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
    elif detected_agent == "claude":
        console.print("  1. Try a command: /speckit.bugfix \"test bug\"")
        console.print("  2. Read the docs: .specify/extensions/README.md")
    elif detected_agent == "copilot":
        console.print("  1. Reload VS Code or restart Copilot")
        console.print("  2. Use in Copilot Chat: @workspace /speckit.bugfix \"test bug\"")
        console.print("  3. Read the docs: .specify/extensions/README.md")
    elif detected_agent == "cursor-agent":
        console.print("  1. Ask Cursor: /speckit.bugfix \"test bug\"")
        console.print("  2. Read the docs: .specify/extensions/README.md")
    else:
        console.print("  1. Run: .specify/scripts/bash/create-bugfix.sh \"test bug\"")
        console.print("  2. Ask your AI agent to implement following the generated files")
        console.print("  3. Read the docs: .specify/extensions/README.md")

    console.print()


if __name__ == "__main__":
    app()
