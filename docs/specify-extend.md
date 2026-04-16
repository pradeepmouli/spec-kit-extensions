# specify-extend: Installation Tool

`specify-extend` is a Python CLI tool that works alongside GitHub's [spec-kit](https://github.com/github/spec-kit) to install and reconcile spec-kit-extensions in an existing spec-kit project. It automatically:
- Detects your existing spec-kit installation and agent configuration
- Reconciles requested agents through native spec-kit integrations when needed
- Installs the workflows extension from either the published archive or a local development source
- Optionally installs curated companion extensions, workflow packages, hooks, and GitHub integration assets

**Version**: 2.4.0 (CLI tool is versioned separately from extension templates)

## Installation

```bash
# Method 1: Install with pip
pip install git+https://github.com/pradeepmouli/spec-kit-extensions.git

# Method 2: Use with uvx (no installation needed)
uvx --from git+https://github.com/pradeepmouli/spec-kit-extensions.git specify-extend --all

# Method 3: Run directly with Python
python specify_extend.py --all
```

## Quick Start

After running `specify init` in your project:

```bash
# Install all extensions (auto-detects your agent)
specify-extend --all

# Install specific extensions
specify-extend bugfix modify refactor

# Preview what would be installed
specify-extend --dry-run --all

# Install from a local checkout during development
specify-extend --all --extension-source /path/to/spec-kit-extensions
```

## How It Works

### 1. Detects Your Setup

`specify-extend` automatically detects which AI agent you're using by examining your project structure:

| Agent | Detection Marker | Installed To |
|-------|-----------------|--------------|
| **Claude Code** | `.claude/commands/` directory | `.claude/commands/speckit.*.md` |
| **GitHub Copilot** | `.github/agents/` directory or `.github/copilot-instructions.md` | `.github/agents/speckit.{extension}.agent.md` + `.github/prompts/speckit.{extension}.prompt.md` |
| **Cursor** | `.cursor/commands/` directory | `.cursor/commands/speckit.{extension}.md` |
| **Gemini CLI** | `.gemini/commands/` directory | `.gemini/commands/speckit.{extension}.md` |
| **Qwen Code** | `.qwen/commands/` directory | `.qwen/commands/speckit.{extension}.md` |
| **opencode** | `.opencode/commands/` directory | `.opencode/commands/speckit.{extension}.md` |
| **Codex CLI** | `.codex/commands/` directory | `.codex/commands/speckit.{extension}.md` |
| **Amazon Q** | `.q/commands/` directory | `.q/commands/speckit.{extension}.md` |
| **Windsurf** | `.windsurf/` directory | `.windsurf/workflows/speckit.{extension}.md` |
| **Manual/Generic** | None of the above | Scripts only (use manually) |

### 2. Installs Extensions

Based on detected agent, it installs:

**Always installed:**
- The workflows extension via native `specify extension add`
- Extension workflow templates under `.specify/extensions/workflows/`
- Workflow creation scripts under `.specify/scripts/{bash|powershell}/`
- Constitution updates and enabled workflow configuration

**Agent-specific:**
- **Claude Code**: Command files → `.claude/commands/speckit.{extension}.md`
- **GitHub Copilot**: Agent files → `.github/agents/speckit.{extension}.agent.md` + Prompt files → `.github/prompts/speckit.{extension}.prompt.md`
- **Cursor**: Command files → `.cursor/commands/speckit.{extension}.md`
- **Gemini CLI**: Command files → `.gemini/commands/speckit.{extension}.md`
- **Qwen Code**: Command files → `.qwen/commands/speckit.{extension}.md`
- **opencode**: Command files → `.opencode/commands/speckit.{extension}.md`
- **Codex CLI**: Command files → `.codex/commands/speckit.{extension}.md`
- **Amazon Q**: Command files → `.q/commands/speckit.{extension}.md`
- **Windsurf**: Command files → `.windsurf/workflows/`
- **Manual**: Usage instructions printed to console

### 3. Validates Installation

Before installing, `specify-extend` checks:
- ✅ Git repository exists
- ✅ `.specify/` directory exists (spec-kit installed)
- ✅ Permissions to create/modify files

## Command Reference

### Options

