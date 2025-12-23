---
description: Update CHANGELOG and bump version for CLI or extension templates release.
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

The text the user typed after `/speckit.bump-version` in the triggering message **is** the new version number. Assume you always have it available in this conversation even if `$ARGUMENTS` appears literally below.

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

## Step 3: Execute Version Bump Script

After CHANGELOG is updated and user confirms:

### If CLI version has changed:

1. Run the version bump script:
   ```bash
   ./scripts/bump-version.sh <version>
   ```

2. The script will:
   - Update version in `pyproject.toml` and `specify_extend.py`
   - Show diff of changes
   - Prompt for confirmation
   - Commit changes with message "Bump version to X.Y.Z"
   - Create git tag (`cli-vX.Y.Z`)

3. Push changes and tag to remote:
   ```bash
   git push origin main --tags
   ```

### If Template version has changed:

1. Create git tag:
   ```bash
   git tag -a templates-v<version> -m "Release Extension Templates v<version>"
   ```
2. Push tag to remote:
   ```bash
   git push origin templates-v<version>
   ```

## Quality Gates

- ✅ All changes since last release are documented in CHANGELOG
- ✅ Change categories are appropriate (Added/Changed/Fixed/etc.)
- ✅ Version numbers follow semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Component versions are updated consistently
- ✅ Git tag prefix matches release type (cli-v or templates-v)
- ✅ User reviews CHANGELOG before executing bump script

## Notes

- For template releases, you'll need to manually update the version in relevant template files if they reference version numbers
- Always review `git log` output to ensure no changes are missed
- Breaking changes should increment MAJOR version
- New features increment MINOR version
- Bug fixes increment PATCH version
