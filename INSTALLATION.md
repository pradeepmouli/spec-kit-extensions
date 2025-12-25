# Installation Guide

This guide covers installing **spec-kit-extensions** for different scenarios.

## Prerequisites

Before installing, ensure you have:

- ✅ **spec-kit** installed (v0.0.18+)
  ```bash
  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
  ```
- ✅ **Git** repository initialized
- ✅ **AI coding agent** (Claude Code, GitHub Copilot, etc.) - optional but recommended

## Quick Install (Recommended)

**The `specify-extend` tool is the easiest way to install extensions:**

```bash
# 1. In your project, initialize spec-kit (if not already done)
cd your-project
specify init .

# 2. Install specify-extend (choose one method)

# Method A: Install with pip from PyPI (Recommended)
pip install specify-extend
specify-extend --all
specify-extend --all --script ps  # Optional: install PowerShell workflows

# Optional: install command files for multiple agents in the same repo
specify-extend --agents claude,copilot,cursor-agent --all

# Optional (advanced): use symlinks instead of copying agent command files
specify-extend --agents claude,cursor-agent --all --link

# Method B: Use with uvx (no installation)
uvx specify-extend --all

# Method C: Install from GitHub (for development or latest unreleased features)
pip install git+https://github.com/pradeepmouli/spec-kit-extensions.git
specify-extend --all

# Method D: Run Python script directly from source
git clone https://github.com/pradeepmouli/spec-kit-extensions.git /tmp/spec-kit-extensions
python3 /tmp/spec-kit-extensions/specify_extend.py --all
rm -rf /tmp/spec-kit-extensions
```

**What it does:**
- ✅ Downloads latest extensions from GitHub releases
- ✅ Automatically detects your AI agent (Claude, Gemini, Copilot, Cursor, Qwen, opencode, Codex, Amazon Q, etc.)
- ✅ Installs appropriate extensions and commands
- ✅ Updates constitution with quality gates
- ✅ Makes scripts executable

See [specify-extend documentation](docs/specify-extend.md) for advanced usage.

## Manual Installation Methods

If you prefer manual installation or need more control, choose one of these methods:

### Method 1: Add to Existing spec-kit Project

**Use this if:** You already have a spec-kit project and want to add extensions manually

```bash
# 1. Clone extensions repo to temporary location
git clone https://github.com/pradeepmouli/spec-kit-extensions.git /tmp/spec-kit-extensions

# 2. Navigate to your project
cd your-project

# 3. Copy extension workflows
cp -r /tmp/spec-kit-extensions/extensions/* .specify/extensions/

# 4. Copy bash scripts
cp /tmp/spec-kit-extensions/scripts/create-*.sh .specify/scripts/bash/

# 4b. Optional: Copy PowerShell scripts (Windows-friendly)
cp /tmp/spec-kit-extensions/scripts/powershell/create-*.ps1 .specify/scripts/powershell/

# 5. Copy Claude Code commands (if using Claude Code)
mkdir -p .claude/commands
cp /tmp/spec-kit-extensions/commands/*.md .claude/commands/

# 6. Merge constitution (append workflow quality gates)
cat /tmp/spec-kit-extensions/docs/constitution-template.md >> .specify/memory/constitution.md

# 7. Make scripts executable
chmod +x .specify/scripts/bash/create-*.sh

# 8. Clean up
rm -rf /tmp/spec-kit-extensions

# 9. Verify installation
/bugfix --help
```

### Method 2: Git Submodule (For Teams)

**Use this if:** You want to track updates to extensions or share across multiple projects

