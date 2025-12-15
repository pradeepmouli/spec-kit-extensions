# Architecture

This document explains how spec-kit-extensions work internally.

## Overview

spec-kit-extensions add 5 new workflows to spec-kit by:

1. **Detecting workflow type** from git branch names
2. **Loading appropriate templates** based on workflow
3. **Running workflow-specific scripts** to create proper structure
4. **Enforcing quality gates** via constitution

## System Components

### 1. Workflow Detection

**File**: `.specify/scripts/bash/common.sh`

Branch names encode workflow type:

```bash
detect_workflow_type() {
    local branch="$1"

    # Pattern matching on branch name
    if [[ "$branch" =~ ^[0-9]{3}-mod-[0-9]{3}- ]]; then
        echo "modify"
    elif [[ "$branch" =~ ^bugfix/ ]]; then
        echo "bugfix"
    elif [[ "$branch" =~ ^refactor/ ]]; then
        echo "refactor"
    elif [[ "$branch" =~ ^hotfix/ ]]; then
        echo "hotfix"
    elif [[ "$branch" =~ ^deprecate/ ]]; then
        echo "deprecate"
    else
        echo "feature"  # Default to core spec-kit
    fi
}
```

### 2. Branch Naming Conventions

Each workflow has unique branch pattern:

| Workflow | Pattern | Example |
|----------|---------|---------|
| Feature (core) | `NNN-description` | `014-edit-profile` |
| Bugfix | `bugfix/NNN-description` | `bugfix/001-form-crash` |
| Modification | `NNN-mod-MMM-description` | `014-mod-001-optional-fields` |
| Refactor | `refactor/NNN-description` | `refactor/001-extract-service` |
| Hotfix | `hotfix/NNN-description` | `hotfix/001-auth-bypass` |
| Deprecation | `deprecate/NNN-description` | `deprecate/001-old-editor` |

**Why this matters**: Branch name alone tells us workflow type, no config needed.

#### Branch Pattern Compatibility

spec-kit's `common.sh` enforces branch naming via `check_feature_branch()`, which originally only accepted the standard pattern `^[0-9]{3}-`. To support extension patterns, `specify-extend` automatically patches this function during installation:

**Original spec-kit pattern:**
- `001-feature-name` (standard feature branches)

**Patched to accept extension patterns:**
- `bugfix/001-description` (bugfix workflow)
- `modify/001^002-description` (modify workflow)
- `refactor/003-description` (refactor workflow)
- `hotfix/004-description` (hotfix workflow)
- `deprecate/005-description` (deprecate workflow)

The patch:
1. Creates `.specify/scripts/bash/common.sh.backup` before modification
2. Updates `check_feature_branch()` to validate both standard and extension patterns
3. Preserves non-git repository behavior
4. Provides helpful error messages listing all supported patterns
5. Gracefully handles already-patched files

This ensures extension workflows integrate seamlessly with spec-kit's branch validation system.

### 3. Directory Structure

Workflows create different directory patterns:

```bash
get_feature_paths() {
    local workflow_type=$(detect_workflow_type "$current_branch")

    case "$workflow_type" in
        modify)
            # Extract parent feature number (014-mod-001-desc -> 014)
            local parent_num=$(echo "$current_branch" | grep -o '^[0-9]\{3\}')
            # Find parent feature directory
            local parent_feature=$(find "$repo_root/specs" -maxdepth 1 -name "${parent_num}-*" -type d)
            # Extract modification part (014-mod-001-desc -> 001-desc)
            local mod_part=$(echo "$current_branch" | sed "s/^${parent_num}-mod-//")
            # Nest under parent
            feature_dir="$parent_feature/modifications/$mod_part"
            spec_file="$feature_dir/modification-spec.md"
            ;;

        bugfix)
            feature_dir="$repo_root/specs/bugfix-$branch_suffix"
            spec_file="$feature_dir/bug-report.md"
            ;;

        refactor)
            feature_dir="$repo_root/specs/refactor-$branch_suffix"
            spec_file="$feature_dir/refactor-spec.md"
            ;;

        # ... etc
    esac
}
```

### 4. Templates

Each workflow has templates in `.specify/extensions/workflows/{workflow}/`:

```
workflows/
├── bugfix/
│   ├── bug-report-template.md        # Bug analysis template
│   ├── tasks-template.md             # Bugfix-specific tasks
│   └── README.md                     # Workflow documentation
├── modify/
│   ├── modification-spec-template.md # Modification spec
│   ├── impact-analysis-template.md   # Auto-generated impact
│   ├── tasks-template.md            # Modification tasks
│   └── README.md
└── ... (other workflows)
```

Templates use placeholder syntax:

```markdown
# Bug Report: {{BUG_DESCRIPTION}}

**Reported**: {{DATE}}
**Branch**: {{BRANCH_NAME}}
**Status**: {{STATUS}}

## Problem Description

{{DESCRIPTION}}

## Environment
- **Affected Version**: {{VERSION}}
- **Steps to Reproduce**:
  1. {{STEP_1}}
  2. {{STEP_2}}
```

### 5. Creation Scripts

