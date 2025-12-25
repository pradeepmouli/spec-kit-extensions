# Adding New AI Agent Support to spec-kit-extensions

This guide explains how to add support for a new AI coding agent to spec-kit-extensions.

> **Note**: This document is for **maintainers** who want to add new agent support to the codebase. If you're a **user** looking to use spec-kit-extensions with your AI agent, see [AI-AGENTS.md](AI-AGENTS.md) instead.

## Overview

spec-kit-extensions supports multiple AI coding agents by:
1. Detecting agent configuration in user projects
2. Installing extension commands in agent-specific formats
3. Configuring agent-specific directory structures

The integration is handled primarily through the `specify-extend` CLI tool (`specify_extend.py`).

## Steps to Add a New Agent

### 1. Update Agent Configuration

Add the new agent to the `AGENT_CONFIG` dictionary in `specify_extend.py`:

```python
AGENT_CONFIG = {
    # ... existing agents ...
    "new-agent-cli": {  # Use actual CLI tool name, not shorthand!
        "name": "New Agent Display Name",
        "folder": ".new-agent/commands",  # Directory where commands are stored
        "file_extension": "md",  # or "toml" depending on agent format
        "requires_cli": True,  # True if agent has a CLI tool to check
    },
}
```

**Configuration fields:**
- `name`: Human-readable agent name for display
- `folder`: Directory where agent-specific command files are stored (relative to project root)
- `file_extension`: File format for commands (`md` for Markdown, `toml` for TOML)
- `requires_cli`: Whether the agent requires a CLI tool check during installation

#### Critical: Use Actual CLI Tool Names as Keys

**Always use the actual executable name** as the dictionary key, not a shortened or convenient version.

**Why this matters:**
- The detection and validation code uses the key to check for the actual CLI tool
- Using shorthand requires special-case mappings throughout the codebase
- This creates unnecessary complexity and maintenance burden

**Example - The Cursor Lesson:**

The codebase currently has an `Agent` enum with `cursor = "cursor-agent"` which creates a mapping. While this works, it's an exception that should be avoided for new agents.

❌ **Avoid this pattern** (requires enum mapping):
```python
# In Agent enum
class Agent(str, Enum):
    newagent = "new-agent-cli"  # Creates extra mapping layer

# In AGENT_CONFIG
AGENT_CONFIG = {
    "new-agent-cli": {  # Must match enum value, not enum name
        "name": "New Agent",
        # ...
    }
}
```

✅ **Preferred approach** (direct naming):
```python
# In Agent enum
class Agent(str, Enum):
    new_agent_cli = "new-agent-cli"  # Enum name matches value (using underscore)

# In AGENT_CONFIG
AGENT_CONFIG = {
    "new-agent-cli": {  # Matches both enum value and actual CLI tool name
        "name": "New Agent",
        # ...
    }
}
```

### 2. Update Agent Detection

Add detection logic to the `detect_agent()` function in `specify_extend.py`:

```python
def detect_agent(repo_root: Path) -> str:
    """Detect which AI agent is configured by examining project structure"""

    # ... existing checks ...

    # Check for New Agent (example)
    if (repo_root / ".new-agent-cli" / "commands").exists():
        return "new-agent-cli"  # Return value matching AGENT_CONFIG key

    # ... remaining checks ...
```

Detection is based on the presence of agent-specific directories or configuration files.

#### Agent Detection Priority Order

The `detect_agent()` function checks for agents in this priority order (as of specify_extend.py:473-513):

1. **Claude Code**: `.claude/commands/`
2. **GitHub Copilot**: `.github/agents/` or `.github/copilot-instructions.md`
3. **Cursor**: `.cursor/commands/` or `.cursorrules`
4. **Windsurf**: `.windsurf/`
5. **Other agents**: Based on AGENT_CONFIG directory patterns
6. **Fallback**: Manual agent selection if no detection succeeds

When adding a new agent, consider where it should fit in this priority order based on:
- Specificity of detection (more specific = higher priority)
- Likelihood of false positives (less likely = higher priority)
- Common usage patterns (more common = higher priority)

### 3. Add Command Templates

Create command template files in the `commands/` directory following the agent's format:

#### Markdown Format (Claude, Cursor, Copilot, opencode, Windsurf, Amazon Q)

