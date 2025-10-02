# Tasks: Bug Fix - [BUG TITLE]

**Bug ID**: bugfix-###
**Input**: Bug report from `specs/bugfix-###-description/bug-report.md`

## Format: `[ID] Description`
- Tasks are numbered sequentially (T001, T002, etc.)
- All tasks should be completed in order for bug fixes

---

## Phase 1: Investigation & Reproduction

- [ ] **T001** Read bug report and understand current vs expected behavior
- [ ] **T002** Set up clean environment to reproduce bug
- [ ] **T003** Reproduce bug following documented steps (verify it actually fails)
- [ ] **T004** Investigate root cause - read relevant code, add debug logging, trace execution
- [ ] **T005** Document root cause in bug-report.md (technical explanation section)
- [ ] **T006** Identify all files that need modification
- [ ] **T007** Document fix strategy in bug-report.md (approach and files to modify)

## Phase 2: Regression Test (MUST WRITE BEFORE FIX)

- [ ] **T008** Create regression test file in appropriate test directory
  - Test MUST fail initially (reproduces the bug)
  - Test should be focused on the specific bug behavior
  - Include comments explaining what bug this prevents
- [ ] **T009** Run regression test to verify it fails as expected
- [ ] **T010** Document test file path and description in bug-report.md

## Phase 3: Apply Fix

- [ ] **T011** Implement fix in identified files
  - Keep changes minimal and focused
  - Add comments explaining the fix if not obvious
  - Preserve backward compatibility unless explicitly breaking
- [ ] **T012** Run regression test - MUST pass after fix
- [ ] **T013** Run existing test suite - all tests MUST still pass
- [ ] **T014** If tests fail, debug and adjust fix (do not weaken tests)

## Phase 4: Verification & Documentation

- [ ] **T015** Manual verification of fix in clean environment
  - Follow original reproduction steps
  - Verify expected behavior now occurs
  - Test edge cases identified during investigation
- [ ] **T016** Check for similar bugs in related code
  - Search for same pattern in other files
  - Fix proactively if found
- [ ] **T017** Update relevant documentation if bug revealed gaps
  - API docs if behavior was misunderstood
  - README if setup was unclear
  - Comments if code was confusing
- [ ] **T018** Update bug-report.md verification checklist (mark all complete)
- [ ] **T019** Update CLAUDE.md or agent-specific file if patterns changed

## Phase 5: Prevention (Optional but Recommended)

- [ ] **T020** Document prevention strategy in bug-report.md
  - Could this class of bug be prevented with linting?
  - Should validation be added elsewhere?
  - Is refactoring needed to make this more robust?
- [ ] **T021** If prevention requires follow-up work, create separate task
  - Use `/refactor` workflow if code quality improvements needed
  - Use `/modify` workflow if feature enhancements needed

---

## Completion Criteria

✅ Bug reproduced and root cause documented
✅ Regression test written and initially failing
✅ Fix implemented
✅ Regression test now passing
✅ All existing tests still passing
✅ Manual verification complete
✅ Documentation updated
✅ Prevention strategy documented

**Estimated Time**: 2-4 hours (typical bug fix with testing)

---
*Tasks generated from bugfix workflow - See .specify/extensions/workflows/bugfix/*
