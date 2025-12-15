---
description: Create a refactoring workflow with metrics tracking and behavior preservation validation.
handoffs:
  - label: Create Implementation Plan
    agent: speckit.plan
    prompt: Create a plan for the refactoring. I am refactoring...
    send: true
  - label: Break Down Into Tasks
    agent: speckit.tasks
    prompt: Break the refactoring plan into tasks
    send: true
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.refactor` in the triggering message **is** the refactoring description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that refactoring description, do this:

1. Run the script `.specify/scripts/bash/create-refactor.sh --json "$ARGUMENTS"` from repo root and parse its JSON output for REFACTOR_ID, BRANCH_NAME, REFACTOR_SPEC_FILE, METRICS_BEFORE, BEHAVIORAL_SNAPSHOT. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

2. Load `.specify/extensions/workflows/refactor/refactor-template.md` to understand required sections.

3. Write the refactor spec to REFACTOR_SPEC_FILE using the template structure:
   - Fill "Motivation" section with code smells and justification from description
   - Fill "Proposed Improvement" with refactoring approach
   - Identify files that will be affected
   - Leave metrics sections empty (will be filled by measure-metrics.sh)
   - Document behavior preservation requirements
   - Assess risk level (High/Medium/Low)

4. Update BEHAVIORAL_SNAPSHOT file with key behaviors to preserve:
   - Extract observable behaviors from description
   - Document inputs and expected outputs
   - Create verification checklist

5. Report completion with Next Steps:

```
✅ Refactor workflow initialized

**Refactor ID**: [REFACTOR_ID]
**Branch**: [BRANCH_NAME]
**Refactor Spec**: [REFACTOR_SPEC_FILE]
**Behavioral Snapshot**: [BEHAVIORAL_SNAPSHOT]

📋 **Next Steps:**
1. Review refactoring goals and behaviors to preserve
2. Capture baseline metrics:
   .specify/extensions/workflows/refactor/measure-metrics.sh --before
3. Run `/speckit.plan` to create refactoring plan
4. Run `/speckit.tasks` to break down into tasks
5. Run `/speckit.implement` to execute refactoring

💡 **Reminder**: Behavior must not change - all tests must still pass
```

Note: The script creates and checks out the new branch before writing files. Refactoring MUST follow test-first approach - all existing tests must pass before and after.
