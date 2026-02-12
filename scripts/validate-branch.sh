#!/usr/bin/env bash
# validate-branch.sh
# Hook script to validate branch names match spec-kit-workflows extension patterns
# Called by spec-kit's hook system to validate branch names

set -euo pipefail

# Get current branch name
BRANCH_NAME="${1:-$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")}"

if [ -z "$BRANCH_NAME" ] || [ "$BRANCH_NAME" = "HEAD" ]; then
    echo "Warning: Could not determine current branch name" >&2
    exit 0  # Don't fail on detached HEAD or other edge cases
fi

# Standard feature branches (from spec-kit core)
# Pattern: NNN-description
if [[ "$BRANCH_NAME" =~ ^[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# Extension workflow patterns
# bugfix/NNN-description
if [[ "$BRANCH_NAME" =~ ^bugfix/[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# modify/NNN^MMM-description (modification of feature NNN, new number MMM)
if [[ "$BRANCH_NAME" =~ ^modify/[0-9]{3,}\^[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# refactor/NNN-description
if [[ "$BRANCH_NAME" =~ ^refactor/[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# hotfix/NNN-description
if [[ "$BRANCH_NAME" =~ ^hotfix/[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# deprecate/NNN-description
if [[ "$BRANCH_NAME" =~ ^deprecate/[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# cleanup/NNN-description
if [[ "$BRANCH_NAME" =~ ^cleanup/[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# baseline/NNN-description
if [[ "$BRANCH_NAME" =~ ^baseline/[0-9]{3,}-[a-z0-9-]+$ ]]; then
    exit 0
fi

# Allow main/master/develop branches
if [[ "$BRANCH_NAME" =~ ^(main|master|develop)$ ]]; then
    exit 0
fi

# Branch doesn't match any known patterns
echo "❌ Invalid branch name: $BRANCH_NAME" >&2
echo "" >&2
echo "Valid branch patterns:" >&2
echo "  - NNN-description (standard feature)" >&2
echo "  - bugfix/NNN-description" >&2
echo "  - modify/NNN^MMM-description" >&2
echo "  - refactor/NNN-description" >&2
echo "  - hotfix/NNN-description" >&2
echo "  - deprecate/NNN-description" >&2
echo "  - cleanup/NNN-description" >&2
echo "  - baseline/NNN-description" >&2
echo "" >&2
echo "Use /speckit.bugfix, /speckit.modify, etc. to create properly named branches" >&2
exit 1
