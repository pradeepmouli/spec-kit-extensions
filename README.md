# spec-kit-extensions

**11 production-tested workflows that extend [spec-kit](https://github.com/github/spec-kit) to cover the complete software development lifecycle.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What Is This?

**spec-kit** provides structured workflows for feature development (`/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement`). These extensions add 11 additional workflows for the remaining ~75% of software development work:

### Workflow Extensions (full spec-kit workflow with branch, specs, and templates)

- **`/speckit.workflows.bugfix`** - Fix bugs with regression-test-first approach
- **`/speckit.workflows.hotfix`** - Handle production emergencies with expedited process
- **`/speckit.workflows.enhance`** - Make minor enhancements with streamlined single-doc workflow
- **`/speckit.workflows.refactor`** - Improve code quality with metrics tracking
- **`/speckit.workflows.deprecate`** - Sunset features with phased 3-step rollout
- **`/speckit.workflows.modify`** - Modify existing features with automatic impact analysis
- **`/speckit.workflows.baseline`** - Establish project baseline and track all changes
- **`/speckit.workflows.cleanup`** - Validate and reorganize spec-kit artifacts

### Command Extensions (provide commands without workflow structure)

- **`/speckit.workflows.review`** - Review completed work with structured feedback
- **`/speckit.workflows.phasestoissues`** - Create individual GitHub issues for each development phase
- **`/speckit.workflows.incorporate`** - Incorporate documents into workflows

> **Note:** All commands also have short aliases (e.g., `/speckit.bugfix` instead of `/speckit.workflows.bugfix`).

## Why Use These Extensions?

### The Problem

With vanilla spec-kit, you get structure for ~25% of your work (new features), but the remaining 75% happens ad-hoc:

- **Bugs**: No systematic approach → regressions happen
- **Feature changes**: No impact analysis → breaking changes
- **Code quality**: No metrics → unclear if refactor helped
- **Emergencies**: No process → panic-driven development
- **Feature removal**: No plan → angry users

### The Solution

These extensions bring spec-kit's structured approach to all development activities:

| Activity | Without Extensions | With Extensions |
|----------|-------------------|-----------------|
| **New Feature** | `/speckit.specify` workflow | Same |
| **Project Baseline** | Ad-hoc | `/speckit.workflows.baseline` with comprehensive docs |
| **Bug Fix** | Ad-hoc | `/speckit.workflows.bugfix` with regression tests |
| **Minor Enhancement** | Ad-hoc | `/speckit.workflows.enhance` with streamlined planning |
| **Modify Feature** | Ad-hoc | `/speckit.workflows.modify` with impact analysis |
| **Refactor Code** | Ad-hoc | `/speckit.workflows.refactor` with metrics |
| **Production Fire** | Panic | `/speckit.workflows.hotfix` with post-mortem |
| **Remove Feature** | Hope | `/speckit.workflows.deprecate` with 3-phase sunset |
| **Codebase Cleanup** | Manual | `/speckit.workflows.cleanup` with automation |
| **Work Review** | Inconsistent | `/speckit.workflows.review` with structured feedback |
| **GitHub Issues** | Manual | `/speckit.workflows.phasestoissues` with phase-level tracking |

## Quick Start

### Prerequisites

- **spec-kit** installed from source ([github.com/github/spec-kit](https://github.com/github/spec-kit)) — requires version with extension support (v0.2.0+)
- **AI coding agent** (Claude Code, GitHub Copilot, Gemini CLI, Cursor, etc.)
- **Git** repository

### Installation

**Step 1: Initialize spec-kit** (if not already done):
```bash
specify init --here --integration claude
```

`--ai` remains accepted for compatibility on current releases, but newer spec-kit versions prefer `--integration`.

**Step 2: Install extensions** (recommended):
```bash
# Install the CLI tool
pip install specify-extend
# or: uvx specify-extend --all

# Install all extensions
specify-extend --all
```

`specify-extend --all` is the **recommended installation method** until spec-kit natively supports alternate feature branch patterns (bugfix/, hotfix/, etc.). It:
1. Reconciles the requested AI agents via upstream `specify integration install`
2. Downloads and installs the extension via `specify extension add`
3. Patches spec-kit's `common.sh` to recognize extension branch patterns

If you want to align multiple agents before installing the workflow pack, you can do that in one step:

```bash
specify-extend --agents claude,copilot --all
```

**Alternative: Native spec-kit install** (advanced — does not patch branch patterns):
```bash
# Install extension only (no branch pattern support)
specify extension add workflows --from https://github.com/pradeepmouli/spec-kit-extensions/archive/refs/heads/main.zip

# Then manually patch branch patterns
specify-extend --patch
```

### Optional Companion Extensions

You can optionally have `specify-extend` install curated community extensions that complement this workflow pack.

```bash
# See curated companions
specify-extend --list-community

# Install this extension + recommended companions
specify-extend --all --with-community recommended

# Install this extension + specific companions
specify-extend --all --with-community worktree,spec-refine

# Preview without changes
specify-extend --all --with-community recommended --dry-run
```

Supported selectors for `--with-community`:

- `recommended` — installs a curated default set
- `all` — installs every curated community extension
- Comma-separated keys — installs only selected companions

Replacement keys for overlapping workflows:

- `review-plus` — community replacement candidate for `/speckit.review`
- `cleanup-plus` — community replacement candidate for `/speckit.cleanup`
- `bugfix-artifacts` — community bugfix workflow focused on in-place artifact patching

GitHub issue companion note:

- `github-issues` complements, but does not replace, this extension's native issue-sync hooks.
- Use `github-issues` for issue import, spec linkage, and manual spec-to-issue synchronization.
- Use native issue sync for lifecycle status/label updates at workflow boundaries (`before_*` / `after_*`).

Deprecation note:

### Optional Workflow Packages

For spec-kit `0.7.0+`, you can also have `specify-extend` install curated standalone workflow-engine packages alongside the extension.

```bash
# See curated workflow packages
specify-extend --list-workflows

# Install this extension + recommended workflow packages
specify-extend --all --with-workflows recommended

# Install this extension + specific workflow packages
specify-extend --all --with-workflows bugfix-lifecycle,enhance-lifecycle

# Preview without changes
specify-extend --all --with-workflows recommended --dry-run
```

Supported selectors for `--with-workflows`:

- `recommended` — installs the curated default workflow set
- `all` — installs every curated workflow package
- `none` — skips workflow package installation
- Comma-separated keys — installs only selected workflow packages

Current curated workflow packages:

- `bugfix-lifecycle`
- `enhance-lifecycle`
- `modify-lifecycle`
- `refactor-lifecycle`
- `hotfix-lifecycle`
- `deprecate-lifecycle`

Local development install mode:

```bash
# Install the extension from your local checkout instead of GitHub
specify-extend --all --extension-source ../spec-kit-extensions

# Combine local extension install with local workflow package files
specify-extend --all --extension-source ../spec-kit-extensions --with-workflows recommended
```

When `--extension-source` is used, `specify-extend` stages a sanitized temporary copy of that checkout before running `specify extension add --dev`. This avoids recursive copies of generated `.specify` state while still letting you validate unpushed local changes.

When `--ai` or `--agents` is provided, `specify-extend` first runs upstream `specify integration install` for those agent keys before installing this extension. That keeps base Spec Kit integration state aligned with the requested targets.

- `review` and `cleanup` in this extension are soft-deprecated and remain installable for compatibility.
- Prefer companion installs (`review-plus`, `cleanup-plus`) for new projects.

### Why The CLI Still Patches Branch Validation

Spec Kit core branch validation still accepts numeric/timestamp feature branches by default. This extension introduces typed workflow branches (`bugfix/`, `hotfix/`, `refactor/`, etc.), so `specify-extend` patches branch validation until Spec Kit natively supports extension-registered branch patterns.

### Verify Installation

```bash
# Check extension is installed
specify extension list

# Should show:
#   Spec Kit Workflow Extensions (v3.4.1)
#   Commands: 19 | Status: Enabled

# Try a command:
/speckit.workflows.bugfix "test bug"
# Or use the alias:
/speckit.bugfix "test bug"
```

### Post-Installation Structure

After installation, your project will have:

```
your-project/
├── .specify/
│   ├── extensions/
│   │   └── workflows/           # Extension install directory
│   │       ├── extension.yml    # Extension manifest
│   │       ├── commands/        # 19 command files (11 user + hook helpers)
│   │       │   ├── bugfix.md
│   │       │   ├── hotfix.md
│   │       │   ├── issue-sync-before-specify.md
│   │       │   └── ...
│   │       ├── scripts/
│   │       │   ├── bash/        # Bash create scripts + utils
│   │       │   └── powershell/  # PowerShell create scripts
│   │       └── templates/       # Workflow templates
│   │           ├── bugfix/
│   │           ├── hotfix/
│   │           └── ...
│   ├── scripts/bash/
│   │   └── common.sh            # Patched with extension branch support
│   └── memory/
│       └── constitution.md
└── .claude/commands/             # Agent-specific command files (auto-generated)
```

## Usage

### Quick Decision Tree

```
Starting with spec-kit?
└─ Use /speckit.workflows.baseline to establish project context

Building something new?
├─ Major feature → /speckit.specify "description"
└─ Minor enhancement → /speckit.workflows.enhance "description"

Fixing broken behavior?
├─ Production emergency → /speckit.workflows.hotfix "incident"
└─ Non-urgent bug → /speckit.workflows.bugfix "bug description"

Changing existing feature?
├─ Adding/modifying behavior → /speckit.workflows.modify 014 "change"
└─ Improving code quality → /speckit.workflows.refactor "improvement"

Removing a feature?
└─ /speckit.workflows.deprecate 014 "reason"

Reviewing completed work?
└─ /speckit.workflows.review [task-id]

Creating GitHub issues?
└─ /speckit.workflows.phasestoissues
```

### Example: Fix a Bug

```bash
# Step 1: Create bug report
/speckit.workflows.bugfix "profile form crashes when submitting without image"
# Creates: bug-report.md with initial analysis

# Step 2: Investigate and update bug-report.md with root cause

# Step 3: Create fix plan
/speckit.plan

# Step 4: Break down into tasks
/speckit.tasks

# Step 5: Execute fix
/speckit.implement
```

### Example: Modify Existing Feature

```bash
# Step 1: Create modification spec with impact analysis
/speckit.workflows.modify 014 "make profile fields optional"
# Creates: modification-spec.md + impact-analysis.md

# Step 2: Review impact analysis

# Step 3-5: Plan, tasks, implement (same as above)
```

### Native Hook Issue Sync

The extension runs mandatory lifecycle hook syncing for linked GitHub issues at:

- `before_specify`, `after_specify`
- `before_plan`, `after_plan`
- `before_tasks`, `after_tasks`
- `before_implement`, `after_implement`

Hook commands call `scripts/bash/update-linked-issue.sh`, which:

- Resolves the linked issue (PR closing references, feature docs, or explicit env var)
- Applies event-specific labels
- Optionally posts event status comments
- Optionally bootstraps missing labels in the target repository

Configuration files installed with the extension:

- `.specify/extensions/workflows/workflows-config.yml`
- `.specify/extensions/workflows/issue-sync.env`

Use `issue-sync.env` to customize per-event mappings (`SPECKIT_ISSUE_SYNC_LABEL_*` and `SPECKIT_ISSUE_SYNC_STATUS_*`).

If you also install the optional `github-issues` companion, treat responsibilities separately:

- `github-issues` owns importing issues into specs and syncing spec content when source issues change.
- Native issue sync owns workflow-phase signaling on the linked issue (labels, status text, optional comments).

## Workflow Cheat Sheet

| Workflow | Command | Alias | Key Feature |
|----------|---------|-------|-------------|
| **Feature** | `/speckit.specify "..."` | — | Full spec + design |
| **Baseline** | `/speckit.workflows.baseline` | `/speckit.baseline` | Context tracking |
| **Bugfix** | `/speckit.workflows.bugfix "..."` | `/speckit.bugfix` | Regression test |
| **Enhance** | `/speckit.workflows.enhance "..."` | `/speckit.enhance` | Single-doc workflow |
| **Modify** | `/speckit.workflows.modify 014 "..."` | `/speckit.modify` | Impact analysis |
| **Refactor** | `/speckit.workflows.refactor "..."` | `/speckit.refactor` | Baseline metrics |
| **Hotfix** | `/speckit.workflows.hotfix "..."` | `/speckit.hotfix` | Post-mortem |
| **Deprecate** | `/speckit.workflows.deprecate 014 "..."` | `/speckit.deprecate` | 3-phase sunset |
| **Cleanup** | `/speckit.workflows.cleanup` | `/speckit.cleanup` | Automated validation |
| **Review** | `/speckit.workflows.review` | `/speckit.review` | Structured feedback |
| **Phases→Issues** | `/speckit.workflows.phasestoissues` | `/speckit.phasestoissues` | GitHub integration |
| **Incorporate** | `/speckit.workflows.incorporate` | `/speckit.incorporate` | Doc integration |

## Workflow Engine Assets

For spec-kit `0.7.0+`, this repo also includes standalone workflow-engine definitions under [workflows](workflows/README.md).

- [workflows/bugfix-lifecycle/workflow.yml](workflows/bugfix-lifecycle/workflow.yml)
- [workflows/enhance-lifecycle/workflow.yml](workflows/enhance-lifecycle/workflow.yml)
- [workflows/modify-lifecycle/workflow.yml](workflows/modify-lifecycle/workflow.yml)
- [workflows/refactor-lifecycle/workflow.yml](workflows/refactor-lifecycle/workflow.yml)
- [workflows/hotfix-lifecycle/workflow.yml](workflows/hotfix-lifecycle/workflow.yml)
- [workflows/deprecate-lifecycle/workflow.yml](workflows/deprecate-lifecycle/workflow.yml)

These workflows orchestrate the existing extension commands with explicit review gates and an optional implement step.

They are additive:

- Keep using `/speckit.workflows.*` commands for direct manual flow.
- Use `specify workflow run .../workflow.yml` when you want explicit gates and resume support.
- Install them directly with `specify workflow add ...` or via `specify-extend --with-workflows ...`.
- Install the extension first; upstream extension installs still do not auto-install workflow assets.

Example:

```bash
specify workflow run workflows/bugfix-lifecycle/workflow.yml --input request="login button broken on mobile" --input integration=copilot
```

## Compatibility

### spec-kit Versions

- **Required**: spec-kit v0.3.1+ (with extension system support)
- **Tested**: spec-kit v0.5.1, v0.6.0, v0.7.0, v0.7.4, and v0.8.0
- Install from source: `uv tool install specify-cli --from "git+https://github.com/github/spec-kit.git"`

### AI Agents

Commands are registered by spec-kit's extension system and work with any supported agent:

| Agent | Status |
|-------|--------|
| Claude Code | Supported |
| GitHub Copilot | Supported |
| Cursor | Supported |
| Windsurf | Supported |
| Gemini CLI | Supported |
| Codex CLI | Supported |
| Amazon Q Developer CLI | Supported |

### Component Versions

- **Extension** (v3.4.1) — Workflows, commands, templates, and scripts
- **CLI Tool** (v2.5.3) — `specify-extend` installation and patching tool

## FAQ

### Do I need to use all 11 workflows?

No! Use only what you need. Common combinations:
- **Minimal**: Just `bugfix` (most teams need this)
- **Standard**: `bugfix` + `enhance` + `modify` (covers most scenarios)
- **Complete**: All 11 workflows (full lifecycle coverage)

### Why use `specify-extend --all` instead of `specify extension add`?

`specify-extend --all` additionally patches spec-kit's `common.sh` to support extension branch patterns (`bugfix/`, `hotfix/`, `refactor/`, etc.). Without this patch, spec-kit's branch validation will reject these branch names. Once spec-kit natively supports alternate branch patterns, `specify extension add` alone will be sufficient.

### Can I customize the workflows?

Yes! After installation, all files are in `.specify/extensions/workflows/`. Edit templates, commands, or scripts to suit your needs.

### Do these work without Claude Code?

Yes! The workflows are **agent-agnostic**. They work with any AI agent that supports spec-kit.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License — Same as spec-kit. See [LICENSE](LICENSE).

## Credits

Built for the spec-kit community by developers who wanted structured workflows for more than just new features.

- [GitHub spec-kit team](https://github.com/github/spec-kit) for the foundation
- Early adopters who tested these workflows in production

## Support

- **Issues**: [GitHub Issues](https://github.com/pradeepmouli/spec-kit-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pradeepmouli/spec-kit-extensions/discussions)
- **spec-kit**: [Original spec-kit repo](https://github.com/github/spec-kit)