Bash scripts create workflow instances:

**File**: `.specify/scripts/bash/create-bugfix.sh`

```bash
#!/usr/bin/env bash

set -e

# 1. Validate inputs
if [ $# -lt 1 ]; then
    error "Usage: $0 \"bug description\""
fi

# 2. Generate branch name
BRANCH_NAME="bugfix/$(get_next_number)-$(slugify "$DESCRIPTION")"

# 3. Create and checkout branch
git checkout -b "$BRANCH_NAME"

# 4. Create directory structure
mkdir -p "specs/bugfix-$(get_next_number)-$(slugify "$DESCRIPTION")"

# 5. Copy templates
cp .specify/extensions/workflows/bugfix/bug-report-template.md \
   specs/bugfix-NNN/bug-report.md

# 6. Replace placeholders
sed -i "s/{{BUG_DESCRIPTION}}/$DESCRIPTION/g" specs/bugfix-NNN/bug-report.md

# 7. Generate tasks
generate_tasks "bugfix" > specs/bugfix-NNN/tasks.md

# 8. Output success
echo "✅ Created bugfix workflow: $BRANCH_NAME"
```

### 6. Impact Analysis (Modification Workflow)

**File**: `.specify/scripts/bash/scan-impact.sh`

Automatically scans codebase for files affected by modification:

```bash
scan_impact() {
    local parent_feature="$1"
    local feature_dir="specs/$parent_feature"

    # 1. Read original feature spec to identify key files
    local key_files=$(extract_files_from_spec "$feature_dir/spec.md")

    # 2. Scan for imports/references
    for file in $key_files; do
        find_references "$file"
    done

    # 3. Check contracts
    if [ -d "$feature_dir/contracts" ]; then
        scan_contract_usage "$feature_dir/contracts"
    fi

    # 4. Generate impact report
    generate_impact_report > impact-analysis.md
}
```

This auto-generated report identifies:
- Files that will need updates
- Files that reference the feature
- Contract changes required
- Backward compatibility concerns

### 7. Quality Gates (Constitution)

**File**: `.specify/memory/constitution.md`

Each workflow has defined quality gates:

```markdown
## Section VI: Workflow Selection and Quality Gates

### 2. Bug Fixes
**Workflow**: `/bugfix`
**Quality Gates**:
- [ ] Bug reproduced reliably
- [ ] **Regression test written BEFORE fix** (enforced)
- [ ] Test fails initially (proves it reproduces bug)
- [ ] Fix implemented
- [ ] Test passes after fix
- [ ] Prevention measures documented

**Exception**: None - test MUST come before fix
```

These gates are enforced by task templates and workflow scripts.

### 8. Integration with `/implement`

**File**: `.claude/commands/implement.md`

The `/implement` command detects workflow type and loads appropriate files:

```markdown
## Workflow Detection

You will receive JSON from check-prerequisites.sh containing WORKFLOW_TYPE.

**For modify workflow**:
- REQUIRED: Read modification-spec.md, impact-analysis.md, tasks.md
- IF EXISTS: Read parent feature's spec.md for context

**For bugfix workflow**:
- REQUIRED: Read bug-report.md, tasks.md
- Key: Regression test MUST be written before fix

## Execution Rules

**For modify workflow**:
1. Review impact analysis - identify all affected files
2. Update files in order listed in impact analysis
3. Run tests after each file change
4. Check for backward compatibility

**For bugfix workflow**:
1. Understand bug from bug-report.md
2. Write regression test FIRST (it should fail)
3. Implement fix
4. Verify test passes
5. Document prevention in bug-report.md
```

## Data Flow

### Example: `/bugfix` Workflow

```
User runs: /bugfix "form crashes without image"
    ↓
SlashCommand tool invokes: .claude/commands/bugfix.md
    ↓
Command calls: .specify/scripts/bash/create-bugfix.sh
    ↓
Script performs:
    1. Generates branch: bugfix/001-form-crashes
    2. Creates dir: specs/bugfix/001-form-crashes/
    3. Copies templates:
       - bug-report-template.md → bug-report.md
       - tasks-template.md → tasks.md
    4. Replaces placeholders:
       - {{BUG_DESCRIPTION}} → "form crashes without image"
       - {{DATE}} → "2025-10-02"
    5. Outputs success message
    ↓
User runs: /implement
    ↓
Command calls: .specify/scripts/bash/check-prerequisites.sh
    ↓
Script returns: {"WORKFLOW_TYPE": "bugfix", ...}
    ↓
/implement loads bugfix-specific files:
    - bug-report.md (understand problem)
    - tasks.md (execution plan)
    ↓
AI follows tasks enforcing quality gates:
    ✅ Phase 1: Analyze bug
    ✅ Phase 2: Write regression test (BEFORE fix)
    ✅ Phase 3: Implement fix
    ✅ Phase 4: Verify test passes
```

## Design Principles

### 1. Non-Invasive

Extensions don't modify core spec-kit:
- ✅ Separate directory (`.specify/extensions/`)
- ✅ Separate scripts (`create-*.sh` not `setup-*.sh`)
- ✅ Separate commands (`.claude/commands/` is optional)
- ✅ Can be removed without breaking features

