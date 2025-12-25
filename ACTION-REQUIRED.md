# IMMEDIATE ACTION REQUIRED

## TL;DR - Run this command:

```bash
./fix-tag-cli-v1.5.2.sh
```

Or manually:

```bash
# Delete old tag
git tag -d cli-v1.5.2
git push --delete origin cli-v1.5.2

# Create new tag at correct commit
git tag -a cli-v1.5.2 3eea581 -m "Release CLI v1.5.2"

# Push new tag
git push origin cli-v1.5.2
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
