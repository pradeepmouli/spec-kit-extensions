#!/usr/bin/env bash

set -e

# Source common functions from spec-kit
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if we're in spec-kit repo (scripts/bash/common.sh) or extensions (need to go up to spec-kit)
if [ -f "$SCRIPT_DIR/../bash/common.sh" ]; then
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

# Use spec-kit common functions
REPO_ROOT=$(get_repo_root)
HAS_GIT=$(has_git && echo "true" || echo "false")

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

# Function to generate branch name with stop word filtering and length filtering
generate_branch_name() {
    local description="$1"
    
    # Common stop words to filter out
    local stop_words="^(i|a|an|the|to|for|of|in|on|at|by|with|from|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|should|could|can|may|might|must|shall|this|that|these|those|my|your|our|their|want|need|add|get|set)$"
    
    # Convert to lowercase and split into words
    local clean_name=$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/ /g')
    
    # Filter words: remove stop words and words shorter than 3 chars (unless they're uppercase acronyms in original)
    local meaningful_words=()
    for word in $clean_name; do
        # Skip empty words
        [ -z "$word" ] && continue
        
        # Keep words that are NOT stop words AND (length >= 3 OR are potential acronyms)
        if ! echo "$word" | grep -qiE "$stop_words"; then
            if [ ${#word} -ge 3 ]; then
                meaningful_words+=("$word")
            elif echo "$description" | grep -q "\b${word^^}\b"; then
                # Keep short words if they appear as uppercase in original (likely acronyms)
                meaningful_words+=("$word")
            fi
        fi
    done
    
    # If we have meaningful words, use first 3-4 of them
    if [ ${#meaningful_words[@]} -gt 0 ]; then
        local max_words=3
        if [ ${#meaningful_words[@]} -eq 4 ]; then max_words=4; fi
        
        local result=""
        local count=0
        for word in "${meaningful_words[@]}"; do
            if [ $count -ge $max_words ]; then break; fi
            if [ -n "$result" ]; then result="$result-"; fi
            result="$result$word"
            count=$((count + 1))
        done
        echo "$result"
    else
        # Fallback to original logic if no meaningful words found
        local cleaned=$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
        echo "$cleaned" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//'
    fi
}

# Find highest bugfix number
HIGHEST=0
if [ -d "$SPECS_DIR/bugfix" ]; then
    for dir in "$SPECS_DIR"/bugfix/*/; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
BUG_NUM=$(printf "%03d" "$NEXT")

# Create branch name from description using smart filtering
WORDS=$(generate_branch_name "$BUG_DESCRIPTION")
BRANCH_NAME="bugfix/${BUG_NUM}-${WORDS}"
BUG_ID="bugfix-${BUG_NUM}"

# Create git branch if git available
if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[bugfix] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

# Create bug directory under bugfix/ subdirectory
BUGFIX_SUBDIR="$SPECS_DIR/bugfix"
mkdir -p "$BUGFIX_SUBDIR"
BUG_DIR="$BUGFIX_SUBDIR/${BUG_NUM}-${WORDS}"
mkdir -p "$BUG_DIR"

# Copy template
BUGFIX_TEMPLATE="$REPO_ROOT/.specify/extensions/workflows/bugfix/bug-report-template.md"
BUG_REPORT_FILE="$BUG_DIR/bug-report.md"

if [ -f "$BUGFIX_TEMPLATE" ]; then
    cp "$BUGFIX_TEMPLATE" "$BUG_REPORT_FILE"
else
    echo "# Bug Report" > "$BUG_REPORT_FILE"
fi

# Create symlink from spec.md to bug-report.md
ln -sf "bug-report.md" "$BUG_DIR/spec.md"

# Set environment variable for current session
export SPECIFY_BUGFIX="$BUG_ID"

if $JSON_MODE; then
    printf '{"BUG_ID":"%s","BRANCH_NAME":"%s","BUG_REPORT_FILE":"%s","BUG_NUM":"%s"}\n' \
        "$BUG_ID" "$BRANCH_NAME" "$BUG_REPORT_FILE" "$BUG_NUM"
else
    echo "BUG_ID: $BUG_ID"
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "BUG_REPORT_FILE: $BUG_REPORT_FILE"
    echo "BUG_NUM: $BUG_NUM"
    echo "SPECIFY_BUGFIX environment variable set to: $BUG_ID"
fi
