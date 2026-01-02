# Reinforcement Learning Intake Process

A systematic process for improving spec-kit-extensions prompts, templates, and workflows based on real-world usage data.

## Overview

This process enables continuous improvement of spec-kit by:
1. **Collecting** usage data from repositories that use spec-kit workflows
2. **Analyzing** what worked well and what caused friction
3. **Optimizing** prompts, templates, and commands based on findings

**This is an internal process for spec-kit-extensions maintainers only** - it is not a distributable workflow.

## When to Use This Process

- After a significant project uses spec-kit workflows
- When users report recurring friction with a workflow
- After adding or modifying a workflow extension
- During periodic workflow health reviews
- When onboarding support for a new AI agent

## Process Flow

```
1. INTAKE          2. ANALYZE           3. OPTIMIZE          4. VALIDATE
   ↓                  ↓                    ↓                    ↓
Collect data    → Evaluate         → Apply changes    → Test & release
from usage        effectiveness      to prompts/         improvements
                                     templates
```

## Directory Structure

```
spec-kit-extensions/
├── specs/rl-intake/                    # Intake documents (gitignored sensitive data)
│   └── 001-project-workflow/
│       ├── intake.md                   # Collected usage data
│       ├── analysis.md                 # Findings and root causes
│       └── optimization.md             # Specific changes to apply
├── docs/rl-intake/                     # Templates and guides
│   ├── intake-template.md
│   ├── analysis-template.md
│   └── optimization-template.md
└── .claude/commands/                   # Claude Code commands for this repo
    ├── rl-intake.md
    └── rl-analyze.md
```

---

## Stage 1: Intake

### What to Collect

| Data Type | Source | Purpose |
|-----------|--------|---------|
| **Chat Logs** | AI agent transcripts | Understand agent behavior and friction |
| **Spec Documents** | specs/*/spec.md, plan.md, tasks.md | Assess template utilization |
| **Git Commits** | git log from workflow branch | Evaluate commit quality and flow |
| **Test Output** | CI/CD or local test runs | Verify quality gate compliance |
| **Code** (optional) | Relevant source files | Analyze generated code quality |

### Exporting Chat Logs by Agent

#### Claude Code (CLI)

```bash
# Export current session to markdown
claude export --format markdown > session.md

# Export specific session by ID
claude export --session <session-id> --format markdown > session.md

# List recent sessions to find session ID
claude sessions list
```

**Alternative**: Copy from terminal scrollback or use terminal logging:
```bash
# Enable terminal logging before session
script -q session.log
claude
# ... run workflow ...
exit
```

#### GitHub Copilot (VS Code)

1. Open the Copilot Chat panel (`Ctrl+Shift+I` / `Cmd+Shift+I`)
2. Click the `...` menu in the chat panel header
3. Select **Export Chat History**
4. Save as JSON or markdown

**Alternative**: Select all chat content (`Ctrl+A`) and copy to a file.

#### Cursor

1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Search for **"Cursor: Export Chat History"**
3. Select the session to export
4. Save to file

**Alternative**: Open chat history, select conversation, copy content.

**Location of chat history**: `~/.cursor/chat_history/` (may vary by version)

#### Windsurf (Codeium)

1. Open the Cascade panel
2. Click the history icon to view past conversations
3. Select the relevant session
4. Use the export/copy option

**Alternative**: Chat logs stored in `~/.codeium/` directory.

#### Aider

Aider automatically logs all sessions:

```bash
# Default log location
cat .aider.chat.history.md

# Or check the aider log directory
ls ~/.aider/logs/
```

**Tip**: Aider's `--chat-history-file` flag customizes the log location.

#### Continue (VS Code/JetBrains)

1. Open Continue panel
2. Click the history icon (clock) in the panel header
3. Find the relevant session
4. Click **Export** or copy the conversation

**Log location**:
- VS Code: `~/.continue/sessions/`
- JetBrains: `~/.continue/sessions/`

#### Amazon Q Developer

1. Open the Amazon Q panel in your IDE
2. Navigate to conversation history
3. Select the session covering the workflow
4. Copy or export the conversation

#### Generic Fallback

If no export option exists:

1. **Terminal recording**: Use `script` or `asciinema` before starting
2. **Screen capture**: Take screenshots during the session
3. **Manual copy**: Select and copy from the chat interface
4. **Browser DevTools**: For web-based agents, check Network tab for conversation API responses

### Using GitHub MCP for Other Artifacts

If the GitHub MCP server is configured, automate collection of non-chat artifacts:

```bash
# Commits from workflow branch
mcp__github__list_commits owner="{{OWNER}}" repo="{{REPO}}" sha="{{BRANCH}}"

# Spec files
mcp__github__get_file_contents owner="{{OWNER}}" repo="{{REPO}}" path="specs/{{WORKFLOW}}/*/spec.md"

