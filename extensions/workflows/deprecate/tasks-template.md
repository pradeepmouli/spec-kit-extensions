# Tasks: Deprecation - [FEATURE NAME]

**Deprecation ID**: deprecate-###
**Original Feature**: [Link to feature spec]
**Input**: Deprecation plan from `specs/deprecate-###-feature-name/deprecation.md`

## Format: `[ID] Description`
- Tasks numbered sequentially
- Three-phase approach: Warnings → Disabled → Removed

---

## Phase 0: Planning & Preparation

- [ ] **T001** Analyze feature usage
  - Query analytics for active users
  - Identify high-usage accounts
  - Determine usage patterns
  - Document in deprecation.md

- [ ] **T002** Run dependency scan
  - Execute scan-dependencies.sh
  - Identify all code importing/using feature
  - Find indirect dependencies
  - Document in deprecation.md

- [ ] **T003** Assess business impact
  - Calculate revenue impact
  - Estimate support burden reduction
  - Identify affected customers
  - Get stakeholder input

- [ ] **T004** Determine timeline
  - Consider user migration needs
  - Balance with business goals
  - Set phase dates (Phase 1, 2, 3)
  - Document in deprecation.md

- [ ] **T005** Identify alternative solution
  - What should users migrate to?
  - Is alternative feature-complete?
  - Document differences
  - Create comparison chart

- [ ] **T006** Get approvals
  - Product owner sign-off
  - Engineering lead sign-off
  - Support lead sign-off
  - Legal review (if needed for contracts)

## Phase 1: Warnings & Communication (No Functionality Removed)

### Communication Tasks

- [ ] **T007** Write migration guide
  - Step-by-step migration instructions
  - Code examples (before/after)
  - FAQ section
  - Troubleshooting tips
  - Publish to documentation site

- [ ] **T008** Create user notification content
  - Email template
  - In-app notification text
  - Support article
  - Blog post announcement
  - Get copywriting review

- [ ] **T009** Prepare support team
  - Brief support on deprecation
  - Provide talking points
  - Create canned responses
  - Set up tracking labels

- [ ] **T010** Announce deprecation
  - Send emails to active users
  - Post blog announcement
  - Update documentation homepage
  - Add to API changelog
  - Social media (if applicable)

### Technical Tasks

- [ ] **T011** Add deprecation warnings to UI
  - Banner/toast in feature UI
  - Modal on first use (if appropriate)
  - Link to migration guide
  - Test across all entry points

- [ ] **T012** Add API deprecation headers
  - Add `Deprecation` header to responses
  - Add `Sunset` header with Phase 3 date
  - Add `Link` header to migration guide
  - Test with curl/Postman

- [ ] **T013** Add console/log warnings
  - Warning on feature initialization
  - Daily warning in server logs
  - Include sunset date
  - Include migration URL

- [ ] **T014** Update documentation
  - Add deprecation notice to all feature docs
  - Mark as "deprecated" in navigation
  - Add sunset date
  - Link to alternative

- [ ] **T015** Add usage tracking
  - Log deprecated feature usage
  - Track user IDs
  - Send to analytics
  - Create dashboard

- [ ] **T016** Run full test suite
  - Ensure warnings don't break functionality
  - Test all feature entry points
  - Verify no performance impact
  - Fix any issues

- [ ] **T017** Deploy Phase 1 changes
  - Deploy to staging first
  - Verify warnings appear correctly
  - Deploy to production
  - Monitor for issues

### Monitoring Tasks

- [ ] **T018** Monitor usage trends
  - Daily check of usage metrics
  - Track migration rate
  - Identify laggards
  - Weekly report to stakeholders

- [ ] **T019** Outreach to high-usage accounts
  - Identify top 10 users
  - Personal outreach via email/call
  - Offer migration assistance
  - Track their progress

- [ ] **T020** Support ticket monitoring
  - Track deprecation-related tickets
  - Identify common issues
  - Update FAQ/migration guide
  - Weekly summary