```bash
specify-extend [OPTIONS] [EXTENSIONS...]
```

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message |
| `-v, --version` | Show version number |
| `--list` | List all available extensions |
| `--all` | Install all available extensions |
| `--ai AGENT` | Force a specific agent configuration |
| `--ai-commands-dir PATH` | Command directory for `--ai generic` |
| `--agents AGENTS` | Install for multiple agents in one repo |
| `--link` | Symlink agent command files instead of copying |
| `--dry-run` | Preview installation without making changes |
| `--with-community PROFILE` | Install curated companion extensions |
| `--with-workflows PROFILE` | Install curated workflow packages |
| `--extension-source PATH` | Install from a local extension source using a staged `--dev` copy |
| `--script {sh,ps}` | Install bash or PowerShell scripts |
| `--github-integration` | Install optional GitHub workflows and templates |
| `--hooks` | Install git hooks such as `commit-msg` |
| `--patch` | Only patch spec-kit's `common.sh` for extension branch support |
| `--llm-enhance` | Create one-time command for LLM-enhanced constitution update |

### Available Extensions

| Extension | Description | Quality Gate |
|-----------|-------------|--------------|
| `bugfix` | Bug remediation with regression-test-first | Test BEFORE fix |
| `modify` | Modify existing features with impact analysis | Review impact analysis first |
| `refactor` | Improve code quality while preserving behavior | Tests pass after EVERY change |
| `hotfix` | Emergency production fixes | Post-mortem within 48hrs |
| `deprecate` | Planned feature sunset with 3-phase rollout | Follow 3-phase process |

### Curated Bundle Options

`specify-extend` can also install curated add-on bundles:

- `--with-community recommended|all|none|...` installs companion extensions curated in this repo
- `--with-workflows recommended|all|none|...` installs standalone workflow packages curated in this repo
- `--extension-source PATH` stages a local checkout and installs it through native `specify extension add --dev`

## Usage Examples

### Basic Usage

```bash
# After running 'specify init'
cd your-project

# Install all extensions (recommended)
specify-extend --all

# Or install specific ones
specify-extend bugfix modify
```

### Advanced Usage

```bash
# Preview what would be installed
specify-extend --dry-run --all

# Install for multiple agents in the same repo (copy/generate)
specify-extend --agents claude,copilot,cursor-agent --all

# Opt-in: use symlinks for agent command files (advanced)
specify-extend --agents claude,cursor-agent --all --link

# Force Claude Code configuration even if not detected
specify-extend --ai claude --all

# Install only bug-related workflows
specify-extend bugfix hotfix

# See all available extensions
specify-extend --list

# Install the local checkout instead of the published archive
specify-extend --all --extension-source /path/to/spec-kit-extensions

# Add curated bundles
specify-extend --all --with-community recommended --with-workflows recommended

# Install PowerShell scripts and optional git/GitHub extras
specify-extend --all --script ps --hooks --github-integration

# Only patch spec-kit's common.sh after native extension installation
specify-extend --patch
```

### LLM-Enhanced Constitution Updates

By default, `specify-extend` appends quality gates to your constitution using simple text formatting. For a more intelligent merge that adapts to your existing constitution style, use `--llm-enhance`:

```bash
# Install with LLM-enhanced constitution update
specify-extend --all --llm-enhance
```

**How it works:**

1. **Creates a one-time prompt/command**:
   - For **GitHub Copilot**: Creates both `.github/agents/speckit.enhance-constitution.agent.md` and `.github/prompts/speckit.enhance-constitution.prompt.md` (matching spec-kit pattern)
   - For **other agents** (Claude, Cursor, etc.): Creates a command like `/speckit.enhance-constitution`
2. **You invoke it**:
   - **GitHub Copilot**: Reference the prompt in Copilot Chat or use as agent
   - **Other agents**: Run the command (e.g., `/speckit.enhance-constitution`)
3. **Intelligent merging**: The prompt/command instructs the AI to:
   - Preserve all existing constitution content
   - Intelligently merge workflow quality gates
   - Match your existing writing style and tone
   - Continue existing section numbering schemes
   - Avoid duplicating content
4. **Self-destructs**: The prompt/command includes instructions to delete itself after use to prevent confusion
   - **GitHub Copilot**: Delete both `.github/prompts/speckit.enhance-constitution.prompt.md` and `.github/agents/speckit.enhance-constitution.agent.md`

