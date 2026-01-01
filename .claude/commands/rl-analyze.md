---
description: Analyze an RL intake document to generate findings and optimization recommendations for spec-kit-extensions.
---

User input:

$ARGUMENTS

## Overview

Analyze a completed RL intake to generate detailed findings, root cause analysis, and specific optimization recommendations.

## Steps

### 1. Load Intake

Find the intake document:
```bash
# If ID provided
cat specs/rl-intake/{{NUM}}-*/intake.md

# Or find most recent
ls -t specs/rl-intake/*/intake.md | head -1
```

### 2. Extract Key Data

From the intake, extract:

**Quantitative**:
- Success metrics scores
- Completion rates
- Intervention counts

**Qualitative**:
- Friction points
- Template usage patterns
- Deviations
- Existing recommendations

### 3. Root Cause Analysis

For each significant issue, apply Five Whys:

1. Why did [problem] happen?
2. Why did [cause 1] happen?
3. Why did [cause 2] happen?
4. Why did [cause 3] happen?
5. Why did [cause 4] happen? → Root cause

Categorize:
- **Prompt**: Unclear/missing guidance
- **Template**: Structure issues
- **Script**: Behavior problems
- **Constitution**: Gate issues
- **Documentation**: Incomplete info

### 4. Analyze Prompts

Load the relevant command file:
```bash
cat commands/speckit.{{WORKFLOW}}.md
```

Evaluate each element:
- Clear objective?
- Step sequence logical?
- Script invocation correct?
- Output guidance clear?
- Error handling present?

Calculate Language Clarity Score (0-50):
- Imperative clarity: /10
- Action specificity: /10
- Sequence logic: /10
- Completeness: /10
- Conciseness: /10

### 5. Analyze Templates

Load templates:
```bash
cat extensions/workflows/{{WORKFLOW}}/*.md
```

Create utilization matrix:
- Section → Usage rate → Value → Action (Keep/Modify/Remove)

Identify:
- Missing sections needed
- Redundant sections
- Better ordering

### 6. Calculate Health Score

```
Health = (Prompt × 0.25) + (Template × 0.20) + (Adherence × 0.25)
       + (Success × 0.20) + (Efficiency × 0.10)
```

| Score | Assessment |
|-------|------------|
| 90+ | Excellent |
| 70-89 | Good |
| 50-69 | Fair |
| <50 | Poor |

### 7. Identify Cross-Workflow Patterns

- Patterns to propagate to other workflows
- Systemic issues affecting multiple workflows

### 8. Create Optimization Backlog

Priority matrix:
- **P0**: Quick wins (high impact, low effort)
- **P1**: Major projects (high impact, high effort)
- **P2**: Fill-ins (low impact, low effort)

### 9. Write Specific Fixes

For each P0/P1 item:

```markdown
**File**: path/to/file.md
**Line**: N

**Before**:
[exact current text]

**After**:
[exact new text]

**Verification**: [how to test]
```

### 10. Create Analysis Document

```bash
cp docs/rl-intake/analysis-template.md specs/rl-intake/{{NUM}}-*/analysis.md
# Fill in all sections
```

### 11. Report Summary

```
✓ RL Analysis Complete

ID: rl-analysis-{{NUM}}
Based On: {{INTAKE_ID}}
Health Score: {{SCORE}}/100

Scores:
- Prompt: {{N}}/100
- Template: {{N}}/100
- Adherence: {{N}}/100
- Success: {{N}}/100
- Efficiency: {{N}}/100

Root Causes: {{N}}
Backlog: {{N}} P0, {{N}} P1, {{N}} P2

Top Fixes:
1. {{FIX_1}}
2. {{FIX_2}}

Next: Create optimization.md with implementation details
```

## Important

- Every finding must cite intake evidence
- Every fix must be specific and testable
- Consider impact on other workflows
- Prioritize high-impact, low-effort items

## Files

- Analysis template: `docs/rl-intake/analysis-template.md`
- Output: `specs/rl-intake/{{NUM}}-*/analysis.md`
