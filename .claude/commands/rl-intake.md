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

Guide through collecting each section:

#### Chat Logs
- Ask user for chat log file or transcript
- Look for: initiation, decisions, friction, completion

#### Spec Documents
If repo accessible:
```bash
ls {{REPO}}/specs/{{WORKFLOW}}/*/
cat {{REPO}}/specs/{{WORKFLOW}}/*/spec.md
```

#### Git Commits
```bash
cd {{REPO}} && git log --oneline {{BRANCH}}
```

#### Test Output
Ask for final test results

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
