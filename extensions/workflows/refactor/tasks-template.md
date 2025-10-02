# Tasks: Refactor - [IMPROVEMENT DESCRIPTION]

**Refactor ID**: refactor-###
**Input**: Refactor spec from `specs/refactor-###-description/refactor-spec.md`

## Format: `[ID] Description`
- Tasks numbered sequentially
- Must complete in order for refactoring work

---

## Phase 1: Baseline Capture (BEFORE touching any code)

- [ ] **T001** Ensure clean working directory (commit or stash changes)
- [ ] **T002** Verify all existing tests pass (100% pass rate required)
  - Run full test suite
  - Document current pass rate
  - Fix any failing tests BEFORE refactoring

- [ ] **T003** Capture baseline metrics
  - Run `.specify/extensions/workflows/refactor/measure-metrics.sh --before`
  - Review metrics-before.md
  - Document in refactor-spec.md baseline section

- [ ] **T004** Create behavioral snapshot
  - Document key inputs and outputs
  - Run critical user flows and record results
  - Screenshot UI states if applicable
  - Save to behavioral-snapshot.md

- [ ] **T005** Create git tag for rollback point
  - `git tag pre-refactor-### -m "Baseline before refactor-###"`
  - Verify tag created: `git tag -l pre-refactor-###`

- [ ] **T006** Set up monitoring (if production refactoring)
  - Baseline performance metrics
  - Error rate baseline
  - Key business metrics baseline

## Phase 2: Refactoring Implementation (Incremental & Test-Driven)

**CRITICAL RULE**: After EVERY step below, run tests. All tests MUST pass before proceeding.

### Step 1: Prepare
- [ ] **T007** Create new files for extracted code (if extracting)
  - Empty files with proper structure
  - Export statements prepared
  - Tests still pass (no-op change)

- [ ] **T008** Add tests for new abstractions (if creating new classes/functions)
  - Write tests for extracted functionality
  - Tests fail initially (no implementation yet)

### Step 2: Extract/Refactor (Small Atomic Steps)
- [ ] **T009** First incremental change: [specific small change]
  - Make minimal change
  - Run tests - MUST pass
  - Commit immediately if green

- [ ] **T010** Second incremental change: [specific small change]
  - Make minimal change
  - Run tests - MUST pass
  - Commit immediately if green

- [ ] **T011** Third incremental change: [specific small change]
  - Make minimal change
  - Run tests - MUST pass
  - Commit immediately if green

- [ ] **T012** Continue incremental changes...
  - [Add more tasks as needed, one per logical step]
  - Each task: change → test → commit
  - NEVER batch multiple changes before testing

### Step 3: Remove Duplication
- [ ] **T013** Replace first duplicated block with abstraction
  - Tests pass
  - Commit

- [ ] **T014** Replace second duplicated block
  - Tests pass
  - Commit

- [ ] **T015** Replace remaining duplications
  - Tests pass
  - Commit

### Step 4: Clean Up
- [ ] **T016** Remove dead code
  - Delete unused functions/classes
  - Remove commented-out code
  - Tests still pass

- [ ] **T017** Update comments and documentation
  - Reflect new structure
  - Explain new abstractions
  - Remove obsolete comments

- [ ] **T018** Run linter and fix issues
  - Auto-fix formatting
  - Manually fix linting errors
  - Tests still pass

## Phase 3: Validation (Behavior Preservation Proof)

- [ ] **T019** Run full test suite
  - MUST be 100% pass rate
  - If any failures, this is a RED FLAG - investigate before proceeding
  - Tests should NOT need modification (behavior unchanged)

- [ ] **T020** Capture post-refactoring metrics
  - Run `.specify/extensions/workflows/refactor/measure-metrics.sh --after`
  - Review metrics-after.md
  - Compare with baseline

- [ ] **T021** Verify target metrics achieved
  - Check cyclomatic complexity reduction
  - Check duplication elimination
  - Check coverage maintained/improved
  - Document improvements in refactor-spec.md

- [ ] **T022** Reproduce behavioral snapshot
  - Run same inputs as baseline
  - Compare outputs - MUST be identical
  - If different, STOP and investigate

- [ ] **T023** Performance regression testing
  - Run performance benchmarks
  - Compare with baseline
  - Max acceptable regression: 5%
  - If > 5% regression, optimize or reconsider refactoring

- [ ] **T024** Manual testing of critical paths
  - Test key user flows
  - Verify UI behavior unchanged (if applicable)
  - Check error handling still correct

## Phase 4: Code Review & Documentation

- [ ] **T025** Self-review changes
  - Read entire diff
  - Verify no behavior changes
  - Check for accidental complexity introduction
  - Ensure no new dependencies added unnecessarily

- [ ] **T026** Update architecture documentation (if applicable)
  - Update diagrams
  - Update design docs
  - Explain new patterns introduced

- [ ] **T027** Create pull request with evidence
  - Include before/after metrics
  - Include behavioral preservation proof
  - Explain refactoring rationale
  - Link to refactor spec

- [ ] **T028** Request peer review
  - Focus on behavior preservation
  - Verify improvements achieved
  - Check for hidden coupling
  - Approve before merge

## Phase 5: Deployment & Monitoring

- [ ] **T029** Deploy to staging environment
  - Run full test suite in staging
  - Manual smoke tests
  - Monitor for 24 hours

- [ ] **T030** Monitor staging metrics
  - Performance stable?
  - Error rate unchanged?
  - No unexpected behavior?

- [ ] **T031** Deploy to production (phased if possible)
  - Feature flag on (if available)
  - Deploy to small % of users first
  - Monitor closely

- [ ] **T032** Monitor production metrics (48-72 hours)
  - Performance within acceptable range?
  - Error rate unchanged?
  - User reports normal?
  - Business metrics unaffected?

- [ ] **T033** Full rollout (if stable)
  - Remove feature flag (if used)
  - Monitor for 1 week
  - Mark refactoring complete

## Phase 6: Cleanup & Learning

- [ ] **T034** Remove rollback tag (if stable after 1 week)
  - `git tag -d pre-refactor-###`
  - Keep tag in remote for 1 month before deletion

- [ ] **T035** Document lessons learned
  - What went well?
  - What could be improved?
  - Patterns to reuse?
  - Patterns to avoid?

- [ ] **T036** Identify future refactoring opportunities
  - Similar patterns elsewhere?
  - Related technical debt?
  - Create follow-up refactor specs if needed

---

## Rollback Procedure (If Needed)

If at ANY point things go wrong:

1. **Immediate Rollback**:
   ```bash
   git reset --hard pre-refactor-###
   git push --force origin <branch>  # If already pushed
   ```

2. **Verify Rollback**:
   - Run tests (should be 100% pass)
   - Check production metrics
   - Verify user experience restored

3. **Post-Mortem**:
   - Document what went wrong
   - Update refactor spec with learnings
   - Adjust approach before retrying

---

## Completion Criteria

✅ All tests passing (100% pass rate, no modifications)
✅ Target metrics achieved (documented improvement)
✅ Behavioral snapshot matches (behavior unchanged)
✅ No performance regression (< 5%)
✅ Code review approved
✅ Deployed to production successfully
✅ 1 week stability period completed
✅ No rollbacks required

**Estimated Time**: Varies by refactoring size
- Small (extract function): 2-4 hours
- Medium (extract class, eliminate duplication): 1-2 days
- Large (architectural refactoring): 3-5 days

---
*Tasks generated from refactor workflow - See .specify/extensions/workflows/refactor/*
