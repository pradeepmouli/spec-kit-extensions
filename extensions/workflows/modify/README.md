# Modification Workflow

## Overview

The modification workflow handles changes to existing features. It emphasizes **impact analysis** and **backward compatibility** to ensure changes don't break existing functionality.

## When to Use

Use `/modify` when:

- Changing behavior of an existing feature
- Adding capabilities to existing functionality
- Removing functionality from a feature
- Altering contracts/APIs of existing code
- Responding to changed requirements

**Do NOT use `/modify` for**:
- Creating new features → use `/specify` instead
- Fixing bugs without changing intended behavior → use `/bugfix` instead
- Improving code quality without behavior changes → use `/refactor` instead
- Deprecating entire features → use `/deprecate` instead

## Process

### 1. Impact Analysis
- Run `scan-impact.sh` to identify affected code
- Review original feature specification
- Identify all files that import/use the feature
- Check contracts and API usage
- Find related tests that may need updates

### 2. Modification Planning
- Document what's being added/modified/removed
- Assess backward compatibility
- Plan migration path for breaking changes
- Update original feature documentation
- Define rollback strategy

### 3. Implementation
- Make changes incrementally
- Update affected code paths
- Modify contracts/interfaces
- Update integration points
- Add new tests for modified behavior

### 4. Verification
- All existing tests still pass (or updated appropriately)
- New tests cover modified behavior
- Dependent features still work
- Migration path tested (if applicable)
- Documentation updated

### 5. Communication
- Document breaking changes clearly
- Update API documentation
- Notify affected teams/users
- Provide migration examples
- Update CHANGELOG

## Quality Gates

- ✅ Impact analysis MUST identify all affected files and contracts
- ✅ Original feature spec MUST be linked
- ✅ Backward compatibility MUST be assessed
- ✅ Migration path MUST be documented if breaking changes
- ✅ All dependent code MUST be updated

## Files Created

```
specs/
└── 014-edit-profile-form/
    └── modifications/
        └── 001-add-avatar-compression/
            ├── modification.md   # Change documentation
            ├── impact.md         # Auto-generated impact analysis
            └── tasks.md          # Sequential tasks
```

## Command Usage

```bash
/modify 014 "add avatar compression to reduce storage costs"
```

This will:
1. Find original feature `014-edit-profile-form`
2. Run impact analysis on feature files
3. Create branch `014-mod-001-add-avatar-compression`
4. Generate `modification.md` with template
5. Generate `impact.md` with scan results
6. Generate `tasks.md` with tasks
7. Set `SPECIFY_MODIFICATION` environment variable

## Example Modification Document

```markdown
# Modification: Add Avatar Compression

**Modification ID**: 014-mod-001
**Original Feature**: specs/014-edit-profile-form/
**Status**: Planning

## Changes Overview

### Added Functionality
- Compress uploaded avatars to max 500KB
- Support JPEG, PNG, WebP formats
- Generate multiple sizes (thumbnail, small, medium, large)

### Modified Functionality
- Profile image upload now triggers compression pipeline
- API response includes URLs for all image sizes
- Storage path structure changed to include size variants

### Removed Functionality
- None

## Backward Compatibility

**Breaking Changes**: Yes

1. **API Response Shape Changed**
   - Before: `{ avatarUrl: string }`
   - After: `{ avatarUrl: { thumbnail: string, small: string, medium: string, large: string } }`

   **Migration**: Clients should use `avatarUrl.medium` for default display

2. **Storage Structure Changed**
   - Before: `/avatars/user-123.jpg`
   - After: `/avatars/user-123/medium.jpg`

   **Migration**: Run migration script to restructure existing avatars

## Impact Analysis

From `impact.md`:
- 3 files directly use profile upload
- 12 components display user avatars
- 2 API endpoints return avatar URLs
- 5 tests verify upload behavior

**Risk Level**: Medium - Multiple components affected
```

## Impact Analysis Output

The `scan-impact.sh` script automatically generates:

```markdown
# Impact Analysis

**Feature**: 014-edit-profile-form
**Scan Date**: 2025-10-01

## Feature Files (Created by This Feature)
- `app/routes/profile.edit.tsx` (245 lines)
- `app/components/EditProfileForm.tsx` (180 lines)
- `tests/profile-edit.test.ts` (95 lines)

## Code Dependencies (Other Files Importing Feature Files)
Files importing `app/components/EditProfileForm.tsx`:
- `app/routes/profile.tsx`
- `app/routes/settings.tsx`

## Contract Dependencies
Contracts affected by this feature:
- `contracts/profile-request.ts` (used by 3 routes)
- `contracts/profile-response.ts` (used by 5 components)

## Test Dependencies
Tests referencing feature files:
- `tests/integration/profile-flow.test.ts`
```

## Task Breakdown

The workflow generates 28 tasks across 6 phases:

- **T001-T004**: Analysis (impact scan, review contracts)
- **T005-T008**: Planning (assess compatibility, plan migration)
- **T009-T015**: Update Contracts
- **T016-T020**: Update Implementation
- **T021-T025**: Update Tests
- **T026-T028**: Verification & Documentation

## Tips

### Managing Breaking Changes

**Option 1: Versioned APIs**
```typescript
// Support both old and new structure
export function getAvatarUrl(profile: Profile, size: 'thumbnail' | 'medium' = 'medium') {
  // New structure
  if (typeof profile.avatarUrl === 'object') {
    return profile.avatarUrl[size]
  }
  // Old structure (deprecated)
  return profile.avatarUrl
}
```

**Option 2: Gradual Migration**
```typescript
// Phase 1: Add new field alongside old
{
  avatarUrl: string,  // deprecated
  avatarUrls: { thumbnail, small, medium, large }
}

// Phase 2: Remove old field after clients migrate
{ avatarUrls: { ... } }
```

**Option 3: Feature Flags**
```typescript
if (featureFlags.avatarCompression) {
  return compressedAvatarUrl
} else {
  return originalAvatarUrl
}
```

### When to Create a Modification vs. New Feature

**Create Modification If**:
- Building on existing feature's foundation
- Sharing most of the original code
- Users think of it as "enhancing X"
- Original spec is still mostly accurate

**Create New Feature If**:
- Largely independent functionality
- Could exist without original feature
- Users think of it as "new feature Y"
- Requires extensive new specification

## Integration with Constitution

This workflow upholds:

- **Section IV: Progressive Enhancement** - Build upon stable foundations
- **Section VI: Workflow Selection** - Proper workflow for feature changes
- **Quality Gates** - Impact analysis and compatibility assessment required

## Related Workflows

- **Specify** - For creating new features from scratch
- **Refactor** - For improving code without changing behavior
- **Deprecate** - For removing features entirely

## Common Modifications

### Adding Optional Parameter
```typescript
// Before
function createTweet(content: string): Tweet

// After (backward compatible)
function createTweet(content: string, options?: { tags?: string[] }): Tweet
```

### Extending Response Data
```typescript
// Before
{ id, username, displayName }

// After (backward compatible)
{ id, username, displayName, bio, avatarUrl }  // Added fields
```

### Changing Validation Rules
```typescript
// Before: Username 3-15 chars
// After: Username 3-30 chars

// Impact: Users can now choose longer usernames
// Compatibility: Existing usernames still valid
// Migration: None required
```

---

*Modification Workflow Documentation - Part of Specify Extension System*