**File**: `commands/speckit.bugfix.md` (example)

```markdown
---
description: "Fix bugs with regression-test-first approach"
---

Execute the bugfix workflow script with the provided description:

```bash
.specify/scripts/bash/create-bugfix.sh "$ARGUMENTS"
```

This creates:
- Branch: `bugfix/NNN-description`
- Directory: `specs/bugfix/NNN-description/`
- Files: `bug-report.md`, `tasks.md`

Quality Gate: **Write regression test BEFORE implementing fix**
```

**For GitHub Copilot** (special case with mode):
```markdown
---
description: "Fix bugs with regression-test-first approach"
mode: speckit.bugfix
---

Execute the bugfix workflow script...
```

#### TOML Format (Gemini, Qwen)

**File**: `commands/speckit.bugfix.toml` (example)

```toml
description = "Fix bugs with regression-test-first approach"

prompt = """
Execute the bugfix workflow script with the provided description:

```bash
.specify/scripts/bash/create-bugfix.sh "{{args}}"
```

This creates:
- Branch: `bugfix/NNN-description`
- Directory: `specs/bugfix/NNN-description/`
- Files: `bug-report.md`, `tasks.md`

Quality Gate: **Write regression test BEFORE implementing fix**
"""
```

**Note the placeholder difference:**
- Markdown format: `$ARGUMENTS`
- TOML format: `{{args}}`

### 4. Update Documentation

#### README.md

Add the new agent to the **Supported AI Agents** table:

```markdown
| Agent | Native Commands | Setup Complexity | Best For |
|-------|----------------|------------------|----------|
| **New Agent** | ✅ Yes | ⭐ Easy | Description of best use case |
```

And to the **Compatibility** section:

```markdown
- ✅ **New Agent** (via native commands or appropriate integration method)
```

#### AI-AGENTS.md

Add a complete setup guide for the new agent following the existing pattern:

```markdown
### N. New Agent

**Why choose**: [Key benefits]

**Setup Steps**:

1. Install spec-kit-extensions per [INSTALLATION.md](INSTALLATION.md)

2. [Agent-specific setup steps]

3. Test a command:
   ```bash
   /speckit.bugfix --help
   ```

**Usage**:
[Usage examples]

**Pros**:
- ✅ [Benefits]

**Cons**:
- ⚠️ [Limitations]
```

### 5. Test the Integration

1. **Create test project**:
   ```bash
   mkdir test-project && cd test-project
   git init
   # Example using Claude (replace with your new agent once added to spec-kit)
   specify init --ai claude .
   ```

2. **Install extensions**:
   ```bash
   # Use your new agent key from AGENT_CONFIG
   specify-extend --all --agent new-agent-cli
   ```

3. **Verify installation**:
   ```bash
   # Check directory structure
   ls .new-agent/commands/
   # Should show: speckit.bugfix.md, speckit.modify.md, etc.
   ```

4. **Test command execution**:
   ```bash
   # Test with the actual agent CLI
   new-agent-cli /speckit.bugfix "test workflow"
   ```

5. **Verify workflow creation**:
   ```bash
   git branch  # Should show bugfix/001-test-workflow
   ls specs/bugfix/001-test-workflow/  # Should show bug-report.md, tasks.md
   ```

6. **Test non-git repository support**:
   ```bash
   mkdir /tmp/non-git-test && cd /tmp/non-git-test
   specify-extend --all --agent new-agent-cli
   # Scripts should work with informative warnings, not errors
   ```

7. **Test JSON output mode** (for programmatic usage):
   ```bash
   .specify/scripts/bash/create-bugfix.sh --json "test"
   # Should output valid JSON with branch, directory, and file information
   ```

## Branch Naming Design Pattern

spec-kit-extensions uses branch naming to identify workflow types. Understanding this is crucial when testing new agent integrations:

| Workflow | Branch Pattern | Example |
|----------|---------------|----------|
| Standard Feature | `NNN-description` | `001-user-auth` |
| Bugfix | `bugfix/NNN-description` | `bugfix/001-fix-login` |
| Modify | `modify/NNN^MMM-description` | `modify/001^002-update-api` |
| Refactor | `refactor/NNN-description` | `refactor/001-clean-utils` |
| Hotfix | `hotfix/NNN-description` | `hotfix/001-patch-security` |
| Deprecate | `deprecate/NNN-description` | `deprecate/001-remove-v1-api` |
| Cleanup | `cleanup/NNN-description` | `cleanup/001-remove-old-code` |
| Baseline | `baseline/NNN-description` | `baseline/001-initial-state` |

