# specify-extend: Installation Tool

`specify-extend` is a Python CLI tool that works alongside GitHub's [spec-kit](https://github.com/github/spec-kit) to seamlessly install spec-kit-extensions. It automatically:
- Downloads the latest extensions from GitHub releases
- Detects your existing spec-kit installation and agent configuration
- Installs extensions matching your setup

**Version**: v1.1.1 (CLI tool is versioned separately from extension templates)

## Installation

```bash
# Method 1: Install with pip
pip install git+https://github.com/pradeepmouli/spec-kit-extensions.git

# Method 2: Use with uvx (no installation needed)
uvx --from git+https://github.com/pradeepmouli/spec-kit-extensions.git specify-extend --all

# Method 3: Run directly with Python
python -m specify_extend --all
```

## Quick Start

After running `specify init` in your project:

```bash
# Install all extensions (auto-detects your agent, downloads latest from GitHub)
specify-extend --all

# Install specific extensions
specify-extend bugfix modify refactor

# Preview what would be installed
specify-extend --dry-run --all
```

## How It Works

### 1. Detects Your Setup

`specify-extend` automatically detects which AI agent you're using by examining your project structure:

| Agent | Detection Marker | Installed To |
|-------|-----------------|--------------|
| **Claude Code** | `.claude/commands/` directory | `.claude/commands/speckit.*.md` |
| **GitHub Copilot** | `.github/agents/` directory | `.github/agents/speckit.{extension}.md` + `.github/prompts/speckit.{extension}.prompt.md` |
| **Cursor** | `.cursor/commands/` directory | `.cursor/commands/speckit.{extension}.md` |
| **Gemini CLI** | `.gemini/commands/` directory | `.gemini/commands/speckit.{extension}.toml` |
| **Qwen Code** | `.qwen/commands/` directory | `.qwen/commands/speckit.{extension}.toml` |
| **opencode** | `.opencode/commands/` directory | `.opencode/commands/speckit.{extension}.md` |
| **Codex CLI** | `.codex/commands/` directory | `.codex/commands/speckit.{extension}.md` |
| **Amazon Q** | `.q/commands/` directory | `.q/commands/speckit.{extension}.md` |
| **Windsurf** | `.windsurf/` directory | `.windsurf/workflows/speckit.{extension}.md` (coming soon) |
| **Manual/Generic** | None of the above | Scripts only (use manually) |

### 2. Installs Extensions

Based on detected agent, it installs:

**Always installed:**
- Extension workflow templates → `.specify/extensions/workflows/{extension}/`
- Bash scripts → `.specify/scripts/bash/create-{extension}.sh`
- Quality gates → `.specify/memory/constitution.md` (appended)

**Agent-specific:**
- **Claude Code**: Command files → `.claude/commands/speckit.{extension}.md`
- **GitHub Copilot**: Agent files → `.github/agents/speckit.{extension}.md` + Prompt files → `.github/prompts/speckit.{extension}.prompt.md`
- **Cursor**: Command files → `.cursor/commands/speckit.{extension}.md`
- **Gemini CLI**: Command files → `.gemini/commands/speckit.{extension}.toml`
- **Qwen Code**: Command files → `.qwen/commands/speckit.{extension}.toml`
- **opencode**: Command files → `.opencode/commands/speckit.{extension}.md`
- **Codex CLI**: Command files → `.codex/commands/speckit.{extension}.md`
- **Amazon Q**: Command files → `.q/commands/speckit.{extension}.md`
- **Windsurf**: Command files → `.windsurf/workflows/` (coming soon)
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
| `--agent AGENT` | Force specific agent configuration |
| `--dry-run` | Preview installation without making changes |
| `--llm-enhance` | Create one-time command for LLM-enhanced constitution update |

### Available Extensions

| Extension | Description | Quality Gate |
|-----------|-------------|--------------|
| `bugfix` | Bug remediation with regression-test-first | Test BEFORE fix |
| `modify` | Modify existing features with impact analysis | Review impact analysis first |
| `refactor` | Improve code quality while preserving behavior | Tests pass after EVERY change |
| `hotfix` | Emergency production fixes | Post-mortem within 48hrs |
| `deprecate` | Planned feature sunset with 3-phase rollout | Follow 3-phase process |

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
specify-extend --agent claude --all

# Install only bug-related workflows
specify-extend bugfix hotfix

# See all available extensions
specify-extend --list
```

### LLM-Enhanced Constitution Updates

By default, `specify-extend` appends quality gates to your constitution using simple text formatting. For a more intelligent merge that adapts to your existing constitution style, use `--llm-enhance`:

```bash
# Install with LLM-enhanced constitution update
specify-extend --all --llm-enhance
```

**How it works:**

1. **Creates a one-time prompt/command**:
   - For **GitHub Copilot**: Creates both `.github/agents/speckit.enhance-constitution.md` and `.github/prompts/speckit.enhance-constitution.prompt.md` (matching spec-kit pattern)
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
   - **GitHub Copilot**: Delete both `.github/prompts/speckit.enhance-constitution.prompt.md` and `.github/agents/speckit.enhance-constitution.md`

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
# and .github/agents/speckit.enhance-constitution.md

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
/bugfix "test bug"
```