- [ ] **T021** Phase 1 readiness check (before Phase 2)
  - Usage dropped by [X]%?
  - Critical users migrated?
  - Support team confident?
  - Go/no-go decision

## Phase 2: Disabled by Default (Opt-in Available)

### Communication Tasks

- [ ] **T022** Send Phase 2 reminder emails
  - Email remaining active users
  - Emphasize Phase 2 date approaching
  - Repeat migration instructions
  - Offer help

- [ ] **T023** Announce Phase 2 deployment
  - Blog post update
  - API changelog entry
  - In-app notification
  - Support team briefing

### Technical Tasks

- [ ] **T024** Implement feature flag
  - Add flag to feature flags system
  - Default: disabled
  - Allow opt-in via settings/config
  - Test flag toggling

- [ ] **T025** Add opt-in UI (if applicable)
  - Settings page toggle
  - Warning modal before enabling
  - Show sunset date
  - Require confirmation

- [ ] **T026** Update feature entry points
  - Check feature flag before rendering UI
  - Show "disabled" message if off
  - Provide link to alternative
  - Link to opt-in instructions

- [ ] **T027** Strengthen warnings for opt-in users
  - More prominent warning banner
  - Modal on every session start
  - Email after opting in
  - Daily reminder

- [ ] **T028** Update API behavior
  - Return 410 Gone for new users
  - Return 200 with warnings for opted-in users
  - Update API documentation
  - Test both scenarios

- [ ] **T029** Update tests
  - Tests should handle feature disabled state
  - Add tests for opt-in flow
  - Test error messages
  - Test alternative feature suggestion

- [ ] **T030** Run full test suite
  - All tests pass with feature disabled
  - All tests pass with feature enabled
  - No regressions in other features
  - Fix any failures

- [ ] **T031** Deploy Phase 2 changes
  - Deploy to staging
  - Test disabled state
  - Test opt-in flow
  - Deploy to production
  - Monitor errors

### Monitoring Tasks

- [ ] **T032** Monitor opt-in rate
  - How many users opted back in?
  - Are they high-value users?
  - Personal outreach if needed
  - Weekly report

- [ ] **T033** Track errors/issues
  - Any features breaking without deprecated feature?
  - Dependency scan missed anything?
  - Fix issues quickly
  - Update scan script if needed

- [ ] **T034** Phase 2 readiness check (before Phase 3)
  - Opt-in rate < [X]%?
  - Zero critical users remaining?
  - No major blockers reported?
  - Go/no-go decision

## Phase 3: Complete Removal

### Communication Tasks

- [ ] **T035** Final warning to remaining users
  - Email to any opted-in users
  - Phone call if high-value customer
  - Offer emergency migration assistance
  - Set hard deadline

- [ ] **T036** Announce Phase 3 deployment
  - API changelog entry
  - Blog post (removal complete)
  - Mark as resolved in support system

### Technical Tasks - Code Removal

- [ ] **T037** Remove feature UI components
  - Delete React components
  - Delete routes
  - Delete styles
  - Commit with clear message

- [ ] **T038** Remove feature backend code
  - Delete API endpoints
  - Delete service layer code
  - Delete utility functions
  - Commit with clear message

- [ ] **T039** Remove database schema
  - Create migration to drop tables
  - Backup data before dropping (if needed)
  - Run migration on staging
  - Verify app still works
  - Run migration on production

- [ ] **T040** Remove feature tests
  - Delete unit tests
  - Delete integration tests
  - Delete E2E tests
  - Remove test fixtures/mocks

- [ ] **T041** Remove feature flags
  - Delete flag from feature flag system
  - Remove flag checks from code
  - Clean up flag-related config

- [ ] **T042** Update dependencies
  - Remove packages only used by this feature
  - Update import statements
  - Run `npm prune` or equivalent
  - Update lockfile