# PR discussion and reviews
mcp__github__get_pull_request owner="{{OWNER}}" repo="{{REPO}}" pull_number={{N}}

# CI/CD test results
mcp__github__list_workflow_runs owner="{{OWNER}}" repo="{{REPO}}" branch="{{BRANCH}}"
```

### Intake Checklist

- [ ] Identify the repository and workflow type being analyzed
- [ ] Obtain chat logs (with user permission if external)
- [ ] Export spec documentation produced
- [ ] Extract git commit history from workflow branch
- [ ] Capture final test output
- [ ] Note any user-reported friction points
- [ ] Redact sensitive/proprietary information

### Creating an Intake

Use the `/rl-intake` command in Claude Code:

```
/rl-intake "project-name workflow-type"
```

Or manually create:

```bash
mkdir -p specs/rl-intake/001-project-workflow
cp docs/rl-intake/intake-template.md specs/rl-intake/001-project-workflow/intake.md
# Fill in the template with collected data
```

---

## Stage 2: Analysis

### Evaluation Framework

#### Prompt Effectiveness (25% weight)

| Metric | How to Assess |
|--------|---------------|
| Initial understanding | Did agent understand what to do immediately? |
| Step sequence | Were steps followed in the correct order? |
| Output format | Was output structured correctly? |
| Error recovery | How well were issues handled? |
| Completion detection | Did agent know when done? |

**Score**: 0-100 based on evidence from chat logs

#### Template Effectiveness (20% weight)

| Metric | How to Assess |
|--------|---------------|
| Section utilization | Which sections were filled vs skipped? |
| Missing elements | What was needed but not in template? |
| Placeholder clarity | Were placeholders helpful? |
| Structure logic | Was the order intuitive? |

**Score**: (Sections used / Total sections) × 100

#### Workflow Adherence (25% weight)

| Metric | How to Assess |
|--------|---------------|
| Quality gate compliance | Were all gates followed? |
| Deviation count | How many process deviations? |
| Deviation severity | Critical/blocking or minor? |

**Score**: (Gates followed / Total gates) × 100

#### Success Rate (20% weight)

| Metric | How to Assess |
|--------|---------------|
| Task completion | Tasks done / Tasks defined |
| Tests passing | Final test status |
| Spec coverage | All requirements addressed? |

**Score**: Weighted average of completion metrics

#### Efficiency (10% weight)

| Metric | How to Assess |
|--------|---------------|
| User interventions | Times user redirected agent |
| Retries/corrections | Times agent self-corrected |
| Duration | Time from start to completion |

**Score**: 100 - (Interventions × 10), minimum 0

### Root Cause Analysis

For each significant issue, apply Five Whys:

1. Why did [problem] happen?
2. Why did [answer 1] happen?
3. Why did [answer 2] happen?
4. Why did [answer 3] happen?
5. Why did [answer 4] happen? → **Root cause**

Categorize root causes:
- **Prompt**: Unclear instructions, missing guidance
- **Template**: Missing sections, poor structure
- **Script**: Incorrect behavior, missing features
- **Constitution**: Wrong gates, missing enforcement
- **Documentation**: Incomplete guides

### Health Score Calculation

```
Health Score = (Prompt × 0.25) + (Template × 0.20) + (Adherence × 0.25)
             + (Success × 0.20) + (Efficiency × 0.10)