#### Cursor

```bash
# After 'specify init' with Cursor
specify-extend --all

# Ask Cursor
/bugfix "test bug"
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

### "Extensions directory not found"

**Problem**: Running specify-extend from wrong location

**Solution**:
```bash
# Option 1: Install specify-extend globally
cp specify-extend /usr/local/bin/
chmod +x /usr/local/bin/specify-extend

# Option 2: Use full path
/path/to/spec-kit-extensions/specify-extend --all

# Option 3: Add to PATH
export PATH="/path/to/spec-kit-extensions:$PATH"
```

### Agent Not Detected Correctly

**Problem**: Wrong agent detected

**Solution**: Force the agent:
```bash
specify-extend --agent claude --all
specify-extend --agent copilot --all
specify-extend --agent cursor --all
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
rm .specify/scripts/bash/create-{bugfix,modification,refactor,hotfix,deprecate}.sh

# Remove agent config (choose one)
rm -rf .claude/commands/speckit.*.md  # Claude
# or manually edit .github/copilot-instructions.md  # Copilot
# or manually edit .cursorrules  # Cursor

# Reinstall
specify-extend --all
```

## Updating Extensions

To update to newer versions:

```bash
# Get latest spec-kit-extensions
cd /path/to/spec-kit-extensions
git pull

# Reinstall (overwrites templates and scripts)
cd your-project
/path/to/spec-kit-extensions/specify-extend --all
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
rm .specify/scripts/bash/create-{bugfix,modification,refactor,hotfix,deprecate}.sh

# Remove agent-specific files
rm .claude/commands/speckit.*.md  # Claude Code

# Manually edit these to remove extension sections:
# - .github/copilot-instructions.md (Copilot)
# - .cursorrules (Cursor)
# - .specify/memory/constitution.md (all)

# Remove workflow directories (optional)
rm -rf specs/bugfix
rm -rf specs/refactor
rm -rf specs/hotfix
rm -rf specs/deprecate
# Keep feature modifications
# rm -rf specs/*/modifications/
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

Currently, `specify-extend` doesn't use environment variables, but you can configure behavior via options.

Future versions may support:
- `SPECIFY_EXTEND_AGENT` - Default agent
- `SPECIFY_EXTEND_EXTENSIONS_PATH` - Custom extensions path

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (see error message) |

## Version History

### 1.1.1 (2025-12-08)
- **GitHub Copilot Prompt File Naming**: Corrected prompt file naming pattern to `speckit.*.prompt.md` to match GitHub Copilot's expected convention
- **Removed Unsupported Scripts Section**: Removed `scripts:` frontmatter from all command files (GitHub Copilot does not support it)
- **Explicit Script Paths**: Replaced `{SCRIPT}` template variables with explicit script paths in command files

### 1.1.0 (2025-12-08)
- **LLM-Enhanced Constitution Updates**: New `--llm-enhance` flag for intelligent constitution merging using AI
  - Creates one-time prompt/command that leverages AI to intelligently merge quality gates
  - For GitHub Copilot: Creates both `.github/agents/` and `.github/prompts/` files
  - For other agents: Creates command file for invocation
  - Self-destruct instructions to prevent accidental re-use
- **GitHub Copilot Agent + Prompt Support**: Proper dual-file installation matching spec-kit pattern
  - All workflow commands create both agent and prompt files for Copilot
  - Prompt files are lightweight pointers (`agent: speckit.{workflow}`)
  - Follows spec-kit's implementation for better integration
- **Documentation**: Comprehensive guide for `--llm-enhance` feature and Copilot-specific patterns

### 1.0.1 (2025-12-08)
- **Intelligent Section Numbering**: Auto-detects and continues Roman numeral (I, II, III) or numeric (1, 2, 3) section numbering in constitutions
- **Edge Case Handling**: Improved section detection and parsing robustness for malformed constitution files
- **Code Quality**: Refactored with named constants and enhanced documentation
- **Bug Fixes**: More reliable section insertion logic with better error handling

### 1.0.0 (2025-12-06)
- **Python CLI tool**: Built with `typer` framework, installable via pip, uvx, or runnable directly
- **GitHub Download**: Automatically downloads latest extensions from GitHub releases
- **Multi-agent Support**: Claude, Gemini, Copilot, Cursor, Qwen, opencode, Codex, Amazon Q, Windsurf
- **Auto-detection**: Identifies agent by examining project structure
- **Agent-specific installation**: Installs commands matching detected agent format
- **Features**: `--all`, `--dry-run`, `--agent` options
- **Validation**: Extension name and agent validation with clear error messages
- **Compatibility**: Python 3.11+
- Note: Windsurf support marked as "coming soon" pending full implementation
- Note: Gemini and Qwen use markdown files as fallback (TOML generation coming soon)

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
