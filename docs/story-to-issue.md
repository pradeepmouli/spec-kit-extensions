# Story-to-Issue Command

## Overview

The `speckit.story-to-issue` command creates **one GitHub issue per story/feature** with tasks as checkboxes, rather than creating one issue per task.

## Comparison: Tasks vs Story Approach

### Original `tasks-to-issues.md` (Spec-Kit Core)

**Creates**: One GitHub issue per task

```
spec.md (Feature: User Authentication)
└── tasks.md
    ├── T001: Create login form
    ├── T002: Implement password validation
    ├── T003: Add session management
    └── T004: Write authentication tests

Creates 4 separate GitHub issues:
#123 - T001: Create login form
#124 - T002: Implement password validation
#125 - T003: Add session management
#126 - T004: Write authentication tests
```

**Pros:**
- Each task independently trackable
- Can assign different people to different tasks
- Granular progress tracking
- Works well when tasks are large/complex

**Cons:**
- Issue list becomes cluttered
- Loses story context in individual issues
- No clear parent-child relationship
- Hard to see overall feature progress
- Lots of cross-referencing needed

### New `speckit.story-to-issue` (This Extension)

**Creates**: One GitHub issue per story with tasks as checkboxes

```
spec.md (Feature: User Authentication)
└── tasks.md
    ├── T001: Create login form
    ├── T002: Implement password validation
    ├── T003: Add session management
    └── T004: Write authentication tests

Creates 1 GitHub issue:
#123 - Implement User Authentication
  ✓ Story description
  ✓ Acceptance criteria
  ✓ Implementation plan
  Tasks:
  - [ ] T001: Create login form
  - [ ] T002: Implement password validation
  - [ ] T003: Add session management
  - [ ] T004: Write authentication tests
```

**Pros:**
- Cleaner issue list (one issue = one story)
- Full context in single issue
- Natural hierarchy (story → tasks)
- Progress visible at a glance
- Better for discussion/comments
- Aligns with agile story concept

**Cons:**
- Can't assign tasks to different people easily
- Less granular tracking in GitHub
- Large stories might have many checkboxes

## When to Use Each Approach

### Use `tasks-to-issues` (One Issue Per Task) When:
- Tasks are **large and complex** (multi-day efforts)
- Tasks will be **assigned to different people**
- Tasks need **separate discussions/reviews**
- Tasks have **their own acceptance criteria**
- Team prefers **granular GitHub tracking**

### Use `story-to-issue` (One Issue Per Story) When:
- Following **agile/scrum methodology** (stories as units of work)
- Tasks are **small implementation steps** (hours, not days)
- Want **cleaner issue tracker** with less noise
- Story is the **right level for team discussion**
- Tasks are **sequential dependencies** within one feature
- **One person/pair** working on entire story

## Recommendation

For **most spec-kit workflows**, use `story-to-issue` because:

1. **Spec-kit's task breakdown** is designed for implementation steps, not independent work items
2. **Stories align with branches** in spec-kit (one branch = one story)
3. **Acceptance criteria** are at the story level, not task level
4. **GitHub issue = discussion forum** works better at story granularity
5. **Reduces noise** in issue tracker

## Usage

### Story-to-Issue

```bash
# From your feature branch
/speckit.story-to-issue

# Or with context
/speckit.story-to-issue "Include priority: high label"
```

**Creates:**
- One GitHub issue with story title
- Issue body includes:
  - Story description from spec.md
  - Acceptance criteria
  - All tasks as checkboxes
  - Implementation plan summary
  - Workflow-aware labels
  - Branch and feature context

**Output:**
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

### Tasks-to-Issues (Spec-Kit Core)

```bash
# From your feature branch
/speckit.taskstoissues
```

**Creates:**
- N GitHub issues (one per task)
- Each issue gets task description as title
- Limited context per issue

## Issue Structure (Story Approach)

```markdown
## Story

As a user, I want to authenticate securely so that my data remains private.

## Acceptance Criteria

- [ ] Users can log in with email and password
- [ ] Passwords are hashed using bcrypt
- [ ] Sessions expire after 24 hours
- [ ] Failed login attempts are rate-limited

## Tasks

- [ ] T001: Create login form component
- [ ] T002: Implement password validation logic
- [ ] T003: Add session management middleware
- [ ] T004: Write authentication tests

## Implementation Plan

### Technical Approach
- Use JWT for session tokens
- bcrypt for password hashing
- Express middleware for auth checking

### Dependencies
- jsonwebtoken package
- bcrypt package
- Express session middleware

## Context

**Branch**: `feature/001-user-authentication`
**Feature Directory**: `specs/001-user-authentication/`
**Created from spec-kit workflow**

---

**Note**: Check off tasks as they are completed. Use `/speckit.review` to validate implementation.
```

## Workflow Integration

### Story-to-Issue fits naturally into spec-kit workflows:

1. **Planning Phase**
   ```bash
   /speckit.plan      # Create spec.md with story and criteria
   /speckit.tasks     # Break down into tasks.md
   ```

2. **Issue Creation**
   ```bash
   /speckit.story-to-issue  # Create GitHub issue with full context
   ```

3. **Implementation Phase**
   ```bash
   /speckit.implement  # Execute tasks
   # Check off tasks in GitHub as you complete them
   ```

4. **Review Phase**
   ```bash
   /speckit.review     # Validate against acceptance criteria
   # Update issue with review results
   ```

## Migration Strategy

If you're currently using `tasks-to-issues` and want to switch:

### Option 1: Fresh Start
- Use `story-to-issue` for all new features going forward
- Leave existing task-based issues as-is

### Option 2: Consolidate Existing
1. Create new story issue with `/speckit.story-to-issue`
2. Link old task issues to new story issue
3. Close old task issues as duplicates
4. Track progress in new story issue

### Option 3: Hybrid Approach
- Use `story-to-issue` for small-medium stories (< 10 tasks)
- Use `tasks-to-issues` for large epics (10+ tasks or multi-week)

## Best Practices

1. **Keep stories small**: If you have 15+ tasks, consider splitting the story
2. **Update checkboxes**: Check off tasks in GitHub as you complete them
3. **Link from commits**: Reference issue in commit messages (`#123`)
4. **Assign to team**: Assign story issue to person/pair working on it
5. **Use labels**: Add milestone, priority, and workflow labels
6. **Update on review**: Post review results as comments on story issue
7. **Close on merge**: Close issue when feature branch merges to main

## Future Enhancements

Potential improvements to consider:

- **Subtask conversion**: Option to convert large tasks into GitHub subtasks (beta feature)
- **Epic linking**: Automatically link to parent epic/milestone
- **Progress tracking**: Update issue description with task completion percentage
- **Dependency graphs**: Visualize task dependencies in issue
- **Time estimates**: Include estimated effort per task
- **Auto-update**: Sync task status between tasks.md and GitHub issue

## Related Commands

- `/speckit.plan` - Create story specification
- `/speckit.tasks` - Break story into tasks
- `/speckit.review` - Validate story completion
- `/speckit.implement` - Execute task implementation
