# Agent Tool Matrix

Reference guide for where each tool type is deployed across different AI agents.

Last Updated: 2026-04-15

---

## Matrix Overview

| Tool Type | Claude | Copilot | Cursor | Gemini | Qwen | Codex | OpenCode | Windsurf | Amazon Q |
|-----------|--------|---------|--------|--------|------|-------|----------|----------|----------|
| **Commands/Prompts** | [`.claude/commands/`](#claude-commands) | [`.github/agents/` + `.github/prompts/`](#copilot-commands) | [`.cursor/commands/`](#cursor-commands) | [`.gemini/commands/`](#gemini-commands) | [`.qwen/commands/`](#qwen-commands) | [`.codex/commands/`](#codex-commands) | [`.opencode/commands/`](#opencode-commands) | [`.windsurf/workflows/`](#windsurf-commands) | [`.q/commands/`](#q-commands) |
| **Subagents** | [`.claude/agents/`](#claude-subagents) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Skills** | [`.claude/skills/`](#claude-skills) | ❌ | ❌ | ❌ | ❌ | [`.codex/skills/`](#codex-skills) | [`.opencode/skills/`](#opencode-skills) | ❌ | ❌ |
| **Instructions** | [`.claude/`](#claude-instructions) | [`.github/`](#copilot-instructions) | [`.cursorrules/`](#cursor-instructions) | ❌ | ❌ | ❌ | [`.opencode/`](#opencode-instructions) | [`.windsurf/`](#windsurf-rules) | ❌ |
| **MCP Servers** | [`.claude/mcp.json`](#claude-mcp) | ✅ | [`.cursorrules/mcp.json`](#cursor-mcp) | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

---

## Tool Type Definitions

### 1. Commands/Prompts
Workflow entry points that users invoke to trigger spec-kit operations. Format varies by agent (markdown, TOML, or agent-specific).

### 2. Subagents
Delegation targets that handle specific workflow steps. Only Claude Code supports true subagents.

### 3. Skills
Reusable capabilities that provide specialized knowledge or workflows to agents. In the current architecture, spec-kit-extensions keeps repository skill sources under `.agents/skills/`, while any agent-specific registration is handled by native spec-kit integrations or the agent itself.

### 4. Instructions
Agent-specific configuration files that modify behavior or provide context.

### 5. MCP Servers
Model Context Protocol servers that provide external tool integrations.

---

## Claude Code

### Claude Commands
**Location:** `.claude/commands/`
**Format:** Markdown with YAML frontmatter
**File Pattern:** `speckit.{workflow}.md`

**Features:**
- Supports handoffs in frontmatter
- Hooks for lifecycle events (Start, Stop, etc.)
- Markdown body with instructions

**Documentation:**
- [Claude Code Commands Spec](https://docs.anthropic.com/claude/docs/claude-code#commands)
- [spec-kit AGENTS.md](../AGENTS.md#claude-code)

**Example:**
```markdown
---
description: Fix bugs with regression-test-first approach
handoffs:
  - agent: speckit.plan
    label: Create fix plan
    prompt: Plan the bug fix approach
---

# Bugfix Workflow

[Command instructions...]
```

### Claude Subagents
**Location:** `.claude/agents/`
**Format:** Markdown with YAML frontmatter
**File Pattern:** `speckit.{workflow}.md`

**Features:**
- Created from handoff definitions
- Can be delegated to from commands
- Independent execution context

**Documentation:**
- [Claude Code Agents](https://docs.anthropic.com/claude/docs/claude-code#agents)

**Example:**
```markdown
---
name: speckit.plan
description: Create implementation plan
tools: Read, Glob, Grep, Bash, Write
model: haiku
---

# Plan Subagent

[Subagent instructions...]
```

### Claude Skills
**Repository Skill Sources:** `.agents/skills/`
**Agent-Managed Location:** Commonly `.claude/skills/` when upstream spec-kit installs Claude skills
**Format:** Markdown with YAML frontmatter
**File Pattern:** `{skill-name}/SKILL.md`

**Features:**
- Automatically loaded based on frontmatter triggers
- Provides specialized knowledge
- Can bundle scripts, references, and assets
- spec-kit-extensions does not create or synchronize `.claude/skills/` directly

**Documentation:**
- [Claude Code Skills](https://docs.anthropic.com/claude/docs/claude-code#skills)
- [skill-creator skill](../.agents/skills/skill-creator/SKILL.md)

**Example Structure:**
```
.agents/skills/spec-kit-skill/
├── SKILL.md
├── helpers/
│   └── detection-logic.md
└── scripts/
    └── detect-phase.sh
```

### Claude Instructions
**Location:** `.claude/`
**Files:** `INSTRUCTIONS.md`, `.claueignore`

**Features:**
- Project-wide instructions
- File ignore patterns

**Documentation:**
- [Claude Code Instructions](https://docs.anthropic.com/claude/docs/claude-code#instructions)

### Claude MCP
**Location:** `.claude/mcp.json`
**Format:** JSON configuration

**Features:**
- Configure MCP servers
- Tool integrations
- External service connections

**Documentation:**
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude MCP Integration](https://docs.anthropic.com/claude/docs/model-context-protocol)

---

## GitHub Copilot

### Copilot Commands
**Location:**
- Agents: `.github/agents/`
- Prompts: `.github/prompts/`

**Format:** Markdown with YAML frontmatter
**File Pattern:**
- Agent: `speckit.{workflow}.agent.md`
- Prompt: `speckit.{workflow}.prompt.md`

**Features:**
- Dual-file system (agent + prompt pointer)
- Supports handoffs in frontmatter
- Agent file contains logic, prompt points to agent

**Documentation:**
- [GitHub Copilot Extensions](https://docs.github.com/en/copilot/customizing-copilot/using-github-copilot-agents)
- [spec-kit AGENTS.md](../AGENTS.md#github-copilot)

**Example Agent:**
```markdown
---
description: Fix bugs with regression-test-first approach
handoffs:
  - agent: speckit.plan
    label: Create fix plan
---

# Bugfix Workflow

[Command instructions...]
```

**Example Prompt:**
```markdown
---
agent: speckit.bugfix
---
```

### Copilot Skills
**Status:** Not installed or synchronized by spec-kit-extensions

**Current model:**
- Copilot support in this repository is command/prompt based via `.github/agents/` and `.github/prompts/`
- This repo does not fan out repository skills into `.github/skills/`
- If GitHub introduces or documents a native Copilot skills path for this workflow pack, document it from observed upstream behavior before adding it here

**Documentation:**
- [GitHub Copilot Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

### Copilot Instructions
**Location:** `.github/`
**Files:** `INSTRUCTIONS.md`, `.copilotignore`

**Features:**
- Workspace-level instructions
- File ignore patterns

**Documentation:**
- [GitHub Copilot Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

---

## Cursor

### Cursor Commands
**Location:** `.cursor/commands/`
**Format:** Markdown
**File Pattern:** `speckit.{workflow}.md`

**Features:**
- Markdown instructions
- No frontmatter handoff support (converted to text)

**Documentation:**
- [Cursor Composer](https://docs.cursor.com/context/rules-for-ai#composer)
- [spec-kit AGENTS.md](../AGENTS.md#cursor)

### Cursor Skills
**Location:** `.cursorrules/skills/` → `../../.agents/skills/{skill-name}` (symlink)
**Canonical:** `.agents/skills/`
**Format:** Markdown with YAML frontmatter
**File Pattern:** `{skill-name}/SKILL.md`

**Features:**
- Provides specialized knowledge
- Loaded based on triggers

**Documentation:**
- [Cursor Rules](https://docs.cursor.com/context/rules-for-ai)

### Cursor Instructions
**Location:** `.cursorrules/`
**Files:** `.cursorrules` (root level config)

**Features:**
- Project-wide AI instructions
- Behavior customization

**Documentation:**
- [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai)

### Cursor MCP
**Location:** `.cursorrules/mcp.json`
**Format:** JSON configuration

**Features:**
- MCP server configuration
- Tool integrations

**Documentation:**
- [Cursor MCP Support](https://docs.cursor.com/)

---

## Gemini CLI

### Gemini Commands
**Location:** `.gemini/commands/`
**Format:** TOML (planned, currently markdown fallback)
**File Pattern:** `speckit.{workflow}.toml` (future) or `.md` (current)

**Features:**
- TOML configuration format (future)
- Markdown fallback for now
- No handoff support

**Documentation:**
- [Gemini CLI](https://github.com/google/generative-ai-cli)
- [spec-kit AGENTS.md](../AGENTS.md#gemini-cli)

**Note:** TOML format not yet implemented in spec-kit-extensions. Currently uses markdown.

### Gemini Skills
**Location:** `.gemini/skills/` → `../../.agents/skills/{skill-name}` (symlink)
**Canonical:** `.agents/skills/`
**Format:** Markdown with YAML frontmatter
**File Pattern:** `{skill-name}/SKILL.md`

**Features:**
- Provides specialized knowledge
- Loaded based on triggers

---

## Qwen Code

### Qwen Commands
**Location:** `.qwen/commands/`
**Format:** TOML (planned, currently markdown fallback)
**File Pattern:** `speckit.{workflow}.toml` (future) or `.md` (current)

**Features:**
- TOML configuration format (planned)
- Markdown fallback
- No handoff support

**Documentation:**
- [Qwen Code](https://github.com/QwenLM/Qwen-Code)
- [spec-kit AGENTS.md](../AGENTS.md#qwen-code)

**Note:** TOML format not yet implemented in spec-kit-extensions.

---

## Codex CLI

### Codex Commands
**Location:** `.codex/commands/`
**Format:** Markdown
**File Pattern:** `speckit.{workflow}.md`

**Features:**
- Markdown instructions
- No frontmatter handoff support (converted to text)
- Creates skills from handoffs for workflow delegation

**Documentation:**
- [Codex CLI](https://github.com/codex-cli/codex)
- [spec-kit AGENTS.md](../AGENTS.md#codex-cli)

### Codex Skills
**Location:**
- Handoff skills: `.codex/skills/` (auto-generated from handoffs)
- General skills: `.codex/skills/` → `../../.agents/skills/{skill-name}` (symlink)

**Canonical:** `.agents/skills/`
**Format:** Markdown with YAML frontmatter
**File Pattern:** `{skill-name}.md` or `{skill-name}/SKILL.md`

**Features:**
- Two types:
  1. Handoff skills: Auto-generated for workflow delegation
  2. General skills: Symlinked from canonical location
- Provides specialized capabilities

**Documentation:**
- [Codex Skills](https://github.com/codex-cli/codex#skills)

**Example Handoff Skill:**
```markdown
---
name: speckit.plan
description: Create implementation plan
allowed-tools: [read, glob, grep, bash, write]
---

# Create Implementation Plan

[Skill instructions...]
```

---

## OpenCode

### OpenCode Commands
**Location:** `.opencode/commands/`
**Format:** Markdown with YAML frontmatter
**File Pattern:** `speckit.{workflow}.md`

**Features:**
- Supports handoffs in frontmatter
- Markdown body with instructions

**Documentation:**
- [OpenCode](https://github.com/opencode/opencode)
- [spec-kit AGENTS.md](../AGENTS.md#opencode)

---

## Windsurf

### Windsurf Commands
**Location:** `.windsurf/workflows/`
**Format:** Markdown with YAML frontmatter
**File Pattern:** `speckit.{workflow}.md`

**Features:**
- Supports handoffs in frontmatter
- Workflow-based (not command-based)
- Markdown body with instructions

**Documentation:**
- [Windsurf](https://codeium.com/windsurf)
- [spec-kit AGENTS.md](../AGENTS.md#windsurf)

---

## Amazon Q Developer

### Q Commands
**Location:** `.q/commands/`
**Format:** Markdown
**File Pattern:** `speckit.{workflow}.md`

**Features:**
- Markdown instructions
- No handoff support (converted to text)

**Documentation:**
- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
- [spec-kit AGENTS.md](../AGENTS.md#amazon-q-developer)

---

## Repository Skills Layout

spec-kit-extensions keeps shared skill content in a repository source tree:

### Repository Source Location
`.agents/skills/{skill-name}/`
- Single source of truth for skill content shipped in this repository
- Version controlled with the rest of the project
- Referenced by docs and packaging logic

### Installation Model
- Older versions of this project used a local fan-out/symlink installer for agent skill directories
- Current versions do not implement that installer in `specify_extend.py`
- Native spec-kit integrations are responsible for any agent-specific skill registration
- Do not assume `.github/skills/`, `.claude/skills/`, or similar directories are generated by this repository unless you have verified current upstream behavior

### Skill Structure
```
.agents/skills/{skill-name}/
├── SKILL.md              # Required: Main skill definition
├── LICENSE.txt           # Optional: License information
├── scripts/              # Optional: Executable scripts
│   └── *.py, *.sh
├── references/           # Optional: Documentation to load as needed
│   └── *.md
└── assets/               # Optional: Files used in output
    └── templates, images, etc.
```

**Documentation:**
- [skill-creator skill](../.agents/skills/skill-creator/SKILL.md)
- [Skills Best Practices](../.agents/skills/skill-creator/references/workflows.md)

---

## Handoff Support Matrix

| Agent | Frontmatter Handoffs | Delegation Mechanism | Notes |
|-------|---------------------|---------------------|-------|
| **Claude** | ❌ (converted to hooks) | ✅ Subagents | Creates subagent files for delegation |
| **Copilot** | ✅ Native | ✅ Handoff system | Supports handoffs natively |
| **Cursor** | ❌ | ❌ Text guidance | Handoffs converted to text |
| **Gemini** | ❌ | ❌ Text guidance | Handoffs converted to text |
| **Qwen** | ❌ | ❌ Text guidance | Handoffs converted to text |
| **Codex** | ❌ | ✅ Skills | Creates skill files for delegation |
| **OpenCode** | ✅ Native | ✅ Handoff system | Supports handoffs natively |
| **Windsurf** | ✅ Native | ✅ Handoff system | Supports handoffs natively |
| **Amazon Q** | ❌ | ❌ Text guidance | Handoffs converted to text |

---

## Implementation Reference

### Code Location
All mapping logic is in `specify_extend.py`:

- **AGENT_CONFIG** (lines 87-148): Primary configuration
- **Native spec-kit integration reconciliation**: performed before extension install when `--agent` or `--agents` is used
- **Agent command installation**: command/prompt/workflow artifacts are installed per agent capability
- **Claude/Codex delegation artifact generation**: handoffs may still produce subagents or delegation skills where supported

**Important:** The historical `install_agent_skills()` symlink installer referenced by older docs has been removed. See [CHANGELOG.md](../CHANGELOG.md) for the transition to native spec-kit skill handling.

### Related Documentation
- [AGENTS.md](../AGENTS.md) - Agent-specific setup instructions
- [specify-extend.md](./specify-extend.md) - Installation tool documentation
- [architecture.md](./architecture.md) - System architecture overview

---

## Quick Reference

### Get Agent Configuration
```bash
# List all supported agents
specify-extend --list

# Install for specific agent
specify-extend --all --agent claude

# Install for multiple agents
specify-extend --all --agents claude,copilot,cursor-agent
```

### Verify Installation
```bash
# Check commands/workflows
ls -la .claude/commands/
ls -la .github/agents/
ls -la .codex/commands/

# Check repository skill sources
ls -la .agents/skills/

# Check agent-managed skills only if you intentionally enabled native skills upstream
ls -la .claude/skills/ 2>/dev/null
ls -la .codex/skills/ 2>/dev/null
```

---

## Notes

1. `.agents/skills/` is the repository source tree for shared skill content
2. This repository no longer guarantees agent-local skill symlinks or copies
3. Commands are installed per agent and may be transformed based on agent capabilities
4. Handoffs are either preserved, converted to text guidance, or materialized as delegation artifacts depending on the agent
5. MCP servers are supported by most agents (Claude, Cursor, Copilot, Windsurf, OpenCode, Amazon Q, Gemini, Qwen)

---

*Last updated: 2026-04-15*
*spec-kit-extensions version: 1.5.10+*
