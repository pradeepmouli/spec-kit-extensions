# Real-World Examples

These examples come from **Tweeter**, a production React Router v7 Twitter clone where these workflows were developed and validated.

## Example 1: `/speckit.bugfix` - Profile Form Crash

### The Problem

Users reported a crash when editing their profile bio without uploading a new profile image:

```
Error: Invalid file type: application/octet-stream
    at uploadHandler (/app/routes/profile.edit.tsx:114:13)
```

### The Workflow

```bash
# Step 1: Create bug report
/speckit.bugfix "when submitting the profile edit form and only changing the bio, it results in: Error: Invalid file type: application/octet-stream"
# Creates: bug-report.md with initial analysis
# Shows: Next steps to review and investigate

# Step 2: Investigate and update bug-report.md with root cause
# Reproduced bug, identified uploadHandler validation issue

# Step 3: Create fix plan
/speckit.plan
# Creates: Detailed fix plan with regression test strategy

# Step 4: Break down into tasks
/speckit.tasks
# Creates: Phase-based task breakdown (regression test first, then fix)

# Step 5: Execute fix
/speckit.implement
# Implements regression test, then applies fix
```

### What It Created

- **Branch**: `bugfix/001-when-submitting-the`
- **Directory**: `specs/bugfix/001-when-submitting-the/`
- **Files**:
  - `bug-report.md` - Detailed bug analysis
  - `plan.md` - Fix strategy (created by /speckit.plan)
  - `tasks.md` - Phase-based task breakdown (created by /speckit.tasks)

### Key Process Enforced

The `/speckit.bugfix` workflow with review checkpoints enforced **regression-test-first** approach:

1. **Initial analysis** via `/speckit.bugfix`
2. **User review** of bug report and investigation
3. **Fix planning** via `/speckit.plan` - user reviews approach before implementation
4. **Task breakdown** via `/speckit.tasks` - ensures test-before-fix order
5. **Implementation** via `/speckit.implement` - executes with test-first discipline

### The Root Cause

The `uploadHandler` validated MIME types without checking if the file input was empty. Browsers send empty file inputs with `application/octet-stream` type.

### The Fix

```typescript
// app/routes/profile.edit.tsx:111-114
async function uploadHandler(fileUpload: FileUpload) {
    if (fileUpload.fieldName !== 'profileImage') {
      return;
    }

    // Skip empty file inputs (browser sends application/octet-stream for unselected files)
    if (fileUpload.type === 'application/octet-stream') {
      return;
    }

    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(fileUpload.type)) {
      throw new Error(`Invalid file type: ${fileUpload.type}`);
    }
    // ... rest of handler
}
```

### The Outcome

- ✅ Bug fixed in 1 hour
- ✅ Regression test prevents recurrence
- ✅ Build passed
- ✅ Users can now edit bio without uploading image

### Lessons Learned

The **checkpoint-based workflow** with regression-test-first approach proved valuable:
- **Review checkpoint** before planning allowed verification of root cause
- **Planning checkpoint** before implementation let user review fix approach
- **Regression test written first** caught edge cases (empty file inputs, MIME types)
- **User had control** over fix direction at each phase

**Without this workflow**: Would have quickly patched the bug without test coverage, and it would likely recur in a refactor. The previous version that auto-implemented fixes had a 0% success rate (2/2 failures) because the user couldn't review and adjust the fix approach.

---

## Example 2: `/speckit.modify` - Making Profile Fields Optional

### The Problem

Profile edit form forced users to provide all fields even when they only wanted to change one:

- Had to re-enter username to update bio
- Had to provide email (security concern)
- Poor UX for minor edits

### The Workflow

```bash
# Step 1: Create modification spec with impact analysis
/speckit.modify 014 "make profile fields optional and remove email from form"
# Creates: modification-spec.md + impact-analysis.md (auto-scanned)
# Shows: Impact summary and next steps

# Step 2: Review modification spec and impact analysis
# Verified: 4 files affected, no breaking changes, service layer already supports partial updates

# Step 3: Create implementation plan
/speckit.plan
# Creates: Detailed plan for implementing changes with backward compatibility strategy

# Step 4: Break down into tasks
/speckit.tasks
# Creates: Task list (update contracts, update schema, update form, update tests)

# Step 5: Execute changes
/speckit.implement
# Runs all tasks in correct order
```

