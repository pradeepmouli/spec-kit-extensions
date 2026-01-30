# PhasesToIssues Command

## Overview

The `speckit.phasestoissues` command creates **one GitHub issue per development phase**, enabling parallel work and better tracking of complex features.

## The Phases Approach

### What Are Development Phases?

Development phases are logical stages in feature development:

1. **Design & Planning** - Architecture, API design, dependencies
2. **Implementation** - Core functionality development
3. **Testing & Validation** - Quality assurance, edge cases
4. **Documentation** - User guides, API docs, examples
5. **Deployment** - Release preparation, rollout

### Why Phase-Based Issues with Task Sub-Issues?

**Creates**: One parent issue per phase + individual sub-issues for each task

```
spec.md (Feature: User Authentication)
├── Phase 1: Design & Planning
│   └── Tasks: T001, T002
├── Phase 2: Implementation
│   └── Tasks: T003, T004, T005
└── Phase 3: Testing
    └── Tasks: T006, T007

Creates 3 parent phase issues + 7 task sub-issues:

#123 - Phase 1: Design & Planning
  ├── #124 (sub): T001: Create architecture diagram
  └── #125 (sub): T002: Define API contracts

#126 - Phase 2: Implementation (depends on #123)
  ├── #127 (sub): T003: Implement auth service
  ├── #128 (sub): T004: Add session management
  └── #129 (sub): T005: Create login UI

#130 - Phase 3: Testing (depends on #126)
  ├── #131 (sub): T006: Write unit tests
  └── #132 (sub): T007: Integration testing
```

**Benefits:**
- **Parallel work**: Different team members work on different phases AND tasks
- **Clear dependencies**: Phases show what blocks what, tasks show granular dependencies
- **Better ownership**: Each phase AND each task can have its own assignee
- **Granular tracking**: Track progress per phase AND per task
- **Flexible pacing**: Phases and tasks can move at different speeds
- **Natural milestones**: Each phase completion is a milestone
- **Individual discussions**: Each task has its own comment thread
- **Native GitHub integration**: Uses GitHub's sub-issues feature for proper hierarchy
- **Status propagation**: Parent phase issue auto-updates based on sub-issue completion

## Comparison: Different Issue Strategies

### Tasks-to-Issues (One Issue Per Task)

```
Creates N issues (one per task):
#123 - T001: Create architecture diagram
#124 - T002: Define API contracts
#125 - T003: Implement auth service
...
```

**Best for**: Large, independent tasks needing separate discussions

**Challenges**: Issue tracker clutter, lost context, hard to see big picture
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

### Single Issue (One Issue Per Feature)

```
Creates 1 issue with all tasks:
#123 - Implement User Authentication
  - [ ] T001: Create architecture diagram
  - [ ] T002: Define API contracts
  - [ ] T003: Implement auth service
  ...
```

**Best for**: Small features, single-person work, simple tracking

**Challenges**: Can't parallelize, hard to assign different parts to different people

### PhasesToIssues (Parent Phase + Task Sub-Issues) ⭐

```
Creates 3 parent issues + N sub-issues (one per task):
#123 - Phase 1: Design & Planning
  ├── #124 (sub): T001: Create architecture diagram
  └── #125 (sub): T002: Define API contracts
#126 - Phase 2: Implementation (depends on #123)
  ├── #127 (sub): T003: Implement auth service
  ├── #128 (sub): T004: Add session management
  └── #129 (sub): T005: Create login UI
#130 - Phase 3: Testing (depends on #126)
  └── ...
```

**Best for**: Complex features, team collaboration, parallel work, task-level delegation

**Benefits**: Clear hierarchy, phase AND task dependencies, individual task ownership, task-level discussions, native GitHub sub-issues

## When to Use PhasesToIssues

Use this command when:

- **Complex features**: Multiple logical stages of work
- **Team collaboration**: Different people own different phases
- **Parallel work**: Some phases can progress simultaneously
- **Clear milestones**: Each phase represents a significant milestone
- **Better visibility**: Track progress at phase level, not just task level

## Usage

```bash
# From your feature branch
/speckit.phasestoissues

# Or with context
/speckit.phasestoissues "Include priority: high, mark dependencies"
```

**Creates:**
- Parent GitHub issues (one per phase) with:
  - Phase description and goals
  - Acceptance criteria for that phase
  - Dependencies on other phases
  - Implementation guidance
- Task sub-issues (one per task) with:
  - Task ID and description (e.g., "T001: Create architecture diagram")
  - Link to parent phase issue
  - Same labels as parent phase
  - Individual assignment and tracking

## Example Output

```
✅ GitHub Issues Created

Phase 1: Design & Planning
  Parent Issue: #123
  Sub-Issues: 2 tasks
    - #124: T001: Create architecture diagram
    - #125: T002: Define API contracts
  Status: Ready to start

Phase 2: Implementation
  Parent Issue: #126
  Sub-Issues: 3 tasks
    - #127: T003: Implement auth service
    - #128: T004: Add session management
    - #129: T005: Create login UI
  Depends on: #123
  Status: Blocked

Phase 3: Testing & Validation
  Parent Issue: #130
  Sub-Issues: 2 tasks
    - #131: T006: Write unit tests
    - #132: T007: Integration testing
  Depends on: #126
  Status: Blocked

Total: 3 phase issues, 7 task sub-issues
Labels: feature, multi-phase

Next Steps:
1. Assign phases to team members
2. Start work on Phase 1
3. Track progress per phase
4. Unblock subsequent phases as dependencies complete
```

## Workflow Integration

### PhasesToIssues fits naturally into spec-kit workflows:

1. **Planning Phase**
   ```bash
   /speckit.plan      # Create spec.md with phases defined
   /speckit.tasks     # Break down into tasks.md
   ```

2. **Issue Creation**
   ```bash
   /speckit.phasestoissues  # Create GitHub issues per phase
   ```

3. **Implementation Phase**
   ```bash
   /speckit.implement  # Execute tasks
   # Update phase issues as work progresses
   ```

4. **Review Phase**
   ```bash
   /speckit.review     # Validate per phase
   # Update phase issues with review results
   ```

## Best Practices

1. **Define clear phases**: Ensure spec.md has well-defined phase sections
2. **Document dependencies**: Make dependencies between phases explicit
3. **Assign ownership**: Assign each phase issue to appropriate team member
4. **Update regularly**: Keep phase issues updated as work progresses
5. **Link commits**: Reference phase issues in commit messages (`#123`)
6. **Use milestones**: Add all phase issues to the same milestone
7. **Review per phase**: Validate each phase before marking complete
8. **Close together**: Close all phase issues when feature is complete

## Defining Phases in spec.md

Structure your spec.md to clearly define phases:

```markdown
# User Authentication

## Overview
[Feature description]

## Phases

### Phase 1: Design & Planning
**Goal**: Establish architecture and contracts
**Deliverables**:
- Architecture diagram
- API contract definitions
- Security requirements

### Phase 2: Implementation
**Goal**: Build core authentication functionality
**Deliverables**:
- Auth service implementation
- Session management
- Login UI components
**Depends on**: Phase 1

### Phase 3: Testing & Validation
**Goal**: Ensure quality and security
**Deliverables**:
- Unit tests
- Integration tests
- Security audit
**Depends on**: Phase 2
```

## Related Commands

- `/speckit.plan` - Create specification with phases
- `/speckit.tasks` - Break down into tasks
- `/speckit.review` - Validate phase completion
- `/speckit.implement` - Execute task implementation
