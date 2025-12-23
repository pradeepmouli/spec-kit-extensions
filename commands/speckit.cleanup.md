---
description: Validate and reorganize spec-kit artifacts with proper numbering and structure
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

## Purpose

This workflow validates the organization of all spec-kit artifacts in the `specs/` directory, checking for:
- Sequential numbering (001, 002, 003, etc.)
- Proper directory structure based on workflow type
- Required files presence
- No gaps or duplicate numbers

**IMPORTANT**: This workflow only validates and reorganizes documentation in `specs/`. It **NEVER** moves or modifies code files.

## Instructions

1. **Understand the request**: Parse the user input for:
   - Whether they want a dry-run (validate only) or to apply fixes
   - The reason for cleanup (for documentation)
   - Whether to auto-fix issues or just report them

2. **Run the cleanup script** from the repo root:

   **For validation only (dry-run):**
   ```bash
   .specify/scripts/bash/create-cleanup.sh --json --dry-run "$ARGUMENTS"
   ```

   **For validation with auto-fix:**
   ```bash
   .specify/scripts/bash/create-cleanup.sh --json --auto-fix "$ARGUMENTS"
   ```

   **For validation only:**
   ```bash
   .specify/scripts/bash/create-cleanup.sh --json "$ARGUMENTS"
   ```

3. **Parse the JSON output** which includes:
   - `status`: "success" or "issues_found"
   - `message`: Summary message
   - `issues`: Array of issues found (with severity)
   - `actions`: Array of actions taken or suggested

4. **Present the results** to the user:

   If status is "success":
   ```
   ✅ Spec structure validation complete

   No issues found - all spec-kit artifacts are properly organized!
   ```

   If status is "issues_found":
   ```
   ⚠️ Spec structure validation found issues

   **Issues detected: [count]**
   [List issues from JSON with severity badges]

   **Actions [taken/suggested]: [count]**
   [List actions from JSON]

   💡 **Next Steps:**
   - Review the issues and actions
   - If this was a dry-run, run again with --auto-fix to apply changes
   - Commit the cleanup changes separately from feature work
   ```

5. **Provide guidance based on issues**:

   - For **duplicate numbers**: Suggest running with --auto-fix
   - For **gaps**: Explain gaps are OK if specs were deleted, or can be closed with --auto-fix
   - For **missing files**: Suggest creating the required spec files
   - For **misplaced directories**: Explain which workflow subdirectory they should be in

## Example Usage

**Validation before release:**
```
/speckit.cleanup "validate before v2.0 release"
```

**Fix numbering after merge:**
```
/speckit.cleanup --auto-fix "fix numbering after merge"
```

**Dry-run to see what would change:**
```
/speckit.cleanup --dry-run --auto-fix "check organization"
```

## Safety Notes

Remind users that:
- ✅ Only affects documentation in `specs/` directory
- ✅ Code files are never touched
- ✅ Changes are reversible (git history preserved)
- ✅ Dry-run mode available to preview changes
- ✅ Detailed report generated for every run

## Common Scenarios

**After merging branches**: Specs from different branches may have overlapping numbers. Cleanup detects duplicates and can renumber automatically.

**Before releases**: Validate that all specs are properly organized before tagging a release.

**Periodic maintenance**: Monthly or quarterly cleanup runs help keep specs organized as the project grows.

**After reorganization**: If you manually moved or renamed specs, run cleanup to validate the new structure.

---

*Remember: This workflow is about organization and validation, not content. It ensures specs are numbered and located correctly but doesn't change what's written in them.*