**When to use `--llm-enhance`:**

- ✅ You have a heavily customized constitution
- ✅ You want quality gates integrated naturally with your existing content
- ✅ Your constitution uses specific writing style/formatting
- ✅ You want to avoid simple append-to-end behavior

**When NOT to use:**

- ❌ Fresh project with minimal constitution (default works fine)
- ❌ You prefer deterministic, predictable updates
- ❌ You don't have an AI agent configured

**Examples:**

```bash
# Install with LLM enhancement
specify-extend --all --llm-enhance

# For GitHub Copilot users:
# In Copilot Chat, reference the prompt:
# "Review and apply .github/prompts/speckit.enhance-constitution.prompt.md"
# Then delete both .github/prompts/speckit.enhance-constitution.prompt.md
# and .github/agents/speckit.enhance-constitution.agent.md

# For Claude Code users:
/speckit.enhance-constitution

# The prompt/command will:
# 1. Read your existing constitution
# 2. Intelligently merge quality gates
# 3. Update .specify/memory/constitution.md
# 4. Instruct you to delete itself
```

### Agent-Specific Examples

#### Claude Code

```bash
# After 'specify init' creates .claude/commands/
specify-extend --all

# Try a command
/speckit.bugfix "test bug"
```

#### GitHub Copilot

```bash
# After 'specify init' with Copilot
specify-extend --all

# In Copilot Chat
/speckit.bugfix "test bug"
```

#### Cursor

```bash
# After 'specify init' with Cursor
specify-extend --all

# Ask Cursor
/speckit.bugfix "test bug"
```

#### Manual/Generic

```bash
# After 'specify init'
specify-extend --all

# Use scripts directly
.specify/scripts/bash/create-bugfix.sh "test bug"

# Then ask your AI agent to implement
```

## Installation Location

After running `specify-extend --all`, your project structure will be:

```
your-project/
├── .specify/
│   ├── extensions/              # ← Extension files
│   │   ├── README.md
│   │   ├── enabled.conf
│   │   └── workflows/
│   │       ├── bugfix/
│   │       ├── modify/
│   │       ├── refactor/
│   │       ├── hotfix/
│   │       └── deprecate/
│   ├── scripts/bash/            # ← Bash scripts
│   │   ├── create-bugfix.sh
│   │   ├── create-modification.sh
│   │   ├── create-refactor.sh
│   │   ├── create-hotfix.sh
│   │   └── create-deprecate.sh
│   ├── scripts/powershell/      # ← Optional when --script ps is used
│   │   ├── create-bugfix.ps1
│   │   ├── create-modification.ps1
│   │   ├── create-refactor.ps1
│   │   ├── create-hotfix.ps1
│   │   └── create-deprecate.ps1
│   └── memory/
│       └── constitution.md      # ← Updated with quality gates
├── .claude/commands/            # ← If using Claude Code
│   ├── speckit.bugfix.md
│   ├── speckit.modify.md
│   ├── speckit.refactor.md
│   ├── speckit.hotfix.md
│   └── speckit.deprecate.md
└── .github/                     # ← If using GitHub Copilot
    ├── agents/
   │   ├── speckit.bugfix.agent.md
   │   ├── speckit.modify.agent.md
   │   ├── speckit.refactor.agent.md
   │   ├── speckit.hotfix.agent.md
   │   └── speckit.deprecate.agent.md
    └── prompts/
        ├── speckit.bugfix.prompt.md
        ├── speckit.modify.prompt.md
        ├── speckit.refactor.prompt.md
        ├── speckit.hotfix.prompt.md
        └── speckit.deprecate.prompt.md
```

## Troubleshooting

### "No .specify directory found"

**Problem**: spec-kit not installed

**Solution**: Run `specify init` first:
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify init .
```

### "Permission denied"

**Problem**: Script not executable

**Solution**: Make it executable:
```bash
chmod +x specify-extend
```

### "Extensions directory not found" or local source validation errors

**Problem**: The local checkout passed to `--extension-source` is missing required files such as `extension.yml`, `commands/`, or `scripts/`.

**Solution**:
```bash
# Point to the repository root
specify-extend --all --extension-source /path/to/spec-kit-extensions

