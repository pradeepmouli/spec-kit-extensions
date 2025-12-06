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
from pathlib import Path
from typing import Optional, List
from enum import Enum

import typer
import httpx
import ssl
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

__version__ = "1.0.0"

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
CONSTITUTION_SECTION = "Section VI: Workflow Selection and Quality Gates"

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
            console.print(f"[green]✓[/green] Installed /speckit.{ext} command")
        else:
            console.print(f"[yellow]⚠[/yellow] Command file for {ext} not found")


def update_constitution(
    repo_root: Path,
    source_dir: Path,
    dry_run: bool = False,
) -> None:
    """Update constitution with quality gates"""
    
    console.print("[blue]ℹ[/blue] Updating constitution with quality gates...")
    
    constitution_file = repo_root / ".specify" / "memory" / "constitution.md"
    
    if not dry_run:
        constitution_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if already has quality gates
        if constitution_file.exists():
            content = constitution_file.read_text()
            if CONSTITUTION_SECTION in content:
                console.print(
                    "[yellow]⚠[/yellow] Constitution already contains quality gates section"
                )
                return
        else:
            constitution_file.touch()
        
        # Append quality gates from template
        template_file = source_dir / "docs" / "constitution-template.md"
        if template_file.exists():
            template_content = template_file.read_text()
            with open(constitution_file, "a") as f:
                f.write("\n")
                f.write(template_content)
            console.print("[green]✓[/green] Constitution updated with quality gates")
        else:
            console.print("[yellow]⚠[/yellow] Constitution template not found")
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
        update_constitution(repo_root, source_dir, dry_run)
    
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
    
    if detected_agent == "claude":
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
