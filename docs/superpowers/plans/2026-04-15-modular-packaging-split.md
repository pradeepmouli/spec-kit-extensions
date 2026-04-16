# Modular Packaging Split Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split spec-kit-extensions into a modular product made of multiple extensions and standalone workflow packages while preserving a single curated install UX through `specify-extend`.

**Architecture:** Keep this repository as the umbrella/orchestrator repo and gradually extract lifecycle orchestration into standalone workflow packages plus domain-focused extension packages. Use the CLI as the compatibility contract and bundle manager so users still install a coherent product rather than thinking in raw package boundaries.

**Tech Stack:** spec-kit extension manifests, spec-kit workflow packages, Python CLI orchestration, git subtree for vendoring published workflow repos.

---

## Chunk 1: Target Product Topology

### Task 1: Lock the package taxonomy

**Files:**
- Create: `docs/superpowers/plans/2026-04-15-modular-packaging-split.md`
- Modify: `README.md`
- Modify: `INSTALLATION.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Adopt the package types**

Use exactly three package classes:

1. **Umbrella repo + CLI**
   - Owns: installer UX, compatibility rules, bundle definitions, docs, release notes.
   - Stays in this repository.

2. **Extension packages**
   - Own: command prompts, templates, scripts, config, hook registrations.
   - Install via `specify extension add ...`.

3. **Workflow packages**
   - Own: orchestration YAML + package README/license/changelog.
   - Install via `specify workflow add ...`.

- [ ] **Step 2: Freeze the top-level repo responsibilities**

This repository remains the home for:

- `specify_extend.py`
- umbrella documentation
- curated bundle metadata
- release coordination
- subtree-vendored workflow packages
- any shared scripts/templates that are not yet extracted

- [ ] **Step 3: Write the target package matrix**

Use this target matrix.

| Package | Type | Responsibility |
|---|---|---|
| `workflows-core` | extension | shared scripts, shared templates, shared config, compatibility shims |
| `workflows-lifecycle` | extension | bugfix, modify, refactor, deprecate, hotfix, enhance commands |
| `workflows-governance` | extension | review, cleanup, baseline |
| `workflows-issues` | extension | phase-to-issues, issue-sync commands and related config |
| `bugfix-lifecycle` | workflow | gated orchestration for bugfix |
| `modify-lifecycle` | workflow | gated orchestration for modify |
| `refactor-lifecycle` | workflow | gated orchestration for refactor |
| `deprecate-lifecycle` | workflow | gated orchestration for deprecate |

- [ ] **Step 4: Record the key non-goal**

Do not split into one-extension-per-command. That increases release and compatibility overhead without improving UX.

### Task 2: Define bundle semantics

**Files:**
- Modify: `specify_extend.py`
- Modify: `README.md`
- Modify: `INSTALLATION.md`

- [ ] **Step 1: Define the install bundles**

Use these user-facing bundles:

| Bundle | Installs |
|---|---|
| `core` | `workflows-core` |
| `standard` | `workflows-core`, `workflows-lifecycle` |
| `full` | `workflows-core`, `workflows-lifecycle`, `workflows-governance`, `workflows-issues` |
| `standard-with-workflows` | `standard` + all four lifecycle workflow packages |
| `full-with-workflows` | `full` + all four lifecycle workflow packages |

- [ ] **Step 2: Define installation order**

Always install in this order:

1. core extension
2. domain extensions
3. workflow packages

Reason: workflows depend on extension commands being present at runtime.

- [ ] **Step 3: Define idempotent behavior**

CLI should:

- skip installed packages unless upgrade/force is requested
- verify spec-kit version before install
- print exact extension and workflow units selected
- stop on missing prerequisites with a targeted error

---

## Chunk 2: File Boundary Plan

### Task 3: Assign current files to target packages

**Files:**
- Modify: `README.md`
- Modify: `INSTALLATION.md`
- Modify: `docs/architecture.md`

- [ ] **Step 1: Assign lifecycle commands**

Move these command files into `workflows-lifecycle` during the split:

- `commands/bugfix.md`
- `commands/modify.md`
- `commands/refactor.md`
- `commands/deprecate.md`
- `commands/hotfix.md`
- `commands/enhance.md`

- [ ] **Step 2: Assign governance commands**

Move these command files into `workflows-governance`:

- `commands/review.md`
- `commands/cleanup.md`
- `commands/baseline.md`

- [ ] **Step 3: Assign issue commands**

Move these command files into `workflows-issues`:

- `commands/phasestoissues.md`
- `commands/issue-sync-before-specify.md`
- `commands/issue-sync-after-specify.md`
- `commands/issue-sync-before-plan.md`
- `commands/issue-sync-after-plan.md`
- `commands/issue-sync-before-tasks.md`
- `commands/issue-sync-after-tasks.md`
- `commands/issue-sync-before-implement.md`
- `commands/issue-sync-after-implement.md`

- [ ] **Step 4: Assign shared assets**

Move these shared assets into `workflows-core` unless a more specific package owns them:

- shared bash/powershell helpers in `scripts/`
- shared config templates in `config/`
- any common template fragments
- branch compatibility notes and install metadata

- [ ] **Step 5: Assign workflow packages**

Each standalone workflow repo owns only:

- `workflow.yml`
- `README.md`
- `LICENSE`
- `CHANGELOG.md`

Keep the workflow packages thin. They should orchestrate installed commands, not duplicate extension logic.

---

## Chunk 3: Repo and Release Layout

### Task 4: Define repository naming and subtree layout

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture.md`