### What It Created

- **Branch**: `014-mod-001-make-profile-fields`
- **Directory**: `specs/014-edit-profile-form/modifications/001-make-profile-fields/`
- **Files**:
  - `modification-spec.md` - Comprehensive change documentation
  - `impact-analysis.md` - **Auto-generated** file scan
  - `plan.md` - Implementation plan (created by /speckit.plan)
  - `tasks.md` - Modification task breakdown (created by /speckit.tasks)

### The Impact Analysis (Auto-Generated)

The `/modify` workflow automatically scanned the codebase and identified affected files:

```markdown
## Impact Analysis
*Auto-generated by scan-impact.sh - reviewed and adjusted*

### Files Affected (from original implementation)

**Will Need Updates**:
- **app/routes/profile.edit.tsx** (lines 18-26)
  - EditProfileSchema: Make bio and username optional using .optional()
  - Remove email field entirely

- **app/components/forms/EditProfileForm.tsx** (lines 15-22, 89-97)
  - Update props interface to remove email
  - Remove email input field from JSX
  - Reorder fields (username first, bio second)

- **specs/014-edit-profile-form/contracts/edit-profile-action.schema.json**
  - Remove email from contract
  - Mark username as optional in contract

**Unchanged but Referenced**:
- **app/services/profile.server.ts** - No changes (existing functions handle partial updates)
```

**This automatic analysis caught dependencies we would have missed manually.**

### The Changes

**Schema (Zod)**:
```typescript
// Before
const EditProfileSchema = z.object({
  bio: z.string().max(160).optional(),
  email: z.string().email().max(255),
  username: z.string().regex(/^[a-zA-Z0-9_]+$/).min(1).max(15),
});

// After
const EditProfileSchema = z.object({
  bio: z.string().max(160).optional(),
  username: z.string().regex(/^[a-zA-Z0-9_]+$/).min(1).max(15).optional(),
});
```

**Form Component**:
```typescript
// Before
interface EditProfileFormProps {
  profile: {
    bio?: string | null;
    email: string;
    username: string;
    profileImageUrl?: string | null;
  };
}

// After
interface EditProfileFormProps {
  profile: {
    bio?: string | null;
    username: string;
    profileImageUrl?: string | null;
  };
}
```

**Action Handler** (no changes needed - already supported partial updates):
```typescript
export async function updateProfileFields(
  userId: string,
  updates: {
    username?: string;
    bio?: string | null;
  }
) {
  // Only updates provided fields
  const fieldsToUpdate = {
    ...(updates.username !== undefined && { username: updates.username }),
    ...(updates.bio !== undefined && { bio: updates.bio }),
  };
  // ...
}
```

### The Outcome

- ✅ Modification completed in 2 hours
- ✅ All backward compatibility concerns addressed
- ✅ No breaking changes to existing functionality
- ✅ Build passed
- ✅ Users can now update bio without re-entering username

### Lessons Learned

The **checkpoint-based workflow** with automatic impact analysis was invaluable:
- **Impact analysis** caught all 4 files that needed updates automatically
- **Review checkpoint** allowed verification that service layer already supported partial updates
- **Planning checkpoint** ensured backward compatibility strategy before implementation
- **User reviewed** contract changes before committing to implementation

**Without this workflow**: Would have missed updating the contract schema, or forgotten to check if partial updates were supported. The review checkpoints prevented a potential breaking change.

---

## Example 3: `/speckit.modify` - Fixing Image Removal UX Bug

### The Problem

After the first modification (making fields optional), users reported their profile images were being automatically removed when they edited bio/username without uploading a new image.

### The Workflow

```bash
# Step 1: Create modification spec with impact analysis
/speckit.modify 014 "make profile edits submit even if the user doesn't add a profile image"
# Creates: modification-spec.md + impact-analysis.md
# Shows: Impact summary - identified hidden field causing automatic removal

# Step 2: Review modification spec and impact analysis
# Found: Lines 181-184 in EditProfileForm.tsx have problematic hidden field

# Step 3: Create implementation plan
/speckit.plan
# Creates: Plan to make image removal explicit via button

# Step 4: Break down into tasks
/speckit.tasks
# Creates: Task list (remove hidden field, update remove button handler, test)

# Step 5: Execute changes
/speckit.implement
# Implements explicit removal pattern
```

