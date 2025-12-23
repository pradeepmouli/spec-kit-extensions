#!/bin/bash
# bump-version.sh - Update CLI version, commit, and create tag
#
# Usage: ./scripts/bump-version.sh <version>
# Example: ./scripts/bump-version.sh 1.4.1

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if version argument is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 <version>"
    echo "Example: $0 1.4.1"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format (semantic versioning)
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    echo -e "${RED}Error: Invalid version format${NC}"
    echo "Version must be in format: MAJOR.MINOR.PATCH (e.g., 1.4.1)"
    echo "Optional pre-release: 1.4.1-alpha, 1.4.1-beta, 1.4.1-rc1"
    exit 1
fi

# Get repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo -e "${YELLOW}Updating version to $NEW_VERSION...${NC}"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}Error: You have uncommitted changes${NC}"
    echo "Please commit or stash your changes before bumping version"
    git status --short
    exit 1
fi

# Extract current versions
CURRENT_TOML=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
CURRENT_PY=$(grep '^__version__ = ' specify_extend.py | sed 's/__version__ = "\(.*\)"/\1/')

echo -e "Current pyproject.toml version: ${YELLOW}$CURRENT_TOML${NC}"
echo -e "Current specify_extend.py version: ${YELLOW}$CURRENT_PY${NC}"
echo -e "New version: ${GREEN}$NEW_VERSION${NC}"

# Check if version already exists in CHANGELOG
if grep -q "### \[$NEW_VERSION\]" CHANGELOG.md; then
    echo -e "${RED}Error: Version $NEW_VERSION already exists in CHANGELOG.md${NC}"
    exit 1
fi

# Confirm update
read -p "Proceed with version update? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Version update cancelled"
    exit 0
fi

# Prompt for changelog entry
echo -e "\n${YELLOW}Enter changelog entry (leave empty to skip CHANGELOG update):${NC}"
echo "Example: Fixed branch naming bug in create-bugfix.sh"
read -p "> " CHANGELOG_ENTRY

# Update pyproject.toml
echo -e "${YELLOW}Updating pyproject.toml...${NC}"
sed -i.bak "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml && rm pyproject.toml.bak

# Update specify_extend.py
echo -e "${YELLOW}Updating specify_extend.py...${NC}"
sed -i.bak "s/^__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" specify_extend.py && rm specify_extend.py.bak

# Update CHANGELOG.md if entry provided
if [ -n "$CHANGELOG_ENTRY" ]; then
    echo -e "${YELLOW}Updating CHANGELOG.md...${NC}"

    # Get current date
    CURRENT_DATE=$(date +%Y-%m-%d)

    # Create the new changelog entry
    NEW_ENTRY="### [$NEW_VERSION] - $CURRENT_DATE

#### 🔧 Changed

- $CHANGELOG_ENTRY

#### 📦 Components

- **CLI Tool Version**: v$NEW_VERSION
- **Compatible Spec Kit Version**: v0.0.80+

---

"

    # Find the line number after "## CLI Tool (\`specify-extend\`)"
    LINE_NUM=$(grep -n "^## CLI Tool" CHANGELOG.md | head -1 | cut -d: -f1)

    if [ -z "$LINE_NUM" ]; then
        echo -e "${RED}Error: Could not find '## CLI Tool' section in CHANGELOG.md${NC}"
        exit 1
    fi

    # Insert the new entry after the CLI Tool header and empty line
    INSERT_LINE=$((LINE_NUM + 2))

    # Use awk to insert the new entry
    awk -v line="$INSERT_LINE" -v text="$NEW_ENTRY" '
        NR == line {print text}
        {print}
    ' CHANGELOG.md > CHANGELOG.md.tmp && mv CHANGELOG.md.tmp CHANGELOG.md

    # Also update the current version note at the top
    sed -i.bak "s/- \*\*CLI Tool\*\* (\`specify-extend\`) - Currently at v.*/- **CLI Tool** (\`specify-extend\`) - Currently at v$NEW_VERSION/" CHANGELOG.md && rm CHANGELOG.md.bak

    echo -e "${GREEN}✅ CHANGELOG.md updated${NC}"
fi

# Show diff
echo -e "\n${YELLOW}Changes:${NC}"
git diff pyproject.toml specify_extend.py CHANGELOG.md

# Commit changes
echo -e "\n${YELLOW}Committing changes...${NC}"
git add pyproject.toml specify_extend.py
if [ -n "$CHANGELOG_ENTRY" ]; then
    git add CHANGELOG.md
fi
git commit -m "Bump version to $NEW_VERSION"

# Create tag
TAG_NAME="cli-v$NEW_VERSION"
echo -e "\n${YELLOW}Creating tag $TAG_NAME...${NC}"
git tag -a "$TAG_NAME" -m "Release CLI version $NEW_VERSION"

# Push to remote
read -p "Push to remote? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Pushing to origin...${NC}"
    git push origin main
    git push origin "$TAG_NAME"
    echo -e "\n${GREEN}✅ Version $NEW_VERSION released!${NC}"
    echo -e "Tag ${GREEN}$TAG_NAME${NC} pushed to origin"
    echo -e "GitHub Actions will create the release automatically"
else
    echo -e "\n${YELLOW}⚠️  Changes committed locally but not pushed${NC}"
    echo "To push later, run:"
    echo "  git push origin main && git push origin $TAG_NAME"
fi

echo -e "\n${GREEN}Done!${NC}"