**Key Implementation Details:**

- **Branch naming utility**: `generate_branch_name()` in `common.sh` (lines 66-112)
  - Filters stop words (the, a, an, with, for, to, etc.)
  - Filters short words (< 3 characters) to keep meaningful terms
  - Handles acronyms properly
  - Enforces word count limits

- **Multiple branches per spec**: The system supports multiple branches sharing the same spec:
  - Example: `bugfix/004-fix-a` and `bugfix/004-fix-b` both use `specs/bugfix/004-*/`
  - The numeric prefix is the key, not the full branch name
  - Implemented via `find_feature_dir_by_prefix()` in `common.sh`

## Agent Categories

### CLI-Based Agents

Require a command-line tool to be installed:
- **Claude Code**: `claude` CLI
- **Gemini CLI**: `gemini` CLI
- **Cursor**: `cursor-agent` CLI
- **Qwen Code**: `qwen` CLI
- **opencode**: `opencode` CLI
- **Amazon Q Developer CLI**: `q` CLI
- **Codex CLI**: `codex` CLI

Configuration: `requires_cli: True`

### IDE-Based Agents

Work within integrated development environments:
- **GitHub Copilot**: Built into VS Code/compatible editors
- **Windsurf**: Built into Windsurf IDE

Configuration: `requires_cli: False`

## Command File Formats

### Markdown Format

Used by: Claude, Cursor, Copilot, opencode, Windsurf, Amazon Q, Codex

**Standard format:**
```markdown
---
description: "Command description"
---

Command content with $ARGUMENTS placeholder.
```

**GitHub Copilot Chat Mode format:**
```markdown
---
description: "Command description"
mode: speckit.command-name
---

Command content with $ARGUMENTS placeholder.
```

### TOML Format

Used by: Gemini, Qwen

```toml
description = "Command description"

prompt = """
Command content with {{args}} placeholder.
"""
```

## Directory Conventions

- **CLI agents**: Usually `.<agent-name>/commands/`
- **IDE agents**: Follow IDE-specific patterns:
  - Copilot: `.github/agents/`
  - Cursor: `.cursor/commands/`
  - Windsurf: `.windsurf/workflows/`

## Argument Placeholders

Different agents use different argument placeholders:
- **Markdown-based**: `$ARGUMENTS`
- **TOML-based**: `{{args}}`

The `specify-extend` tool automatically handles these differences when installing commands.

## Extension Workflows

spec-kit-extensions provides these workflows that must be supported for each agent:

1. **bugfix** - Fix bugs with regression-test-first approach
   - Script: `.specify/scripts/bash/create-bugfix.sh`
   - Command: `/speckit.bugfix "description"`

2. **modify** - Modify existing features with impact analysis
   - Script: `.specify/scripts/bash/create-modification.sh`
   - Command: `/speckit.modify NNN "description"`

3. **refactor** - Improve code quality with metrics tracking
   - Script: `.specify/scripts/bash/create-refactor.sh`
   - Command: `/speckit.refactor "description"`

4. **hotfix** - Handle production emergencies
   - Script: `.specify/scripts/bash/create-hotfix.sh`
   - Command: `/speckit.hotfix "description"`

5. **deprecate** - Sunset features with phased rollout
   - Script: `.specify/scripts/bash/create-deprecate.sh`
   - Command: `/speckit.deprecate NNN "reason"`

## Common Pitfalls

1. **Using shorthand keys instead of actual CLI tool names**:
   - Rule: Always use the actual executable name as the AGENT_CONFIG key (e.g., `"cursor-agent"` not `"cursor"`)
   - Existing exception: The codebase has an `Agent` enum with `cursor = "cursor-agent"`, which creates an extra mapping layer
   - Recommended for new agents: Keep the enum name aligned with the value using underscores: `new_agent_cli = "new-agent-cli"`

2. **Wrong argument format**: Use correct placeholder format for each agent type:
   - `$ARGUMENTS` for Markdown
   - `{{args}}` for TOML