### 2. Convention Over Configuration

Workflow type determined by branch name:
- ✅ No config files to manage
- ✅ Works across all AI agents
- ✅ Self-documenting (branch tells you workflow)

### 3. Agent-Agnostic

Works with any AI agent that supports spec-kit:
- ✅ Bash scripts are universal
- ✅ Markdown templates are readable by all agents
- ✅ Claude Code commands are optional enhancement

### 4. Progressive Disclosure

Start simple, add complexity as needed:
- ✅ Basic usage: Just run `/bugfix`
- ✅ Advanced: Customize templates
- ✅ Expert: Create custom workflows

## Extension Points

### Adding a New Workflow

To add a new workflow (e.g., `/performance-audit`):

1. **Create branch pattern** (choose unique pattern):
   ```
   performance/NNN-description
   ```

2. **Add to workflow detection**:
   ```bash
   # In common.sh
   elif [[ "$branch" =~ ^performance/ ]]; then
       echo "performance"
   ```

3. **Create templates**:
   ```
   .specify/extensions/workflows/performance/
   ├── performance-audit-template.md
   ├── tasks-template.md
   └── README.md
   ```

4. **Create bash script**:
   ```bash
   .specify/scripts/bash/create-performance-audit.sh
   ```

5. **Add command** (for Claude Code):
   ```markdown
   .claude/commands/performance.md
   ```

6. **Add quality gates** to constitution:
   ```markdown
   ### N. Performance Audits
   **Workflow**: `/performance`
   **Quality Gates**: ...
   ```

See [DEVELOPMENT.md](../extensions/DEVELOPMENT.md) for detailed guide.

### Customizing Existing Workflows

**Change templates**:
```bash
nano .specify/extensions/workflows/bugfix/bug-report-template.md
```

**Modify task phases**:
```bash
nano .specify/extensions/workflows/bugfix/tasks-template.md
```

**Adjust quality gates**:
```bash
nano .specify/memory/constitution.md
```

## Performance Considerations

### Impact Analysis Speed

Modification workflow scans codebase for affected files. For large codebases:

**Optimization strategies**:
1. Cache previous scans (if feature hasn't changed)
2. Limit search depth
3. Use `.gitignore` to skip node_modules, etc.
4. Parallel file scanning

**Current implementation**:
- Scans complete in <2 seconds for typical projects
- Uses `grep -r` with smart ignores
- Caches nothing (fast enough without)

### Template Copying

Templates are ~10KB each, copying is instant.

### Branch Creation

Git operations are fastest part (milliseconds).

## Security Considerations

### Script Execution

All bash scripts should:
- ✅ Validate inputs (no injection attacks)
- ✅ Use absolute paths (no path traversal)
- ✅ Check file existence before reading
- ✅ Escape user input in shell commands

**Example**:
```bash
# BAD
eval "git checkout -b $BRANCH_NAME"

# GOOD
BRANCH_NAME=$(sanitize "$INPUT")
git checkout -b "$BRANCH_NAME"
```

### Template Injection

Templates use `{{PLACEHOLDER}}` syntax, which is replaced via `sed`:

```bash
# Safe replacement
sed "s/{{DESCRIPTION}}/$(escape_for_sed "$DESCRIPTION")/g"
```

### File Permissions

Creation scripts set appropriate permissions:
- `chmod 644` for markdown files
- `chmod 755` for bash scripts
- Respect user's umask

## Troubleshooting

### Workflow Not Detected

**Symptoms**: Wrong workflow type detected

**Debug**:
```bash
# Check branch name
git branch --show-current

# Test detection
source .specify/scripts/bash/common.sh
detect_workflow_type "$(git branch --show-current)"
```

**Fix**: Ensure branch follows pattern exactly.

### Templates Not Found

**Symptoms**: "Template not found" error

**Debug**:
```bash
# Check templates exist
ls -la .specify/extensions/workflows/*/
```

**Fix**: Reinstall extensions or check for typos in script.

### Impact Analysis Incomplete

**Symptoms**: Modification misses affected files

**Debug**:
```bash
# Run impact scan manually
.specify/scripts/bash/scan-impact.sh 014
```

**Fix**: Impact analysis is heuristic - manually add missed files to report.

## Future Improvements

Potential enhancements:

1. **Metrics Dashboard**: Aggregate data across workflows (bugs fixed, time saved, etc.)
2. **Workflow Linting**: Validate workflow compliance before merge
3. **Automated Testing**: Run workflow scripts in CI
4. **Visual Timeline**: Show feature evolution (original → mods → bugfixes)
5. **Impact Analysis ML**: Use ML to better predict affected files

## References

- [spec-kit Architecture](https://github.com/github/spec-kit) - Core spec-kit design
- [Extension Development Guide](../extensions/DEVELOPMENT.md) - Creating custom workflows
- [bash Best Practices](https://bertvv.github.io/cheat-sheets/Bash.html)

---

**Questions about architecture?** [Open a discussion](https://github.com/[your-username]/spec-kit-extensions/discussions)