- [ ] **T043** Remove documentation
  - Remove feature docs from main nav
  - Archive docs (don't delete - keep for reference)
  - Remove from sitemap
  - Keep migration guide accessible

- [ ] **T044** Update architecture diagrams
  - Remove feature from system diagrams
  - Update API documentation
  - Update data flow diagrams
  - Update CLAUDE.md if mentioned

### Technical Tasks - Dependency Cleanup

- [ ] **T045** Fix code that depended on deprecated feature
  - Review scan-dependencies.sh output
  - Update each dependent file
  - Remove imports
  - Use alternative where needed

- [ ] **T046** Update related features
  - Features that had optional integration
  - Remove integration code
  - Update UI to remove references
  - Update documentation

- [ ] **T047** Clean up workarounds
  - Were there workarounds for this feature's quirks?
  - Remove no-longer-needed hacks
  - Simplify code that worked around issues

### Testing Tasks

- [ ] **T048** Run full test suite
  - All tests pass
  - No references to removed feature
  - No broken imports
  - No console errors

- [ ] **T049** Manual testing (critical flows)
  - Test main user journeys
  - Ensure no UI references remain
  - Check error handling
  - Verify performance unchanged

- [ ] **T050** Staging deployment test
  - Deploy to staging
  - Smoke test all features
  - Check logs for errors
  - Monitor for 24 hours

- [ ] **T051** Production deployment
  - Deploy during low-traffic window
  - Monitor error rates
  - Monitor performance metrics
  - Be ready to rollback

### Post-Removal Tasks

- [ ] **T052** Monitor for regressions (1 week)
  - Daily check of error logs
  - Monitor support tickets
  - Watch for reports of missing feature
  - Check dependent features working

- [ ] **T053** Verify data cleanup
  - Confirm database tables dropped
  - Verify backups if data retained
  - Check for orphaned data
  - Document data retention policy

- [ ] **T054** Update build/deploy processes
  - Remove feature-specific build steps
  - Remove feature-specific deploy checks
  - Update CI/CD configs
  - Clean up environment variables

- [ ] **T055** Final documentation update
  - Mark deprecation as complete
  - Archive migration guide
  - Update CHANGELOG
  - Document lessons learned

## Phase 4: Post-Mortem & Lessons Learned

- [ ] **T056** Write lessons learned
  - What went well?
  - What was harder than expected?
  - How long did migration take vs. estimate?
  - What would you do differently?

- [ ] **T057** Review deprecation metrics
  - Total sunset duration
  - Migration completion rate
  - Support ticket volume
  - Cost savings achieved

- [ ] **T058** Update deprecation process
  - Based on lessons learned
  - Update templates
  - Update timeline recommendations
  - Share with team

---

## Rollback Procedures

### If Need to Rollback Phase 1
(Decided not to deprecate after all)
1. Remove deprecation warnings
2. Remove deprecation from docs
3. Announce continued support
4. Resume normal development

### If Need to Rollback Phase 2
(Too many users need feature, can't migrate)
1. Change feature flag default back to enabled
2. Remove stronger warnings
3. Announce continued support
4. Re-evaluate deprecation timeline

### If Need to Rollback Phase 3
(Critical issue discovered after removal)
1. Revert commits that removed feature
2. Restore database schema from migration
3. Redeploy previous version
4. Test thoroughly
5. Announce issue and timeline

---

## Completion Criteria

✅ All three phases completed successfully
✅ Zero active users of deprecated feature
✅ All code removed from codebase
✅ Database cleaned up
✅ Documentation archived
✅ No regressions in other features
✅ Lessons learned documented
✅ Team updated on process improvements

**Actual Sunset Duration**: [Track from Phase 1 start to Phase 3 complete]
- Target: [X months]
- Actual: [Y months]
- Variance: [explain if different]

---

*Tasks generated from deprecate workflow - See .specify/extensions/workflows/deprecate/*
