# RL Optimization: {{ANALYSIS_ID}}

**Optimization ID**: rl-opt-{{NUM}}
**Based On**: {{ANALYSIS_ID}}
**Date**: {{DATE}}

---

## Summary

**Changes**:
- Prompts: {{N}}
- Templates: {{N}}
- Scripts: {{N}}
- Docs: {{N}}

**Expected Impact**: Health score {{BEFORE}} → {{AFTER}}

---

## Pre-Flight Checklist

- [ ] Analysis reviewed
- [ ] Backups created
- [ ] Test environment ready

**Versions**: CLI {{VERSION}}, Templates {{VERSION}}

---

## 1. Prompt Changes

### P-001: {{TITLE}}

**File**: `commands/speckit.{{WORKFLOW}}.md`
**Line**: {{N}}

```diff
- [old line]
+ [new line]
```

**Test**: [How to verify]

---

## 2. Template Changes

### T-001: {{TITLE}}

**File**: `extensions/workflows/{{WORKFLOW}}/{{FILE}}.md`

**Change**: [Add/Remove/Modify section]

```markdown
[New/modified content]
```

---

## 3. Script Changes

### S-001: {{TITLE}}

**File**: `scripts/{{FILE}}.sh`

```bash
# Before
[old code]

# After
[new code]
```

---

## 4. Implementation Order

1. [ ] Shared utilities
2. [ ] Templates
3. [ ] Scripts
4. [ ] Commands
5. [ ] Documentation

---

## 5. Testing

### Regression Tests

- [ ] Baseline workflow
- [ ] Bugfix workflow
- [ ] All other workflows

### Validation

```bash
# Test commands
./scripts/create-{{WORKFLOW}}.sh --json "test"
```

---

## 6. Rollback

```bash
# If issues arise
git revert {{COMMIT}}
```

---

## 7. Release

### CHANGELOG Entry

```markdown
## [{{VERSION}}] - {{DATE}}

### Optimized (RL Intake)
- [Change] - from {{INTAKE_ID}}
```

### Commit Message

```
optimize({{WORKFLOW}}): improve based on rl-intake-{{NUM}}

- [Change 1]
- [Change 2]
```

---

## 8. Follow-up

- [ ] Schedule validation intake in 2-4 weeks
- [ ] Monitor for user feedback
- [ ] Update metrics dashboard

---

*Changes applied in version {{VERSION}}*
