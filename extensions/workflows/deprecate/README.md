# Deprecation Workflow

## Overview

The deprecation workflow manages the planned sunset of features. It uses a **3-phase approach** (warnings → disabled by default → removal) to ensure smooth user migration with minimal disruption.

## When to Use

Use `/deprecate` when:

- Feature no longer aligns with product vision
- Better alternative exists and users should migrate
- Feature has low/no usage
- Maintenance burden is high relative to value
- Security/compliance concerns
- Technical debt reduction initiative

**Do NOT use `/deprecate` for**:
- Quick bug fixes → use `/bugfix` instead
- Temporary feature disabling → use feature flags
- Emergency removal → explain why it's urgent first
- Features still actively used → understand impact first

## Core Principles

1. **Users need time to migrate** - Don't surprise them with sudden removal
2. **Communication is key** - Over-communicate throughout process
3. **Provide alternatives** - Give users a migration path
4. **Be patient** - Full sunset typically takes 3-6 months

## Process

### Phase 0: Planning & Preparation (2-4 weeks)

1. **Analyze usage** - How many users? How often?
2. **Run dependency scan** - What code depends on this feature?
3. **Assess business impact** - Revenue? Support burden?
4. **Determine timeline** - How long for each phase?
5. **Identify alternative** - Where should users go?
6. **Get approvals** - Product, Engineering, Support sign-off

### Phase 1: Warnings & Communication (1-3 months)

**Goal**: Inform users, provide migration resources

- Add deprecation warnings to UI
- Add console warnings/logs
- Update API with deprecation headers
- Email all active users
- Publish migration guide
- Brief support team
- Monitor usage trends

**Success Criteria**: All users notified, migration guide available

### Phase 2: Disabled by Default (1-2 months)

**Goal**: Feature off for new users, opt-in for existing users

- Feature disabled by default
- Allow opt-in via settings if needed
- Stronger warnings when enabled
- Personal outreach to remaining users
- Monitor opt-in rate

**Success Criteria**: < 5% of users still opted-in

### Phase 3: Complete Removal (Final)

**Goal**: Remove all code and clean up

- Remove feature code
- Drop database tables
- Remove API endpoints
- Remove tests
- Archive documentation
- Final notice to any remaining users

**Success Criteria**: Code removed, no regressions, zero usage

## Quality Gates

- ✅ Dependency scan MUST be run to identify affected code
- ✅ Migration guide MUST be created before Phase 1
- ✅ All three phases MUST complete in sequence (no skipping)
- ✅ Stakeholder approvals MUST be obtained before starting
- ✅ 48-hour stability period MUST be observed post-removal

## Files Created

```
specs/
└── deprecate-001-edit-profile-form/
    ├── deprecation.md      # Deprecation plan
    ├── dependencies.md     # Auto-generated dependency scan
    └── tasks.md            # 58 phased tasks
```

## Command Usage

```bash
/deprecate 014 "low usage (< 1% users) and high maintenance burden"
```

This will:
1. Find original feature `014-edit-profile-form`
2. Run dependency scan automatically
3. Create branch `deprecate/001-edit-profile-form`
4. Generate `deprecation.md` with plan template
5. Generate `dependencies.md` with scan results
6. Generate `tasks.md` with 58 tasks
7. Set `SPECIFY_DEPRECATE` environment variable

## Example Deprecation Plan

```markdown
# Deprecation Plan: Edit Profile Form (Old Version)

**Deprecation ID**: deprecate-001
**Original Feature**: specs/014-edit-profile-form/
**Status**: Phase 1 (Warnings)

## Deprecation Timeline

**Deprecation Announced**: 2025-10-01
**Phase 1 Start (Warnings)**: 2025-10-01
**Phase 2 Start (Disabled)**: 2025-12-01 (2 months)
**Phase 3 Start (Removal)**: 2026-02-01 (4 months total)
**Total Sunset Period**: 4 months

## Rationale

### Why Deprecate?
- [X] Replaced by better alternative (new profile editor with live preview)
- [X] Low usage (0.8% of users in last 30 days)
- [X] High maintenance burden (12 bug tickets in 6 months)

### Supporting Data
**Usage Statistics**:
- Active users (last 30 days): 42 out of 5,000 (0.84%)
- API calls (last 30 days): 127
- Feature engagement: Declining 15% month-over-month

**Maintenance Cost**:
- LOC maintained: 1,245
- Bug tickets: 12 in last 6 months
- Engineering hours/month: ~4 hours
- Support tickets: 8/month

**Business Impact**:
- Revenue: Negligible (<$50/month estimated)
- Strategic value: Low (superseded by new editor)

## Affected Users

### User Segments
**Internal Users**:
- QA team: Uses for testing (can migrate easily)

**External Users**:
- 42 active users in last 30 days
- Mostly power users who prefer old UI

### Migration Path

**Recommended Alternative**: New Profile Editor (feature 023)

**Why better**:
- Live preview of changes
- Drag-and-drop avatar upload
- Auto-save functionality
- Mobile-optimized

**Migration complexity**: Easy (< 5 minutes)

**Migration guide**: `/docs/migrating-from-old-profile-editor`

## Dependencies (from scan)

**Code Dependencies**:
- `app/routes/profile.edit.tsx` (direct feature file)
- `app/components/EditProfileForm.tsx` (direct feature file)
- `app/routes/settings.tsx` (imports EditProfileForm)

**Risk Level**: Low - Only 1 external dependency

## Phase 1: Warnings (Oct 1 - Dec 1)

**Technical Changes**:
- Banner in old profile editor: "This editor will be removed Feb 1. Switch to new editor."
- Console warning when rendering old component
- API response includes `Deprecation` header

**Communication**:
- Email to 42 active users
- Blog post announcement
- In-app notification
- Support team briefing

## Phase 2: Disabled by Default (Dec 1 - Feb 1)

**Technical Changes**:
- Old editor disabled by default
- Opt-in via settings toggle
- Modal warning before enabling
- Stronger deprecation notice

**Communication**:
- Email reminder to remaining users
- Personal outreach to high-usage accounts

## Phase 3: Complete Removal (Feb 1+)

**Technical Changes**:
- Remove all old editor code
- Remove routes
- Update settings page
- Archive documentation

**Communication**:
- Final warning email
- Changelog entry
```

