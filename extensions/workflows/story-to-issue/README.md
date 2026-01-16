# Story-to-Issue Workflow

## Overview

The **story-to-issue** utility creates a single GitHub issue per story/feature with all tasks as checkboxes, providing a cleaner alternative to creating one issue per task.

## Purpose

Convert your spec-kit feature specification into a comprehensive GitHub issue that includes:
- Story description and context
- Acceptance criteria
- All tasks as interactive checkboxes
- Implementation plan summary
- Workflow-aware labels

## When to Use

Use this command when you want to:
- Create **one GitHub issue per story** (instead of one per task)
- Keep your issue tracker clean and organized
- Provide full context in a single issue for team discussion
- Track progress at the story level with task checkboxes
- Align with agile/scrum methodology (stories as units of work)

## Command

```bash
/speckit.story-to-issue [optional context]
```

## Prerequisites

- Feature branch checked out
- `spec.md` exists in feature directory (story description and acceptance criteria)
- `tasks.md` exists in feature directory (task breakdown)
- Git remote is a GitHub repository
- GitHub MCP server configured (for issue creation)

## What It Creates

A single GitHub issue with this structure:

```markdown
## Story
[Story description from spec.md]

## Acceptance Criteria
[Criteria from spec.md]

## Tasks
- [ ] T001: Task description
- [ ] T002: Task description
- [ ] T003: Task description

## Implementation Plan
[Summary from plan.md if available]

## Context
**Branch**: feature/001-user-auth
**Feature Directory**: specs/001-user-auth/
**Created from spec-kit workflow**
```

## Labels

Automatically adds workflow-aware labels based on branch pattern:

- `bugfix/*` → `bug`, `bugfix`
- `refactor/*` → `refactor`, `technical-debt`
- `hotfix/*` → `hotfix`, `urgent`
- `modify/*` → `enhancement`, `modification`
- `deprecate/*` → `deprecation`, `breaking-change`
- Standard features → `feature`, `enhancement`

Plus status labels:
- `status: planning` - Tasks exist but none completed
- `status: in-progress` - Some tasks completed

## Example Usage

### Basic Usage

```bash
# From your feature branch
/speckit.story-to-issue
```

### With Context

```bash
# Add specific context or labels
/speckit.story-to-issue "Mark as priority: high"
```

### Output

```
✅ GitHub Issue Created

Issue: #123
Title: Implement User Authentication
URL: https://github.com/user/repo/issues/123

Tasks Included: 4 tasks
Labels: feature, status: planning

Next Steps:
1. Review issue on GitHub
2. Assign to team members
3. Add to project board/milestone
4. Track progress by checking off tasks
```

## Workflow Integration

Fits naturally into spec-kit workflows:

### 1. Planning Phase
```bash
/speckit.plan      # Create spec.md with story
/speckit.tasks     # Break down into tasks.md
```

### 2. Issue Creation
```bash
/speckit.story-to-issue  # Create GitHub issue
```

### 3. Implementation
```bash
/speckit.implement  # Execute tasks
# Check off tasks in GitHub as you complete them
```

### 4. Review
```bash
/speckit.review     # Validate completion
# Update issue with review results
```

## Comparison with tasks-to-issues

| Aspect | tasks-to-issues (Core) | story-to-issue (Extension) |
|--------|----------------------|---------------------------|
| **Creates** | One issue per task | One issue per story |
| **GitHub Issues** | N issues (task count) | 1 issue with checkboxes |
| **Context** | Task-specific only | Full story context |
| **Discussion** | Fragmented across issues | Centralized in one issue |
| **Issue List** | Can get cluttered | Clean and organized |
| **Best For** | Large, independent tasks | Agile stories with small tasks |

## Best Practices

1. **Keep stories small**: If you have 15+ tasks, consider splitting the story
2. **Update checkboxes**: Check off tasks in GitHub as you complete them
3. **Link from commits**: Reference issue in commit messages (`fixes #123`)
4. **Assign appropriately**: Assign story issue to person/pair working on it
5. **Use milestones**: Add story to appropriate milestone/project
6. **Review and close**: Use `/speckit.review` to validate, then close when merged

## Troubleshooting

### "Remote is not a GitHub URL"
- Ensure your Git remote points to a GitHub repository
- Check with: `git config --get remote.origin.url`

### "No spec.md found"
- Run `/speckit.plan` first to create the specification
- Ensure you're on a feature branch with a feature directory

### "No tasks.md found"
- Run `/speckit.tasks` to break down the story into tasks
- Or create issue with story and criteria only (will note tasks needed)

### "Issue already exists"
- Check if an issue with the same title already exists
- Consider updating the existing issue instead of creating a duplicate

## Safety Features

- **Validates GitHub remote**: Won't create issues in wrong repository
- **Comprehensive error handling**: Clear messages for missing prerequisites
- **CAUTION checks**: Multiple safety checks before creating issues
- **Context preservation**: All feature context included in issue

## Related Commands

- `/speckit.plan` - Create story specification
- `/speckit.tasks` - Break story into tasks
- `/speckit.implement` - Execute task implementation
- `/speckit.review` - Validate story completion

## Additional Resources

See also:
- [Story-to-Issue Comparison Guide](../../../docs/story-to-issue.md)
- [Spec-Kit Documentation](https://github.com/github/spec-kit)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
