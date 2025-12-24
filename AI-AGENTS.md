# AI Agent Compatibility Guide

This guide provides detailed setup instructions for using spec-kit-extensions with different AI coding agents.

## Why It Works Across Multiple Agents

spec-kit-extensions are **agent-agnostic** by design:

```
User Command (any agent)
    ↓
Bash Script (.specify/scripts/bash/create-*.sh)
    ↓
Markdown Templates (universal format)
    ↓
Git Branch (workflow detection)
    ↓
Any AI Agent Reads & Implements
```

**Key Design Principles**:
- ✅ **Bash scripts** - Universal across all platforms
- ✅ **Markdown templates** - Human-readable, AI-parseable
- ✅ **Git conventions** - Branch names encode workflow type
- ✅ **No agent-specific code** - Works with any tool that can read files and run bash (PowerShell optional)

> **PowerShell support (opt-in)**: Run `specify-extend --all --script ps` (or manually copy from `scripts/powershell/`) to install `.ps1` workflows in `.specify/scripts/powershell/`. If installed, replace the bash examples below with the corresponding PowerShell script (e.g., `create-bugfix.ps1`).

## Supported AI Agents

| Agent | Native Commands | Setup Complexity | Best For |
|-------|----------------|------------------|----------|
| **Claude Code** | ✅ Yes | ⭐ Easy | Best overall experience |
| **GitHub Copilot** | ⚠️ Via instructions | ⭐⭐ Medium | GitHub-integrated projects |
| **Cursor** | ⚠️ Via rules | ⭐⭐ Medium | VS Code users wanting AI |
| **Windsurf** | ⚠️ Via config | ⭐⭐ Medium | Codeium users |
| **Gemini CLI** | ⚠️ Manual | ⭐⭐⭐ Advanced | CLI enthusiasts |
| **Qwen CLI** | ⚠️ Manual | ⭐⭐⭐ Advanced | CLI power users |
| **Any Agent** | ⚠️ Bash fallback | ⭐ Easy | Universal fallback |

## Setup by Agent

All agents can be installed via `specify-extend`. By default it detects your configured agent, but you can also install for multiple agents in one repo:

```bash
# Install workflow templates + scripts + commands for multiple agents
specify-extend --agents claude,copilot,cursor-agent --all

# Opt-in (advanced): symlink agent command files instead of copying
specify-extend --agents claude,cursor-agent --all --link
```

### 1. Claude Code (Recommended)

**Why choose**: Best integration, native slash commands, fully tested

**Setup Steps**:

1. Install spec-kit-extensions per [INSTALLATION.md](INSTALLATION.md)

2. Verify commands are present:
   ```bash
   ls .claude/commands/
   # Should show: bugfix.md, modify.md, refactor.md, hotfix.md, deprecate.md
   ```

3. Test a command:
   ```bash
   /bugfix --help
   ```

**Usage**:
```bash
# Commands work natively
/speckit.bugfix "form crashes when submitting"
/speckit.modify 014 "make fields optional"
/speckit.refactor "extract duplicate code"
/speckit.hotfix "production database connection timeout"
/speckit.deprecate 003 "feature has low usage"
```

**Pros**:
- ✅ Native slash commands (no configuration)
- ✅ Best user experience
- ✅ Fully tested and validated
- ✅ Automatic context loading

**Cons**:
- ❌ Only works with Claude Code

---

### 2. GitHub Copilot

**Why choose**: Already using GitHub ecosystem, want AI assistance

**Setup Steps**:

1. Install spec-kit-extensions per [INSTALLATION.md](INSTALLATION.md)

2. Create `.github/copilot-instructions.md`:

