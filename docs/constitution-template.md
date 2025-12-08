## Development Workflow

### Core Workflow (Feature Development)
1. Feature request initiates with `/specify <description>`
2. Clarification via `/clarify` to resolve ambiguities
3. Technical planning with `/plan` to create implementation design
4. Task breakdown using `/tasks` for execution roadmap
5. Implementation via `/implement` following task order

### Extension Workflows
- **Bugfix**: `/bugfix "<description>"` → bug-report.md + tasks.md with regression test requirement
- **Modification**: `/modify <feature_num> "<description>"` → modification.md + impact analysis + tasks.md
- **Refactor**: `/refactor "<description>"` → refactor.md + baseline metrics + incremental tasks.md
- **Hotfix**: `/hotfix "<incident>"` → hotfix.md + expedited tasks.md + post-mortem.md (within 48 hours)
- **Deprecation**: `/deprecate <feature_num> "<reason>"` → deprecation.md + dependency scan + phased tasks.md

### Workflow Selection
Development activities SHALL use the appropriate workflow type based on the nature of the work. Each workflow enforces specific quality gates and documentation requirements tailored to its purpose:

- **Feature Development** (`/specify`): New functionality - requires full specification, planning, and TDD approach
- **Bug Fixes** (`/bugfix`): Defect remediation - requires regression test BEFORE applying fix
- **Modifications** (`/modify`): Changes to existing features - requires impact analysis and backward compatibility assessment
- **Refactoring** (`/refactor`): Code quality improvements - requires baseline metrics, behavior preservation guarantee, and incremental validation
- **Hotfixes** (`/hotfix`): Emergency production issues - expedited process with deferred testing and mandatory post-mortem
- **Deprecation** (`/deprecate`): Feature sunset - requires phased rollout (warnings → disabled → removed), migration guide, and stakeholder approvals

The wrong workflow SHALL NOT be used - features must not bypass specification, bugs must not skip regression tests, and refactorings must not alter behavior.

### Quality Gates by Workflow

**Feature Development**:
- Specification MUST be complete before planning
- Plan MUST pass constitution checks before task generation
- Tests MUST be written before implementation (TDD)
- Code review MUST verify constitution compliance

**Bugfix**:
- Bug reproduction MUST be documented with exact steps
- Regression test MUST be written before fix is applied
- Root cause MUST be identified and documented
- Prevention strategy MUST be defined

**Modification**:
- Impact analysis MUST identify all affected files and contracts
- Original feature spec MUST be linked
- Backward compatibility MUST be assessed
- Migration path MUST be documented if breaking changes

**Refactor**:
- Baseline metrics MUST be captured before any changes unless explicitly exempted
- Tests MUST pass after EVERY incremental change
- Behavior preservation MUST be guaranteed (tests unchanged)
- Target metrics MUST show measurable improvement unless explicitly exempted

**Hotfix**:
- Severity MUST be assessed (P0/P1/P2)
- Rollback plan MUST be prepared before deployment
- Fix MUST be deployed and verified before writing tests (exception to TDD)
- Post-mortem MUST be completed within 48 hours of resolution

**Deprecation**:
- Dependency scan MUST be run to identify affected code
- Migration guide MUST be created before Phase 1
- All three phases MUST complete in sequence (no skipping)
- Stakeholder approvals MUST be obtained before starting