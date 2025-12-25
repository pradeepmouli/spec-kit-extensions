#!/usr/bin/env bash

set -e

# Source common functions from spec-kit
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we're in spec-kit repo (scripts/bash/common.sh) or extensions (need to go up to spec-kit)
if [ -f "$SCRIPT_DIR/common.sh" ]; then
    # Running from same directory (most common case)
    source "$SCRIPT_DIR/common.sh"
elif [ -f "$SCRIPT_DIR/../bash/common.sh" ]; then
    # Running from spec-kit integrated location: .specify/scripts/bash/
    source "$SCRIPT_DIR/../bash/common.sh"
elif [ -f "$SCRIPT_DIR/../../scripts/bash/common.sh" ]; then
    # Running from spec-kit repo root scripts
    source "$SCRIPT_DIR/../../scripts/bash/common.sh"
else
    # Fallback: try to find common.sh in parent directories
    COMMON_SH_FOUND=false
    SEARCH_DIR="$SCRIPT_DIR"
    for i in {1..5}; do
        if [ -f "$SEARCH_DIR/common.sh" ]; then
            source "$SEARCH_DIR/common.sh"
            COMMON_SH_FOUND=true
            break
        elif [ -f "$SEARCH_DIR/scripts/bash/common.sh" ]; then
            source "$SEARCH_DIR/scripts/bash/common.sh"
            COMMON_SH_FOUND=true
            break
        fi
        SEARCH_DIR="$(dirname "$SEARCH_DIR")"
    done

    if [ "$COMMON_SH_FOUND" = false ]; then
        echo "Error: Could not find common.sh. Please ensure spec-kit is properly installed." >&2
        exit 1
    fi
fi

# Verify generate_branch_name function is available
if ! declare -f generate_branch_name > /dev/null; then
    echo "Error: generate_branch_name function is not available in common.sh." >&2
    echo "Please ensure you have the latest version of spec-kit-extensions installed." >&2
    exit 1
fi

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] <enhancement_description>"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

ENHANCEMENT_DESCRIPTION="${ARGS[*]}"
if [ -z "$ENHANCEMENT_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] <enhancement_description>" >&2
    exit 1
fi

# Use spec-kit common functions
REPO_ROOT=$(get_repo_root)
HAS_GIT=$(has_git && echo "true" || echo "false")

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

# Find highest enhance number
HIGHEST=0
if [ -d "$SPECS_DIR/enhance" ]; then
    for dir in "$SPECS_DIR"/enhance/*/; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
ENHANCE_NUM=$(printf "%03d" "$NEXT")

# Create branch name from description using smart filtering
WORDS=$(generate_branch_name "$ENHANCEMENT_DESCRIPTION")
BRANCH_NAME="enhance/${ENHANCE_NUM}-${WORDS}"
ENHANCE_ID="enhance-${ENHANCE_NUM}"

# Create git branch if git available
if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[enhance] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

# Create enhancement directory under enhance/ subdirectory
ENHANCE_SUBDIR="$SPECS_DIR/enhance"
mkdir -p "$ENHANCE_SUBDIR"
ENHANCE_DIR="$ENHANCE_SUBDIR/${ENHANCE_NUM}-${WORDS}"
mkdir -p "$ENHANCE_DIR"

# Copy template
ENHANCE_TEMPLATE="$REPO_ROOT/.specify/extensions/workflows/enhance/enhancement-template.md"
ENHANCEMENT_FILE="$ENHANCE_DIR/enhancement.md"

if [ -f "$ENHANCE_TEMPLATE" ]; then
    cp "$ENHANCE_TEMPLATE" "$ENHANCEMENT_FILE"
else
    echo "# Enhancement" > "$ENHANCEMENT_FILE"
fi

# Create symlink from spec.md to enhancement.md
ln -sf "enhancement.md" "$ENHANCE_DIR/spec.md"

# Set environment variable for current session
export SPECIFY_ENHANCE="$ENHANCE_ID"

if $JSON_MODE; then
    printf '{"ENHANCE_ID":"%s","BRANCH_NAME":"%s","ENHANCEMENT_FILE":"%s","ENHANCE_NUM":"%s"}\n' \
        "$ENHANCE_ID" "$BRANCH_NAME" "$ENHANCEMENT_FILE" "$ENHANCE_NUM"
else
    echo "ENHANCE_ID: $ENHANCE_ID"
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "ENHANCEMENT_FILE: $ENHANCEMENT_FILE"
    echo "ENHANCE_NUM: $ENHANCE_NUM"
    echo "SPECIFY_ENHANCE environment variable set to: $ENHANCE_ID"
fi