## Dependency Scan Output

The `scan-dependencies.sh` script generates:

```markdown
# Dependency Scan Results

**Feature**: 014-edit-profile-form
**Scan Date**: 2025-10-01

## Feature Files (Created by This Feature)
- `app/routes/profile.edit.tsx` (245 lines)
- `app/components/EditProfileForm.tsx` (180 lines)
- `tests/profile-edit.test.ts` (95 lines)

## Code Dependencies (Other Files Importing Feature Files)
Files importing `app/components/EditProfileForm.tsx`:
- `app/routes/settings.tsx`

## Summary
- **Feature Files**: 3
- **Dependency Categories**: 1

✅ **Low Risk**: This feature appears mostly isolated. Deprecation should be straightforward.
```

## Task Breakdown

The workflow generates 58 tasks across 4 phases:

- **T001-T006**: Phase 0 - Planning & Preparation (6 tasks)
- **T007-T021**: Phase 1 - Warnings & Communication (15 tasks)
- **T022-T034**: Phase 2 - Disabled by Default (13 tasks)
- **T035-T055**: Phase 3 - Complete Removal (21 tasks)
- **T056-T058**: Phase 4 - Post-Mortem & Lessons Learned (3 tasks)

## Tips

### Setting Realistic Timelines

**Phase 1 Duration** (Warnings):
- Internal/power users: 1 month minimum
- Consumer product: 2-3 months
- Enterprise/API: 6-12 months (longer contracts)

**Phase 2 Duration** (Disabled):
- Low-stakes feature: 1 month
- Medium-stakes: 2 months
- High-stakes: 3+ months

**Total Sunset**:
- Minor feature: 3 months
- Major feature: 6 months
- Core functionality: 12+ months

### Effective Communication

**Email Template**:
```
Subject: [Feature Name] will be retired on [Date]

Dear [User],

We're writing to let you know that [Feature Name] will be retired on [Date].

Why: [Brief, honest reason]

What to do: We recommend migrating to [Alternative]. Here's a guide: [Link]

Timeline:
- Now - [Date]: Feature available with warnings
- [Date] - [Date]: Disabled by default (opt-in available)
- [Date]: Completely removed

Questions? Reply to this email or contact support.

Thanks for your understanding,
[Team]
```

### Handling Pushback

**Common objections**:

1. **"I like the old one better"**
   - Acknowledge their preference
   - Explain the maintenance/strategic reasons
   - Offer to incorporate feedback into new version

2. **"I don't have time to migrate"**
   - Offer migration assistance
   - Extend timeline if many users feel this way
   - Provide detailed migration guide

3. **"This breaks my workflow"**
   - Understand their workflow
   - Find equivalent in new version
   - Consider if feature gap exists

4. **"You're breaking backward compatibility"**
   - For APIs: Valid concern, be very careful
   - Offer versioned API if possible
   - Give very long timeline (12+ months)

### Measuring Success

Track these metrics:

- **Migration rate**: % of users who switched
- **Opt-in rate** (Phase 2): How many came back?
- **Support tickets**: Are users struggling?
- **Sentiment**: What are users saying?

### When to Abort Deprecation

Consider stopping if:

- Usage increases instead of decreases (users need it more than you thought)
- Major customers threaten to churn
- No suitable alternative emerges
- Engineering cost to remove is too high
- Business circumstances change

## Integration with Constitution

This workflow upholds:

- **Section IV: Progressive Enhancement** - Phased approach prevents disruption
- **Section VI: Workflow Selection** - Proper workflow for feature sunset
- **Quality Gates** - Dependency analysis and approvals required

## Related Workflows

- **Modify** - For changing features rather than removing
- **Specify** - For creating the replacement feature

## Communication Templates

### API Deprecation Header
```
Deprecation: version="1.0"
Sunset: "2026-02-01T00:00:00Z"
Link: <https://example.com/docs/migration-guide>; rel="deprecation"
```

### In-App Warning
```
⚠️ This feature will be removed on February 1, 2026

We recommend switching to the new [Feature Name].

[View Migration Guide] [Switch Now] [Remind Me Later]
```

### Console Warning
```javascript
console.warn(
  '[DEPRECATED] OldFeature will be removed on 2026-02-01. ' +
  'Please migrate to NewFeature. See: https://example.com/migration'
)
```

---

*Deprecation Workflow Documentation - Part of Specify Extension System*
