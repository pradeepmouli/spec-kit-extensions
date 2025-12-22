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
HAS_ERRORS=false

# Function to add an issue
add_issue() {
    local severity="$1"
    local message="$2"
    ISSUES+=("[$severity] $message")
    if [[ "$severity" == "ERROR" ]]; then
        HAS_ERRORS=true
    fi
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
    
    # Explicitly skip cleanup directory
    if [[ "$dirname" == "cleanup" ]]; then
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
    declare -A dup_check
    
    for dir in "$workflow_dir"/*/; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        
        # Extract number from directory name (001, 002, etc.)
        if [[ "$dirname" =~ ^([0-9]{3})- ]]; then
            number="${BASH_REMATCH[1]}"
            number_int=$((10#$number))
            
            # Check for duplicates before adding
            if [[ -n "${dup_check[$number_int]}" ]]; then
                add_issue "ERROR" "Duplicate number in $workflow_type/: $(printf "%03d" $number_int) (found in ${dup_check[$number_int]} and $dirname)"
            else
                numbers+=($number_int)
                dir_map[$number_int]="$dirname"
                dup_check[$number_int]="$dirname"
            fi
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
            # Don't auto-fix if there are ERROR-level issues (like duplicates)
            if $HAS_ERRORS; then
                add_action "Cannot auto-fix $workflow_type/: resolve ERROR-level issues first (e.g., duplicates)"
            else
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
                    shopt -s nullglob
                    move_error=false
                    for item in "$temp_dir"/*; do
                        if ! mv "$item" "$workflow_dir/"; then
                            move_error=true
                        fi
                    done
                    shopt -u nullglob
                    
                    if ! rmdir "$temp_dir"; then
                        echo "Error: Failed to remove temporary directory '$temp_dir'" >&2
                        move_error=true
                    fi
                    
                    if $move_error; then
                        echo "Error: One or more operations failed while renumbering '$workflow_type/' directories." >&2
                        exit 1
                    fi
                    
                    add_action "✓ Renumbered $workflow_type/ directories"
                fi
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
        # Properly escape JSON special characters (backslash first, then quotes)
        escaped_issue="${issue//\\/\\\\}"
        escaped_issue="${escaped_issue//\"/\\\"}"
        escaped_issue="${escaped_issue//$'\n'/\\n}"
        escaped_issue="${escaped_issue//$'\r'/\\r}"
        escaped_issue="${escaped_issue//$'\t'/\\t}"
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
        # Properly escape JSON special characters (backslash first, then quotes)
        escaped_action="${action//\\/\\\\}"
        escaped_action="${escaped_action//\"/\\\"}"
        escaped_action="${escaped_action//$'\n'/\\n}"
        escaped_action="${escaped_action//$'\r'/\\r}"
        escaped_action="${escaped_action//$'\t'/\\t}"
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
    
    printf '{"status":"%s","message":"%s","issues":%s,"actions":%s}\n' \
        "$status" "$message" "$issues_json" "$actions_json"
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
