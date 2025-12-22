#!/usr/bin/env bash

set -e

# Cleanup workflow - validates and reorganizes spec-kit artifacts
# IMPORTANT: This script only moves/renames documentation in specs/, never code files

JSON_MODE=false
DRY_RUN=false
AUTO_FIX=false
ARGS=()

for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --dry-run) DRY_RUN=true ;;
        --auto-fix) AUTO_FIX=true ;;
        --help|-h)
            echo "Usage: $0 [--json] [--dry-run] [--auto-fix] [reason]"
            echo ""
            echo "Validates spec-kit artifact structure and optionally fixes issues."
            echo ""
            echo "Options:"
            echo "  --json       Output in JSON format"
            echo "  --dry-run    Show what would be done without making changes"
            echo "  --auto-fix   Automatically fix numbering and organization issues"
            echo "  reason       Optional: reason for cleanup (for documentation)"
            echo ""
            echo "This script validates:"
            echo "  - Sequential numbering of specs (001, 002, 003, etc.)"
            echo "  - Correct directory structure under specs/"
            echo "  - Presence of required files (spec.md, etc.)"
            echo "  - No gaps or duplicate numbers"
            echo ""
            echo "IMPORTANT: Only moves/renames docs in specs/, never touches code files"
            exit 0
            ;;
        *) ARGS+=("$arg") ;;
    esac
done

CLEANUP_REASON="${ARGS[*]}"
if [ -z "$CLEANUP_REASON" ]; then
    CLEANUP_REASON="Validate and organize spec-kit artifacts"
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

# Check if specs directory exists
if [ ! -d "$SPECS_DIR" ]; then
    if $JSON_MODE; then
        echo '{"status":"success","message":"No specs directory found - nothing to clean up","issues":[]}'
    else
        echo "✓ No specs directory found - nothing to clean up"
    fi
    exit 0
fi

# Array to store issues found
declare -a ISSUES=()
declare -a ACTIONS=()

# Function to add an issue
add_issue() {
    local severity="$1"
    local message="$2"
    ISSUES+=("[$severity] $message")
}

# Function to add an action
add_action() {
    local action="$1"
    ACTIONS+=("$action")
}

# Validate workflow subdirectories
# Expected: bugfix/, modify/, refactor/, hotfix/, deprecate/
WORKFLOW_TYPES=("bugfix" "modify" "refactor" "hotfix" "deprecate")

# Collect all directories in specs/
declare -A WORKFLOW_DIRS
for workflow_type in "${WORKFLOW_TYPES[@]}"; do
    if [ -d "$SPECS_DIR/$workflow_type" ]; then
        WORKFLOW_DIRS[$workflow_type]=1
    fi
done

