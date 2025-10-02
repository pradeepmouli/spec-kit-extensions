# Extension System Quickstart

Get started with Specify extension workflows in 5 minutes.

## What Are Extensions?

Extensions add specialized workflows to Specify for activities beyond feature development:

- `/bugfix` - Fix defects with regression tests
- `/modify` - Change existing features with impact analysis
- `/refactor` - Improve code quality with metrics tracking
- `/hotfix` - Emergency production fixes with expedited process
- `/deprecate` - Sunset features with phased rollout

## Quick Decision Tree

**What are you doing?**

```
Building something new?
└─ Use `/specify "description"`

Fixing broken behavior?
├─ Production emergency?
│  └─ Use `/hotfix "incident description"`
└─ Non-urgent bug?
   └─ Use `/bugfix "bug description"`

Changing existing feature?
├─ Adding/modifying behavior?
│  └─ Use `/modify 014 "change description"`
└─ Improving code without changing behavior?
   └─ Use `/refactor "improvement description"`

Removing a feature?
└─ Use `/deprecate 014 "deprecation reason"`
```

## 5-Minute Tutorial

### Example 1: Fix a Bug

```bash
# Discover a bug: save button doesn't work
/bugfix "save button doesn't persist data"

# This creates:
# - Branch: bugfix/001-save-button-doesnt
# - Files: bug-report.md, tasks.md

# Follow the tasks:
# 1. Reproduce the bug
# 2. Write failing test (BEFORE fixing)
# 3. Apply fix
# 4. Verify test passes
# 5. Document prevention
```

**Key principle**: Test-first approach ensures bug won't recur.

### Example 2: Modify a Feature

```bash
# Want to add avatar compression to feature 014
/modify 014 "add avatar compression to reduce storage costs"

# This creates:
# - Branch: 014-mod-001-add-avatar-compression
# - Files: modification.md, impact.md (auto-scanned), tasks.md
# - Impact analysis identifies affected files automatically

# Follow the tasks:
# 1. Review impact analysis
# 2. Plan backward compatibility
# 3. Update contracts
# 4. Implement changes
# 5. Update dependent code
```

**Key principle**: Impact analysis prevents breaking other features.

### Example 3: Refactor Code

```bash
# Extract tweet service to reduce duplication
/refactor "extract tweet submission into reusable service"

# This creates:
# - Branch: refactor/001-extract-tweet-service
# - Files: refactor.md, tasks.md, metrics-before.md, metrics-after.md

# Follow the tasks:
# 1. Capture baseline metrics (BEFORE any changes)
# 2. Make one small change
# 3. Run tests (must pass)
# 4. Commit
# 5. Repeat steps 2-4 incrementally
# 6. Capture final metrics
# 7. Compare improvement
```

**Key principle**: Incremental changes with tests between each step.

### Example 4: Emergency Hotfix

```bash
# Production is down!
/hotfix "database connection pool exhausted causing 503 errors"

# This creates:
# - Branch: hotfix/001-database-connection-pool
# - Files: hotfix.md, post-mortem.md, tasks.md
# - Reminder: post-mortem due within 48 hours

# Follow the URGENT tasks:
# 1. Assess severity (P0/P1/P2)
# 2. Notify stakeholders
# 3. Find root cause quickly
# 4. Apply fix (tests come AFTER - exception to TDD)
# 5. Deploy immediately
# 6. Monitor for 24-48 hours
# 7. Write regression test (within 24 hours)
# 8. Complete post-mortem (within 48 hours)
```

**Key principle**: Speed matters in emergencies - tests can wait, but post-mortem is mandatory.

### Example 5: Deprecate a Feature

