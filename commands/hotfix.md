---
description: Create an emergency hotfix workflow with expedited process and mandatory post-mortem.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/hotfix` in the triggering message **is** the incident description. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

**⚠️  EMERGENCY WORKFLOW - EXPEDITED PROCESS ⚠️**

Given that incident description, do this:

1. Run the script `.specify/scripts/bash/create-hotfix.sh --json "$ARGUMENTS"` from repo root and parse its JSON output for HOTFIX_ID, BRANCH_NAME, HOTFIX_FILE, POSTMORTEM_FILE, and TIMESTAMP. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

2. Load `.specify/extensions/workflows/hotfix/hotfix-template.md` to understand required sections.

3. Write the hotfix incident log to HOTFIX_FILE using the template structure:
   - Fill incident timeline with TIMESTAMP from script output
   - Assess severity from description (P0 = service down, P1 = major feature broken, P2 = workaround available)
   - Describe the incident clearly
   - Leave "Immediate Fix Applied" section empty (to be filled during fix)
   - Leave root cause analysis preliminary (to be refined)
   - Document impact assessment from description

4. Load `.specify/extensions/workflows/hotfix/tasks-template.md` and create `tasks.md` in the hotfix directory.

5. Report completion with:
   - **EMERGENCY STATUS**: Hotfix workflow initiated
   - Hotfix ID
   - Branch name
   - Incident start timestamp
   - Severity assessment
   - Hotfix file path
   - **URGENT**: Begin Phase 1 tasks immediately (assess, notify, investigate)
   - **REMINDER**: Post-mortem REQUIRED within 48 hours of resolution

Note: Hotfix workflow bypasses normal TDD process due to emergency nature. Tests must be added AFTER fix is deployed. This is the ONLY workflow that permits this deviation from the constitution.
