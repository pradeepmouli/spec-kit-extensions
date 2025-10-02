---
description: Create a refactoring workflow with metrics tracking and behavior preservation validation.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/refactor` in the triggering message **is** the refactoring description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

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

5. Load `.specify/extensions/workflows/refactor/tasks-template.md` and create `tasks.md` in the refactor directory.

6. Report completion with:
   - Refactor ID
   - Branch name
   - Refactor spec file path
   - **CRITICAL REMINDER**: Must capture baseline metrics BEFORE changing any code:
     ```bash
     .specify/extensions/workflows/refactor/measure-metrics.sh --before
     ```
   - Next steps: capture metrics, document behaviors, begin refactoring

Note: The script creates and checks out the new branch before writing files. Refactoring MUST follow test-first approach - all existing tests must pass before and after.