# Check for misplaced directories (numbered dirs directly under specs/)
for entry in "$SPECS_DIR"/*; do
    [ -d "$entry" ] || continue
    dirname=$(basename "$entry")
    
    # Skip known workflow subdirectories
    if [[ " ${WORKFLOW_TYPES[@]} " =~ " ${dirname} " ]]; then
        continue
    fi
    
    # Check if it's a numbered directory (001-*, 002-*, etc.)
    if [[ "$dirname" =~ ^[0-9]{3}- ]]; then
        add_issue "WARNING" "Numbered directory found directly under specs/: $dirname (should be under a workflow type)"
        # Try to determine workflow type from directory content or name
        # For now, suggest manual review
        add_action "Review and move $dirname to appropriate workflow subdirectory (bugfix/, modify/, etc.)"
    fi
done

# Validate each workflow subdirectory
for workflow_type in "${WORKFLOW_TYPES[@]}"; do
    workflow_dir="$SPECS_DIR/$workflow_type"
    [ -d "$workflow_dir" ] || continue
    
    # Collect all numbered directories
    declare -a numbers=()
    declare -A dir_map
    
    for dir in "$workflow_dir"/*/; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        
        # Extract number from directory name (001, 002, etc.)
        if [[ "$dirname" =~ ^([0-9]{3})- ]]; then
            number="${BASH_REMATCH[1]}"
            number_int=$((10#$number))
            numbers+=($number_int)
            dir_map[$number_int]="$dirname"
        else
            add_issue "ERROR" "Invalid directory name in $workflow_type/: $dirname (should start with 3-digit number)"
        fi
    done
    
    # Skip if no numbered directories
    [ ${#numbers[@]} -eq 0 ] && continue
    
    # Sort numbers
    IFS=$'\n' sorted_numbers=($(sort -n <<<"${numbers[*]}"))
    unset IFS
    
    # Check for duplicates
    for i in "${!sorted_numbers[@]}"; do
        if [ $i -gt 0 ] && [ "${sorted_numbers[$i]}" -eq "${sorted_numbers[$((i-1))]}" ]; then
            add_issue "ERROR" "Duplicate number in $workflow_type/: $(printf "%03d" ${sorted_numbers[$i]})"
        fi
    done
    
    # Check for gaps and suggest renumbering
    expected=1
    needs_renumber=false
    for num in "${sorted_numbers[@]}"; do
        if [ $num -ne $expected ]; then
            needs_renumber=true
            break
        fi
        expected=$((num + 1))
    done
    
    if $needs_renumber; then
        add_issue "INFO" "Non-sequential numbering in $workflow_type/ (gaps detected)"
        if $AUTO_FIX; then
            add_action "Renumber $workflow_type/ directories to be sequential"
            
            # Perform renumbering if not dry-run
            if ! $DRY_RUN; then
                # Create temp directory for safe renaming
                temp_dir=$(mktemp -d "$workflow_dir/.tmp.XXXXXX")
                
                # Move all numbered directories to temp with new numbers
                counter=1
                for num in "${sorted_numbers[@]}"; do
                    old_dir="$workflow_dir/${dir_map[$num]}"
                    new_num=$(printf "%03d" $counter)
                    
                    # Extract suffix (everything after the number and dash)
                    old_name="${dir_map[$num]}"
                    suffix="${old_name#*-}"
                    new_name="${new_num}-${suffix}"
                    
                    mv "$old_dir" "$temp_dir/$new_name"
                    counter=$((counter + 1))
                done
                
                # Move back from temp to workflow directory
                mv "$temp_dir"/* "$workflow_dir/"
                rmdir "$temp_dir"
                
                add_action "✓ Renumbered $workflow_type/ directories"
            fi
        else
            add_action "Run with --auto-fix to renumber $workflow_type/ directories sequentially"
        fi
    fi
    
    # Validate required files in each directory
    for num in "${sorted_numbers[@]}"; do
        dir_path="$workflow_dir/${dir_map[$num]}"
        
        # Check for spec.md or workflow-specific spec files
        has_spec=false
        case "$workflow_type" in
            bugfix)
                [ -f "$dir_path/bug-report.md" ] && has_spec=true
                ;;
            refactor)
                [ -f "$dir_path/refactor-spec.md" ] && has_spec=true
                ;;
            hotfix)
                [ -f "$dir_path/hotfix.md" ] && has_spec=true
                ;;
            deprecate)
                [ -f "$dir_path/deprecation-plan.md" ] && has_spec=true
                ;;
            modify)
                [ -f "$dir_path/modification-spec.md" ] && has_spec=true
                ;;
        esac
        
        # Also check for generic spec.md
        [ -f "$dir_path/spec.md" ] && has_spec=true
        
        if ! $has_spec; then
            add_issue "WARNING" "Missing spec file in ${dir_map[$num]}"
        fi
    done
done

# Generate report
CLEANUP_DIR="$SPECS_DIR/cleanup"
mkdir -p "$CLEANUP_DIR"

# Find highest cleanup number
HIGHEST=0
for dir in "$CLEANUP_DIR"/*/; do
    [ -d "$dir" ] || continue
    dirname=$(basename "$dir")
    number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
    number=$((10#$number))
    if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
done

NEXT=$((HIGHEST + 1))
CLEANUP_NUM=$(printf "%03d" "$NEXT")

# Create cleanup report directory
REPORT_DIR="$CLEANUP_DIR/${CLEANUP_NUM}-cleanup-report"
mkdir -p "$REPORT_DIR"

# Write report
REPORT_FILE="$REPORT_DIR/cleanup-report.md"
cat > "$REPORT_FILE" << EOF
# Cleanup Report

**Cleanup ID**: cleanup-${CLEANUP_NUM}
**Date**: $(date +%Y-%m-%d)
**Reason**: $CLEANUP_REASON

## Summary

Total issues found: ${#ISSUES[@]}
Actions taken/suggested: ${#ACTIONS[@]}

## Issues Found

EOF

if [ ${#ISSUES[@]} -eq 0 ]; then
    echo "✓ No issues found - spec structure is valid" >> "$REPORT_FILE"
else
    for issue in "${ISSUES[@]}"; do
        echo "- $issue" >> "$REPORT_FILE"
    done
fi

cat >> "$REPORT_FILE" << EOF

## Actions

EOF

if [ ${#ACTIONS[@]} -eq 0 ]; then
    echo "✓ No actions needed" >> "$REPORT_FILE"
else
    for action in "${ACTIONS[@]}"; do
        echo "- $action" >> "$REPORT_FILE"
    done
fi

cat >> "$REPORT_FILE" << EOF

## Validation Checks Performed

- ✓ Sequential numbering validation
- ✓ Directory structure validation
- ✓ Required files presence check
- ✓ Duplicate number detection
- ✓ Gap detection in numbering

**Note**: This cleanup script only validates and reorganizes documentation in the specs/ directory. Code files are never moved or modified.
EOF

# Output results
if $JSON_MODE; then
    # Build JSON array of issues
    issues_json="["
    first=true
    for issue in "${ISSUES[@]}"; do
        if $first; then
            first=false
        else
            issues_json+=","
        fi
        # Escape quotes in issue message
        escaped_issue="${issue//\"/\\\"}"
        issues_json+="\"$escaped_issue\""
    done
    issues_json+="]"
    
    # Build JSON array of actions
    actions_json="["
    first=true
    for action in "${ACTIONS[@]}"; do
        if $first; then
            first=false
        else
            actions_json+=","
        fi
        # Escape quotes in action message
        escaped_action="${action//\"/\\\"}"
        actions_json+="\"$escaped_action\""
    done
    actions_json+="]"
    
    if [ ${#ISSUES[@]} -eq 0 ]; then
        status="success"
        message="Spec structure is valid"
    else
        status="issues_found"
        message="Found ${#ISSUES[@]} issue(s)"
    fi
    
    printf '{"status":"%s","message":"%s","issues":%s,"actions":%s,"report_file":"%s","cleanup_num":"%s"}\n' \
        "$status" "$message" "$issues_json" "$actions_json" "$REPORT_FILE" "$CLEANUP_NUM"
else
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Spec-Kit Cleanup Report"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    
    if [ ${#ISSUES[@]} -eq 0 ]; then
        echo "✓ No issues found - spec structure is valid"
    else
        echo "Issues found: ${#ISSUES[@]}"
        echo ""
        for issue in "${ISSUES[@]}"; do
            echo "  $issue"
        done
    fi
    
    echo ""
    
    if [ ${#ACTIONS[@]} -gt 0 ]; then
        if $DRY_RUN; then
            echo "Actions suggested:"
        else
            echo "Actions taken:"
        fi
        echo ""
        for action in "${ACTIONS[@]}"; do
            echo "  $action"
        done
        echo ""
    fi
    
    echo "Report saved to: $REPORT_FILE"
    echo ""
    
    if $DRY_RUN; then
        echo "💡 This was a dry run. Run without --dry-run to apply changes."
    fi
    
    if [ ${#ISSUES[@]} -gt 0 ] && ! $AUTO_FIX; then
        echo "💡 Run with --auto-fix to automatically fix numbering issues."
    fi
fi

# Exit with appropriate code
if [ ${#ISSUES[@]} -eq 0 ]; then
    exit 0
else
    exit 1
fi
