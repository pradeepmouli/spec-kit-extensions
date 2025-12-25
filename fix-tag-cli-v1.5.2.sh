#!/bin/bash
# Script to delete and recreate the cli-v1.5.2 tag
# This fixes the issue where the tag was created before the CHANGELOG was updated

set -e

echo "Fixing cli-v1.5.2 tag..."
echo ""

# Get the commit that should be tagged
TARGET_COMMIT="3eea581ddf9131d50842d3c485980cb29dff0445"

echo "Step 1: Verify that commit $TARGET_COMMIT has correct versions"
TOML_VERSION=$(git show $TARGET_COMMIT:pyproject.toml | grep '^version = ' | sed 's/version = "\(.*\)"/\1/')
PY_VERSION=$(git show $TARGET_COMMIT:specify_extend.py | grep '^__version__ = ' | sed 's/__version__ = "\(.*\)"/\1/')
CHANGELOG_VERSION=$(git show $TARGET_COMMIT:CHANGELOG.md | sed -n '/## CLI Tool/,/^## /p' | grep '^### \[' | head -1 | sed 's/### \[\(.*\)\].*/\1/')

echo "  pyproject.toml version:    $TOML_VERSION"
echo "  specify_extend.py version: $PY_VERSION"
echo "  CHANGELOG.md version:      $CHANGELOG_VERSION"

if [ "$TOML_VERSION" != "1.5.2" ] || [ "$PY_VERSION" != "1.5.2" ] || [ "$CHANGELOG_VERSION" != "1.5.2" ]; then
    echo "❌ Error: Version mismatch detected!"
    exit 1
fi

echo "✅ All versions are correct at commit $TARGET_COMMIT"
echo ""

echo "Step 2: Delete existing cli-v1.5.2 tag locally and remotely"
git tag -d cli-v1.5.2 2>/dev/null || echo "  Local tag doesn't exist (already deleted)"
git push --delete origin cli-v1.5.2 || echo "  Remote tag deletion failed (may require force or manual deletion)"
echo ""

echo "Step 3: Create new cli-v1.5.2 tag at commit $TARGET_COMMIT"
git tag -a cli-v1.5.2 $TARGET_COMMIT -m "Release CLI v1.5.2

🐛 Fixed:
- Template Download - Fixed template download to use templates-v* tags
- Changed from fetching /releases/latest to /tags endpoint
- Filters for tags starting with templates-v prefix
- Downloads latest template release (templates-v2.5.1)
- Displays template version in UI during download

🧪 Testing:
- Added Unit Tests - Created comprehensive test suite for download functionality
- Tests template tag filtering and selection
- Mocks GitHub API responses
- Verifies correct tag is downloaded

📦 Components:
- CLI Tool Version: v1.5.2
- Compatible Spec Kit Version: v0.0.80+
- Extension Templates Version: v2.5.1"

echo "✅ Tag created successfully"
echo ""

echo "Step 4: Push the new tag to trigger release workflow"
git push origin cli-v1.5.2

echo ""
echo "✅ Done! The release workflow should now run successfully."
echo "   Monitor the workflow at: https://github.com/pradeepmouli/spec-kit-extensions/actions/workflows/release.yml"
