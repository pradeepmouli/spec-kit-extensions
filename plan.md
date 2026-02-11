# Migration Plan: spec-kit-extensions → Native spec-kit Extension System

## Context

spec-kit v0.0.93 introduced a modular extension system (`specify extension add/remove/list`). This plan migrates spec-kit-extensions from its custom installation approach (the `specify-extend` CLI tool that patches files and manually copies templates) to the native extension format, making the workflows installable via `specify extension add`.

## Key Differences Between Current and Target

| Aspect | Current (custom) | Target (native) |
|--------|-------------------|------------------|
| Installation | `specify-extend --all` (custom CLI) | `specify extension add spec-kit-extensions` |
| Manifest | None (hardcoded in `specify_extend.py`) | `extension.yml` per spec |
| Configuration | `enabled.conf` (custom format) | `config-template.yml` (YAML, layered) |
| Agent commands | Custom per-agent transformation in Python | `CommandRegistrar` handles agent formats |
| Branch validation | Monkey-patches `common.sh` | Hooks system (`after_tasks`, etc.) or upstream PR |
| Constitution | Custom append/LLM-enhance logic | Hook-based or config-based |
| Discovery | GitHub release download | `specify extension search` / catalog |

## Architecture Decision: One Extension or Many?

**Option A: Single monolithic extension** — One `spec-kit-extensions` extension containing all 9 workflows.
- Simpler catalog entry, single install command
- All-or-nothing (users can't pick individual workflows)

**Option B: Individual extensions per workflow** — `speckit-bugfix`, `speckit-hotfix`, etc.
- Users install only what they need: `specify extension add speckit-bugfix`
- More catalog entries, but matches the `enabled.conf` concept
- Better aligns with the native extension philosophy of modular packages

**Option C (Recommended): Meta-extension + individual extensions** — A `spec-kit-workflows` meta-extension that installs all workflows, plus each workflow publishable individually.
- `specify extension add spec-kit-workflows` installs everything
- `specify extension add speckit-bugfix` installs just bugfix
- Shared scripts/common.sh packaged as a dependency or bundled in each
- Best user experience: simple for "give me everything" and granular for selective users

### Decision: Start with Option A (single extension), refactor to Option C later.

Rationale: Get the migration working first as one cohesive package. In this initial monolithic extension, enable/disable is at the extension level (all workflows together). Per-workflow toggling will be driven by a `workflows: { ... }` config and enforced in the native system via conditional command registration and/or runtime gating, and breaking this out into individual extensions (Option C) remains a follow-up once the catalog and dependency mechanisms mature.

---

## Phase 1: Create the Native Extension Manifest

### 1.1 Create `extension.yml`

Create a manifest at the repository root that declares all workflows as commands:

```yaml
schema: "1.0"

id: spec-kit-workflows
name: "Spec-Kit Workflow Extensions"
version: "2.2.0"  # v2 native-format release
description: "7 production-tested workflows for the complete software development lifecycle"
author: "pradeepmouli"
repository: "https://github.com/pradeepmouli/spec-kit-extensions"
license: "MIT"

requirements:
  speckit: ">=0.0.93"

provides:
  commands:
    - name: speckit.bugfix
      file: commands/speckit.bugfix.md
      description: "Create a bug fix workflow with regression test"
    - name: speckit.baseline
      file: commands/speckit.baseline.md
      description: "Create a baseline documentation workflow"
    - name: speckit.enhance
      file: commands/speckit.enhance.md
      description: "Create an enhancement workflow"
    - name: speckit.modify
      file: commands/speckit.modify.md
      description: "Create a modification workflow for existing features"
    - name: speckit.refactor
      file: commands/speckit.refactor.md
      description: "Create a refactoring workflow"
    - name: speckit.hotfix
      file: commands/speckit.hotfix.md
      description: "Create a hotfix workflow for critical production issues"
    - name: speckit.deprecate
      file: commands/speckit.deprecate.md
      description: "Create a deprecation workflow"
    - name: speckit.cleanup
      file: commands/speckit.cleanup.md
      description: "Create a cleanup workflow"
    - name: speckit.review
      file: commands/speckit.review.md
      description: "Code review with quality gates"
    - name: speckit.phasestoissues
      file: commands/speckit.phasestoissues.md
      description: "Convert spec phases to GitHub issues"
    - name: speckit.incorporate
      file: commands/speckit.incorporate.md
      description: "Document incorporation workflow"
  configs:
    - file: config-template.yml
      description: "Workflow extension configuration"

hooks:
  - event: after_tasks
    command: speckit.review
    optional: true
    prompt: "Run code review quality gates?"

defaults:
  enabled_workflows:
    - baseline
    - bugfix
    - enhance
    - modify
    - refactor
    - hotfix
    - deprecate
    - cleanup
  branch_validation: true
  constitution_updates: true

tags:
  - workflows
  - bugfix
  - refactor
  - hotfix
  - lifecycle
```

### 1.2 Create `config-template.yml`

Replace `enabled.conf` with the native YAML config format:

```yaml
# Spec-Kit Workflow Extensions Configuration
# Copy to .specify/extensions/spec-kit-workflows/config.yml and customize

workflows:
  # Enable/disable individual workflows
  baseline: true
  bugfix: true
  enhance: true
  modify: true
  refactor: true
  hotfix: true
  deprecate: true
  cleanup: true

branch_validation:
  # Whether to validate branch names match workflow patterns
  enabled: true
  # Additional branch prefixes to allow (beyond standard workflow prefixes)
  extra_prefixes: []

constitution:
  # Whether to suggest constitution updates when installing
  auto_update: true
  # Numbering style for constitution sections: "roman", "numeric", or "auto"
  numbering_style: "auto"
```

### Files to create:
- `extension.yml` (new, at repo root)
- `config-template.yml` (new, at repo root)

---

## Phase 2: Restructure the Directory Layout

The native extension system expects files at specific locations. Restructure:

### 2.1 Current → Target directory mapping

```
CURRENT                                    TARGET (native extension format)
─────────────────────────────────────────  ────────────────────────────────────
commands/speckit.bugfix.md                 commands/speckit.bugfix.md         ✅ (already correct)
commands/speckit.baseline.md               commands/speckit.baseline.md       ✅ (already correct)
...                                        ...
extensions/enabled.conf                    config-template.yml                🔄 (replaced)
extensions/workflows/bugfix/*              workflows/bugfix/*                 🔄 (move up one level)
extensions/workflows/modify/*              workflows/modify/*                 🔄 (move up one level)
...                                        ...
scripts/create-bugfix.sh                   scripts/create-bugfix.sh           ✅ (keep as-is)
scripts/create-baseline.sh                 scripts/create-baseline.sh         ✅ (keep as-is)
common.sh                                  scripts/common.sh                  🔄 (move into scripts/)
extension.yml                              extension.yml                      🆕 (new)
config-template.yml                        config-template.yml                🆕 (new)
README.md                                  README.md                          ✅ (update content)
LICENSE                                    LICENSE                            ✅ (already exists)
CHANGELOG.md                               CHANGELOG.md                       ✅ (update)
```

### 2.2 Key changes:
- Move `extensions/workflows/*` → `workflows/*` (flatten one level — the `extensions/` wrapper was for the custom install; native system installs the whole extension into `.specify/extensions/spec-kit-workflows/`)
- Move `common.sh` into `scripts/` directory
- Remove `extensions/enabled.conf` (replaced by `config-template.yml`)
- Keep `extensions/README.md`, `extensions/DEVELOPMENT.md`, `extensions/QUICKSTART.md` as docs or merge into main README

### 2.3 Update all script references

Scripts currently source common.sh with fallback search paths. After the move, update:
- `create-bugfix.sh` and all `create-*.sh` scripts to look for `common.sh` in the same directory or via `$SPECIFY_ROOT/extensions/spec-kit-workflows/scripts/common.sh`
- Command `.md` files that reference `.specify/extensions/workflows/bugfix/...` → `.specify/extensions/spec-kit-workflows/workflows/bugfix/...`

---

## Phase 3: Refactor Command Files for Native Registration

### 3.1 Standardize command frontmatter

The native `CommandRegistrar` expects a specific frontmatter format. Current commands already use YAML frontmatter with `description` and `handoffs`, which is close. Adjustments needed:

- Ensure `description` field is present (already is)
- The `handoffs` field is already supported by the native system for Copilot/OpenCode/Windsurf
- Remove any agent-specific transformation assumptions — the native `CommandRegistrar` handles agent-specific format conversion

### 3.2 Update file path references in commands

All command files reference paths like:
```
.specify/scripts/bash/create-bugfix.sh
.specify/extensions/workflows/bugfix/bug-report-template.md
```

After native installation, the extension lives at `.specify/extensions/spec-kit-workflows/`. Update references:
```
.specify/extensions/spec-kit-workflows/scripts/create-bugfix.sh
.specify/extensions/spec-kit-workflows/workflows/bugfix/bug-report-template.md
```

### 3.3 Commands to update:
- `commands/speckit.bugfix.md`
- `commands/speckit.baseline.md`
- `commands/speckit.enhance.md`
- `commands/speckit.modify.md`
- `commands/speckit.refactor.md`
- `commands/speckit.hotfix.md`
- `commands/speckit.deprecate.md`
- `commands/speckit.cleanup.md`
- `commands/speckit.review.md`
- `commands/speckit.phasestoissues.md`
- `commands/speckit.incorporate.md`

---

## Phase 4: Eliminate the Patching System

### 4.1 Problem

Currently, `specify_extend.py` monkey-patches spec-kit's `common.sh` to add branch pattern validation for extension workflows (bugfix/, modify/, etc.). This is fragile and version-dependent.

### 4.2 Solution: Upstream PR + Hook-based validation

**Short-term**: The native hook system can intercept before/after commands. Register a `before_commit` or custom validation hook that checks branch patterns. Add a validation script:

```bash
# scripts/validate-branch.sh
# Called by hook system to validate branch names
```

**Medium-term**: Submit a PR to spec-kit core to make `check_feature_branch()` extensible — either:
1. Read extension-registered patterns from a config file, or
2. Accept a pluggable validator function, or
3. Add the common workflow prefixes (bugfix/, hotfix/, refactor/, etc.) to core

### 4.3 Files affected:
- Remove `patch_common_sh()` function from `specify_extend.py` (or the replacement tool)
- Remove `patch_common_ps1()` function
- Create `scripts/validate-branch.sh` (new hook script)
- Register hook in `extension.yml`

---

## Phase 5: Simplify or Replace the CLI Tool

### 5.1 What `specify-extend` currently does

1. Downloads releases from GitHub ← **replaced by** `specify extension add`
2. Copies workflow files ← **replaced by** native installer
3. Copies scripts ← **replaced by** native installer
4. Installs agent commands ← **replaced by** `CommandRegistrar`
5. Patches common.sh ← **eliminated** (Phase 4)
6. Updates constitution ← **keep as a post-install hook or command**
7. Manages enabled.conf ← **replaced by** native config system
8. Detects agents ← **replaced by** native agent detection

### 5.2 What remains

Most of `specify-extend` becomes unnecessary. Two pieces of logic still need a home:

**Constitution updates**: The logic for parsing section numbering, detecting existing workflows, and appending quality gates. This can become:
- A standalone command: `speckit.enhance-constitution` (already exists as a one-time command)
- Or a post-install hook that runs automatically

**Migration helper**: A one-time script to migrate existing installations from the custom format to the native format (move files, update configs, clean up patches).

### 5.3 Decision

- **Keep `specify-extend` as a thin migration/compatibility tool** (v2.0.0)
  - `specify-extend migrate` — migrates existing custom installs to native format
  - `specify-extend --legacy` — falls back to old behavior for pre-0.0.93 spec-kit
  - Remove all other functionality (replaced by native system)
- **Or deprecate entirely** and provide a migration guide in README

### Recommended: Deprecate `specify-extend` with a migration command

Create a simple migration script instead of maintaining the full CLI:

```bash
# scripts/migrate-to-native.sh
# Converts existing .specify/extensions/ layout to native format
# Removes patches from common.sh
# Updates config from enabled.conf to config.yml
```

---

## Phase 6: Publish to the Extension Catalog

### 6.1 Create GitHub release in native format

Structure the release ZIP to match what `specify extension add --from <url>` expects:

```
spec-kit-workflows-v2.2.0.zip
├── extension.yml
├── config-template.yml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── commands/
│   ├── speckit.bugfix.md
│   ├── speckit.baseline.md
│   ├── ... (all 11 command files)
├── workflows/
│   ├── bugfix/
│   │   ├── bug-report-template.md
│   │   └── README.md
│   ├── modify/
│   │   ├── modification-template.md
│   │   ├── scan-impact.sh
│   │   └── README.md
│   └── ... (all workflow directories)
├── scripts/
│   ├── common.sh
│   ├── create-bugfix.sh
│   ├── create-baseline.sh
│   └── ... (all creation scripts)
└── docs/
    └── constitution-template.md
```

### 6.2 Submit catalog PR

Fork spec-kit, add entry to `extensions/catalog.json`:

```json
{
  "spec-kit-workflows": {
    "name": "Spec-Kit Workflow Extensions",
    "description": "7 production-tested workflows for the complete SDLC",
    "author": "pradeepmouli",
    "repository": "https://github.com/pradeepmouli/spec-kit-extensions",
    "latest_version": "2.2.0",
    "download_url": "https://github.com/pradeepmouli/spec-kit-extensions/releases/download/v2.2.0/spec-kit-workflows-v2.2.0.zip",
    "speckit_version": ">=0.0.93",
    "tags": ["workflows", "bugfix", "refactor", "hotfix", "lifecycle"],
    "verified": false,
    "updated_at": "2026-02-10T00:00:00Z"
  }
}
```

### 6.3 Update GitHub Actions

Update the release workflow to:
1. Build the extension ZIP in the native format
2. Attach it to the GitHub release
3. Optionally auto-submit a catalog update PR

---

## Phase 7: Update Documentation

### 7.1 README.md

Rewrite installation section:

```markdown
## Installation

### With spec-kit v0.0.93+
specify extension add spec-kit-workflows

### From GitHub (any version)
specify extension add --from https://github.com/pradeepmouli/spec-kit-extensions/releases/latest

### Legacy (spec-kit < 0.0.93)
pip install specify-extend
specify-extend --all
```

### 7.2 Migration guide

Create `MIGRATION.md` documenting:
- How to migrate from `specify-extend` to `specify extension add`
- What changed in file paths
- How to convert `enabled.conf` to `config.yml`
- How to remove old patches from `common.sh`

### 7.3 Update CLAUDE.md

Update development instructions to reflect the native extension structure.

### 7.4 Files to update:
- `README.md` — new installation instructions
- `INSTALLATION.md` — native installation primary, legacy secondary
- `AI-AGENTS.md` — remove custom agent detection docs (native system handles it)
- `CLAUDE.md` — update development commands and architecture
- `CHANGELOG.md` — document v2.2.0 migration
- Create `MIGRATION.md` (new)

---

## Phase 8: Testing & Validation

### 8.1 Test native installation

```bash
# In a fresh spec-kit project
specify init .
specify extension add --dev /path/to/spec-kit-extensions

# Verify
specify extension list  # Should show spec-kit-workflows
ls .specify/extensions/spec-kit-workflows/  # Files present

# Test a workflow
/speckit.bugfix "test bug"  # Should work end-to-end
```

### 8.2 Test migration from legacy

```bash
# In a project with existing specify-extend installation
./scripts/migrate-to-native.sh
specify extension list  # Should show migrated extension
```

### 8.3 Test enable/disable

```bash
specify extension disable spec-kit-workflows
# Verify commands no longer available
specify extension enable spec-kit-workflows
# Verify commands restored
```

### 8.4 Validate all workflows

Run each workflow creation script and verify:
- Branch creation works
- Directory structure created correctly
- Templates are found at new paths
- JSON output is correct

---

## Implementation Order

1. **Phase 1** — Create `extension.yml` and `config-template.yml`
2. **Phase 2** — Restructure directory layout
3. **Phase 3** — Update command file path references
4. **Phase 4** — Replace patching with hooks/upstream PR
5. **Phase 5** — Deprecate `specify-extend` CLI, create migration script
6. **Phase 8** — Test everything locally with `--dev` install
7. **Phase 6** — Publish release and submit catalog PR
8. **Phase 7** — Update all documentation

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing users on legacy spec-kit | High | Keep `specify-extend --legacy` working; document migration path |
| Path references break after restructuring | High | Comprehensive grep/replace and test each workflow |
| Native extension system API changes | Medium | Pin `speckit: ">=0.0.93"` in manifest; test against latest |
| Branch validation gap without patching | Medium | Ship validation hook; pursue upstream PR |
| Constitution update logic lost | Low | Preserve as standalone command or hook |

---

## What Gets Deleted

- `specify_extend.py` — ~2600 lines of custom installation logic (replaced by native system)
- `test_specify_extend.py` — tests for the above
- `extensions/enabled.conf` — replaced by `config-template.yml`
- `extensions/README.md`, `extensions/DEVELOPMENT.md`, `extensions/QUICKSTART.md` — merge into main docs
- Agent-specific directories (`.claude/`, `.github/`, `.cursor/`, etc.) — in this repo only; native system generates these at install time in target repos
- `pyproject.toml` `[project.scripts]` entry — no more CLI tool to install

## What Gets Kept (restructured)

- All 11 command `.md` files (with updated paths)
- All workflow templates and READMEs
- All creation scripts (`create-*.sh`)
- `common.sh` (moved to `scripts/`)
- `docs/constitution-template.md`
- PowerShell scripts (optional)
