# Tasks: Hotfix - [INCIDENT TITLE]

**Hotfix ID**: hotfix-###
**Severity**: [P0/P1/P2]
**Input**: Hotfix spec from `specs/hotfix-###-description/hotfix.md`

## Format: `[ID] Description`
- Tasks numbered sequentially
- Emergency process - complete as fast as safely possible

---

## Phase 1: Immediate Response (URGENT)

- [ ] **T001** Assess severity and impact
  - How many users affected?
  - Is service completely down or degraded?
  - Is data at risk?
  - Document in hotfix.md

- [ ] **T002** Notify incident commander and stakeholders
  - Alert on-call engineer
  - Notify management (if P0/P1)
  - Start incident channel/room

- [ ] **T003** Reproduce the issue
  - Confirm the problem exists
  - Document exact steps to reproduce
  - Capture error messages/logs

- [ ] **T004** Investigate root cause
  - Check recent deployments (was this a regression?)
  - Review error logs
  - Check monitoring dashboards
  - Identify the problematic code/config

- [ ] **T005** Document root cause in hotfix.md
  - What file/code is causing the issue
  - Why it's failing
  - Why tests didn't catch it

## Phase 2: Fix Implementation (FAST BUT SAFE)

- [ ] **T006** Determine fix strategy
  - Option 1: Quick code fix (if simple and safe)
  - Option 2: Rollback to previous version (if recent deployment)
  - Option 3: Feature flag disable (if feature-specific)
  - Option 4: Configuration change (if config issue)
  - Document chosen approach in hotfix.md

- [ ] **T007** Implement the fix
  - Make minimal code changes
  - Focus on stopping the bleeding, not perfect solution
  - Can refactor later - right now just make it work
  - Document files changed

- [ ] **T008** Test fix locally
  - Reproduce original issue
  - Apply fix
  - Verify issue resolved
  - Check for obvious side effects

- [ ] **T009** Quick code review (if time permits)
  - Get another pair of eyes
  - 5-minute sanity check
  - Focus on: does this fix the issue without breaking something else?
  - Skip if P0 and every second counts

## Phase 3: Deployment (URGENT)

- [ ] **T010** Prepare rollback plan
  - Document how to undo this fix
  - Test rollback steps (if time permits)
  - Have rollback commands ready

- [ ] **T011** Deploy to staging (if P1/P2, skip if P0)
  - Quick staging test
  - Verify fix works
  - 5-10 minutes max

- [ ] **T012** Deploy to production
  - Follow deployment process
  - Monitor error logs during deployment
  - Be ready to rollback immediately

- [ ] **T013** Verify fix in production
  - Check error rates dropped
  - Test affected functionality
  - Monitor user reports
  - Document verification in hotfix.md

- [ ] **T014** Update incident status
  - Mark as "Deployed - Monitoring"
  - Update incident channel
  - Notify stakeholders

## Phase 4: Monitoring (24-48 Hours)

- [ ] **T015** Active monitoring (first 2 hours)
  - Watch error rates
  - Watch performance metrics
  - Watch user reports
  - Be ready to rollback

- [ ] **T016** Extended monitoring (24 hours)
  - Check dashboards regularly
  - Review error logs
  - Watch for related issues
  - Confirm stability

- [ ] **T017** Rollback decision checkpoint (2 hours after deployment)
  - Are metrics stable?
  - Any new issues introduced?
  - Decision: keep fix or rollback?

## Phase 5: Post-Incident (Within 48 Hours)

- [ ] **T018** Add regression test
  - Write test that reproduces the bug
  - Verify test fails on old code
  - Verify test passes with fix
  - Add to test suite

- [ ] **T019** Run full test suite
  - Ensure fix didn't break other tests
  - Fix any failures
  - Get to 100% pass rate

- [ ] **T020** Update hotfix.md with final details
  - Complete all sections
  - Add commit SHA
  - Document final impact numbers
  - Mark verification checklist complete

- [ ] **T021** Schedule post-mortem meeting
  - Within 48 hours of resolution
  - Invite all relevant stakeholders
  - Prepare timeline and data

- [ ] **T022** Write detailed post-mortem
  - Complete post-mortem.md template
  - Timeline of events
  - Root cause analysis
  - Action items for prevention
  - Lessons learned

- [ ] **T023** Create prevention tasks
  - Tests to add
  - Monitoring to improve
  - Code to refactor
  - Process to change
  - Create separate tasks (use `/bugfix` or `/refactor`)

- [ ] **T024** Communication (if needed)
  - User-facing incident report (if public-facing issue)
  - Internal post-mortem sharing
  - Status page update

- [ ] **T025** Update documentation
  - Runbooks (add this failure mode)
  - Architecture docs (document vulnerability)
  - API docs (if behavior changed)
  - CLAUDE.md (note the fix)

## Phase 6: Resolution

- [ ] **T026** Verify 48-hour stability
  - No recurrence
  - No related issues
  - Metrics normal
  - User reports resolved

- [ ] **T027** Close incident
  - Update incident status to "Resolved"
  - Close incident channel
  - Archive incident data

- [ ] **T028** Review action items from post-mortem
  - Ensure owners assigned
  - Ensure due dates set
  - Track to completion

---

## Rollback Procedure (If Needed)

If the fix causes worse problems:

1. **Immediate Rollback**:
   ```bash
   git revert <hotfix-commit-sha>
   # OR
   git reset --hard <previous-good-commit>
   # Deploy previous version
   ```

2. **Verify Rollback**:
   - Confirm service restored
   - Check metrics
   - Notify stakeholders

3. **Re-Plan**:
   - Root cause analysis was wrong?
   - Fix introduced new bug?
   - Need different approach?
   - Start over at Phase 1

---

## Completion Criteria

✅ Incident resolved (service restored)
✅ Fix deployed and stable (48+ hours)
✅ Regression test added
✅ Post-mortem complete
✅ Action items created and assigned
✅ Documentation updated
✅ No recurrence observed

**Time to Resolution**: [Track actual time]
- P0 Target: < 1 hour
- P1 Target: < 4 hours
- P2 Target: < 8 hours

---
*Tasks generated from hotfix workflow - See .specify/extensions/workflows/hotfix/*