- [ ] **Step 1: Use these repository names**

Recommended repositories:

- `spec-kit-extensions` (umbrella + CLI)
- `spec-kit-ext-workflows-core`
- `spec-kit-ext-workflows-lifecycle`
- `spec-kit-ext-workflows-governance`
- `spec-kit-ext-workflows-issues`
- `spec-kit-workflow-bugfix-lifecycle`
- `spec-kit-workflow-modify-lifecycle`
- `spec-kit-workflow-refactor-lifecycle`
- `spec-kit-workflow-deprecate-lifecycle`

- [ ] **Step 2: Use these subtree paths in the umbrella repo**

Vendor external repos back into this repo at:

- `packages/extensions/workflows-core/`
- `packages/extensions/workflows-lifecycle/`
- `packages/extensions/workflows-governance/`
- `packages/extensions/workflows-issues/`
- `packages/workflows/bugfix-lifecycle/`
- `packages/workflows/modify-lifecycle/`
- `packages/workflows/refactor-lifecycle/`
- `packages/workflows/deprecate-lifecycle/`

- [ ] **Step 3: Keep a user-facing compatibility layer**

For one or more releases, preserve current top-level paths or provide a thin compatibility index so documentation and contributors are not broken all at once.

### Task 5: Define versioning strategy

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `README.md`

- [ ] **Step 1: Version units independently**

Rules:

- each extension repo has its own semantic version
- each workflow repo has its own semantic version
- umbrella CLI has its own semantic version
- umbrella repo changelog records bundle-level compatibility, not every internal patch detail

- [ ] **Step 2: Maintain a bundle lock table**

The umbrella CLI should own a version map like:

```text
bundle standard-with-workflows:
  workflows-core: 1.2.0
  workflows-lifecycle: 1.1.0
  bugfix-lifecycle: 1.0.0
  modify-lifecycle: 1.0.0
  refactor-lifecycle: 1.0.0
  deprecate-lifecycle: 1.0.0
```

This is the real product contract.

---

## Chunk 4: CLI Orchestration Plan

### Task 6: Turn `specify-extend` into the bundle installer

**Files:**
- Modify: `specify_extend.py`
- Modify: `test_specify_extend.py`
- Modify: `README.md`
- Modify: `INSTALLATION.md`

- [ ] **Step 1: Add package descriptors**

Add two registries in the CLI:

- extension package registry
- workflow package registry

Each entry should include:

- id
- type (`extension` or `workflow`)
- source URL or local subtree path
- required spec-kit version
- prerequisites
- bundle membership

- [ ] **Step 2: Add bundle selection logic**

Implement a `--bundle` style UX with values:

- `core`
- `standard`
- `full`
- `standard-with-workflows`
- `full-with-workflows`

- [ ] **Step 3: Add workflow installation execution**

After required extensions are installed, run:

```bash
specify workflow add <path-or-url>
```

for each selected workflow package.

- [ ] **Step 4: Add install reporting**

Print a summary grouped by type:

- extensions installed
- workflows installed
- skipped because already installed
- failed with reason

- [ ] **Step 5: Add tests**

Add tests covering:

- bundle expansion
- install ordering
- workflow install invocation
- skip/idempotency behavior
- failure on missing prerequisite extension

---

## Chunk 5: Migration and Compatibility

### Task 7: Migrate without breaking users

**Files:**
- Modify: `README.md`
- Modify: `INSTALLATION.md`
- Modify: `CHANGELOG.md`
- Modify: `extension.yml`

- [ ] **Step 1: Preserve current aliases first**

Keep current commands and aliases working while packages are being split.

- [ ] **Step 2: Publish workflows as additive first**

Do not remove current command-based lifecycle flows until the standalone workflow packages and CLI bundle installs are proven in real usage.

- [ ] **Step 3: Deprecate by documentation before removal**

If a capability moves from extension command surface to workflow package surface, document that first and keep the old path available for at least one transition release.

- [ ] **Step 4: Keep namespace ownership crisp**

Rules:

- extension command IDs always stay inside that extension's namespace
- workflow IDs are standalone and do not mirror extension command shapes unnecessarily
- orchestration belongs in workflow packages, not in extension command sprawl

---

## Recommended First Execution Slice

Implement this slice first because it proves the architecture with the least blast radius:

1. Keep the current repo as-is for commands and templates.
2. Treat the existing lifecycle workflow assets as the future standalone workflow packages.
3. Add workflow package metadata to the CLI.
4. Teach `specify-extend` to install the four lifecycle workflows after the existing extension.
5. Validate that `standard-with-workflows` works end-to-end.

That proves the orchestrator model before any extension extraction work starts.

## Decision Summary

- Use **multiple extensions** for domain boundaries.
- Use **standalone workflow packages** for lifecycle orchestration.
- Use **git subtree** for vendoring published package repos back into the umbrella repo.
- Use **`specify-extend` as the product orchestrator** so users still experience a single curated install surface.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-15-modular-packaging-split.md`. Ready to execute?