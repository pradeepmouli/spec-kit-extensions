# IMMEDIATE ACTION REQUIRED

## Current Status

✅ Local tag `cli-v1.5.2` has been created at the correct commit (`3eea581`)
❌ Remote tag `cli-v1.5.2` still points to incorrect commit (`259a288`)

## TL;DR - Run these commands:

```bash
# Delete remote tag
git push --delete origin cli-v1.5.2

# Push corrected local tag
git push origin cli-v1.5.2
```

Or run the full automated script:

```bash
./fix-tag-cli-v1.5.2.sh
```

## Why?

The `cli-v1.5.2` tag currently points to commit `259a288` which doesn't have the CHANGELOG updated.

The release workflow at https://github.com/pradeepmouli/spec-kit-extensions/actions/runs/20509560063 failed because of this.

The correct commit is `3eea581` (on main branch) which has CHANGELOG, pyproject.toml, and specify_extend.py all at version 1.5.2.

## What happens after running this?

The GitHub Actions release workflow will automatically:
1. Build the package
2. Create a GitHub release
3. Publish to PyPI

See: `.github/workflows/release.yml`

---

For full details, see: `FIX-TAG-INSTRUCTIONS.md`