```markdown
# Custom Workflow Commands

## /bugfix

When user types `/bugfix "description"`:

1. Execute bash script:
   ```bash
   .specify/scripts/bash/create-bugfix.sh "description"
   ```

2. The script creates:
   - Branch: `bugfix/NNN-description`
   - Directory: `specs/bugfix-NNN-description/`
   - Files: `bug-report.md`, `tasks.md`

3. Read the generated files:
   - `bug-report.md` - Understand the bug
   - `tasks.md` - Follow the task breakdown

4. Key Quality Gate: **Write regression test BEFORE implementing fix**

5. Execute tasks in order:
   - Phase 1: Analyze & Reproduce
   - Phase 2: Regression Test (MUST come first)
   - Phase 3: Fix Implementation
   - Phase 4: Verification

## /modify

When user types `/modify NNN "description"`:

1. Execute bash script:
   ```bash
   .specify/scripts/bash/create-modification.sh NNN "description"
   ```

2. The script creates:
   - Branch: `NNN-mod-MMM-description`
   - Directory: `specs/NNN-feature/modifications/MMM-description/`
   - Files: `modification-spec.md`, `impact-analysis.md`, `tasks.md`

3. Read the generated files, paying special attention to `impact-analysis.md`

4. Key Quality Gate: **Review impact analysis before making changes**

5. Execute tasks respecting backward compatibility

## /refactor

When user types `/refactor "description"`:

1. Execute bash script:
   ```bash
   .specify/scripts/bash/create-refactor.sh "description"
   ```

2. The script creates:
   - Branch: `refactor/NNN-description`
   - Files: `refactor-spec.md`, `baseline-metrics.md`, `tasks.md`

3. Key Quality Gate: **Tests must pass after EVERY incremental change**

4. Capture baseline metrics before starting

## /hotfix

When user types `/hotfix "incident"`:

1. Execute bash script:
   ```bash
   .specify/scripts/bash/create-hotfix.sh "incident"
   ```

2. Key Quality Gate: **Tests written AFTER fix (only exception), post-mortem required**

## /deprecate

When user types `/deprecate NNN "reason"`:

1. Execute bash script:
   ```bash
   .specify/scripts/bash/create-deprecate.sh NNN "reason"
   ```

2. Key Quality Gate: **Follow 3-phase sunset (Warnings → Disabled → Removed)**

---

## Workflow Quality Gates

All workflows follow quality gates defined in `.specify/memory/constitution.md` Section VI.

When implementing any workflow, read the constitution and follow the appropriate quality gates.
```

3. Restart Copilot or reload VS Code

**Usage**:
```
# In Copilot Chat
/speckit.bugfix "form crashes when submitting"

# Copilot will execute the script and help you implement
```

**Pros**:
- ✅ Integrated with GitHub workflow
- ✅ Works in VS Code
- ✅ Access to multiple models (GPT-4, Claude, Gemini)

**Cons**:
- ⚠️ Requires creating instructions file
- ⚠️ Commands go through Copilot Chat (not direct)
- ⚠️ May need to remind Copilot to follow quality gates

---

### 3. Cursor

**Why choose**: Want AI-powered IDE with flexibility

**Setup Steps**:

1. Install spec-kit-extensions per [INSTALLATION.md](INSTALLATION.md)

2. Create or edit `.cursorrules`:

```
# spec-kit-extensions Workflows

## Workflow Commands

When user requests any of these commands, execute the corresponding bash script and follow the generated specifications.

### /bugfix "description"

Execute:
```bash
.specify/scripts/bash/create-bugfix.sh "description"
```

Creates:
- Branch: bugfix/NNN-description
- Files: bug-report.md, tasks.md

Quality Gate: **Regression test BEFORE fix**

Implementation Steps:
1. Read bug-report.md to understand issue
2. Read tasks.md for phase-based breakdown
3. Write failing test (Phase 2 - MUST come before fix)
4. Implement fix (Phase 3)
5. Verify test passes (Phase 4)

### /modify NNN "description"

Execute:
```bash
.specify/scripts/bash/create-modification.sh NNN "description"
```

Creates:
- Branch: NNN-mod-MMM-description
- Files: modification-spec.md, impact-analysis.md, tasks.md

Quality Gate: **Review impact analysis first**

Implementation Steps:
1. Read modification-spec.md for requirements
2. Review impact-analysis.md for affected files
3. Update files in dependency order
4. Test after each file change
5. Verify backward compatibility

### /refactor "description"

Execute:
```bash
.specify/scripts/bash/create-refactor.sh "description"
```

Quality Gate: **Tests pass after EVERY change**

Implementation Steps:
1. Capture baseline metrics
2. Make one small incremental change
3. Run tests (must pass)
4. Commit
5. Repeat until complete

### /hotfix "incident"

Execute:
```bash
.specify/scripts/bash/create-hotfix.sh "incident"
```

Quality Gate: **Tests after fix (only exception), post-mortem within 48hrs**

### /deprecate NNN "reason"

Execute:
```bash
.specify/scripts/bash/create-deprecate.sh NNN "reason"
```

Quality Gate: **3-phase sunset required**

## General Rules

1. Always read generated markdown files before implementing
2. Follow quality gates from `.specify/memory/constitution.md`
3. Respect task phases and dependencies
4. Run tests at appropriate checkpoints
5. For modifications, check impact-analysis.md first
6. For bugfixes, write regression test before fix
7. For refactors, ensure tests pass after each increment

## File Reading Priority

When implementing workflows, read files in this order:
1. Main spec file (bug-report.md, modification-spec.md, etc.)
2. Impact analysis (if present)
3. tasks.md for execution order
4. Constitution for quality gates
5. Parent feature spec (for modifications)
```