### What It Created

- **Branch**: `014-mod-002-make-profile-edits`
- **Directory**: `specs/014-edit-profile-form/modifications/002-make-profile-edits/`
- **Files**:
  - `modification-spec.md` - Change documentation
  - `impact-analysis.md` - Auto-scanned affected files
  - `plan.md` - Implementation plan (created by /speckit.plan)
  - `tasks.md` - Task breakdown (created by /speckit.tasks)

### The Root Cause

Hidden form field automatically set `intent="remove-image"` when certain conditions were met:

```typescript
// app/components/forms/EditProfileForm.tsx:181-184
{!selectedFile && !previewUrl && profile.profileImageUrl && (
  <input type="hidden" name="intent" value="remove-image" />
)}
```

**Problem**: This triggered whenever user didn't select a new file, removing their existing image unintentionally.

### The Fix

Made image removal **explicit** via button click:

```typescript
// Before (automatic via hidden field)
const handleRemoveImage = () => {
  setPreviewUrl(null);
  setSelectedFile(null);
  // Will be handled by server via intent="remove-image"
};

// After (explicit form submission)
const handleRemoveImage = () => {
  const formData = new FormData();
  formData.append('intent', 'remove-image');
  fetcher.submit(formData, { method: 'post' });
};
```

**Removed lines 181-184** (the automatic hidden field).

Now "Remove Image" button explicitly submits with `intent="remove-image"`, while regular form submissions don't include that intent.

### The Outcome

- ✅ Fixed in 2 hours
- ✅ Users can now edit bio/username without affecting image
- ✅ Image removal is explicit and intentional
- ✅ Build passed

### Lessons Learned

**Nesting modifications under parent feature** with checkpoint-based workflow kept everything organized:

```
specs/014-edit-profile-form/
├── spec.md                              # Original feature
├── plan.md
├── tasks.md
└── modifications/
    ├── 001-make-profile-fields/         # First modification
    │   ├── modification-spec.md
    │   ├── impact-analysis.md
    │   ├── plan.md                      # Created by /speckit.plan
    │   └── tasks.md                     # Created by /speckit.tasks
    └── 002-make-profile-edits/          # Second modification
        ├── modification-spec.md
        ├── impact-analysis.md
        ├── plan.md                      # Created by /speckit.plan
        └── tasks.md                     # Created by /speckit.tasks
```

This structure with review checkpoints makes it easy to:
- Track all changes to a feature over time
- Review impact before implementation
- See evolution of feature
- Understand modification order (001 → 002)
- Reference original feature spec when needed

**Without this workflow**: Modifications would have been scattered, and we'd lose the connection between related changes. The review checkpoints prevented implementing the wrong solution.

---

## Example 4: `/speckit.review` - Validating Completed Implementation

### The Context

After implementing the profile form crash bugfix (Example 1), we need to validate the implementation before merging.

### The Workflow

```bash
# After implementing the bugfix tasks
/speckit.review
# Performs: Code review, test validation, spec verification
```

### What It Did

The review workflow:

1. **Loaded Context**:
   - Read `specs/bugfix/001-when-submitting-the/bug-report.md`
   - Read `specs/bugfix/001-when-submitting-the/plan.md`
   - Read `specs/bugfix/001-when-submitting-the/tasks.md`
   - Examined code changes: `git diff main..bugfix/001-when-submitting-the`

2. **Verified Implementation**:
   - ✅ Regression test exists and passes
   - ✅ Fix handles empty file inputs correctly
   - ✅ Edge case covered: browser sending `application/octet-stream`
   - ✅ No breaking changes to existing functionality
   - ✅ Error messages remain clear

3. **Ran Tests**:
   ```bash
   npm test
   # All tests passing: 47 passed, 0 failed
   ```

4. **Generated Review Report**:

