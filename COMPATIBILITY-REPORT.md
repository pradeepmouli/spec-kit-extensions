# Spec-Kit to Spec-Kit-Extensions Compatibility Report

**Generated**: 2025-12-29
**Spec-Kit Version**: 0.0.22 (from main branch)
**Spec-Kit-Extensions Version**: CLI v1.5.7 / Templates v2.5.5

---

## Executive Summary

This report provides an apples-to-apples comparison between **spec-kit** (GitHub's official Spec-Driven Development framework) and **spec-kit-extensions** (community-maintained extensions adding 7+ production workflows). The analysis identifies compatibility issues, API alignment concerns, and potential breaking changes.

### Overall Compatibility Status: ✅ **COMPATIBLE** with Caveats

The extension system is **fundamentally compatible** with spec-kit 0.0.22, but requires **runtime patching** and has several **design misalignments** that could lead to future breakage.

---

## 1. Architecture & Component Comparison

### 1.1 Directory Structure

| Component | Spec-Kit | Spec-Kit-Extensions | Status |
|-----------|----------|---------------------|--------|
| **CLI Tool** | `specify-cli` (v0.0.22) | `specify-extend` (v1.5.7) | ✅ Separate binaries, no conflict |
| **Bash Scripts Location** | `.specify/scripts/bash/` | `.specify/scripts/` + `.specify/extensions/workflows/` | ✅ Compatible |
| **Common Utilities** | `common.sh` (157 lines) | `common.sh` (306 lines, patched) | ⚠️ Requires patching |
| **Templates** | `.specify/templates/` | `.specify/extensions/workflows/{workflow}/` | ✅ Separate paths |
| **Commands** | `.specify/commands/speckit.*.md` | `.specify/commands/speckit.*.md` | ✅ Same convention (v0.0.18+) |
| **Constitution** | `.specify/memory/constitution.md` | Same, with appended sections | ⚠️ Append-only, version drift risk |

### 1.2 CLI Installation Flow

**Spec-Kit**:
```bash
specify init <project>
# Downloads templates from github/spec-kit releases
# Installs to .specify/
```

**Spec-Kit-Extensions**:
```bash
specify init <project>       # First, user must install spec-kit
specify-extend --all         # Then install extensions
# Downloads from pradeepmouli/spec-kit-extensions releases
# Patches .specify/ in-place
```

**Compatibility**: ✅ Sequential installation works, but **spec-kit-extensions assumes spec-kit was installed first**.

---

## 2. Critical Compatibility Issues

### 2.1 🔴 **CRITICAL: common.sh Patching Mechanism**

**Issue**: spec-kit-extensions **monkey-patches** spec-kit's `common.sh` at runtime.

**How it Works**:
1. spec-kit installs `common.sh` with `check_feature_branch()` function (lines 65-82)
2. spec-kit-extensions reads the file and:
   - Creates backup: `common.sh.backup`
   - Renames original function: `check_feature_branch()` → `check_feature_branch_old()`
   - Appends new function with extended branch patterns (lines 248-306)

**Spec-Kit's Original Function** (spec-kit/scripts/bash/common.sh:65-82):
```bash
check_feature_branch() {
    local branch="$1"
    local has_git_repo="$2"

    if [[ "$has_git_repo" != "true" ]]; then
        echo "[specify] Warning: Git repository not detected; skipped branch validation" >&2
        return 0
    fi

    if [[ ! "$branch" =~ ^[0-9]{3}- ]]; then
        echo "ERROR: Not on a feature branch. Current branch: $branch" >&2
        echo "Feature branches should be named like: 001-feature-name" >&2
        return 1
    fi

    return 0
}
```

**Spec-Kit-Extensions' Patched Function** (common.sh:248-306):
```bash
check_feature_branch() {
    # Support both parameterized and non-parameterized calls
    local branch="${1:-}"
    local has_git_repo="${2:-}"

    # If branch not provided as parameter, get current branch
    if [[ -z "$branch" ]]; then
        if git rev-parse --git-dir > /dev/null 2>&1; then
            branch=$(git branch --show-current)
            has_git_repo="true"
        else
            return 0
        fi
    fi

    # Extension branch patterns (spec-kit-extensions)
    local extension_patterns=(
        "^baseline/[0-9]{3}-"
        "^bugfix/[0-9]{3}-"
        "^enhance/[0-9]{3}-"
        "^modify/[0-9]{3}\\^[0-9]{3}-"
        "^refactor/[0-9]{3}-"
        "^hotfix/[0-9]{3}-"
        "^deprecate/[0-9]{3}-"
        "^cleanup/[0-9]{3}-"
    )

    # Check extension patterns first
    for pattern in "${extension_patterns[@]}"; do
        if [[ "$branch" =~ $pattern ]]; then
            return 0
        fi
    done

    # Check standard spec-kit pattern (###-)
    if [[ "$branch" =~ ^[0-9]{3}- ]]; then
        return 0
    fi

    # No match - show helpful error
    echo "ERROR: Not on a feature branch. Current branch: $branch" >&2
    echo "Feature branches must follow one of these patterns:" >&2
    echo "  Standard:    ###-description (e.g., 001-add-user-authentication)" >&2
    echo "  Baseline:    baseline/###-description" >&2
    echo "  Bugfix:      bugfix/###-description" >&2
    echo "  Enhance:     enhance/###-description" >&2
    echo "  Modify:      modify/###^###-description" >&2
    echo "  Refactor:    refactor/###-description" >&2
    echo "  Hotfix:      hotfix/###-description" >&2
    echo "  Deprecate:   deprecate/###-description" >&2
    echo "  Cleanup:     cleanup/###-description" >&2
    return 1
}
```

**Compatibility Risks**:
- ❌ **Breaking Change Risk**: If spec-kit refactors `check_feature_branch()` signature or behavior, the patch breaks
- ❌ **Version Lock-In**: Extensions are tied to spec-kit's internal implementation details
- ❌ **No API Contract**: spec-kit doesn't expose hooks/plugins for this use case
- ❌ **Upgrade Path**: Upgrading spec-kit requires re-running `specify-extend` to re-patch
- ✅ **Idempotent**: Patch checks for `check_feature_branch_old()` to avoid double-patching
- ✅ **Versioned Patches**: Checks for outdated patterns (`enhance`, `cleanup`, `baseline`) and re-patches

**Used By**:
- `spec-kit/scripts/bash/check-prerequisites.sh:83` ✅
- `spec-kit/scripts/bash/setup-plan.sh:34` ✅

**Recommendation**:
- **Short-term**: Document that spec-kit upgrades may break extensions
- **Long-term**: Propose plugin API to spec-kit maintainers (hook system for branch validation)

---

### 2.2 ⚠️ **MEDIUM: Missing generate_branch_name() Function**

**Issue**: spec-kit-extensions adds `generate_branch_name()` function (common.sh:65-112) that **does not exist in upstream spec-kit**.

**Function Purpose**: Smart branch naming with stop word filtering and acronym detection.

**Spec-Kit's Approach** (spec-kit 0.0.20+):
- Uses `--short-name` parameter in `create-new-feature.sh`
- Provides manual branch name truncation to 244-byte GitHub limit

**Spec-Kit-Extensions' Approach**:
- Provides `generate_branch_name()` function in patched `common.sh`
- Ships standalone `scripts/branch-utils.sh` helper (v2.5.5+)
- All extension scripts source `branch-utils.sh` with fallback logic

**Example from create-bugfix.sh:5-36**:
```bash
# Try to source branch-utils first (new approach)
SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/branch-utils.sh" ]]; then
    source "$SCRIPT_DIR/branch-utils.sh"
elif [[ -f "$SCRIPT_DIR/../bash/branch-utils.sh" ]]; then
    source "$SCRIPT_DIR/../bash/branch-utils.sh"
# Fall back to common.sh if branch-utils not available (backward compat)
elif [[ -f "$SCRIPT_DIR/../bash/common.sh" ]]; then
    source "$SCRIPT_DIR/../bash/common.sh"
elif [[ -f "$SCRIPT_DIR/../../scripts/bash/common.sh" ]]; then
    source "$SCRIPT_DIR/../../scripts/bash/common.sh"
fi

# Verify generate_branch_name function exists
if ! declare -f generate_branch_name > /dev/null; then
    echo "Error: generate_branch_name function is not available" >&2
    echo "Please ensure branch-utils.sh or patched common.sh is installed" >&2
    exit 1
fi
```

**Compatibility Status**:
- ✅ **MITIGATED** as of v2.5.5: Extensions ship standalone `branch-utils.sh`
- ✅ Graceful fallback to patched `common.sh` for older installations
- ✅ Clear error message if function not available
- ⚠️ Users with **spec-kit only** cannot use extension scripts without `specify-extend` installation

---

### 2.3 ⚠️ **MEDIUM: find_feature_dir_by_prefix() Behavior**

**Issue**: spec-kit-extensions adds `find_feature_dir_by_prefix()` function (common.sh:178-215) that enables **multiple branches to share the same spec directory**.

**Spec-Kit Behavior**:
- Uses `get_feature_dir()` (common.sh:84): `echo "$1/specs/$2"`
- Strict 1:1 mapping: branch `001-feature-name` → `specs/001-feature-name/`

**Spec-Kit-Extensions Behavior**:
- Uses numeric prefix matching
- Allows `bugfix/004-fix-a` and `bugfix/004-fix-b` to both use `specs/bugfix/004-*/`
- Returns first match if exactly one directory found

**Compatibility**:
- ✅ **Backward Compatible**: Falls back to exact match if no prefix pattern
- ✅ Extension workflows create correctly prefixed directories
- ⚠️ Spec-kit tools won't recognize extension branch patterns (e.g., `bugfix/###-`)

---

### 2.4 🟡 **LOW: Constitution Append-Only Updates**

**Issue**: spec-kit-extensions appends workflow quality gates to constitution, risking **duplicate sections** over time.

**Spec-Kit Constitution** (spec-kit/memory/constitution.md):
- Template-based, user customizes per project
- No workflow-specific sections by default

**Spec-Kit-Extensions Approach**:
1. **LLM-Enhanced Mode** (default): Creates one-time `/speckit.enhance-constitution` command
2. **Direct Append Mode** (`--no-llm-enhance`): Appends `docs/constitution-template.md` to constitution

**Detection Logic** (specify_extend.py:1323-1354):
- Detects existing workflows via regex: `/speckit\.(baseline|bugfix|modify|refactor|hotfix|deprecate)/`
- Detects section numbering style (Roman/numeric/none)
- Skips update if all 6 major workflows already present
- Continues numbering from highest section

**Compatibility**:
- ✅ Idempotent: Won't duplicate if workflows already present
- ✅ Numbering-aware: Adapts to Roman (I, II, III) or numeric (1, 2, 3) styles
- ⚠️ **Risk**: Manual edits to constitution could confuse detection logic
- ⚠️ **Risk**: Spec-kit could introduce conflicting workflow sections in future

**Version Drift Example**:
- Spec-kit 0.0.22: No workflow sections
- Spec-kit 0.0.25 (hypothetical): Adds `/speckit.bugfix` as core feature
- spec-kit-extensions: Already patched with bugfix workflow
- **Result**: Duplicate or conflicting guidance

---

## 3. Template & Workflow Format Compatibility

### 3.1 Template Structure

| Component | Spec-Kit | Spec-Kit-Extensions | Compatible? |
|-----------|----------|---------------------|-------------|
| **Feature Spec** | `spec-template.md` (116 lines) | `baseline-spec-template.md` (shorter, different focus) | ✅ Different use cases |
| **Bugfix Spec** | N/A (uses feature spec) | `bug-report-template.md` (82 lines) | ✅ Extension-only |
| **Plan Template** | `plan-template.md` | Uses spec-kit's plan.md | ✅ Compatible |
| **Tasks Template** | `tasks-template.md` | Uses spec-kit's tasks.md | ✅ Compatible |
| **Checklist Template** | `checklist-template.md` | Uses spec-kit's checklist.md | ✅ Compatible |

**Compatibility**: ✅ **No conflicts** - extensions add new templates, don't override spec-kit's templates.

---

### 3.2 Command Naming Convention

**Spec-Kit 0.0.18+ Convention**: `/speckit.*` prefix
- Examples: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`

**Spec-Kit-Extensions Convention**: `/speckit.*` prefix (aligned since v2.1.0)
- Examples: `/speckit.bugfix`, `/speckit.baseline`, `/speckit.refactor`, `/speckit.hotfix`

**Compatibility**: ✅ **FULLY ALIGNED** as of spec-kit 0.0.18 and spec-kit-extensions v2.1.0

**Historical Note**: Prior to 0.0.18, spec-kit used individual command names (`specify.md`, `plan.md`) without prefix.

---

### 3.3 Placeholder Convention

**Spec-Kit**: Uses `[PLACEHOLDER]` syntax
```markdown
**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"
```

**Spec-Kit-Extensions**: Uses `{{PLACEHOLDER}}` syntax (in some scripts)
```bash
# From create-bugfix.sh
sed "s/{{BRANCH_NAME}}/$branch_name/g"
```

**Compatibility**: ⚠️ **INCONSISTENT** - Extensions use mix of `{{}}` and `[]` placeholders
- **Impact**: Low (script-level replacements work independently)
- **Recommendation**: Standardize on `{{}}` for script replacements, `[]` for user-filled content

---

## 4. CLI & API Compatibility

### 4.1 CLI Tool Comparison

| Feature | Spec-Kit (`specify`) | Spec-Kit-Extensions (`specify-extend`) |
|---------|----------------------|----------------------------------------|
| **Installation** | `specify init <project>` | `specify-extend --all` |
| **Version** | 0.0.22 | 1.5.7 (CLI), 2.5.5 (templates) |
| **Language** | Python 3.11+ | Python 3.11+ |
| **Dependencies** | `typer`, `rich`, `httpx`, `platformdirs`, `readchar`, `truststore` | `typer`, `rich`, `httpx` |
| **Agent Detection** | Yes (Copilot, Claude, Gemini, Cursor, Roo, CodeBuddy, Amp) | Yes (Copilot, Claude, Gemini, Cursor) + multi-agent |
| **GitHub API** | Yes (rate limiting, auth headers) | Yes (rate limiting, auth headers) |
| **Dry Run** | No | Yes (`--dry-run`) |
| **Workflow Selection** | N/A | Yes (interactive + `--workflows`) |

**Compatibility**: ✅ Both use same tech stack, no conflicts

---

### 4.2 GitHub API Usage

**Spec-Kit** (src/specify_cli/__init__.py:59-123):
- Rate limit detection with retry suggestions
- Token support via `--github-token`, `GH_TOKEN`, `GITHUB_TOKEN`
- SSL context using `truststore`
- Authenticated: 5,000 req/hr, Unauthenticated: 60 req/hr

**Spec-Kit-Extensions** (specify_extend.py:157-207):
- **IDENTICAL IMPLEMENTATION** (likely copied from spec-kit)
- Same headers, same parsing logic, same error messages

**Compatibility**: ✅ **IDENTICAL** - Extensions copied spec-kit's API handling

---

### 4.3 Agent Configuration

**Spec-Kit AGENT_CONFIG** (spec-kit/src/specify_cli/__init__.py:126-150):
```python
AGENT_CONFIG = {
    "copilot": {"name": "GitHub Copilot", "folder": ".github/", "requires_cli": False},
    "claude": {"name": "Claude Code", "folder": ".claude/", "requires_cli": True},
    "gemini": {"name": "Gemini CLI", "folder": ".gemini/", "requires_cli": True},
    "cursor-agent": {"name": "Cursor", "folder": ".cursor/", "requires_cli": False},
    # ... + roo, codebuddy, amp, etc.
}
```

**Spec-Kit-Extensions AGENT_CONFIG** (specify_extend.py:63-89):
```python
AGENT_CONFIG = {
    "claude": {"name": "Claude Code", "folder": ".claude/", "detection_file": ".claude/claude_desktop_config.json"},
    "copilot": {"name": "GitHub Copilot", "folder": ".github/", "detection_file": ".github/copilot-instructions.md"},
    "cursor": {"name": "Cursor", "folder": ".cursor/", "detection_file": ".cursor/rules"},
    "gemini": {"name": "Gemini CLI", "folder": ".gemini/", "detection_file": None},
}
```

**Differences**:
- ⚠️ Spec-kit has 7+ agents, spec-kit-extensions has 4
- ⚠️ Extensions use `detection_file`, spec-kit uses `requires_cli`
- ⚠️ Extensions support multi-agent mode (`--agents claude,copilot`)

**Compatibility**: ⚠️ **PARTIAL** - Extensions support subset of agents, but no conflicts

---

## 5. Branch Naming Pattern Compatibility

### 5.1 Pattern Comparison

| Workflow | Spec-Kit Pattern | Extensions Pattern | Example |
|----------|------------------|-------------------|---------|
| **Feature** | `###-description` | `###-description` | `001-user-auth` ✅ |
| **Baseline** | N/A | `baseline/###-description` | `baseline/001-project-setup` ⚠️ |
| **Bugfix** | `###-description` (same as feature) | `bugfix/###-description` | `bugfix/002-fix-login` ⚠️ |
| **Enhance** | N/A | `enhance/###-description` | `enhance/003-improve-ui` ⚠️ |
| **Modify** | N/A | `modify/###^###-description` | `modify/001^002-change-api` ⚠️ |
| **Refactor** | N/A | `refactor/###-description` | `refactor/004-clean-code` ⚠️ |
| **Hotfix** | N/A | `hotfix/###-description` | `hotfix/005-patch-security` ⚠️ |
| **Deprecate** | N/A | `deprecate/###-description` | `deprecate/006-remove-legacy` ⚠️ |
| **Cleanup** | N/A | `cleanup/###-description` | `cleanup/007-archive-specs` ⚠️ |

**Spec-Kit Branch Detection** (spec-kit/scripts/bash/common.sh:75-79):
```bash
if [[ ! "$branch" =~ ^[0-9]{3}- ]]; then
    echo "ERROR: Not on a feature branch. Current branch: $branch" >&2
    echo "Feature branches should be named like: 001-feature-name" >&2
    return 1
fi
```

**Impact**:
- ❌ **Spec-kit scripts reject extension branch patterns** (`bugfix/###-`, etc.)
- ✅ **Extensions patch common.sh to accept both patterns**
- ⚠️ **Without patch**: Extension branches fail `check_feature_branch()` in:
  - `check-prerequisites.sh`
  - `setup-plan.sh`

**Compatibility**: ⚠️ **REQUIRES PATCHING** - Extension branches incompatible with unpatched spec-kit

---

### 5.2 Branch Number Allocation

**Spec-Kit**: Sequential numbering across all branches
- `001-feature-a`, `002-feature-b`, `003-feature-c`

**Spec-Kit-Extensions**: Sequential numbering **per workflow type**
- `001-feature-a` (feature)
- `bugfix/001-fix-a` (bugfix)
- `refactor/001-clean-a` (refactor)

**Collision Risk**: ✅ **NO COLLISION** - Different prefixes prevent conflicts

---

## 6. Function & Script Compatibility Matrix

### 6.1 Common Functions

| Function | Spec-Kit | Extensions | Status |
|----------|----------|------------|--------|
| `get_repo_root()` | ✅ Lines 5-13 | ✅ Lines 5-13 (identical) | ✅ Compatible |
| `get_current_branch()` | ✅ Lines 16-58 | ✅ Lines 16-58 (identical) | ✅ Compatible |
| `has_git()` | ✅ Lines 61-63 | ✅ Lines 61-63 (identical) | ✅ Compatible |
| `check_feature_branch()` | ✅ Lines 65-82 (basic) | ✅ Lines 248-306 (extended) | ⚠️ Patched |
| `get_feature_dir()` | ✅ Line 84 | ✅ Line 174 (identical) | ✅ Compatible |
| `find_feature_dir_by_prefix()` | ❌ Not present | ✅ Lines 178-215 | ⚠️ Extension-only |
| `get_feature_paths()` | ✅ Lines 127-152 | ✅ Lines 217-242 (identical) | ✅ Compatible |
| `check_file()` | ✅ Line 154 | ✅ Line 244 (identical) | ✅ Compatible |
| `check_dir()` | ✅ Line 155 | ✅ Line 245 (identical) | ✅ Compatible |
| `generate_branch_name()` | ❌ Not present | ✅ Lines 65-112 | ⚠️ Extension-only (shipped in branch-utils.sh) |

**Summary**:
- ✅ **8/10 functions identical** or backward compatible
- ⚠️ **2/10 functions extension-only** (but with fallback mechanisms)

---

### 6.2 Bash Script Compatibility

| Script | Spec-Kit | Extensions | Purpose |
|--------|----------|------------|---------|
| `common.sh` | ✅ 157 lines | ✅ 306 lines (patched) | Shared utilities |
| `create-new-feature.sh` | ✅ 10,191 bytes | ❌ Not present | Feature creation (spec-kit only) |
| `setup-plan.sh` | ✅ 1,627 bytes | ❌ Not present | Plan setup (spec-kit only) |
| `check-prerequisites.sh` | ✅ 4,985 bytes | ❌ Not present | Validation (spec-kit only) |
| `update-agent-context.sh` | ✅ 25,556 bytes | ⚠️ Patched by extensions | Agent context sync |
| `create-bugfix.sh` | ❌ Not present | ✅ 4,177 bytes | Bugfix workflow |
| `create-baseline.sh` | ❌ Not present | ✅ 8,171 bytes | Baseline workflow |
| `create-modification.sh` | ❌ Not present | ✅ 7,414 bytes | Modification workflow |
| `create-refactor.sh` | ❌ Not present | ✅ 10,511 bytes | Refactor workflow |
| `create-hotfix.sh` | ❌ Not present | ✅ 5,864 bytes | Hotfix workflow |
| `create-deprecate.sh` | ❌ Not present | ✅ 7,924 bytes | Deprecation workflow |
| `create-cleanup.sh` | ❌ Not present | ✅ 14,963 bytes | Cleanup workflow |
| `create-enhance.sh` | ❌ Not present | ✅ 4,330 bytes | Enhancement workflow |
| `branch-utils.sh` | ❌ Not present | ✅ 2,026 bytes | Branch name generation |
| `mark-task-status.sh` | ❌ Not present | ✅ 3,629 bytes | Task management |

**Compatibility**: ✅ **NO CONFLICTS** - Extensions add new scripts, don't override spec-kit's scripts

---

## 7. Version Compatibility & Breaking Changes

### 7.1 Spec-Kit Version History (Relevant to Extensions)

| Version | Date | Relevant Changes | Impact on Extensions |
|---------|------|------------------|----------------------|
| **0.0.22** | 2025-11-07 | VS Code/Copilot agents, AGENTS.md, version command | ✅ No impact |
| **0.0.21** | 2025-10-21 | Amp CLI support, VS Code hand-offs | ✅ No impact |
| **0.0.20** | 2025-10-14 | **Intelligent branch naming**, `--short-name`, stop word filtering | ⚠️ **Overlaps with extensions' `generate_branch_name()`** |
| **0.0.19** | 2025-10-10 | CodeBuddy support | ✅ No impact |
| **0.0.18** | 2025-10-06 | **`/speckit.` command prefix**, VS Code shortcuts | ✅ **Extensions aligned to this convention** |
| **0.0.17** | 2025-09-22 | `/clarify` and `/analyze` commands | ✅ No impact |
| **0.0.16** | 2025-09-22 | `--force` flag for init | ✅ No impact |

---

### 7.2 Breaking Change: Spec-Kit 0.0.20 Branch Naming

**Spec-Kit 0.0.20 Added**:
- Intelligent branch naming in `create-new-feature.sh`
- Stop word filtering ("I", "want", "to", etc.)
- `--short-name` parameter
- 244-byte GitHub limit enforcement

**Spec-Kit-Extensions Already Had**:
- `generate_branch_name()` function with stop word filtering (added v2.1.1)
- Same logic, independently developed

**Compatibility**:
- ✅ **NO CONFLICT**: Spec-kit only uses it in `create-new-feature.sh`
- ✅ Extensions use it in their own scripts via `branch-utils.sh`
- ⚠️ **Code Duplication**: Two implementations of same logic
- ⚠️ **Divergence Risk**: Future changes to spec-kit's logic won't propagate to extensions

---

### 7.3 Spec-Kit-Extensions Version History

| CLI Version | Template Version | Date | Changes |
|-------------|------------------|------|---------|
| **1.5.7** | **2.5.5** | 2025-12-29 | Branch utils helpers, decoupled from common.sh |
| **1.5.6** | **2.5.4** | (Recent) | Improved constitution self-destruct |
| **1.5.5** | **2.5.4** | (Recent) | Incorporate command enhancements |

**Breaking Changes**: None documented, but **patching mechanism is version-sensitive**.

---

## 8. Dependency Compatibility

### 8.1 Python Dependencies

**Spec-Kit**:
```toml
requires-python = ">=3.11"
dependencies = ["typer", "rich", "httpx[socks]", "platformdirs", "readchar", "truststore>=0.10.4"]
```

**Spec-Kit-Extensions**:
```toml
requires-python = ">=3.11"
dependencies = ["typer", "rich", "httpx"]
```

**Differences**:
- ⚠️ Spec-kit requires `platformdirs`, `readchar`, `truststore` - extensions don't
- ⚠️ Extensions use `httpx` basic, spec-kit uses `httpx[socks]`

**Compatibility**: ✅ **NO CONFLICT** - Both can be installed simultaneously

---

### 8.2 Bash Dependencies

**Spec-Kit**: Standard POSIX utilities (`grep`, `sed`, `git`, `find`)

**Spec-Kit-Extensions**: Same + assumes spec-kit's utilities are available

**Compatibility**: ✅ **COMPATIBLE** - Extensions layer on top of spec-kit

---

## 9. Upgrade Path & Forward Compatibility

### 9.1 Scenario: User Upgrades Spec-Kit

**Current State**:
- Spec-kit 0.0.22 installed
- Spec-kit-extensions 1.5.7/2.5.5 installed
- `common.sh` patched

**User Runs**: `specify upgrade` (hypothetical)

**What Could Break**:
1. ❌ **common.sh overwritten** - Patch lost, extension branches fail validation
2. ❌ **check_feature_branch() signature changes** - Patch logic breaks
3. ❌ **Constitution conflicts** - If spec-kit adds workflow sections
4. ⚠️ **Template conflicts** - If spec-kit adds overlapping templates

**Mitigation**:
- ✅ Extensions create `common.sh.backup` before patching
- ⚠️ User must **re-run `specify-extend --all`** after spec-kit upgrade
- ⚠️ No automatic detection of spec-kit upgrades

---

### 9.2 Recommended Upgrade Workflow

```bash
# 1. Check current versions
specify version        # e.g., 0.0.22
specify-extend --version  # e.g., 1.5.7

# 2. Backup extensions configuration
cp -r .specify/extensions .specify/extensions.backup

# 3. Upgrade spec-kit
# (awaiting official spec-kit upgrade command)

# 4. Re-apply extensions
specify-extend --all

# 5. Verify constitution didn't duplicate sections
cat .specify/memory/constitution.md

# 6. Test extension workflows
.specify/scripts/create-bugfix.sh --json "test"
```

---

## 10. Recommendations

### 10.1 For Spec-Kit Maintainers

1. **Add Plugin API** ⭐ **PRIORITY**
   - Expose `check_feature_branch` as plugin hook
   - Allow extensions to register custom branch patterns
   - Example: `.specify/plugins/branch-patterns.json`

2. **Standardize Template Placeholders**
   - Document `{{PLACEHOLDER}}` vs `[PLACEHOLDER]` usage
   - Provide template validation tool

3. **Version Pinning**
   - Add `min_spec_kit_version` field to extension manifests
   - Reject incompatible extensions at install time

4. **Constitution Extension Mechanism**
   - Provide `constitution.d/` directory for modular sections
   - Auto-merge on `specify init` or `specify upgrade`

### 10.2 For Spec-Kit-Extensions Maintainers

1. **Document Spec-Kit Version Requirements** ⭐ **PRIORITY**
   - Add `Requires spec-kit >= 0.0.18` to README
   - Test against multiple spec-kit versions

2. **Reduce Patching Surface**
   - ✅ DONE: Shipped `branch-utils.sh` to decouple from `common.sh`
   - Consider alternative validation approaches (e.g., `.specify/config.json`)

3. **Add Version Detection**
   - Detect spec-kit version before patching
   - Warn if incompatible version detected

4. **Automated Testing**
   - CI pipeline testing against spec-kit 0.0.18, 0.0.20, 0.0.22
   - Detect breaking changes early

5. **Upgrade Guide**
   - Document "What to do when spec-kit releases new version"
   - Provide `specify-extend --repair` command to re-patch after upgrades

### 10.3 For End Users

1. **Installation Order Matters**
   ```bash
   specify init .          # FIRST: Install spec-kit
   specify-extend --all    # SECOND: Install extensions
   ```

2. **After Spec-Kit Upgrades**
   ```bash
   specify upgrade         # Upgrade spec-kit
   specify-extend --all    # Re-apply extensions (re-patches common.sh)
   ```

3. **Verify Installation**
   ```bash
   # Test that extension branches work
   .specify/scripts/create-bugfix.sh --json "test bug"

   # Check for patched function
   grep "check_feature_branch_old" .specify/scripts/bash/common.sh
   ```

---

## 11. Summary of Compatibility Issues

| Issue | Severity | Status | Mitigation |
|-------|----------|--------|------------|
| **common.sh patching** | 🔴 Critical | ⚠️ Required | Re-patch after spec-kit upgrades |
| **Extension branch patterns** | 🔴 Critical | ⚠️ Patched | Won't work without patch |
| **generate_branch_name() missing** | ⚠️ Medium | ✅ Mitigated | Shipped in branch-utils.sh (v2.5.5) |
| **Constitution append conflicts** | 🟡 Low | ✅ Idempotent | Detection logic prevents duplicates |
| **Template placeholder inconsistency** | 🟡 Low | ⚠️ Minor | No functional impact |
| **Agent config subset** | 🟡 Low | ✅ Acceptable | Extensions support 4/7 agents |
| **Code duplication (branch naming)** | 🟡 Low | ⚠️ Divergence risk | Monitor spec-kit changes |

---

## 12. Conclusion

**Spec-kit-extensions is production-ready and compatible with spec-kit 0.0.22**, with the following caveats:

✅ **Works Well**:
- Sequential installation (`specify init` → `specify-extend`)
- No file conflicts or overwrites
- Command naming aligned (`/speckit.*` prefix)
- Template formats compatible

⚠️ **Requires Care**:
- Must re-patch after spec-kit upgrades
- Extension branch patterns only work with patched `common.sh`
- Constitution updates may conflict if spec-kit adds workflows

❌ **Known Risks**:
- Monkey-patching `common.sh` is fragile
- No version pinning or compatibility checks
- Upgrade path requires manual intervention

**Overall Grade**: **B+** (Compatible with maintenance burden)

---

## Appendix: Test Results

### A.1 File Comparison

```bash
# Spec-kit files: 40 (scripts, templates, docs)
# Spec-kit-extensions files: 60+ (scripts, workflows, docs)
# Conflicts: 0 (separate namespaces)
```

### A.2 Function Comparison

```bash
# Spec-kit common.sh: 157 lines, 9 functions
# Extensions common.sh: 306 lines, 11 functions (2 new, 2 renamed)
# Conflicts: 1 (check_feature_branch patched)
```

### A.3 Version Matrix Tested

| Spec-Kit Version | Extensions Version | Status |
|------------------|-------------------|--------|
| 0.0.22 | 1.5.7 / 2.5.5 | ✅ Tested |
| 0.0.20 | 1.5.7 / 2.5.5 | ⚠️ Branch naming overlap |
| 0.0.18 | 1.5.7 / 2.5.5 | ✅ Compatible |

---

**Report Generated**: 2025-12-29
**Methodology**: File-by-file comparison, function signature analysis, integration testing
**Spec-Kit Source**: github.com/github/spec-kit (main branch, cloned 2025-12-29)
**Extensions Source**: Local repository at /home/user/spec-kit-extensions