```bash
# 1. Add as submodule
cd your-project
git submodule add https://github.com/pradeepmouli/spec-kit-extensions.git .specify/extension-source

# 2. Create symlinks to extension files
ln -s ..extension-source/extensions .specify/extensions
ln -s ../../.specify/extension-source/scripts/bash/* .specify/scripts/bash/
# Optional: PowerShell scripts (only if you want PowerShell workflows)
ln -s ../../.specify/extension-source/scripts/powershell/* .specify/scripts/powershell/
mkdir -p .claude/commands
ln -s ../../.specify/extension-source/commands/* .claude/commands/

# 3. Merge constitution
cat .specify/extension-source/docs/constitution-template.md >> .specify/memory/constitution.md

# 4. Initialize submodule
git submodule update --init --recursive

# 5. Verify installation
/bugfix --help

# To update extensions later:
git submodule update --remote .specify/extension-source
```

### Method 4: Manual Installation (Without Git)

**Use this if:** You want to manually download and install

1. Download the [latest release](https://github.com/[your-username]/spec-kit-extensions/releases) as ZIP
2. Extract to temporary directory
3. Follow steps from **Method 2** starting at step 2

## Verification

After installation, verify everything works:

### Test Claude Code Commands

```bash
# Test each command (should show usage)
/speckit.bugfix --help
/speckit.modify --help
/speckit.refactor --help
/speckit.hotfix --help
/speckit.deprecate --help
```

### Test Bash Scripts

```bash
# Should list available features
.specify/scripts/bash/create-modification.sh --list-features

# Should show help
.specify/scripts/bash/create-bugfix.sh --help
```

### Check File Structure

```bash
# Verify extensions directory
ls .specify/extensions/
# Should show: README.md, QUICKSTART.md, enabled.conf, workflows/

# Verify scripts
ls .specify/scripts/bash/create-*.sh
# Should show: create-bugfix.sh, create-modification.sh, etc.
ls .specify/scripts/powershell/create-*.ps1
# Should show: create-bugfix.ps1, create-modification.ps1, etc.

# Verify commands (if using Claude Code)
ls .claude/commands/*.md
# Should show: speckit.bugfix.md, speckit.modify.md, speckit.refactor.md, speckit.hotfix.md, speckit.deprecate.md
```

## Configuration

### Enable/Disable Workflows

Edit `.specify/extensions/enabled.conf` to control which workflows are available:

```bash
# Enable a workflow (uncomment)
bugfix

# Disable a workflow (comment out)
# refactor
```

### Customize Templates

Workflow templates are in `.specify/extensions/workflows/{workflow-name}/`:

```bash
# Example: Customize bugfix template
nano .specify/extensions/workflows/bugfix/bug-report-template.md
```

### Update Constitution

The constitution defines quality gates for each workflow. Review and customize:

```bash
nano .specify/memory/constitution.md
```

Look for **Section VI: Workflow Selection and Quality Gates**

## Troubleshooting

### "Command not found" Error

**Problem**: `/bugfix` or other commands don't work

**Solution**:
1. Verify commands are in `.claude/commands/`:
   ```bash
   ls .claude/commands/*.md
   ```
2. If using Claude Code, restart the agent
3. If files are missing, re-run installation step 5

### "Permission denied" When Running Scripts

**Problem**: Scripts won't execute

**Solution**:
```bash
chmod +x .specify/scripts/bash/create-*.sh
```

### "Feature directory not found" Error

**Problem**: `/modify` can't find parent feature

**Solution**:
1. Ensure you're in the repository root
2. Verify parent feature exists:
   ```bash
   ls specs/ | grep "^014-"
   ```
3. Use correct feature number in command

### Wrong Branch Created

**Problem**: Branch names don't match expected pattern

**Solution**:
1. Delete incorrect branch:
   ```bash
   git branch -D incorrect-branch-name
   ```
2. Re-run command with correct syntax (check command documentation)

### Extensions Don't Work with My AI Agent

**Problem**: Using Copilot/Cursor/other agent and commands don't work

**Solution**:

Each AI agent requires different setup. See **[AI-AGENTS.md](AI-AGENTS.md)** for detailed setup guides for:
- GitHub Copilot (with example `.github/copilot-instructions.md`)
- Cursor (with example `.cursorrules`)
- Windsurf (with project rules)
- Gemini CLI and other CLI tools
- Universal fallback for any agent

**Quick fixes**:

**For GitHub Copilot**:
1. Create `.github/copilot-instructions.md`
2. Add content from `.claude/commands/speckit.*.md`
3. Format as Copilot instructions
4. See [AI-AGENTS.md](AI-AGENTS.md#2-github-copilot) for complete example

**For Cursor**:
1. Create `.cursorrules` file
2. Add command definitions as rules
3. See [AI-AGENTS.md](AI-AGENTS.md#3-cursor) for complete example

**For Manual Use (any agent)**:
- Run bash scripts directly (PowerShell scripts are optional):
  ```bash
  .specify/scripts/bash/create-bugfix.sh "bug description"
  ```
  ```powershell
  # Optional: if PowerShell scripts are installed
  .specify/scripts/powershell/create-bugfix.ps1 "bug description"
  ```
- Then ask your AI agent to implement following the generated files
- See [AI-AGENTS.md](AI-AGENTS.md#7-universal-fallback-any-ai-agent) for details

## Updating Extensions

### Check Current Versions

```bash
# Check CLI tool version
specify-extend --version

# Check template version
cat .specify/extensions/README.md | grep "Extension Templates Version"
```

**Note**: This project has two independently versioned components:
- **Extension Templates** (workflows, commands, scripts) - Currently v2.1.1
- **CLI Tool** (`specify-extend`) - Currently v1.0.1

### Update CLI Tool

```bash
# Update from PyPI
pip install --upgrade specify-extend

# Or with uvx (always uses latest)
uvx specify-extend --all
```

### Update Templates

```bash
# Use specify-extend to update templates
specify-extend --all

# This will download the latest template version from GitHub releases
```

### Update from Git (Manual Method)

```bash
# Pull latest version
cd /tmp
git clone https://github.com/[your-username]/spec-kit-extensions.git
cd your-project

# Backup your customizations
cp .specify/extensions/enabled.conf /tmp/enabled.conf.backup

# Update files
cp -r /tmp/spec-kit-extensions/extensions/* .specify/extensions/
cp /tmp/spec-kit-extensions/scripts/create-*.sh .specify/scripts/bash/

# Restore customizations
cp /tmp/enabled.conf.backup .specify/extensions/enabled.conf

# Clean up
rm -rf /tmp/spec-kit-extensions
```

### Update from Submodule (Method 3)

```bash
git submodule update --remote .specify/extension-source
git add .specify/extension-source
git commit -m "Update spec-kit-extensions to latest version"
```

## Uninstallation

To remove extensions:

```bash
# Remove extension files
rm -rf .specify/extensions/
rm .specify/scripts/bash/create-{bugfix,modification,refactor,hotfix,deprecate}.sh
rm .claude/commands/speckit.{bugfix,modify,refactor,hotfix,deprecate}.md

# Remove constitution sections (manual - search for "Section VI")
nano .specify/memory/constitution.md

# Remove workflow specs (if desired)
rm -rf specs/bugfix
rm -rf specs/refactor
rm -rf specs/hotfix
rm -rf specs/deprecate
```

## Next Steps

After successful installation:

1. **Read the Quick Start**: [QUICKSTART.md](extensions/QUICKSTART.md) - 5-minute tutorial
2. **Try a Workflow**: Pick a real bug or refactor and use the appropriate workflow
3. **Read Examples**: [EXAMPLES.md](EXAMPLES.md) - See real-world usage from Tweeter project
4. **Customize**: Adjust templates and enabled workflows for your team's needs

## Getting Help

- **Installation Issues**: [Open an issue](https://github.com/[your-username]/spec-kit-extensions/issues/new?template=installation.md)
- **General Questions**: [Start a discussion](https://github.com/[your-username]/spec-kit-extensions/discussions)
- **spec-kit Issues**: [spec-kit repo](https://github.com/github/spec-kit)

---

**Installation complete?** → [Quick Start Guide](extensions/QUICKSTART.md)