```bash
# Old profile editor has low usage, high maintenance
/deprecate 014 "low usage (< 1%) and high maintenance burden"

# This creates:
# - Branch: deprecate/001-edit-profile-form
# - Files: deprecation.md, dependencies.md (auto-scanned), tasks.md
# - Dependency scan shows what code will break

# Follow the 3-phase approach:
# Phase 1 (1-3 months): Warnings
#   - Add deprecation warnings
#   - Email users
#   - Publish migration guide
#
# Phase 2 (1-2 months): Disabled by default
#   - Turn off for new users
#   - Allow opt-in for existing users
#   - Personal outreach to remaining users
#
# Phase 3 (final): Complete removal
#   - Remove all code
#   - Drop database tables
#   - Archive documentation
```

**Key principle**: Gradual sunset gives users time to migrate.

## Workflow Cheat Sheet

| Workflow | Command | When to Use | Key Feature |
|----------|---------|-------------|-------------|
| **Feature** | `/specify "..."` | New functionality | Full spec + TDD |
| **Bugfix** | `/bugfix "..."` | Broken behavior | Regression test first |
| **Modify** | `/modify 014 "..."` | Change existing | Impact analysis |
| **Refactor** | `/refactor "..."` | Code quality | Metrics + incremental |
| **Hotfix** | `/hotfix "..."` | Production emergency | Tests after (only exception) |
| **Deprecate** | `/deprecate 014 "..."` | Remove feature | 3-phase sunset |

## Common Questions

### When should I use `/bugfix` vs `/hotfix`?

- **Bugfix**: Non-urgent, can wait for proper TDD process
- **Hotfix**: Production emergency, every minute counts

### When should I use `/modify` vs `/refactor`?

- **Modify**: Changing what the code does (behavior)
- **Refactor**: Improving how the code works (structure/quality)

If tests need to change, it's a modification. If tests stay the same, it's a refactor.

### Can I skip phases in deprecation?

No. The 3-phase approach is required to give users adequate migration time. Skipping phases causes user churn and support burden.

### What if I pick the wrong workflow?

No problem! The worst case is you have the wrong template. You can:
1. Create a new branch with the correct workflow
2. Copy over your work
3. Delete the old branch

## File Structure

Extensions create organized directories:

```
specs/
├── 014-edit-profile-form/          # Original feature
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   └── modifications/               # Modifications to feature 014
│       └── 001-add-compression/
│           ├── modification.md
│           ├── impact.md
│           └── tasks.md
├── bugfix-001-save-button/          # Standalone bugfix
│   ├── bug-report.md
│   └── tasks.md
├── refactor-001-extract-service/    # Standalone refactor
│   ├── refactor.md
│   ├── metrics-before.md
│   ├── metrics-after.md
│   └── tasks.md
├── hotfix-001-connection-pool/      # Emergency hotfix
│   ├── hotfix.md
│   ├── post-mortem.md
│   └── tasks.md
└── deprecate-001-old-editor/        # Feature deprecation
    ├── deprecation.md
    ├── dependencies.md
    └── tasks.md
```

## Next Steps

1. **Try it**: Use a workflow on real work
2. **Read docs**: Check workflow-specific READMEs for details
3. **Customize**: Edit templates if needed for your project
4. **Share feedback**: What works? What doesn't?

## Resources

- [Extension README](.specify/extensions/README.md) - Full documentation
- [Development Guide](.specify/extensions/DEVELOPMENT.md) - Create custom workflows
- [Project Constitution](.specify/memory/constitution.md) - Quality gates per workflow
- Workflow-specific docs:
  - [Bugfix](workflows/bugfix/README.md)
  - [Modify](workflows/modify/README.md)
  - [Refactor](workflows/refactor/README.md)
  - [Hotfix](workflows/hotfix/README.md)
  - [Deprecate](workflows/deprecate/README.md)

## Troubleshooting

**Command doesn't work**: Ensure you're using the exact format:
- ✅ `/bugfix "description"`
- ❌ `/bugfix description` (missing quotes)

**Script fails**: Check you're in the repository root with `.specify/` directory

**Wrong workflow used**: Start over with correct workflow, copy work over

**Need help**: Check the workflow-specific README or ask in your project's communication channel

---

**Ready to start?** Pick a workflow above and try it on your next task!

*Extension System Quickstart - Version 1.0.0*
