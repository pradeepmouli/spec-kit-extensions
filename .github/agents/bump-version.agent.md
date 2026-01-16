---
description: Update CHANGELOG and bump version for CLI or extension templates release.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.bump-version` in the triggering message **is** the new version number. If the user does not provide a version number, assume it is a patch version over the last release. You always have it available in this conversation even if `$ARGUMENTS` appears literally below.

Given the version number (e.g., "1.4.2" for CLI or "2.3.1" for templates), do this:

## Step 1: Analyze Changes Since Last Release

1. Determine if this is a CLI release or Template release:
   - **CLI releases**: Version format X.Y.Z (e.g., 1.4.2) - changes in `specify_extend.py`, `pyproject.toml`, or core scripts
   - **Template releases**: Version format X.Y.Z (e.g., 2.3.1) - changes in `extensions/`, `commands/`, or workflow scripts

2. Get the last release tag for the component being released:
   ```bash
   # For CLI releases
   git tag -l 'cli-v*' --sort=-v:refname | head -1

   # For template releases
   git tag -l 'templates-v*' --sort=-v:refname | head -1
   ```

3. Review commits since the last release:
   ```bash
   git log <last-tag>..HEAD --oneline
   ```

4. Categorize changes using Keep a Changelog categories:
   - **🚀 Added**: New features or capabilities
   - **🔧 Changed/Improved**: Changes in existing functionality
   - **🐛 Fixed**: Bug fixes
   - **🗑️ Deprecated**: Soon-to-be removed features
   - **❌ Removed**: Removed features
   - **🔒 Security**: Security fixes

## Step 2: Update CHANGELOG.md

1. Read the current CHANGELOG.md to understand the format and find the correct insertion point.

2. For **CLI releases**:
   - Add new section under `## CLI Tool (\`specify-extend\`)` heading
   - Format:
     ```markdown
     ### [X.Y.Z] - YYYY-MM-DD

     #### [Category]

     - Change description
     - Change description

     #### 📦 Components

     - **CLI Tool Version**: vX.Y.Z
     - **Compatible Spec Kit Version**: v0.0.80+
     - **Extension Templates Version**: v2.3.0

     ---
     ```
   - Update the version in the top note: `- **CLI Tool** (\`specify-extend\`) - Currently at vX.Y.Z`

3. For **Template releases**:
   - Add new section under `## Extension Templates` heading
   - Format:
     ```markdown
     ### [X.Y.Z] - YYYY-MM-DD

     #### [Category]

     - Change description with affected files/workflows

     #### 📦 Components

     - **Extension Templates Version**: vX.Y.Z
     - **Compatible Spec Kit Version**: v0.0.80+

     ---
     ```
   - Update the version in the top note: `- **Extension Templates** (workflows, commands, scripts) - Currently at vX.Y.Z`

4. Provide a summary of changes added to CHANGELOG for user review.

## Step 3: Execute Version Bump and Tag Creation

After CHANGELOG is updated and user confirms:

### If CLI version has changed:

1. Update version files manually (bump-version.sh is interactive):
   ```bash
   # Update pyproject.toml
   sed -i.bak 's/^version = ".*"/version = "<version>"/' pyproject.toml && rm pyproject.toml.bak

   # Update specify_extend.py
   sed -i.bak 's/^__version__ = ".*"/__version__ = "<version>"/' specify_extend.py && rm specify_extend.py.bak
   ```

2. Commit CHANGELOG and version changes together:
   ```bash
   git add CHANGELOG.md pyproject.toml specify_extend.py
   git commit -m "Bump CLI version to <version>

   - Update version in pyproject.toml and specify_extend.py
   - Update CHANGELOG.md with release notes"
   ```

3. Create git tag:
   ```bash
   git tag -a cli-v<version> -m "Release CLI v<version>

   [Summary of key changes from CHANGELOG]"
   ```

4. Push changes and tag to remote:
   ```bash
   git push origin main --tags
   ```

