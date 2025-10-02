# Tasks: Modification - [CHANGE DESCRIPTION]

**Modification ID**: ###-mod-###
**Original Feature**: ###-feature-name
**Input**: Modification spec from `specs/###-feature-name/modifications/###-mod-###/`

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Tasks numbered sequentially

---

## Phase 1: Impact Analysis & Planning

- [ ] **T001** Load original feature spec from `specs/###-feature-name/spec.md`
- [ ] **T002** Load original feature plan from `specs/###-feature-name/plan.md`
- [ ] **T003** Load original feature tasks from `specs/###-feature-name/tasks.md`
- [ ] **T004** Run impact scanner: `.specify/extensions/workflows/modify/scan-impact.sh ###`
- [ ] **T005** Review generated impact-analysis.md and verify accuracy
- [ ] **T006** Identify all files that need modification (list in modification-spec.md)
- [ ] **T007** Identify all tests that will break (expected failures)
- [ ] **T008** Document backward compatibility concerns in modification-spec.md
- [ ] **T009** Update modification-spec.md with complete impact analysis

## Phase 2: Update Contracts & Data Models

- [ ] **T010** Update affected contracts in `specs/###-feature-name/contracts/`
  - Modify existing contract files for changed endpoints/functions
  - Create new contract files for new endpoints/functions
  - Document version changes if breaking

- [ ] **T011** Create new contracts for added functionality (if applicable)
  - Place in `specs/###-feature-name/modifications/###-mod-###/contracts/`
  - Follow same schema format as original feature

- [ ] **T012** Update data-model.md if entity changes (fields added/removed/modified)

- [ ] **T013** Create database migration if needed
  - Write migration script
  - Test migration on copy of production data
  - Document rollback procedure

## Phase 3: Update Tests (Before Implementation)

### Contract Tests [P]
- [ ] **T014 [P]** Update contract tests for modified contracts
  - Tests MUST fail initially if contracts changed
  - Update assertions to match new behavior

- [ ] **T015 [P]** Create contract tests for new contracts
  - Follow TDD: write tests before implementation

### Integration Tests [P]
- [ ] **T016 [P]** Update integration tests from original feature
  - Fix tests that break due to modification
  - Verify you understand WHY they're breaking
  - Don't weaken tests - update to new expected behavior

- [ ] **T017 [P]** Create integration tests for new scenarios
  - Cover added functionality
  - Cover modified behaviors
  - Cover edge cases specific to modification

### Regression Tests
- [ ] **T018** Create regression tests to prevent breaking original functionality
  - Ensure unmodified features still work
  - Test backward compatibility explicitly
  - Verify data migration preserves integrity

## Phase 4: Implementation

### Code Updates [P] (can parallelize if different files)
- [ ] **T019 [P]** Update [file1.ts] per modification spec
  - [Specific changes needed]
  - Maintain backward compatibility where required
  - Add deprecation warnings for removed features

- [ ] **T020 [P]** Update [file2.tsx] per modification spec
  - [Specific changes needed]

- [ ] **T021 [P]** Create [new-file.ts] for new functionality
  - [Purpose and responsibilities]

### Integration
- [ ] **T022** Connect modified components
  - Ensure modified files work together
  - Test integration points
  - Verify data flows correctly

- [ ] **T023** Run full test suite
  - All contract tests MUST pass
  - All integration tests MUST pass
  - All regression tests MUST pass
  - Original feature tests MUST pass (or be deliberately updated)

- [ ] **T024** Fix any failing tests
  - Debug root cause
  - Fix implementation, not tests (unless test was wrong)
  - Re-run until green

## Phase 5: Documentation & Migration

- [ ] **T025** Update original feature's spec.md
  - Add reference to modification in Recent Changes section
  - Do NOT rewrite original spec
  - Link to modification spec

- [ ] **T026** Update quickstart.md from original feature
  - Update steps affected by modification
  - Add new steps for new functionality
  - Mark deprecated steps

- [ ] **T027** Create migration guide (if breaking changes)
  - Document steps users must take
  - Provide code examples
  - Include troubleshooting

- [ ] **T028** Update CLAUDE.md or agent-specific file
  - Add modification to Recent Changes
  - Update tech stack if dependencies changed
  - Note any new patterns or conventions

- [ ] **T029** Update API documentation (if contracts changed)
  - Document new endpoints/fields
  - Mark deprecated endpoints
  - Include examples

## Phase 6: Validation & Rollout

- [ ] **T030** Manual testing per updated quickstart.md
  - Test all modified scenarios
  - Test all new scenarios
  - Test backward compatibility explicitly
  - Test migration path (if applicable)

- [ ] **T031** Performance testing (if behavior changes)
  - Measure before/after performance
  - Ensure no regressions
  - Document any expected changes

- [ ] **T032** Security review (if authentication/data access changed)
  - Verify authorization still correct
  - Check for new vulnerabilities
  - Validate input sanitization

- [ ] **T033** Prepare rollout
  - Create feature flag (if phased rollout)
  - Set up monitoring
  - Prepare rollback plan
  - Document deployment steps

- [ ] **T034** Final verification
  - All tests green
  - Documentation complete
  - Migration guide tested
  - Team review complete

---

## Completion Criteria

✅ Impact analysis complete and accurate
✅ All contracts updated
✅ Database migration created and tested (if needed)
✅ All tests updated and passing
✅ New functionality implemented
✅ Backward compatibility preserved (or migration documented)
✅ Documentation updated
✅ Manual testing complete
✅ Ready for rollout

**Estimated Time**: Varies by modification size
- Small (add field): 4-8 hours
- Medium (modify behavior): 1-3 days
- Large (major enhancement): 3-5 days

---
*Tasks generated from modify workflow - See .specify/extensions/workflows/modify/*