3. Restart Cursor or reload project

**Usage**:
```
# In Cursor AI chat
/speckit.bugfix "form crashes when submitting"

# Or describe the workflow
"Create a bugfix workflow for: form crashes when submitting"
```

**Pros**:
- ✅ Powerful AI capabilities
- ✅ VS Code fork with enhancements
- ✅ Multiple model support
- ✅ Good code context awareness

**Cons**:
- ⚠️ Rules file can be verbose
- ⚠️ May need reminders to follow quality gates
- ⚠️ Commands not as seamless as Claude Code

---

### 4. Windsurf

**Why choose**: Using Codeium ecosystem

**Setup Steps**:

1. Install spec-kit-extensions per [INSTALLATION.md](INSTALLATION.md)

2. Configure Windsurf project rules:

   **File**: `.windsurf/rules.md` (or Windsurf settings)

```markdown
# spec-kit-extensions Workflows

## Custom Commands

### /bugfix
When user requests bugfix workflow:
1. Run: `.specify/scripts/bash/create-bugfix.sh "description"`
2. Read generated bug-report.md and tasks.md
3. Follow regression-test-first approach (test before fix)

### /modify
When user requests modification workflow:
1. Run: `.specify/scripts/bash/create-modification.sh NNN "description"`
2. Read modification-spec.md and impact-analysis.md
3. Review impact analysis before making changes

### /refactor
When user requests refactor workflow:
1. Run: `.specify/scripts/bash/create-refactor.sh "description"`
2. Capture baseline metrics
3. Ensure tests pass after each incremental change

### /hotfix
When user requests hotfix workflow:
1. Run: `.specify/scripts/bash/create-hotfix.sh "incident"`
2. Exception: Tests can be written after fix
3. Post-mortem required within 48 hours

### /deprecate
When user requests deprecation workflow:
1. Run: `.specify/scripts/bash/create-deprecate.sh NNN "reason"`
2. Follow 3-phase sunset process

## Quality Gates

Enforce quality gates from `.specify/memory/constitution.md` Section VI.
```

3. Reload Windsurf project

**Usage**:
Similar to Cursor - use AI chat to invoke workflows

**Pros**:
- ✅ Built on VS Code
- ✅ Free tier available
- ✅ Codeium backing

**Cons**:
- ⚠️ Less mature than Cursor/Copilot
- ⚠️ Configuration may vary by version

---

### 5. Gemini CLI (Google AI)

**Why choose**: Command-line workflow, Google ecosystem

**Setup Steps**:

1. Install spec-kit-extensions per [INSTALLATION.md](INSTALLATION.md)

2. Install Gemini CLI (if not already):
   ```bash
   # Follow Google's installation guide
   ```

3. Create helper script `.specify/ai-workflow.sh`:

```bash
#!/usr/bin/env bash
# Helper script for running workflows with Gemini CLI

WORKFLOW=$1
shift
DESCRIPTION="$@"

case "$WORKFLOW" in
    bugfix)
        .specify/scripts/bash/create-bugfix.sh "$DESCRIPTION"
        echo "Created bugfix workflow. Use Gemini to implement:"
        echo "  gemini-cli 'Implement the bugfix in specs/bugfix-*/ following tasks.md'"
        ;;
    modify)
        FEATURE_NUM=$1
        shift
        .specify/scripts/bash/create-modification.sh "$FEATURE_NUM" "$@"
        echo "Created modification workflow. Use Gemini to implement:"
        echo "  gemini-cli 'Implement the modification in specs/$FEATURE_NUM-*/modifications/*/ following tasks.md'"
        ;;
    *)
        echo "Usage: $0 {bugfix|modify|refactor|hotfix|deprecate} [args...]"
        exit 1
        ;;
esac
```

4. Make executable:
   ```bash
   chmod +x .specify/ai-workflow.sh
   ```

**Usage**:
```bash
# Create workflow
.specify/ai-workflow.sh bugfix "form crashes when submitting"

# Then use Gemini CLI to implement
gemini-cli "Implement the bugfix in specs/bugfix/001-form-crashes/ following tasks.md. Read bug-report.md first. Write regression test before fix."
```

**Pros**:
- ✅ Command-line efficiency
- ✅ Google AI models
- ✅ Scriptable/automatable

**Cons**:
- ⚠️ Two-step process (create workflow, then implement)
- ⚠️ Manual context management
- ⚠️ Requires more explicit instructions

---

### 6. Other CLI Tools (Qwen, opencode, Codex)

**Why choose**: Specific model preferences, experimentation

**Setup**: Same as Gemini CLI above, adapt helper script

**Usage**:
```bash
# Create workflow
.specify/scripts/bash/create-bugfix.sh "bug description"

# Implement with your CLI tool
qwen-cli "Implement bugfix in specs/bugfix/*/ following tasks.md"
# or
opencode "Implement bugfix in specs/bugfix/*/ following tasks.md"
# or
codex "Implement bugfix in specs/bugfix/*/ following tasks.md"
```

---

### 7. Universal Fallback (Any AI Agent)

**Why choose**: Trying a new agent, or agent doesn't support custom commands

**Setup**: Just install spec-kit-extensions

**Usage**:

1. **Create workflow manually**:
   ```bash
   .specify/scripts/bash/create-bugfix.sh "form crashes"
   ```

2. **Ask any AI agent to help**:
   ```
   "Please help me implement the bugfix specified in specs/bugfix/001-form-crashes/bug-report.md.
   Follow the tasks in tasks.md.
   Important: Write a regression test BEFORE implementing the fix."
   ```

**Pros**:
- ✅ Works with ANY AI agent
- ✅ No configuration needed
- ✅ Maximum flexibility

**Cons**:
- ⚠️ Manual workflow creation
- ⚠️ More typing required
- ⚠️ Agent may need reminders about quality gates

---

## Integration Patterns Summary

### Pattern 1: Native Commands (Claude Code)
```
User: /bugfix "description"
    ↓
Command definition (.claude/commands/bugfix.md)
    ↓
Bash script executes
    ↓
AI automatically loads context and implements
```

### Pattern 2: Custom Instructions (Copilot)
```
User: /bugfix "description" (in Copilot Chat)
    ↓
Instructions file (.github/copilot-instructions.md)
    ↓
Copilot executes bash script
    ↓
Copilot helps implement following instructions
```

### Pattern 3: Rules Files (Cursor, Windsurf)
```
User: /bugfix "description" (in AI chat)
    ↓
Rules file (.cursorrules or .windsurf/rules.md)
    ↓
AI executes bash script per rules
    ↓
AI implements following rules
```

### Pattern 4: Direct Invocation (CLI tools, Fallback)
```
User: bash script manually
    ↓
Workflow files created
    ↓
User asks AI to implement
    ↓
AI reads files and implements
```

---

## Feature Comparison