3. **Incorrect `requires_cli` value**: Set to `True` only for agents that have CLI tools; set to `False` for IDE-based agents.

4. **Directory naming**: Follow agent-specific conventions exactly (check existing agents for patterns).

5. **Missing detection logic**: Ensure the `detect_agent()` function can properly identify the new agent by its directory structure or config files.

6. **Incomplete documentation**: Update all three documentation files:
   - `README.md` - Quick reference
   - `AI-AGENTS.md` - Complete setup guide
   - This file (`AGENTS.md`) - Maintainer documentation

## Testing Checklist

Before submitting a PR to add a new agent:

- [ ] Added agent to `AGENT_CONFIG` in `specify_extend.py`
- [ ] Added detection logic to `detect_agent()` function
- [ ] Created all 5 command templates (bugfix, modify, refactor, hotfix, deprecate)
- [ ] Used correct file format (md or toml) for the agent
- [ ] Used correct argument placeholders for the format
- [ ] Updated README.md with agent in compatibility tables
- [ ] Added complete setup guide to AI-AGENTS.md
- [ ] Updated this AGENTS.md file with any agent-specific notes
- [ ] Tested installation: `specify-extend --all --agent new-agent-cli`
- [ ] Verified command files installed to correct directory
- [ ] Tested at least one workflow end-to-end
- [ ] Verified workflow creation (branch, directory, files)
- [ ] Tested non-git repository support (should work with warnings)
- [ ] Tested `--json` output mode for programmatic usage
- [ ] Verified branch naming follows expected patterns
- [ ] Tested with and without GitHub token (for rate limit scenarios)
- [ ] Verified `--dry-run` mode works correctly
- [ ] Documented any special requirements or limitations

## Architecture Notes

### How spec-kit-extensions Works

**spec-kit (`specify init`)**:
1. Creates `.specify/scripts/bash/` (or `/powershell/` with `--script ps`)
2. Installs core spec-kit scripts and templates
3. Creates agent-specific command directories (e.g., `.claude/commands/`)

**specify-extend**:
1. **Detection**: Examines project structure to identify configured agent
2. **Download**: Fetches latest spec-kit-extensions release from GitHub
3. **Installation**: Copies extension command templates to agent-specific directories
4. **Installation**: Copies extension scripts to `.specify/scripts/bash/` or `/powershell/`
5. **Configuration**: Updates constitution with quality gates
6. **Patching**: Patches spec-kit's `common.sh` to recognize extension branch patterns

### Key Files

- `specify_extend.py` - Main CLI tool with agent configuration
- `commands/` - Command templates for all supported agents
- `scripts/` - Bash scripts that implement the workflows
- `extensions/` - Workflow templates and documentation
- `AI-AGENTS.md` - User-facing agent setup guide
- `README.md` - Project overview and quick reference
- `common.sh` - Shared bash utilities for branch naming and git operations

### Important Code Locations

When working with agent support, these are the key locations in `specify_extend.py`:

- **AGENT_CONFIG dictionary**: Lines 78-139
- **Agent enum**: Lines 210-222
- **detect_agent() function**: Lines 473-513
- **patch_common_sh() function**: Lines 1235-1344
- **AVAILABLE_EXTENSIONS list**: Line 63

When working with bash utilities:

- **common.sh**:
  - `generate_branch_name()`: Lines 66-112
  - `find_feature_dir_by_prefix()`: Supports multiple branches per spec
  - Git utilities: `get_repo_root()`, `get_current_branch()`, `has_git()`

- **Workflow scripts** (scripts/*.sh):
  - All support `--json` flag for programmatic output
  - All have fallback logic for non-git repositories
  - All verify required functions exist before execution

## Future Considerations

When adding new agents:
- Consider the agent's native command/workflow patterns
- Ensure compatibility with the Spec-Driven Development process
- Document any special requirements or limitations
- Update this guide with lessons learned
- Verify the actual CLI tool name before adding to AGENT_CONFIG

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/[your-username]/spec-kit-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/[your-username]/spec-kit-extensions/discussions)
- **spec-kit**: [Original spec-kit repo](https://github.com/github/spec-kit)

---

*This documentation should be updated whenever new agents are added to maintain accuracy and completeness.*