5. **Monitor the release workflow:**
   ```bash
   # Get the latest workflow run for the release
   gh run list --workflow=release.yml --limit 1

   # Watch the workflow run in real-time
   gh run watch
   ```

   Or open in browser:
   ```
   https://github.com/pradeepmouli/spec-kit-extensions/actions/workflows/release.yml
   ```

   **Expected workflow steps:**
   - ✅ Version validation (pyproject.toml, specify_extend.py, CHANGELOG.md match)
   - ✅ Build Python package
   - ✅ Create GitHub release with notes
   - ✅ Publish to PyPI

   **If workflow fails:**
   - Check the failed step in GitHub Actions
   - Common issues:
     - Version mismatch → Verify CHANGELOG.md has correct version
     - Build failure → Check pyproject.toml dependencies
     - PyPI publish failure → Verify API token is configured
   - Fix the issue, delete the tag, and recreate:
     ```bash
     git tag -d cli-v<version>
     git push --delete origin cli-v<version>
     # Fix the issue, commit, then recreate tag
     git tag -a cli-v<version> -m "..."
     git push origin cli-v<version>
     ```

### If Template version has changed:

1. Commit CHANGELOG changes:
   ```bash
   git add CHANGELOG.md
   git commit -m "Update CHANGELOG for templates v<version>

   [Summary of key changes]"
   ```

2. Create git tag:
   ```bash
   git tag -a templates-v<version> -m "Release Extension Templates v<version>

   [Summary of key changes from CHANGELOG]"
   ```

3. Push changes and tag to remote:
   ```bash
   git push origin main --tags
   ```

4. **Monitor the release creation:**
   ```bash
   # Check that GitHub created the release
   gh release view templates-v<version>
   ```

   Or verify in browser:
   ```
   https://github.com/pradeepmouli/spec-kit-extensions/releases/tag/templates-v<version>
   ```

   **Expected outcome:**
   - ✅ Release appears on GitHub Releases page
   - ✅ Release notes from tag message are displayed
   - ✅ Source code archives are available

   **If release not created:**
   - Verify tag was pushed: `git ls-remote --tags origin | grep templates-v<version>`
   - Check tag annotation: `git show templates-v<version>`
   - Manually create release if needed via GitHub UI

## Quality Gates

- ✅ CHANGELOG.md is updated BEFORE creating tags
- ✅ CHANGELOG.md is committed WITH version file changes (for CLI) or separately (for templates)
- ✅ All changes since last release are documented in CHANGELOG
- ✅ Change categories are appropriate (Added/Changed/Fixed/etc.)
- ✅ Version numbers follow semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Component versions are updated consistently
- ✅ Git tag prefix matches release type (cli-v or templates-v)
- ✅ User reviews CHANGELOG before executing commands
- ✅ CHANGELOG commit is included before the tag is created
- ✅ **Release workflow completes successfully (CLI releases only)**
- ✅ **GitHub release is created and visible (all releases)**

## Post-Release Verification

After pushing tags, always verify:

### For CLI Releases

1. **Workflow Status**
   ```bash
   gh run list --workflow=release.yml --limit 1 --json conclusion,status,name
   ```
   Expected: `"conclusion": "success"`

2. **PyPI Package**
   ```bash
   pip index versions specify-extend | grep <version>
   ```
   Or visit: https://pypi.org/project/specify-extend/<version>/

3. **GitHub Release**
   ```bash
   gh release view cli-v<version>
   ```
   Or visit: https://github.com/pradeepmouli/spec-kit-extensions/releases/tag/cli-v<version>

### For Template Releases

1. **GitHub Release**
   ```bash
   gh release view templates-v<version>
   ```
   Or visit: https://github.com/pradeepmouli/spec-kit-extensions/releases/tag/templates-v<version>

2. **Verify Download URL**
   ```bash
   curl -I https://github.com/pradeepmouli/spec-kit-extensions/archive/refs/tags/templates-v<version>.zip
   ```
   Expected: HTTP 200 or 302

### If Verification Fails

1. **Check workflow logs** (CLI only):
   ```bash
   gh run view --log
   ```

2. **Verify versions match**:
   ```bash
   git show cli-v<version>:pyproject.toml | grep '^version'
   git show cli-v<version>:specify_extend.py | grep '^__version__'
   git show cli-v<version>:CHANGELOG.md | sed -n '/## CLI Tool/,/^## /p' | grep '^### \['
   ```

3. **If needed, delete and recreate tag** (see troubleshooting steps above)

## Notes

- For template releases, you'll need to manually update the version in relevant template files if they reference version numbers
- Always review `git log` output to ensure no changes are missed
- Breaking changes should increment MAJOR version
- New features increment MINOR version
- Bug fixes increment PATCH version