| Feature | Claude Code | Copilot | Cursor | Windsurf | CLI Tools |
|---------|-------------|---------|--------|----------|-----------|
| **Native commands** | ✅ Yes | ⚠️ Via chat | ⚠️ Via chat | ⚠️ Via chat | ❌ Manual |
| **Setup complexity** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐ Medium | ⭐⭐ Medium | ⭐⭐⭐ Advanced |
| **Auto context loading** | ✅ Yes | ⚠️ Partial | ⚠️ Partial | ⚠️ Partial | ❌ Manual |
| **Quality gate enforcement** | ✅ Strong | ⚠️ Needs reminders | ⚠️ Needs reminders | ⚠️ Needs reminders | ❌ Manual |
| **Multi-model support** | ❌ Claude only | ✅ GPT, Claude, Gemini | ✅ Multiple | ✅ Multiple | ✅ Varies |
| **IDE integration** | ✅ Excellent | ✅ VS Code | ✅ VS Code fork | ✅ VS Code fork | ❌ Terminal only |
| **Workflow creation** | ✅ Automatic | ✅ Automatic | ✅ Automatic | ✅ Automatic | ⚠️ 2-step |

---

## Troubleshooting by Agent

### Claude Code Issues

**Problem**: Commands not found

**Solution**:
```bash
# Verify commands exist
ls .claude/commands/
# Should show: bugfix.md, modify.md, etc.

# Restart Claude Code
```

---

### GitHub Copilot Issues

**Problem**: Commands don't trigger workflow

**Solution**:
1. Verify `.github/copilot-instructions.md` exists
2. Ensure proper markdown formatting
3. Reload VS Code
4. Try: "@workspace /bugfix description" to explicitly invoke

**Problem**: Copilot skips quality gates

**Solution**:
- Add explicit reminders in instructions file
- Include quality gates in every command description
- Reference constitution explicitly

---

### Cursor/Windsurf Issues

**Problem**: Rules not followed

**Solution**:
1. Verify rules file syntax
2. Reload project/window
3. Explicitly mention rules: "Following .cursorrules, create a bugfix workflow"

**Problem**: Bash scripts not executing

**Solution**:
```bash
# Ensure scripts are executable
chmod +x .specify/scripts/bash/*.sh

# Test manually first
.specify/scripts/bash/create-bugfix.sh "test"
```

---

### CLI Tools Issues

**Problem**: Context lost between commands

**Solution**:
- Use longer, more explicit prompts
- Reference file paths explicitly
- Include quality gates in every prompt

---

## FAQ

### Which agent should I use?

**Best overall experience**: Claude Code (native integration, fully tested)

**GitHub-integrated projects**: GitHub Copilot (already in your ecosystem)

**VS Code users wanting AI**: Cursor or Windsurf (enhanced VS Code with AI)

**Command-line enthusiasts**: Gemini CLI or other CLI tools (scriptable, automatable)

**Experimenting/trying agents**: Universal fallback (works with everything)

### Can I switch agents later?

Yes! The workflows are in markdown and bash, so they work with any agent. Just follow the setup for your new agent.

### Do all features work on all agents?

**Core workflows**: ✅ Yes (bugfix, modify, refactor, hotfix, deprecate all work)

**Quality gate enforcement**: ⚠️ Varies by agent:
- Claude Code: Automatic
- Others: May need reminders

**Auto context loading**: ⚠️ Varies by agent:
- Claude Code: Automatic
- Others: Partial or manual

### Can I use multiple agents on the same project?

Yes! The workflows are agent-independent. You could use Claude Code for complex features and CLI tools for quick bugfixes.

### How do I know if my agent is working correctly?

Test with a simple bugfix:
```bash
/speckit.bugfix "test workflow"
# or manually:
.specify/scripts/bash/create-bugfix.sh "test workflow"
```

Check that:
1. Branch created: `git branch` shows `bugfix/001-test-workflow`
2. Files created: `ls specs/bugfix/001-test-workflow/`
3. AI can read files and implement

---

## Getting Help

- **Agent-specific issues**: Check agent's official documentation
- **Workflow issues**: [Open an issue](https://github.com/[your-username]/spec-kit-extensions/issues)
- **General questions**: [Start a discussion](https://github.com/[your-username]/spec-kit-extensions/discussions)

---

**Ready to set up your agent?** Pick your agent above and follow the setup guide!
