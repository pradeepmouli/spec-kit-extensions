---
description: Create a reinforcement learning intake to analyze workflow usage from another repository and improve spec-kit-extensions.
---

User input:

$ARGUMENTS

## Overview

Create a reinforcement learning intake to collect and analyze workflow usage data from a repository that used spec-kit. This is an **internal process for improving spec-kit-extensions**.

## Steps

### 1. Parse Arguments

Extract from user input:
- **Repository**: Path or URL to analyze
- **Workflow type**: Which workflow (bugfix, feature, modify, etc.)
- **Specific branch/spec**: Optional focus area

If missing, ask:
- "Which repository should I analyze?"
- "Which workflow type was used?"

### 2. Create Intake Directory

```bash
# Find next intake number
INTAKE_NUM=$(printf "%03d" $(($(ls -d specs/rl-intake/*/ 2>/dev/null | wc -l) + 1)))
INTAKE_DIR="specs/rl-intake/${INTAKE_NUM}-{{PROJECT_NAME}}"
mkdir -p "$INTAKE_DIR"
```

### 3. Copy Template

```bash
cp docs/rl-intake/intake-template.md "$INTAKE_DIR/intake.md"
```

### 4. Collect Data

Guide through collecting each section. See `docs/rl-intake-process.md` for detailed instructions.

#### Chat Logs

Ask the user which agent was used, then provide export instructions:

**Claude Code**:
```bash
claude export --format markdown > session.md
# Or: claude sessions list  # to find session ID
```

**GitHub Copilot**: VS Code → Copilot Chat panel → `...` menu → Export Chat History

**Cursor**: Command Palette → "Cursor: Export Chat History"

**Aider**: Check `.aider.chat.history.md` or `~/.aider/logs/`

**Continue**: Panel → History icon → Export

**Windsurf**: Cascade panel → History icon → Export

**Fallback**: `script -q session.log` before starting, or copy from terminal/UI

#### Spec Documents (via MCP if available)

```bash
# If GitHub MCP configured:
mcp__github__get_file_contents owner="{{OWNER}}" repo="{{REPO}}" path="specs/{{WORKFLOW}}/*/spec.md"

# Or local access:
cat {{REPO}}/specs/{{WORKFLOW}}/*/spec.md
cat {{REPO}}/specs/{{WORKFLOW}}/*/plan.md
cat {{REPO}}/specs/{{WORKFLOW}}/*/tasks.md
```

#### Git Commits (via MCP if available)

```bash
# If GitHub MCP configured:
mcp__github__list_commits owner="{{OWNER}}" repo="{{REPO}}" sha="{{BRANCH}}"

# Or local:
cd {{REPO}} && git log --oneline {{BRANCH}}
cd {{REPO}} && git diff main...{{BRANCH}}
```

#### Test Output (via MCP if available)

```bash
# If GitHub MCP configured:
mcp__github__list_workflow_runs owner="{{OWNER}}" repo="{{REPO}}" branch="{{BRANCH}}"

# Or ask user to paste CI output or local test results
```

#### PR Discussion (via MCP)

```bash
# If there's a PR for this workflow:
mcp__github__get_pull_request owner="{{OWNER}}" repo="{{REPO}}" pull_number={{N}}
```

### 5. Evaluate Against Quality Gates

Check workflow-specific gates from `docs/constitution-template.md`:
- Which gates were followed?
- Which were skipped and why?

### 6. Rate Prompt Effectiveness

Score 1-5:
- Initial understanding
- Step sequence clarity
- Output format
- Error recovery
- Completion detection

Document friction points with file:line references.

### 7. Assess Template Usage

For each template section:
- Was it filled?
- Was it useful?
- What was missing?

### 8. Calculate Success Metrics

- Task completion rate
- Test pass rate
- User intervention count

### 9. Generate Recommendations

Prioritize by impact:
- **High**: Blocked workflow or major friction
- **Medium**: Notable slowdown
- **Low**: Polish items

Each recommendation needs:
- Location (file:line)
- Problem description
- Proposed fix

### 10. Write Intake Document

Fill the template with all collected data.

### 11. Report Summary

```
✓ RL Intake Created

ID: rl-intake-{{NUM}}
Location: specs/rl-intake/{{NUM}}-{{NAME}}/intake.md

Source: {{REPO}}
Workflow: {{TYPE}}
Assessment: {{LEVEL}}

Key Findings:
- {{FINDING_1}}
- {{FINDING_2}}

Recommendations: {{N}} high, {{N}} medium, {{N}} low

Next: Review intake, then create analysis.md
```

## Important

- Be thorough - missing data limits analysis
- Redact sensitive information
- Cite evidence for every finding
- Focus on actionable improvements

## Files

- Process: `docs/rl-intake-process.md`
- Templates: `docs/rl-intake/`
- Outputs: `specs/rl-intake/`
