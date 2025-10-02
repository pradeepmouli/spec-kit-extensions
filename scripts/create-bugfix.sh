#!/usr/bin/env bash

set -e

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] <bug_description>"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

BUG_DESCRIPTION="${ARGS[*]}"
if [ -z "$BUG_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] <bug_description>" >&2
    exit 1
fi

# Function to find the repository root
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Resolve repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
        exit 1
    fi
    HAS_GIT=false
fi

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

# Find highest bugfix number
HIGHEST=0
if [ -d "$SPECS_DIR" ]; then
    for dir in "$SPECS_DIR"/bugfix-*; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | sed 's/bugfix-//' | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
BUG_NUM=$(printf "%03d" "$NEXT")

# Create branch name from description
BRANCH_SUFFIX=$(echo "$BUG_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
WORDS=$(echo "$BRANCH_SUFFIX" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
BRANCH_NAME="bugfix/${BUG_NUM}-${WORDS}"
BUG_ID="bugfix-${BUG_NUM}"

# Create git branch if git available
if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[bugfix] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

# Create bug directory
BUG_DIR="$SPECS_DIR/${BUG_ID}-${WORDS}"
mkdir -p "$BUG_DIR"

# Copy templates
BUGFIX_TEMPLATE="$REPO_ROOT/.specify/extensions/workflows/bugfix/bug-report-template.md"
TASKS_TEMPLATE="$REPO_ROOT/.specify/extensions/workflows/bugfix/tasks-template.md"
BUG_REPORT_FILE="$BUG_DIR/bug-report.md"
TASKS_FILE="$BUG_DIR/tasks.md"

if [ -f "$BUGFIX_TEMPLATE" ]; then
    cp "$BUGFIX_TEMPLATE" "$BUG_REPORT_FILE"
else
    echo "# Bug Report" > "$BUG_REPORT_FILE"
fi

if [ -f "$TASKS_TEMPLATE" ]; then
    cp "$TASKS_TEMPLATE" "$TASKS_FILE"
else
    echo "# Tasks" > "$TASKS_FILE"
fi

# Set environment variable for current session
export SPECIFY_BUGFIX="$BUG_ID"

if $JSON_MODE; then
    printf '{"BUG_ID":"%s","BRANCH_NAME":"%s","BUG_REPORT_FILE":"%s","TASKS_FILE":"%s","BUG_NUM":"%s"}\n' \
        "$BUG_ID" "$BRANCH_NAME" "$BUG_REPORT_FILE" "$TASKS_FILE" "$BUG_NUM"
else
    echo "BUG_ID: $BUG_ID"
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "BUG_REPORT_FILE: $BUG_REPORT_FILE"
    echo "TASKS_FILE: $TASKS_FILE"
    echo "BUG_NUM: $BUG_NUM"
    echo "SPECIFY_BUGFIX environment variable set to: $BUG_ID"
fi