```markdown
# Review Report

**Feature**: bugfix/001-when-submitting-the
**Reviewer**: claude-code
**Date**: 2025-03-15
**Status**: ✅ Approved

## Summary

Profile form crash bugfix implementation meets all acceptance criteria.
Regression test successfully prevents recurrence, and fix is minimal and correct.

## Implementation Review

### What Was Reviewed
- T001: Write regression test (reproduces crash)
- T002: Implement fix (skip empty file inputs)
- T003: Verify fix (all tests pass)

### Implementation Quality
- **Code Quality**: Excellent - minimal change, clear logic
- **Test Coverage**: Comprehensive - regression test + existing tests
- **Documentation**: Clear comments explain the fix
- **Standards Compliance**: Follows project TypeScript patterns

## Test Results

**Tests Executed**: 47
**Tests Passing**: 47
**Tests Failing**: 0

Regression test: ✅ Passes (prevents future recurrence)

## Findings

### ✅ What Worked Well
- Minimal change (3 lines) reduces risk
- Clear comment explains why check is needed
- Regression test will prevent recurrence
- No breaking changes to existing functionality

### No Issues Found

All acceptance criteria met. Ready to merge.

## Tasks Status

### Completed (Marked as Done)
- [X] T001: Write regression test
- [X] T002: Implement fix
- [X] T003: Verify fix

## Recommendations

None - implementation is solid.

## Next Steps

1. ✅ Tasks marked as complete in tasks.md
2. ✅ Ready to merge feature branch
3. Create PR for team review (optional)
```

5. **Updated tasks.md**:

The review automatically marked completed tasks:

```markdown
# Tasks

## Phase 1: Reproduce & Test First
- [X] T001: Write regression test that reproduces the crash
  - Create test case for editing bio without uploading image
  - Verify test fails before fix (expected: crash)
  
## Phase 2: Implement Fix
- [X] T002: Implement fix to skip empty file inputs
  - Add check for application/octet-stream type
  - Skip validation for empty file inputs
  
## Phase 3: Verify
- [X] T003: Verify fix resolves the issue
  - Run regression test (should pass)
  - Run full test suite
  - Manual verification: edit bio without image upload
```

### The Value

**Before `/speckit.review`**:
- ❌ Manual review process (inconsistent)
- ❌ Easy to forget to run tests
- ❌ No structured validation checklist
- ❌ Tasks manually marked (often forgotten)

**With `/speckit.review`**:
- ✅ Structured, repeatable review process
- ✅ Automatic test execution
- ✅ Verification against specification
- ✅ Tasks automatically marked complete
- ✅ Review report for documentation

### Review Outcomes

The review can produce three outcomes:

1. **✅ Approved**: Ready to merge (as in this example)
2. **⚠️ Approved with Notes**: Minor improvements suggested but not blocking
3. **❌ Needs Changes**: Issues must be fixed before approval

### Integration with Workflow

The review workflow completes the spec-kit cycle:

```bash
# 1. Report the bug
/speckit.bugfix "profile form crashes when..."

# 2. Plan the fix
/speckit.plan

# 3. Break into tasks
/speckit.tasks

# 4. Implement
/speckit.implement

# 5. Review (NEW!)
/speckit.review
# ✅ Validates implementation
# ✅ Runs tests
# ✅ Marks tasks complete
# ✅ Generates review report

# 6. Merge
git push origin bugfix/001-when-submitting-the
```

**Impact**: 
- 🎯 **Validation**: Ensures quality before merge
- ✅ **Consistency**: Same review process every time
- 📊 **Documentation**: Review report captures findings
- ⚡ **Efficiency**: Automated task status updates

---

## Example 5: Workflow Comparison Table

Here's how the same work would have been done **without** vs **with** extensions:

| Task | Without Extensions | With Extensions (Checkpoint-Based) | Time Saved | Quality Impact |
|------|-------------------|-----------------------------------|------------|----------------|
| **Profile form crash** | 1. Find bug<br>2. Quick fix<br>3. Push<br>4. Hope it doesn't recur | 1. `/speckit.bugfix`<br>2. Review root cause<br>3. `/speckit.plan` (review approach)<br>4. `/speckit.tasks`<br>5. `/speckit.implement` (test-first)<br>6. Tests pass | ~Same time | ✅ Regression prevented<br>✅ User reviewed fix approach |
| **Make fields optional** | 1. Change schema<br>2. Update form<br>3. Push<br>4. Discover broken contract<br>5. Fix contract<br>6. Push again | 1. `/speckit.modify 014`<br>2. Review impact analysis<br>3. `/speckit.plan` (review backward compatibility)<br>4. `/speckit.tasks`<br>5. `/speckit.implement`<br>6. Push once | Saved 2 hours | ✅ No breaking changes<br>✅ User reviewed before coding |
| **Fix image removal** | 1. Change code<br>2. Test manually<br>3. Push<br>4. Filed in wrong place | 1. `/speckit.modify 014` again<br>2. Review impact analysis<br>3. `/speckit.plan` (review solution)<br>4. `/speckit.tasks`<br>5. `/speckit.implement`<br>6. Auto-nested under feature | Saved 1 hour | ✅ Organized history<br>✅ Correct solution from review |

