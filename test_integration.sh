#!/bin/bash
# Integration test for specify-extend downloading latest template tag

set -e

echo "🧪 Integration Test: Verifying template download"
echo ""

# Create a temporary test directory
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"

echo "📁 Test directory: $TEST_DIR"
echo ""

# Initialize a git repo (required for specify-extend)
git init -q
git config user.email "test@example.com"
git config user.name "Test User"

# Create minimal .specify directory structure
mkdir -p .specify/memory
echo "# Test Constitution" > .specify/memory/constitution.md

# Run specify-extend to download and install
echo "⬇️  Running specify-extend to download latest templates..."
echo ""

cd /Users/pmouli/GitHub.nosync/spec-kit-extensions
uv run specify-extend --agent manual --dry-run bugfix 2>&1 | tee /tmp/specify-extend-test.log

echo ""
echo "📝 Checking log for template version..."
echo ""

# Check if it downloaded the correct template version
if grep -q "templates-v2.4.1" /tmp/specify-extend-test.log; then
    echo "✅ SUCCESS: Downloaded templates-v2.4.1"
    exit 0
elif grep -q "templates-v" /tmp/specify-extend-test.log; then
    VERSION=$(grep -o "templates-v[0-9.]*" /tmp/specify-extend-test.log | head -1)
    echo "⚠️  WARNING: Downloaded $VERSION (expected templates-v2.4.1)"
    exit 1
else
    echo "❌ FAILED: No template version found in output"
    cat /tmp/specify-extend-test.log
    exit 1
fi

# Cleanup
cd /
rm -rf "$TEST_DIR"
