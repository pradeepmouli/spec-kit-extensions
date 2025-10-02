<!-- Sync Impact Report
Version Change: 1.0.0 → 1.1.0 (Extension System)
Modified Principles: Added Section VI (Workflow Selection), Updated Quality Gates
Added Sections: VI. Workflow Selection
Removed Sections: N/A
Templates Requiring Updates:
- plan-template.md: ✅ Constitution Check section references all principles
- spec-template.md: ✅ Compatible with current structure
- tasks-template.md: ✅ Supports all workflow task categories
- CLAUDE.md: ✅ Already references constitution authority
- Extension workflows: ✅ All 5 new workflows comply with existing principles
Follow-up TODOs: None
Amendment Rationale: Added support for 5 new workflow types (bugfix, modify, refactor, hotfix, deprecate) to extend specification-first development to all software lifecycle activities.
-->

# Tweeter Constitution

## Core Principles

### I. Specification-First Development
Every feature MUST begin with a formal specification document using the `/specify` command. Specifications define the "what" and "why" before any implementation. No code shall be written without an approved spec that clearly articulates user scenarios, requirements, and success criteria. This ensures alignment between stakeholder expectations and delivered functionality.

### II. Minimal Viable Functionality
Features MUST adhere to the 140-character constraint that defines Tweeter's core identity. Complexity SHALL be actively resisted - every feature must justify its existence through clear user value. YAGNI (You Aren't Gonna Need It) principles apply: build only what is specified, avoid premature optimization, and reject feature creep that compromises the platform's simplicity.

### III. Test-Driven Development
Tests MUST be written before implementation following the Red-Green-Refactor cycle. Every contract, endpoint, and user-facing feature SHALL have corresponding tests that fail initially, then pass once implemented. Integration tests are mandatory for inter-component communication. Test coverage SHALL be maintained at minimum 80% for core functionality.

### IV. Progressive Enhancement
Development SHALL proceed from simple to complex in measured iterations. Start with text-only tweets, then add mentions, then hashtags - each enhancement must build upon stable foundations. Database schemas SHALL support forward migration without breaking existing data. APIs MUST maintain backward compatibility within major versions.

### V. Clear Data Boundaries
Data models SHALL maintain strict separation between users, tweets, and interactions. Each entity MUST own its data exclusively - no shared mutable state. Foreign key relationships SHALL be explicit and enforced at the database level. Data access SHALL occur only through defined service interfaces, never through direct database queries from presentation layers.

### VI. Workflow Selection
Development activities SHALL use the appropriate workflow type based on the nature of the work. Each workflow enforces specific quality gates and documentation requirements tailored to its purpose:

- **Feature Development** (`/specify`): New functionality - requires full specification, planning, and TDD approach
- **Bug Fixes** (`/bugfix`): Defect remediation - requires regression test BEFORE applying fix
- **Modifications** (`/modify`): Changes to existing features - requires impact analysis and backward compatibility assessment
- **Refactoring** (`/refactor`): Code quality improvements - requires baseline metrics, behavior preservation guarantee, and incremental validation
- **Hotfixes** (`/hotfix`): Emergency production issues - expedited process with deferred testing and mandatory post-mortem
- **Deprecation** (`/deprecate`): Feature sunset - requires phased rollout (warnings → disabled → removed), migration guide, and stakeholder approvals

The wrong workflow SHALL NOT be used - features must not bypass specification, bugs must not skip regression tests, and refactorings must not alter behavior.

## Technical Constraints

### Character Limits
- Tweet content: Maximum 140 characters (UTF-8)
- Username: Maximum 15 characters (alphanumeric + underscore)
- Display name: Maximum 50 characters

### Performance Standards
- Tweet submission: < 200ms p95 latency
- Timeline loading: < 500ms for 50 tweets
- Search response: < 1s for keyword matches

### Technology Decisions
- Backend: Language/framework determined per feature spec
- Frontend: Progressive web app, mobile-first design
- Storage: Relational database for core data, cache for timelines
- Testing: Framework-appropriate tools (pytest, jest, etc.)

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
- Baseline metrics MUST be captured before any changes
- Tests MUST pass after EVERY incremental change
- Behavior preservation MUST be guaranteed (tests unchanged)
- Target metrics MUST show measurable improvement

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

### Documentation Requirements
- Every public API MUST have inline documentation
- Complex algorithms MUST include explanation comments
- README MUST be updated for user-facing changes
- CLAUDE.md MUST reflect architectural decisions

## Governance

### Amendment Process
Constitution amendments require:
1. Written proposal documenting the change rationale
2. Impact analysis on existing features and workflows
3. Migration plan for affected components
4. Version increment following semantic versioning

### Compliance Verification
- All pull requests MUST include constitution compliance checklist
- Automated checks SHALL enforce character limits and test coverage
- Architecture reviews MUST validate data boundary adherence
- Performance regression tests SHALL guard against degradation

### Version Policy
- MAJOR: Breaking changes to core principles or data models
- MINOR: New principles or significant workflow changes
- PATCH: Clarifications, corrections, or minor adjustments

**Version**: 1.1.0 | **Ratified**: 2025-09-28 | **Last Amended**: 2025-10-01

### Amendment History
- **v1.1.0** (2025-10-01): Added Section VI (Workflow Selection) to support 5 extension workflows (bugfix, modify, refactor, hotfix, deprecate). Updated Quality Gates to document workflow-specific requirements. Minor version bump per semantic versioning.
- **v1.0.0** (2025-09-28): Initial constitution ratified with 5 core principles and development workflow.