# Or install the published archive instead
specify-extend --all
```

### Agent Not Detected Correctly

**Problem**: Wrong agent detected

**Solution**: Force the agent:
```bash
specify-extend --ai claude --all
specify-extend --ai copilot --all
specify-extend --ai cursor-agent --all
```

### Already Existing Files

**Behavior**:
- **Extension files**: Overwritten (safe - templates)
- **Copilot instructions**: Appended (preserves existing)
- **Cursor rules**: Appended (preserves existing)
- **Constitution**: Appended (preserves existing)

If you want to start fresh:
```bash
# Remove extensions
rm -rf .specify/extensions/
rm -f .specify/scripts/bash/create-{baseline,bugfix,cleanup,deprecate,enhance,hotfix,modification,refactor}.sh
rm -f .specify/scripts/powershell/create-{baseline,bugfix,cleanup,deprecate,enhance,hotfix,modification,refactor}.ps1

# Remove agent config (choose one)
rm -rf .claude/commands/speckit.*.md  # Claude
# or remove generated .github/agents/speckit.* and .github/prompts/speckit.*  # Copilot
# or rm -rf .cursor/commands/speckit.*.md  # Cursor

# Reinstall
specify-extend --all
```

## Updating Extensions

To update to newer versions:

```bash
# Reinstall from the published source
specify-extend --all

# Or reinstall from an updated local checkout
specify-extend --all --extension-source /path/to/spec-kit-extensions
```

**Note**: This will overwrite workflow templates and scripts but preserve your:
- Custom modifications to `.specify/extensions/enabled.conf`
- Existing projects in `specs/`
- Custom additions to constitution (it only appends)

## Uninstalling

To remove extensions:

```bash
# Remove extension files
rm -rf .specify/extensions/
rm -f .specify/scripts/bash/create-{baseline,bugfix,cleanup,deprecate,enhance,hotfix,modification,refactor}.sh
rm -f .specify/scripts/powershell/create-{baseline,bugfix,cleanup,deprecate,enhance,hotfix,modification,refactor}.ps1

# Remove agent-specific files
rm .claude/commands/speckit.*.md  # Claude Code
rm .github/agents/speckit.*.agent.md .github/prompts/speckit.*.prompt.md  # GitHub Copilot
rm .cursor/commands/speckit.*.md  # Cursor

# Manually edit these to remove extension sections:
# - .specify/memory/constitution.md (all)

# Remove workflow directories (optional)
rm -rf specs/baseline
rm -rf specs/bugfix
rm -rf specs/cleanup
rm -rf specs/enhance
rm -rf specs/hotfix
rm -rf specs/refactor
rm -rf specs/deprecate
rm -rf specs/modify
```

## Integration with specify init

### Recommended Workflow

```bash
# 1. Clone/create your project
git clone https://github.com/you/your-project.git
cd your-project

# 2. Initialize spec-kit
specify init .

# 3. Install extensions
specify-extend --all

# 4. Start using workflows
/speckit.specify "new feature"        # Core spec-kit
/speckit.bugfix "fix bug"             # Extension
/speckit.modify 001 "change feature"  # Extension
```

### For New Projects

```bash
# Create from template
mkdir my-project && cd my-project
git init

# Setup spec-kit
specify init .

# Add extensions
specify-extend --all

# You're ready!
```

### For Existing Projects

```bash
# Already have spec-kit
cd existing-project

# Add extensions
specify-extend bugfix modify  # Just what you need

# Or add all
specify-extend --all
```

## Environment Variables

`specify-extend` accepts a GitHub token through either the CLI or environment:

- `--github-token`
- `GH_TOKEN`
- `GITHUB_TOKEN`

This is mainly used when downloading the published archive or avoiding GitHub API rate limits.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (see error message) |

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for the current release history. This document focuses on how to use the CLI rather than duplicating release notes.

## Contributing

Found a bug or want to add support for a new agent?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- How to report issues
- How to add new agent support
- Code style guidelines
- Testing requirements

## License

MIT License - Same as spec-kit and spec-kit-extensions

## See Also

- [spec-kit](https://github.com/github/spec-kit) - Core workflow system
- [INSTALLATION.md](../INSTALLATION.md) - Manual installation guide
- [AI-AGENTS.md](../AI-AGENTS.md) - Agent compatibility details
- [README.md](../README.md) - Main project documentation
