# GitHub Copilot Instructions for spec-kit-extensions Projects

## Overview

This project uses spec-kit-extensions workflows for managing feature development, bug fixes, refactoring, and more. When working with this codebase, please follow these guidelines.

## Workflow Types

This project supports these spec-kit workflows:

### Feature Development
- **Command**: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`
- **Branch pattern**: `001-feature-name`
- **Use for**: New features and functionality

### Bug Fixes
- **Command**: `/speckit.bugfix "description"`
- **Branch pattern**: `bugfix/001-description`
- **Use for**: Fixing bugs and issues

### Enhancements
- **Command**: `/speckit.enhance "description"`
- **Branch pattern**: `enhance/001-description`
- **Use for**: Improving existing features

### Modifications
- **Command**: `/speckit.modify "description"`
- **Branch pattern**: `modify/001^002-description`
- **Use for**: Changing existing features

### Refactoring
- **Command**: `/speckit.refactor "description"`
- **Branch pattern**: `refactor/001-description`
- **Use for**: Restructuring code without changing behavior

### Hotfixes
- **Command**: `/speckit.hotfix "description"`
- **Branch pattern**: `hotfix/001-description`
- **Use for**: Critical production issues

### Deprecation
- **Command**: `/speckit.deprecate "description"`
- **Branch pattern**: `deprecate/001-description`
- **Use for**: Deprecating features or APIs

### Cleanup
- **Command**: `/speckit.cleanup "description"`
- **Branch pattern**: `cleanup/001-description`
- **Use for**: Removing dead code and tech debt

### Code Review
- **Command**: `/speckit.review`
- **Use for**: Reviewing completed implementation work

## Important Rules

### Before Merging (CRITICAL)

**Every spec-kit branch MUST have a completed code review before merging:**

1. After completing implementation work, run: `/speckit.review`
2. Ensure the review generates a review file (e.g., `review.md`) in the spec directory
3. The review file must contain one of these statuses:
   - `Status: ✅ Approved`
   - `Status: ⚠️ Approved with Notes`
4. Do NOT merge if status is: `Status: ❌ Needs Changes`
5. Commit and push the review file before creating a PR

**The GitHub workflow will automatically check for review completion and block merges without approved reviews.**

### Workflow Selection

When starting new work:

1. Identify the type of work (feature, bug fix, enhancement, etc.)
2. Use the appropriate `/speckit.*` command
3. Follow the workflow through to review:
   - Create spec (if needed)
   - Create plan
   - Create tasks
   - Implement
   - **Review (REQUIRED)**
   - Commit review file
   - Create PR

### Code Review Process

When reviewing code:

1. Run `/speckit.review` to start the review
2. The review should check:
   - Implementation matches specification
   - All acceptance criteria met
   - Tests pass
   - Code quality is acceptable
   - No obvious bugs or security issues
3. Generate a review report with clear status
4. Save the review to the spec directory
5. Commit the review file

### Spec Directory Structure

Spec directories follow this structure:

```
specs/
├── {workflow-type}/
│   └── {number}-{description}/
│       ├── spec.md          # Feature specification
│       ├── plan.md          # Implementation plan
│       ├── tasks.md         # Task list
│       └── review.md        # Code review (REQUIRED before merge)
```

For standard features (no workflow prefix):
```
specs/
└── {number}-{description}/
    ├── spec.md
    ├── plan.md
    ├── tasks.md
    └── review.md
```

## Best Practices

### When Creating Features

1. Always create a clear specification first
2. Break work into manageable tasks
3. Implement one task at a time
4. Test as you go
5. **Review before creating PR**

### When Fixing Bugs

1. Use `/speckit.bugfix` for bug fixes
2. Document the bug clearly in the spec
3. Include reproduction steps
4. Verify the fix with tests
5. **Review to ensure no regressions**

### When Refactoring

1. Use `/speckit.refactor` for refactoring work
2. Ensure behavior doesn't change
3. Verify all existing tests still pass
4. Document the refactoring goals
5. **Review to confirm no functional changes**

## GitHub Integration

### Issue Templates

When creating issues, use the appropriate template:

- `🚀 Feature Request` - For new features
- `🐛 Bug Report` - For bugs
- `✨ Enhancement Request` - For enhancements
- `🔄 Modification Request` - For modifications
- `🔨 Refactoring Request` - For refactoring
- `🚨 Hotfix Request` - For critical issues
- `⚠️ Deprecation Request` - For deprecations
- `🧹 Cleanup Request` - For cleanup work
- `📋 Baseline/Documentation Request` - For documentation

### Pull Requests

When creating PRs:

1. Ensure review is completed and approved
2. Reference the related issue
3. Include a clear description
4. List what was changed and why
5. Mention any breaking changes
6. Link to the spec directory

### Review Enforcement

The repository has automated checks:

- **spec-kit-review-required**: Checks for review completion
  - Runs on all PRs to main/master/develop
  - Detects spec-kit branch patterns
  - Searches for review file
  - Validates approval status
  - Blocks merge if review missing or not approved

## Common Patterns

### Starting New Work

```bash
# For a new feature
/speckit.specify "user profile page"
/speckit.plan
/speckit.tasks

# For a bug fix
/speckit.bugfix "login button not working on mobile"
```

### Completing Work

```bash
# After implementation
/speckit.review

# Review generates report - ensure it shows "Approved"
# Commit the review file
git add specs/{workflow-type}/{number}-*/review.md
git commit -m "Add code review for {description}"
git push

# Create PR
gh pr create --title "..." --body "..."
```

### Handling Review Feedback

If review shows "Needs Changes":

1. Address the issues listed in the review
2. Run tests to verify fixes
3. Run `/speckit.review` again
4. Commit the updated review file
5. Push changes

## Integration with AI Agents

This project is agent-agnostic and works with:

- **GitHub Copilot** (you!)
- **Claude Code**
- **Cursor**
- **Other spec-kit compatible agents**

All workflows use standard spec-kit commands and patterns, so the experience is consistent across agents.

## Reminders

- ✅ **ALWAYS** run `/speckit.review` before creating a PR
- ✅ **ALWAYS** commit the review file to your branch
- ✅ **ALWAYS** ensure review status is "Approved" or "Approved with Notes"
- ❌ **NEVER** merge without a completed, approved review
- ❌ **NEVER** skip the review step

## Questions?

If you're unsure which workflow to use, ask the developer. Default to:
- Bug fixes → `/speckit.bugfix`
- New features → `/speckit.specify`
- Improvements → `/speckit.enhance`
- Code cleanup → `/speckit.cleanup`

**And remember: ALWAYS review before merge!**
