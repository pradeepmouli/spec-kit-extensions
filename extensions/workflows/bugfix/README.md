# Bugfix Workflow

## Overview

The bugfix workflow is designed for fixing defects in existing code. It enforces a **regression-test-first** approach to ensure bugs are properly captured and prevented from recurring.

## When to Use

Use `/bugfix` when:

- A specific behavior is broken or incorrect
- Users report unexpected behavior
- Tests reveal a failure in existing functionality
- Production monitoring detects an issue
- Edge cases cause crashes or errors

**Do NOT use `/bugfix` for**:
- Adding new features → use `/specify` instead
- Changing existing feature behavior intentionally → use `/modify` instead
- Code quality improvements without behavior change → use `/refactor` instead
- Emergency production issues → use `/hotfix` instead

## Process

### 1. Investigation Phase
- Reproduce the bug locally
- Document exact reproduction steps
- Capture error messages, stack traces, logs
- Identify root cause in code

### 2. Regression Test Phase (BEFORE FIX)
**CRITICAL**: Write failing test BEFORE applying fix
- Write test that reproduces the bug
- Verify test fails on current code
- Test should pass after fix is applied

### 3. Fix Implementation
- Make minimal changes to resolve issue
- Focus on root cause, not symptoms
- Update related tests if needed
- Verify test now passes

### 4. Verification
- All tests pass (old + new)
- Bug cannot be reproduced
- No regressions in related functionality
- Code review if appropriate

### 5. Prevention
- Document why bug occurred
- Identify if similar bugs exist elsewhere
- Consider adding additional test coverage
- Update documentation if needed

## Quality Gates

- ✅ Bug MUST be reproducible with documented steps
- ✅ Regression test MUST be written before fix is applied
- ✅ Root cause MUST be identified and documented
- ✅ Prevention strategy MUST be defined
- ✅ All tests MUST pass before marking complete

## Files Created

```
specs/
└── bugfix-001-description/
    ├── bug-report.md      # Bug documentation
    └── tasks.md           # 21 sequential tasks
```

## Command Usage

```bash
/bugfix "button click doesn't save form data"
```

This will:
1. Create branch `bugfix/001-button-click-doesnt`
2. Generate `bug-report.md` with template
3. Generate `tasks.md` with 21 tasks
4. Set `SPECIFY_BUGFIX` environment variable

## Example Bug Report

```markdown
# Bug Report: Button Click Doesn't Save Form Data

**Bug ID**: bugfix-001
**Severity**: High
**Status**: Investigating

## Current Behavior
When clicking the "Save" button on the profile form, the data is not persisted to the database.

## Expected Behavior
Clicking "Save" should persist all form fields to the database and show a success message.

## Steps to Reproduce
1. Navigate to /profile/edit
2. Change username field to "newusername"
3. Click "Save" button
4. Refresh page
5. Observe username has not changed

## Root Cause
The form submission handler is missing the `await` keyword before the database call, causing the function to return before the data is saved.

File: `app/routes/profile.edit.tsx:45`
```

## Task Breakdown

The workflow generates 21 tasks across 5 phases:

- **T001-T005**: Investigation (reproduce, document, identify)
- **T006-T009**: Regression Test (write BEFORE fix)
- **T010-T013**: Apply Fix
- **T014-T017**: Verification (test, document)
- **T018-T021**: Prevention (coverage, docs, patterns)

## Tips

### Fast Bug Triage

1. Can you reproduce it? If not, gather more info
2. Is it a regression? Check when it broke (git bisect)
3. What changed? Review recent commits/PRs
4. Who owns this code? Check git blame

### Writing Good Regression Tests

```typescript
// Good: Specific test that reproduces the bug
test('profile save button persists data to database', async () => {
  await fillForm({ username: 'newusername' })
  await clickSaveButton()
  await refreshPage()
  const username = await getUsername()
  expect(username).toBe('newusername')
})

// Bad: Generic test that doesn't isolate the bug
test('profile form works', async () => {
  await testProfileForm()
})
```

### Common Pitfalls

- ❌ Applying fix before writing test → Won't catch regressions
- ❌ Treating symptoms instead of root cause → Bug will return
- ❌ Skipping documentation → Team won't learn from it
- ❌ Over-engineering the fix → Introduces new bugs

## Integration with Constitution

This workflow upholds:

- **Section III: Test-Driven Development** - Regression test before fix
- **Section VI: Workflow Selection** - Proper workflow for defect remediation
- **Quality Gates** - Bug reproduction and prevention required

## Related Workflows

- **Hotfix** - For emergency production bugs (expedited, test after fix)
- **Modify** - For intentional behavior changes
- **Refactor** - For improving code without changing behavior

## Metrics

Track these for continuous improvement:

- Time from bug report to fix
- Percentage of bugs caught by tests vs. production
- Recurrence rate (same bug appearing again)
- Number of bugs per feature

---

*Bugfix Workflow Documentation - Part of Specify Extension System*
