#!/usr/bin/env bash
# migrate-to-native.sh
# Migrates existing spec-kit-extensions installations to native format
# Run this script from any repository that has spec-kit-extensions installed via specify-extend

set -euo pipefail

echo "🔄 Migrating spec-kit-extensions to native format..."
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository" >&2
    exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Check if spec-kit is installed
if [ ! -d ".specify" ]; then
    echo "❌ Error: spec-kit not found (.specify directory missing)" >&2
    exit 1
fi

# Check if old extension format exists
OLD_EXTENSION_DIR=".specify/extensions/workflows"
if [ ! -d "$OLD_EXTENSION_DIR" ]; then
    echo "ℹ️  No legacy installation found. Nothing to migrate."
    exit 0
fi

echo "📋 Found legacy installation at $OLD_EXTENSION_DIR"
echo ""

# Backup the old installation
BACKUP_DIR=".specify/extensions-backup-$(date +%Y%m%d-%H%M%S)"
echo "📦 Creating backup at $BACKUP_DIR..."
cp -r .specify/extensions "$BACKUP_DIR"

# Remove old patched common.sh if it exists
if [ -f ".specify/scripts/bash/common.sh.backup" ]; then
    echo "🔧 Removing common.sh patches..."
    if [ -f ".specify/scripts/bash/common.sh" ]; then
        # Restore original if backup exists
        mv .specify/scripts/bash/common.sh.backup .specify/scripts/bash/common.sh
    fi
fi

# Remove old extension files
echo "🗑️  Removing old extension format..."
rm -rf "$OLD_EXTENSION_DIR"

# Remove enabled.conf if it exists
if [ -f ".specify/extensions/enabled.conf" ]; then
    rm -f .specify/extensions/enabled.conf
fi

echo ""
echo "✅ Migration complete!"
echo ""
echo "📋 Next steps:"
echo "1. Install the native extension:"
echo "   specify extension add spec-kit-workflows"
echo ""
echo "   Or from GitHub:"
echo "   specify extension add --from https://github.com/pradeepmouli/spec-kit-extensions/releases/latest"
echo ""
echo "2. Verify installation:"
echo "   specify extension list"
echo ""
echo "3. Your backup is at: $BACKUP_DIR"
echo "   You can safely delete it after verifying the new installation works."
echo ""
