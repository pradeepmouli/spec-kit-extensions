#!/usr/bin/env bash

set -e

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] <refactoring_description>"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

REFACTOR_DESCRIPTION="${ARGS[*]}"
if [ -z "$REFACTOR_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] <refactoring_description>" >&2
    exit 1
fi

# Find repository root
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root" >&2
        exit 1
    fi
    HAS_GIT=false
fi

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

# Find highest refactor number
HIGHEST=0
if [ -d "$SPECS_DIR/refactor" ]; then
    for dir in "$SPECS_DIR"/refactor/*/; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
REFACTOR_NUM=$(printf "%03d" "$NEXT")

# Create branch name from description using smart filtering
WORDS=$(generate_branch_name "$REFACTOR_DESCRIPTION")
BRANCH_NAME="refactor/${REFACTOR_NUM}-${WORDS}"
REFACTOR_ID="refactor-${REFACTOR_NUM}"

# Create git branch
if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[refactor] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

# Create refactor directory under refactor/ subdirectory
REFACTOR_SUBDIR="$SPECS_DIR/refactor"
mkdir -p "$REFACTOR_SUBDIR"
REFACTOR_DIR="$REFACTOR_SUBDIR/${REFACTOR_NUM}-${WORDS}"
mkdir -p "$REFACTOR_DIR"

# Copy template
REFACTOR_TEMPLATE="$REPO_ROOT/.specify/extensions/workflows/refactor/refactor-template.md"
REFACTOR_SPEC_FILE="$REFACTOR_DIR/refactor-spec.md"

if [ -f "$REFACTOR_TEMPLATE" ]; then
    cp "$REFACTOR_TEMPLATE" "$REFACTOR_SPEC_FILE"
else
    echo "# Refactor Spec" > "$REFACTOR_SPEC_FILE"
fi

# Create symlink from spec.md to refactor-spec.md
ln -sf "refactor-spec.md" "$REFACTOR_DIR/spec.md"

# Create placeholder for metrics
METRICS_BEFORE="$REFACTOR_DIR/metrics-before.md"
METRICS_AFTER="$REFACTOR_DIR/metrics-after.md"

cat > "$METRICS_BEFORE" << 'EOF'
# Baseline Metrics (Before Refactoring)

**Status**: Not yet captured

Run the following command to capture baseline metrics:

```bash
.specify/extensions/workflows/refactor/measure-metrics.sh --before --dir "$REFACTOR_DIR"
```

This should be done BEFORE making any code changes.
EOF

cat > "$METRICS_AFTER" << 'EOF'
# Post-Refactoring Metrics (After Refactoring)

**Status**: Not yet captured

Run the following command to capture post-refactoring metrics:

```bash
.specify/extensions/workflows/refactor/measure-metrics.sh --after --dir "$REFACTOR_DIR"
```

This should be done AFTER refactoring is complete and all tests pass.
EOF

# Create placeholder for behavioral snapshot
BEHAVIORAL_SNAPSHOT="$REFACTOR_DIR/behavioral-snapshot.md"
cat > "$BEHAVIORAL_SNAPSHOT" << 'EOF'
# Behavioral Snapshot

**Purpose**: Document observable behavior before refactoring to verify it's preserved after.

## Key Behaviors to Preserve

### Behavior 1: [Description]
**Input**: [Specific input data/conditions]
**Expected Output**: [Exact expected result]
**Actual Output** (before): [Run and document]
**Actual Output** (after): [Re-run after refactoring - must match]

### Behavior 2: [Description]
**Input**: [Specific input data/conditions]
**Expected Output**: [Exact expected result]
**Actual Output** (before): [Run and document]
**Actual Output** (after): [Re-run after refactoring - must match]

### Behavior 3: [Description]
**Input**: [Specific input data/conditions]
**Expected Output**: [Exact expected result]
**Actual Output** (before): [Run and document]
**Actual Output** (after): [Re-run after refactoring - must match]

## Test Commands
```bash
# Commands to reproduce behaviors
npm test -- [specific test]
npm run dev # Manual testing steps...
```

---
*Update this file with actual behaviors before starting refactoring*
EOF

# Set environment variable
export SPECIFY_REFACTOR="$REFACTOR_ID"

if $JSON_MODE; then
    printf '{"REFACTOR_ID":"%s","BRANCH_NAME":"%s","REFACTOR_SPEC_FILE":"%s","METRICS_BEFORE":"%s","METRICS_AFTER":"%s","BEHAVIORAL_SNAPSHOT":"%s","REFACTOR_NUM":"%s"}\n' \
        "$REFACTOR_ID" "$BRANCH_NAME" "$REFACTOR_SPEC_FILE" "$METRICS_BEFORE" "$METRICS_AFTER" "$BEHAVIORAL_SNAPSHOT" "$REFACTOR_NUM"
else
    echo "REFACTOR_ID: $REFACTOR_ID"
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "REFACTOR_SPEC_FILE: $REFACTOR_SPEC_FILE"
    echo "METRICS_BEFORE: $METRICS_BEFORE"
    echo "METRICS_AFTER: $METRICS_AFTER"
    echo "BEHAVIORAL_SNAPSHOT: $BEHAVIORAL_SNAPSHOT"
    echo "REFACTOR_NUM: $REFACTOR_NUM"
    echo "SPECIFY_REFACTOR environment variable set to: $REFACTOR_ID"
fi