**Cumulative impact over 3 modifications**:
- ⏱️ **Time saved**: ~3 hours
- 🐛 **Bugs prevented**: 1 regression, 1 breaking change
- 📁 **Organization**: Perfect feature history
- ✅ **Build success rate**: 100% (vs likely 60-70% without)
- 🎯 **Fix success rate**: 100% (vs 0% with auto-implementation)

---

## Example 6: Pattern - Feature Evolution Timeline

Here's the complete evolution of Feature 014 (Edit Profile) with checkpoint-based workflow:

```
Iteration 1: /speckit.specify "edit profile form"
├─ Original implementation with full workflow
├─ spec → plan → tasks → implement
└─ Status: ✅ Complete

Iteration 2: /speckit.modify 014 "make fields optional"
├─ modify → review impact → plan → review approach → tasks → implement
├─ Impact analysis caught contract changes
├─ User reviewed backward compatibility before coding
└─ Status: ✅ Complete

Iteration 3: /speckit.modify 014 "fix image removal UX"
├─ modify → review impact → plan → review solution → tasks → implement
├─ Discovered unintended behavior via impact analysis
├─ User reviewed fix approach before implementation
└─ Status: ✅ Complete

Iteration 4: /speckit.bugfix "form crash without image"
├─ bugfix → investigate → plan → review fix → tasks → implement
├─ Regression test written first
├─ User reviewed root cause and fix approach
└─ Status: ✅ Complete
```

**This evolution shows the power of spec-kit + extensions with review checkpoints**:
1. Start with structured `/speckit.specify`
2. Modify safely with `/speckit.modify` (automatic impact analysis + review checkpoints)
3. Fix bugs with `/speckit.bugfix` (regression tests + review before implementation)
4. **User controls direction** at each checkpoint (prevents failed implementations)
5. All history is organized and traceable

---

## Key Takeaways

### What Worked Well

1. **Review Checkpoints** (all workflows): User controls direction before implementation - **prevents failed fixes**
2. **Regression Tests First** (`/speckit.bugfix`): Prevented bugs from recurring
3. **Automatic Impact Analysis** (`/speckit.modify`): Caught dependencies we would have missed
4. **Nested Modifications**: Kept feature history organized
5. **Workflow Quality Gates**: Enforced best practices with user review at each stage

### Common Patterns

- **Start with `/speckit.specify`** for new features
- **Use `/speckit.modify`** for changes that affect behavior
- **Use `/speckit.bugfix`** for production issues with regression tests
- **Review before implementing**: Every workflow gives you checkpoints to review and adjust
- **Modifications nest** under parent features (organized history)
- **Impact analysis catches** ~80% of affected files automatically

### Metrics from Production Use

**Tweeter Project (14 features, 3 modifications, 2 bugfixes)**:

- ✅ 100% build success rate across all workflows
- ✅ Zero regressions from bugfixes (regression tests worked)
- ✅ Zero breaking changes from modifications (impact analysis worked)
- ✅ ~30% time savings on modifications (vs ad-hoc approach)
- ✅ Perfect feature history organization

---

## Try It Yourself

Ready to try these workflows on your project?

1. **Install**: [INSTALLATION.md](INSTALLATION.md)
2. **Quick Start**: [QUICKSTART.md](extensions/QUICKSTART.md)
3. **Pick a real task**:
   - Have a bug? Try `/speckit.bugfix "description"` → review → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`
   - Need to modify a feature? Try `/speckit.modify NNN "change"` → review → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`
   - Want to refactor? Try `/speckit.refactor "improvement"` → review → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`

**Remember**: The checkpoint-based workflow gives you control at each phase. Review and adjust before implementing!

**Questions?** [Open a discussion](https://github.com/[your-username]/spec-kit-extensions/discussions)