```

| Score | Assessment |
|-------|------------|
| 90-100 | Excellent - Minor polish only |
| 70-89 | Good - Some improvements needed |
| 50-69 | Fair - Significant issues to address |
| <50 | Poor - Major overhaul required |

---

## Stage 3: Optimization

### Priority Matrix

```
High Impact │ ★ QUICK WINS     │ ☆ MAJOR PROJECTS
            │ Do immediately   │ Plan carefully
            ├──────────────────┼──────────────────
            │ ○ FILL-INS       │ × DON'T DO
Low Impact  │ Do when time     │ Skip entirely
            └──────────────────┴──────────────────
              Low Effort         High Effort
```

### Change Types

#### Prompt Changes (commands/*.md)

```markdown
**Location**: commands/speckit.bugfix.md, line 45

**Before**:
Create the bug report file with the required sections.

**After**:
Create the bug report file. Fill in ALL sections from the template - do not skip any section even if information seems redundant. Pay special attention to the "Reproduction Steps" which must be executable.

**Rationale**: Chat logs showed agent skipping sections; explicit instruction needed.
```

#### Template Changes (extensions/workflows/*/*)

```markdown
**Location**: extensions/workflows/bugfix/bug-report-template.md

**Change**: Add new section after "Root Cause"

**Add**:
## Prevention Strategy

How will similar bugs be prevented in the future?

- [ ] Additional tests to add
- [ ] Code review checklist updates
- [ ] Monitoring/alerting improvements

**Rationale**: Intake showed this information was frequently missing but valuable.
```

#### Script Changes (scripts/*.sh)

```bash
# Location: scripts/create-bugfix.sh, line 95

# Before:
echo "Bug report created at $BUG_REPORT_FILE"

# After:
echo "Bug report created at $BUG_REPORT_FILE"
echo ""
echo "Next steps:"
echo "  1. Fill in all sections of the bug report"
echo "  2. Run /speckit.plan to create implementation plan"
```

#### Constitution Changes (docs/constitution-template.md)

```markdown
**Location**: Quality Gates by Workflow → Bugfix

**Before**:
- Root cause MUST be identified and documented

**After**:
- Root cause MUST be identified using Five Whys analysis
- At least 3 "why" levels MUST be explored
```

### Testing Changes

Before releasing:

1. Create a test repository with spec-kit installed
2. Install the modified extensions
3. Run through the affected workflow
4. Verify improvements address identified issues
5. Check for regressions in other workflows

---

## Stage 4: Validation

### Success Criteria

An optimization is successful when:

- [ ] Health score increases by ≥10 points
- [ ] No new friction points introduced
- [ ] All regression tests pass
- [ ] At least one follow-up intake confirms improvement

### Release Process

1. Update version numbers (pyproject.toml, specify_extend.py)
2. Document changes in CHANGELOG.md
3. Commit with message referencing the intake
4. Create release tag
5. Schedule follow-up intake in 2-4 weeks

---

## Templates

See the templates in `docs/rl-intake/`:

- [intake-template.md](rl-intake/intake-template.md) - Structure for data collection
- [analysis-template.md](rl-intake/analysis-template.md) - Framework for evaluation
- [optimization-template.md](rl-intake/optimization-template.md) - Document for changes

---

## Best Practices

### For Intake

1. **Collect promptly** - Gather data while context is fresh
2. **Include failures** - Failed workflows are most valuable
3. **Redact sensitive information** - Remove proprietary/personal data
4. **Be thorough** - Missing data limits analysis quality

### For Analysis

1. **Evidence-based** - Every finding must cite intake data
2. **Quantify impact** - Use numbers, not just descriptions
3. **Find root causes** - Don't stop at symptoms
4. **Cross-reference** - Compare with other intakes

### For Optimization

1. **Be specific** - Exact file, line, before/after
2. **Test changes** - Verify before releasing
3. **One thing at a time** - Avoid bundling unrelated changes
4. **Track results** - Schedule follow-up validation

---

## Metrics Dashboard

Track these metrics over time:

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Avg workflow health score | >80 | - | - |
| User intervention rate | <2/workflow | - | - |
| Quality gate compliance | >95% | - | - |
| Template fill rate | >90% | - | - |

---

## Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Project development guidance
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [commands/](../commands/) - Current command prompts
- [extensions/workflows/](../extensions/workflows/) - Current templates
