# Changelog

All notable changes to the Specify Extension System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Note**: This project has two versioned components:
- **Extension Templates** (workflows, commands, scripts) - Currently at v3.4.0
- **CLI Tool** (`specify-extend`) - Currently at v2.5.0

## CLI Tool (`specify-extend`)

### [Unreleased]

### [2.5.0] - 2026-04-15

#### 🧹 Removed (dead code cleanup)

- Removed `install_agent_commands()` — superseded by spec-kit native `specify extension add` delegation
- Removed `install_extension_skills()` and `_get_extension_skills_dir()` — spec-kit `CommandRegistrar` handles skill installation
- Removed all `_convert_handoffs_*` helper functions (8 functions, ~370 lines) — agent-specific handoff conversion delegated to spec-kit
- Removed `AGENTS_WITH_HANDOFF_SUPPORT`, `AGENT_SKILLS_DIR_OVERRIDES`, `DEFAULT_SKILLS_DIR`, `EXTENSION_SKILL_DESCRIPTIONS` constants
- Removed `--ai-skills` CLI flag — spec-kit handles skills installation natively via `CommandRegistrar`

### [Unreleased]

#### 🚀 Added

- **Curated community companion installs**
  - New `--list-community` option to view curated companion extensions
  - New `--with-community` option to install `recommended`, `all`, or selected companion keys
  - Companion installs run via native spec-kit command: `specify extension add <id> --from <url>`
- **Standalone workflow-engine assets for spec-kit 0.7.0+**
  - Added local workflow definitions for `bugfix`, `modify`, `refactor`, and `deprecate`
  - Each workflow orchestrates the existing extension commands with explicit review gates and an optional implement step
  - Workflows are shipped as standalone assets under `workflows/` because the current extension system does not yet install workflow packages

#### 🔧 Changed/Improved

- **Kimi skills compatibility shim (spec-kit 0.4.3+)**
  - Canonical Kimi skills now install to shared `.agents/skills` with hyphenated names
  - Automatic legacy alias shim writes dotted skill names under `.kimi/skills` when missing
- **Upstream integration reconciliation is now opt-in by flag usage**
  - `specify integration install` is only validated and invoked when the user explicitly passes `--ai` or `--agents`
  - Restores the previous contract for plain `specify-extend --all` installs against older compatible spec-kit CLIs
- **`common.sh` patch now wraps upstream validation instead of replacing it**
  - The injected `check_feature_branch()` allows extension branch prefixes first, then delegates standard validation back to spec-kit's shipped implementation via `check_feature_branch_old`
  - Reduces risk of drifting from upstream `common.sh` behavior as spec-kit evolves
- **Issue sync lifecycle hooks are mandatory**
  - Hook events `before_*`/`after_*` for specify/plan/tasks/implement are now non-optional in `extension.yml`
- **Canonical extension command namespaces for spec-kit 0.7.0**
  - Renamed noncanonical primary command ids in `extension.yml` under the `speckit.workflows.*` namespace
  - Preserved legacy `speckit.issuesync.*` and `speckit.ultraplan.tasks` names as aliases for backward compatibility
  - Updated hook references to point at canonical command ids expected by newer spec-kit validation

#### 📦 Components

- **CLI Tool Version**: v2.5.0
- **Compatible Spec Kit Version**: v0.3.1+ (tested with v0.7.0)
- **Extension Templates Version**: v3.4.0

#### 📦 Compatibility

- **Tested Spec Kit Versions**: v0.5.1, v0.6.0, v0.7.0


### [2.2.1] - 2026-03-18

#### 🔧 Changed/Improved

- **Template Tag Discovery** - `download_latest_release()` now recognizes both legacy `templates-v*` tags and the newer `v*` template tags
  - Keeps older template releases installable while aligning the CLI with catalog metadata that points at `v3.x` archives
  - Selects the highest semantic template version instead of depending on GitHub tag ordering

#### 📦 Components

- **CLI Tool Version**: v2.2.1
- **Compatible Spec Kit Version**: v0.3.1+
- **Extension Templates Version**: v3.2.0

---

### [2.2.0] - 2026-03-14

#### 🚀 Added

- **spec-kit v0.3.0 Compatibility** - Alignment with spec-kit 0.3.0 features
  - Read agent from `init-options.json` (spec-kit 0.3.0+) for reliable detection before falling back to directory scanning
  - New `detect_agent_from_init_options()` function reads `.specify/init-options.json`

#### 🔧 Changed/Improved

- **Qwen Code CLI**: Changed `file_extension` from `toml` to `md` — Qwen migrated to Markdown in spec-kit 0.3.0
- **Gemini CLI**: Changed `file_extension` from `toml` to `md` — Gemini migrated to Markdown in spec-kit 0.3.0
- **TOML fallback removed**: Removed TOML fallback warning since no agents use TOML format anymore

#### ⚠️ Deprecated

- **agy (Antigravity)**: Marked as deprecated in AGENT_CONFIG — spec-kit 0.3.0 dropped explicit agy command support. A deprecation warning is now emitted when `--ai agy` is used.

#### 📦 Components

- **CLI Tool Version**: v2.2.0
- **Compatible Spec Kit Version**: v0.2.0+ (tested with v0.3.0)
- **Extension Templates Version**: v3.1.0

---

### [1.6.0] - 2026-03-11

#### 🚀 Added

- **spec-kit v0.2.0 Compatibility** - Full support for spec-kit v0.2.0+ features
  - 13 new AI agents added to AGENT_CONFIG: `tabnine`, `kimi`, `kiro-cli`, `vibe`, `shai`, `bob`, `agy`, `kilocode`, `roo`, `codebuddy`, `qodercli`, `auggie`, `amp`
  - Automatic detection for all new agents in `detect_agent()`
  - Copilot command files now use `.agent.md` extension (matching spec-kit v0.1.13+ behavior)
  - Codex commands moved to `.codex/prompts/` folder (matching spec-kit structure)

- **Global Branch Numbering** - Extension scripts now use global spec numbering (mirrors spec-kit v0.2.0)
  - All `create-*.sh` scripts (bugfix, hotfix, enhance, refactor, deprecate) now count across ALL workflow types and feature branches
  - New `get_global_next_number()` and `get_global_highest_number()` functions in `common.sh`
  - Prevents number collisions between feature branches (001-foo) and extension branches (bugfix/001-bar)

- **Agent Skills Support** (`--ai-skills`) - Install extension commands as agent skills (mirrors spec-kit's `--ai-skills`)
  - New `install_extension_skills()` function writes `SKILL.md` per command following [agentskills.io](https://agentskills.io/specification) spec
  - Skills placed in agent's `{base_folder}/skills/{skill_name}/SKILL.md`
  - `EXTENSION_SKILL_DESCRIPTIONS` with rich descriptions for all 10 extension commands
  - Additive installs — never overwrites user-customized skills
  - `AGENT_SKILLS_DIR_OVERRIDES` for special agents (Codex, Amp → `.agents/skills`)
  - Affects: `specify_extend.py` (new functions and constants)

- **CLI Alignment with spec-kit** - Parameters now match `specify init` conventions
  - `--ai` is the new primary agent selector (replacing `--agent`, now hidden/deprecated)
  - `--ai-skills` flag to install extension commands as agent skills
  - `--ai-commands-dir` for generic agents (mirrors spec-kit's `--ai-commands-dir`)
  - `--agent` remains functional but hidden from help output for backward compatibility

#### 📦 Components

- **CLI Tool Version**: v1.6.0
- **Compatible Spec Kit Version**: v0.2.0+
- **Extension Templates Version**: v2.5.11

---

### [1.5.12] - 2026-02-02

#### 🔧 Changed/Improved

- **Workflow Symlink Simplification** - Reduced symlinks for spec-first workflows
  - Removed `plan.md` and `tasks.md` symlinks from bugfix, deprecate, modify, and refactor workflows
  - These workflows now only symlink `spec.md` to their primary document
  - Rationale: These are spec-first workflows where plan and tasks are created after the spec
  - Affects: `scripts/create-bugfix.sh`, `scripts/create-deprecate.sh`, `scripts/create-modification.sh`, `scripts/create-refactor.sh`

#### 📦 Components

- **CLI Tool Version**: v1.5.12
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.11

---

### [1.5.11] - 2026-01-27

#### 🔧 Changed/Improved

- **Review Workflow Quality Gate: Placeholder/TODO Detection** - Enhanced review workflow to flag incomplete code
  - Added placeholder/TODO/FIXME detection to review checklist
  - New quality gate: No placeholder/TODO/FIXME code in reviewed scope unless justified and tracked
  - Reviewers now explicitly confirm reviewed code contains no placeholder text
  - Supports identification of incomplete implementations during code review
  - Affects: `commands/speckit.review.md`

#### 📦 Components

- **CLI Tool Version**: v1.5.11
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.9

---

### [1.5.10] - 2026-01-18

#### 🔧 Changed/Improved

- **Extension Rename: story-to-issue → phasestoissues** - Renamed for consistency with spec-kit naming conventions
  - Updated `WORKFLOW_EXTENSIONS` list: `story-to-issue` → `phasestoissues`
  - Matches spec-kit convention (e.g., `taskstoissues` without hyphens)
  - Conceptual shift: One issue per development phase (vs. one per story)
  - Affects: `specify_extend.py`

#### 📦 Components

- **CLI Tool Version**: v1.5.10
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.8

---

### [1.5.9] - 2026-01-18

#### 🚀 Added

- **PhasesToIssues Workflow Integration** - New command for creating GitHub issues from development phases
  - Added `phasestoissues` to `WORKFLOW_EXTENSIONS` list
  - New command file: `commands/speckit.phasestoissues.md`
  - Supports phase-level GitHub issue creation workflow
  - Affects: `specify_extend.py` (AVAILABLE_EXTENSIONS, WORKFLOW_EXTENSIONS)

- **Agent Handoffs Constant** - Centralized agent capability tracking
  - Added `AGENTS_WITH_HANDOFF_SUPPORT` module-level constant
  - Defines agents supporting handoffs in frontmatter: Copilot, OpenCode, Windsurf
  - Replaces duplicated inline lists across codebase
  - Affects: `specify_extend.py` (agent detection logic)

#### 🔧 Changed/Improved

- **Agent-Specific Handoffs Frontmatter** - Enhanced support for agents using YAML frontmatter
  - Improved handoffs processing for Copilot, OpenCode, and Windsurf agents
  - Better YAML parsing for handoffs removal (replaces regex-based approach)
  - Simplified handoffs removal using `pop()` method for cleaner code
  - More robust handling of agent-specific configuration formats
  - Affects: `specify_extend.py` (frontmatter processing functions)

#### 📦 Components

- **CLI Tool Version**: v1.5.9
- **Compatible Extension Templates**: v2.5.5+
- **Compatible Spec Kit Version**: v0.0.80+

---

### [1.5.8] - 2026-01-02

#### 🚀 Added

- **AI Agent Branch Support** - Relaxed feature branch check for agent-generated branches
  - Branches starting with `claude/`, `copilot/`, `cursor/`, `vscode/`, `windsurf/`, `gemini/`, `qwen/` now bypass validation
  - Allows AI agents to use their own branch naming conventions
  - Affects: `patch_common_sh()` and `patch_common_ps1()` in specify_extend.py
  - Updated error messages to include agent branch pattern examples
  - Patch detection logic updated to recognize agent prefix support

#### 📦 Components

- **CLI Tool Version**: v1.5.8
- **Compatible Extension Templates**: v2.5.5+

---

## Extension Templates

### [3.4.0] - 2026-04-15

#### 🚀 Added

- **Standalone workflow-engine assets for spec-kit 0.7.0+**
  - Added bundled lifecycle workflow definitions for `bugfix`, `enhance`, `modify`, `refactor`, `hotfix`, and `deprecate`
  - Added workflow READMEs plus a top-level `workflows/README.md` explaining direct `specify workflow run` usage

#### 🔧 Changed/Improved

- **Canonical command namespaces for spec-kit 0.7.0**
  - Promoted `speckit.workflows.ultraplan-tasks` and `speckit.workflows.issue-sync-*` as canonical command ids in `extension.yml`
  - Preserved legacy aliases for backward compatibility
  - Updated hook registrations to point at the canonical names expected by newer spec-kit validation
- **Documentation refresh for workflow packages and installs**
  - Updated install docs and README examples to describe workflow package support, issue-sync boundaries, and current version metadata

#### 📦 Components

- **Extension Templates Version**: v3.4.0
- **Compatible Spec Kit Version**: v0.3.1+ (tested with v0.7.0)
- **Compatible specify-extend**: v2.5.0+

---

### [3.2.1] - 2026-03-21

#### 🚀 Added

- **Native Issue Sync Lifecycle Hooks** - Added linked issue synchronization across native spec-kit lifecycle boundaries
  - Added hook handlers for `before_specify`, `after_specify`, `before_plan`, `after_plan`, `before_tasks`, `after_tasks`, `before_implement`, and `after_implement`
  - Registered dedicated issue sync commands under the `speckit.issuesync.*` namespace
  - Added `scripts/bash/update-linked-issue.sh` with linked issue resolution (PR references, feature docs, branch fallback)
  - Supports optional GitHub label bootstrapping and optional status comments via configuration

- **Issue Sync Configuration Template**
  - Added `config/issue-sync.template.env` for per-event label/status mapping and repository overrides
  - Added `issue_sync` defaults and documentation guidance in workflow config templates

- **Project Automation Workflows**
  - Added GitHub Actions for project phase sync and PR merge issue closure automation
  - Updated spec-ready notification flow to align with project automation changes

#### 🔧 Changed/Improved

- **Extension Hook Organization** - Hook-only commands are now separated from workflow commands by namespace
  - Moved issue sync hook command registrations from `speckit.workflows.*` to `speckit.issuesync.*`
  - Preserves clear boundary between workflow creation commands and lifecycle synchronization commands

- **Documentation Refresh**
  - Updated README install/structure notes and hook behavior documentation for issue sync support
  - Refreshed installation/extension docs and local housekeeping updates

#### 📦 Components

- **Extension Templates Version**: v3.2.1
- **Compatible Spec Kit Version**: v0.3.1+
- **Compatible specify-extend**: v2.2.1+

---

### [3.2.0] - 2026-03-18

#### 🚀 Added

- **Workflow Configuration Template** - Added project-level workflow configuration template
  - New `config/workflows-config.template.yml` for configure-on-install behavior
  - Supports enhancement task limits plus bugfix and review quality-gate settings
  - Exposed through `provides.config` in `extension.yml`

- **Review Hooks and Defaults** - Added extension-level hooks and default values in `extension.yml`
  - `after_tasks`, `after_implement`, and `before_commit` can now invoke the review workflow
  - Added defaults for enhancement sizing, regression-test expectations, and review checklist behavior

#### 🔧 Changed/Improved

- **spec-kit v0.3.1 Compatibility** - Minimum supported spec-kit version is now `>=0.3.1`
  - Updated extension metadata in `extension.yml` and `catalog-entry.json`

- **Configurable Enhancement Scope** - The enhancement workflow now resolves task limits from defaults, project config, or environment
  - `commands/enhance.md` now instructs agents to honor `min_tasks` and `max_tasks`
  - `scripts/bash/create-enhance.sh` emits resolved `MAX_TASKS` and `MIN_TASKS` values in both human-readable and JSON output

- **Preset-Aware Template Resolution** - Workflow creation scripts now use `resolve_workflow_template()`
  - Delegates to spec-kit's preset-aware `resolve_template()` when available
  - Falls back to bundled extension templates for older installations and local development

- **Bash Script Hardening** - All workflow creation scripts now use `set -euo pipefail`
  - Aligns with spec-kit 0.3.x bash hardening expectations

- **Agent Prefix Coverage** - Added `trae/`, `codex/`, and `opencode/` to the extension branch helper allowlist

#### 📦 Components

- **Extension Templates Version**: v3.2.0
- **Compatible Spec Kit Version**: v0.3.1+
- **Compatible specify-extend**: v2.2.1+

---

### [2.5.11] - 2026-02-02

#### 🔧 Changed/Improved

- **Workflow Symlink Simplification** - Reduced symlinks for spec-first workflows
  - Removed `plan.md` and `tasks.md` symlinks from bugfix, deprecate, modify, and refactor workflows
  - These workflows now only symlink `spec.md` to their primary document
  - Rationale: These are spec-first workflows where plan and tasks are created after the spec
  - Affects: `scripts/create-bugfix.sh`, `scripts/create-deprecate.sh`, `scripts/create-modification.sh`, `scripts/create-refactor.sh`

#### 📦 Components

- **Extension Templates Version**: v2.5.11
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.12+

---

### [2.5.10] - 2026-01-29

#### 🚀 Added

- **PhasesToIssues Sub-Issues** - Enhanced phasestoissues workflow to create task sub-issues
  - Each task now becomes its own GitHub issue linked as a sub-issue to the parent phase
  - Uses GitHub's native sub-issues API (`mcp_github_github_sub_issue_write`)
  - Task issues preserve spec-kit task IDs (e.g., "T001: Create architecture diagram")
  - Enables individual task assignment and task-level discussions
  - Parent phase issues auto-update status based on sub-issue completion
  - Benefits: Better delegation, parallel work at task level, cleaner phase issue UI
  - Affects: `commands/speckit.phasestoissues.md`, `docs/phasestoissues.md`, `extensions/workflows/phasestoissues/README.md`

#### 📦 Components

- **Extension Templates Version**: v2.5.10
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.11+

---

### [2.5.9] - 2026-01-27

#### 🔧 Changed/Improved

- **Review Workflow Quality Gate: Placeholder/TODO Detection** - Enhanced review workflow to flag incomplete code
  - Added placeholder/TODO/FIXME detection to review steps
  - New quality gate: No placeholder/TODO/FIXME code in reviewed scope unless justified and tracked
  - Updated review process documentation with explicit placeholder checking
  - Reviewers confirm reviewed code contains no incomplete placeholders
  - Affects: `extensions/workflows/review/README.md`

#### 📦 Components

- **Extension Templates Version**: v2.5.9
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.11+

---

### [2.5.8] - 2026-01-18

#### 🔧 Changed/Improved

- **Extension Rename: story-to-issue → phasestoissues** - Renamed for consistency with spec-kit naming conventions
  - Command renamed: `speckit.story-to-issue.md` → `speckit.phasestoissues.md`
  - Workflow directory renamed: `story-to-issue/` → `phasestoissues/`
  - Documentation renamed: `story-to-issue.md` → `phasestoissues.md`
  - Matches spec-kit convention (e.g., `taskstoissues` without hyphens)
  - Conceptual shift: One issue per development phase (vs. one per story)
  - Enables better parallelization and phase-based delegation
  - Affects: `commands/`, `extensions/workflows/`, `docs/`

#### 📦 Components

- **Extension Templates Version**: v2.5.8
- **Compatible Spec Kit Version**: v0.0.80+

---

### [2.5.7] - 2026-01-18

#### 🚀 Added

- **PhasesToIssues Workflow** - New workflow for creating GitHub issues from development phases
  - Added `extensions/workflows/phasestoissues/README.md`
  - New workflow directory structure for phase-level issue creation
  - Supports converting phase specs into properly formatted GitHub issues
  - Affects: `extensions/workflows/phasestoissues/` (new directory)

- **PhasesToIssues Command** - New command template for phase-level issue creation
  - Added `commands/speckit.phasestoissues.md`
  - Provides AI agent guidance for phasestoissues workflow
  - Integrates with GitHub issue creation process
  - Affects: `commands/speckit.phasestoissues.md` (new file)

#### 🔧 Changed/Improved

- **Incorporate Command** - Enhanced incorporate command documentation
  - Updated `commands/speckit.incorporate.md` with improved guidance
  - Better integration instructions and examples
  - Affects: `commands/speckit.incorporate.md`

#### 📦 Components

- **Extension Templates Version**: v2.5.7
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.9+

---

### [2.5.6] - 2026-01-07

#### 🔧 Changed/Improved

- **Standard Artifact Symlinks** - All workflows now create `spec.md`, `plan.md`, and `tasks.md` symlinks
  - Enables consistent tooling compatibility across all workflow types
  - Each workflow-specific file (e.g., `bug-report.md`, `enhancement.md`) symlinks to standard names
  - Supports both bash and PowerShell with graceful fallback
  - Affects:
    - Bash: `create-bugfix.sh`, `create-enhance.sh`, `create-hotfix.sh`, `create-refactor.sh`, `create-modification.sh`, `create-deprecate.sh`, `create-baseline.sh`
    - PowerShell: `create-bugfix.ps1`, `create-enhance.ps1`, `create-hotfix.ps1`, `create-refactor.ps1`, `create-modification.ps1`, `create-deprecate.ps1`, `create-baseline.ps1`

#### 📦 Components

- **Extension Templates Version**: v2.5.6
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.8+
    - PowerShell: `create-bugfix.ps1`, `create-enhance.ps1`, `create-hotfix.ps1`, `create-refactor.ps1`, `create-modification.ps1`, `create-deprecate.ps1`, `create-baseline.ps1`

#### 📦 Components

- **Extension Templates Version**: v2.5.6
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.7+

---

### [2.5.5] - 2025-12-29

#### 🚀 Added

- **Branch Utilities Helper** - Ship `branch-utils.sh` (bash) and `BranchUtils.ps1` (PowerShell) providing branch name generation
  - Decouples workflows from spec-kit's `common.sh` availability
  - Graceful fallback when older installations lack `generate_branch_name`
  - Affects: scripts/branch-utils.sh (new)

#### 🔧 Changed/Improved

- **Workflow Scripts** - Source branch utilities across bash and PowerShell workflows
  - Bash: `create-bugfix.sh`, `create-enhance.sh`, `create-modification.sh`, `create-hotfix.sh`, `create-refactor.sh`
  - Also bash: `create-deprecate.sh` and `create-baseline.sh` for consistency
  - PowerShell: `create-bugfix.ps1`, `create-enhance.ps1`, `create-modification.ps1`, `create-hotfix.ps1`, `create-refactor.ps1`
  - Also PowerShell: `create-deprecate.ps1` and `create-baseline.ps1` for consistency
  - Refactor script retains internal fallback for extra resilience

#### 📦 Components

- **Extension Templates Version**: v2.5.5
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.7+

### [2.5.4] - 2025-12-27

#### 🔧 Changed/Improved

- **Incorporate Command** - Enhanced handoff prompts and documentation clarity
  - Added detailed, context-rich prompts for all 11 handoff definitions
  - Improved guidance for workflow-specific incorporation strategies
  - Enhanced stage advancement handoffs with clearer instructions
  - Better integration with native spec-kit commands
  - More explicit about when to use /speckit.analyze for content merging
  - Affects: commands/speckit.incorporate.md (131 lines changed)

- **Documentation** - Improved constitution template clarity
  - Better formatting and organization of quality gates
  - Enhanced workflow descriptions
  - Clearer guidance for AI agents

#### 📦 Components

- **Extension Templates Version**: v2.5.4
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.5+

---

### [2.5.3] - 2025-12-26

#### 🚀 Added

- **Incorporate Command Extension** - New `/speckit.incorporate` command for intelligent document integration
  - Automatically detects document type (spec, plan, tasks, research, checklist, post-mortem)
  - Intelligently incorporates documents into existing workflows
  - Advances workflow stages automatically based on document type
  - Initiates new workflows from documents when not in a workflow
  - Leverages native `/speckit.analyze` for smart content merging
  - Complete handoff definitions for all 8 workflows + stage advancement
  - Affects: commands/speckit.incorporate.md (376 lines)

#### 🔧 Changed/Improved

- **Code Architecture** - Distinguished between workflow and command extensions
  - Added `WORKFLOW_EXTENSIONS` and `COMMAND_EXTENSIONS` constants
  - Created `is_workflow_extension()` and `is_command_extension()` helpers
  - Clearer separation of concerns in installation logic
  - Self-documenting code structure

- **Documentation** - Enhanced clarity about extension types
  - Explicitly lists "8 workflow extensions + 2 command extensions"
  - Separate sections for workflows vs commands in README
  - Updated activity tables with document integration use case

#### 🐛 Fixed

- **Review Extension Installation** - Fixed warning about missing create-review.sh
  - Review is a command extension, not a workflow extension
  - Skip review when copying scripts and workflow directories
  - Eliminates spurious installation warnings

#### 📦 Components

- **Extension Templates Version**: v2.5.3
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.4+

---

### [2.5.2] - 2025-12-26

#### 🔧 Changed/Improved

- **Windows Path Handling** - Improved path compatibility across different shell environments
  - Added backslash normalization in get_repo_root function
  - Better Git Bash compatibility for Windows users
  - Improved test coverage for Windows path scenarios
  - Affects: All scripts that use path resolution

- **Documentation and Testing** - Enhanced test coverage and documentation clarity
  - Added test cases for Windows paths with backslashes
  - Fixed find command option order for better compatibility
  - Improved copilot configuration documentation
  - Updated README with agent support details

#### 🐛 Fixed

- **Workflow Logic** - Fixed conditional logic in spec-kit-review workflows
  - Corrected workflow decision logic
  - Improved review reminder notifications
  - Better handling of review status checks
  - Affects: spec-kit-review-required.yml, spec-kit-review-reminder.yml

#### 📦 Components

- **Extension Templates Version**: v2.5.2
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.3+

---

### [2.5.1] - 2025-12-25

#### 🐛 Fixed

- **Script Path Resolution** - Fixed common.sh sourcing in all extension scripts
  - Scripts now check same directory first for common.sh
  - Resolves "generate_branch_name is not available" error
  - Fixes installation path compatibility with .specify/scripts/bash/
  - Affects: All create-*.sh scripts

#### 📦 Components

- **Extension Templates Version**: v2.5.1
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.2+

### [2.5.0] - 2025-12-25

#### ✨ New Features

- **Automatic Baseline Metrics** - Refactor workflow now automatically captures baseline metrics
  - Baseline metrics are captured immediately after spec creation
  - Eliminates manual step of running measure-metrics.sh --before
  - PowerShell version supports bash script execution
  - Affects: scripts/create-refactor.sh, scripts/powershell/create-refactor.ps1

#### 📚 Documentation

- Updated documentation to reflect automatic baseline capture
- Added fallback instructions if automatic capture fails
- Updated refactor command, README, and QUICKSTART guides

#### 📦 Components

- **Extension Templates Version**: v2.5.0
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.2+

### [2.4.1] - 2025-12-24

#### 🐛 Fixed

- **Documentation Accuracy** - Corrected workflow count from 8 to 9 in all README sections
  - Updated references to reflect the addition of the enhance workflow
  - Ensures documentation accurately represents all available workflows
  - Affects: README.md

#### 📦 Components

- **Extension Templates Version**: v2.4.1
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.1+

---

### [2.4.0] - 2025-12-24

#### 🚀 Added

- **Enhance Workflow** - New `/speckit.enhance` workflow for minor improvements and enhancements
  - Quick-turnaround improvements that don't require full feature specs
  - Creates enhancement-spec.md with problem statement, proposed changes, and verification steps
  - Lighter-weight alternative to full feature development
  - Templates include: enhancement-template.md
  - Script: `create-enhance.sh` with JSON output support
  - PowerShell support: `create-enhance.ps1`

#### 🔧 Changed/Improved

- **PowerShell Script Support** - Complete PowerShell implementation for all workflows
  - All 8 extension workflows now have PowerShell equivalents (.ps1)
  - Bash scripts remain at `.specify/scripts/bash/`, PowerShell at `.specify/scripts/powershell/`
  - Agent commands automatically reference correct script type based on `--script` flag
  - Consistent behavior with spec-kit's `--script ps` option
  - Affects: All workflow scripts (baseline, bugfix, cleanup, deprecate, enhance, hotfix, modify, refactor)

- **Documentation Improvements** - Enhanced setup and development documentation
  - Clarified that `specify init` (not `specify-extend`) creates `.specify/` directory structure
  - Added development symlink setup instructions in CONTRIBUTING.md
  - Updated README.md with two-step installation process
  - Added `.specify/` and `specs/` to .gitignore for development environments
  - Documented bash vs PowerShell handling

#### 🐛 Fixed

- **Script Type Consistency** - Fixed specify-extend to match spec-kit's either/or behavior
  - Changed from "always install bash + optionally PowerShell" to "install EITHER bash OR PowerShell"
  - Now consistent with `specify init --script sh` (bash only) and `--script ps` (PowerShell only)
  - Prevents mixed script installations that could cause confusion

_(No template changes yet)_

---

## CLI Tool (`specify-extend`)

### [Unreleased]

#### ✨ Added

- **Handoff Conversion System** - Automatically converts workflow delegation to agent-specific formats
  - Agents that support `handoffs:` frontmatter (Copilot, OpenCode, Windsurf) preserve it unchanged
  - **Claude Code**: Triple approach for maximum flexibility
    * Creates `.claude/agents/*.md` subagent files for direct invocation
    * Adds `hooks:` Stop hooks in frontmatter for programmatic suggestions
    * Adds "Recommended Next Steps" text section for manual guidance
  - **Codex**: Creates `.codex/skills/*.md` skill files + "Next Steps" section
  - **Cursor/Qwen/Amazon Q**: Converts to "Workflow Continuation" section with command hints
  - Added `_extract_handoffs_from_frontmatter()` to parse YAML handoffs data
  - Added `_convert_handoffs_to_next_steps()` for agent-specific text generation
  - Added `_convert_handoffs_to_hooks()` to convert handoffs to Claude Code hooks format
  - Added `_add_hooks_to_frontmatter()` to inject hooks into YAML frontmatter
  - Added `_convert_handoffs_for_agent()` as main conversion orchestrator
  - Added `_create_claude_subagent_from_handoff()` to create Claude Code subagent files
  - Added `_create_codex_skill_from_handoff()` to create Codex skill files
  - Added `_create_subagents_from_handoffs()` to orchestrate subagent/skill creation
  - Added `pyyaml` dependency to `pyproject.toml` for YAML parsing

- **True Workflow Delegation** - Claude Code and Codex now support actual delegatable agents/skills
  - **Claude Code**: Stop hooks programmatically suggest next steps after command completion
  - Subagents can be invoked directly: "Use the speckit.plan subagent to create a plan"
  - Claude sees hook suggestions and can automatically delegate to subagents
  - Skills are automatically discovered and invoked by Codex
  - Provides same workflow orchestration as GitHub Copilot handoffs, but agent-native
  - Subagent files are idempotent (won't overwrite existing custom subagents)
  - Hooks use `type: prompt` for LLM-based suggestions (no bash scripts required)

#### 🔧 Changed

- **Improved Agent Support** - Each agent now gets appropriate workflow continuation guidance
  - Previously: Handoffs were simply stripped for unsupported agents
  - Now: Handoffs are intelligently converted to textual guidance matching agent conventions
  - Benefits agents without frontmatter support (Claude Code, Codex, Cursor, Qwen, Amazon Q)

#### 📚 Documentation

- **AGENTS.md** - Comprehensive handoffs conversion documentation
  - Documents which agents support handoffs frontmatter (Copilot, OpenCode, Windsurf)
  - Documents conversion format for each agent type
  - Added conversion examples showing YAML → Markdown transformation
  - Updated "Agent-Specific Adaptations" section with conversion details

---

### [2.3.1] - 2025-12-23

#### 🔧 Improved

- **Branch Name Generation** - Updated all extension workflow scripts to use spec-kit's sophisticated branch name generation logic
  - Added stop word filtering (removes common words like "the", "a", "to", "for", etc.)
  - Added length filtering (removes words shorter than 3 characters)
  - Added smart acronym handling (preserves uppercase acronyms from original input)
  - Intelligent word selection (takes 3-4 most meaningful words)
  - Affects: `create-bugfix.sh`, `create-refactor.sh`, `create-hotfix.sh`, `create-modification.sh`
  - Example impact: "Fix the API authentication bug" → `bugfix/001-fix-api-authentication-bug` (was `bugfix/001-fix-the-api`)
- **Cleanup Workflow** - Detects workflow-prefixed directories placed at the wrong level and can auto-move them after confirmation; clarifies automatic vs agent-driven fixes and verification via `--dry-run`
  - Adds detection for misplaced workflow dirs (e.g., `bugfix-001-*` under `specs/`), proposes moves, and applies when approved
  - Keeps unknown dirs (e.g., `specs/copilot/`) visible as warnings so users decide how to handle them
  - Updated guidance for agents to confirm plans before applying fixes and to rerun `--dry-run` until clean
  - Affects: `scripts/create-cleanup.sh`, `extensions/workflows/cleanup/README.md`, `commands/speckit.cleanup.md`

#### 📦 Components

- **Extension Templates Version**: v2.3.1
- **Compatible Spec Kit Version**: v0.0.80+

---

### [2.3.0] - 2025-12-22

#### 🚀 Added

- **Baseline Workflow** - New `/speckit.baseline` workflow for establishing project context and tracking changes
  - Creates `baseline-spec.md` documenting project architecture, features, and structure
  - Creates `current-state.md` tracking all changes by workflow type
  - Automatically detects if specs exist and determines baseline commit
  - Provides comprehensive context for AI agents working on subsequent tasks
  - Templates include: baseline-spec-template.md, current-state-template.md
  - Script: `create-baseline.sh` with JSON output support

#### 📦 Components

- **Extension Templates Version**: v2.3.0
- **Compatible Spec Kit Version**: v0.0.80+

---

## CLI Tool (`specify-extend`)

### [1.5.7] - 2025-12-29

#### 🚀 Added

- **Helper Installation** - Installer now copies shared helpers
  - Copies `branch-utils.sh` to `.specify/scripts/bash/`
  - Ensures create-* workflows have `generate_branch_name` without relying on spec-kit updates

#### 📦 Components

- **CLI Tool Version**: v1.5.7
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.5

### [1.5.6] - 2025-12-27

#### 🔧 Changed/Improved

- **Multi-Agent Self-Destruct** - Enhanced enhance-constitution self-destruct instructions
  - Updated to list ALL agent directory patterns where files may exist
  - Covers copilot, claude, cursor, windsurf, opencode, amazon-q, codex
  - Handles multi-agent setups (e.g., `--agents claude,copilot,cursor-agent`)
  - Prevents leftover enhance-constitution files in any agent directory
  - Clearer bullet-point list of locations to check
  - Affects: specify_extend.py enhance-constitution generation

#### 📦 Components

- **CLI Tool Version**: v1.5.6
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.4

---

### [1.5.5] - 2025-12-27

#### 🐛 Fixed

- **Branch Validation** - Fixed missing workflow patterns in branch validation
  - Added support for `enhance/###-`, `cleanup/###-`, and `baseline/###-` patterns
  - Previously only recognized bugfix, modify, refactor, hotfix, deprecate patterns
  - Fixes "Not on a feature branch" error when using enhance, cleanup, or baseline workflows
  - Updated error message to show all 8 valid workflow branch patterns
  - Affects: specify_extend.py patch_common_sh() function

- **Patch Versioning** - Auto-update outdated common.sh patches
  - Detects if existing patched common.sh is missing new workflow patterns
  - Automatically restores from backup or removes old patched function
  - Re-applies updated patch with complete pattern support
  - Allows `specify-extend --all` to update existing installations seamlessly
  - No manual intervention needed to get latest patch improvements
  - Affects: specify_extend.py patch_common_sh() detection logic

#### 📦 Components

- **CLI Tool Version**: v1.5.5
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.4

---
### [1.5.5] - 2025-12-27

#### 🐛 Fixed

- **Branch Validation** - Fixed missing workflow patterns in branch validation
  - Added support for `enhance/###-`, `cleanup/###-`, and `baseline/###-` patterns
  - Previously only recognized bugfix, modify, refactor, hotfix, deprecate patterns
  - Fixes "Not on a feature branch" error when using enhance, cleanup, or baseline workflows
  - Updated error message to show all 8 valid workflow branch patterns
  - Affects: specify_extend.py patch_common_sh() function

- **Patch Versioning** - Auto-update outdated common.sh patches
  - Detects if existing patched common.sh is missing new workflow patterns
  - Automatically restores from backup or removes old patched function
  - Re-applies updated patch with complete pattern support
  - Allows `specify-extend --all` to update existing installations seamlessly
  - No manual intervention needed to get latest patch improvements
  - Affects: specify_extend.py patch_common_sh() detection logic

#### 📦 Components

- **CLI Tool Version**: v1.5.5
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.3

---

### [1.5.4] - 2025-12-26

#### 🚀 Added

- **Incorporate Command Support** - Added support for new incorporate command extension
  - Added "incorporate" to `COMMAND_EXTENSIONS` list
  - Installs incorporate command for all supported agents
  - Automatic detection and installation alongside review command

#### 🔧 Changed/Improved

- **Extension Type System** - Improved code organization with explicit extension types
  - Split `AVAILABLE_EXTENSIONS` into `WORKFLOW_EXTENSIONS` and `COMMAND_EXTENSIONS`
  - Added `is_workflow_extension()` and `is_command_extension()` helper functions
  - Replaced magic string checks with semantic function calls
  - Better maintainability and extensibility for future extensions

- **Installation Logic** - Streamlined script and workflow directory installation
  - Use extension type helpers instead of hardcoded checks
  - Skip command extensions when installing scripts/workflows
  - Clearer intent and reduced code duplication

#### 🐛 Fixed

- **Review Command Installation** - Fixed spurious warning during installation
  - Review command is command-only, doesn't have create-review.sh script
  - Installation now correctly skips script/workflow copy for command extensions
  - Eliminates "Script create-review.sh not found" warning

#### 📦 Components

- **CLI Tool Version**: v1.5.4
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.3

---

### [1.5.3] - 2025-12-26

#### 🚀 Added

- **GitHub Integration Features** - New `--github-integration` flag for enhanced GitHub workflow support
  - Enables GitHub code review integration for spec-kit projects
  - Automatic GitHub workflow installation (review-required and review-reminder)
  - Optional workflows can be enabled during setup
  - Improves CI/CD integration and code review processes

#### 🔧 Changed/Improved

- **Typer CLI Framework** - Fixed entry point configuration
  - Added @app.command() decorator to main function
  - Proper Typer integration for CLI command execution
  - Improved command routing and argument handling

- **Path Handling** - Enhanced cross-platform compatibility
  - Improved Windows path handling in get_repo_root function
  - Added backslash normalization for Git Bash compatibility
  - Better path resolution across different shell environments

- **Documentation** - Improved setup and configuration documentation
  - Clarified GitHub integration requirements
  - Added examples for --github-integration flag
  - Updated README with agent support and setup instructions
  - Enhanced troubleshooting documentation

#### 🧪 Testing

- **Comprehensive Test Coverage** - Added extensive tests for core functionality
  - Tests for get_repo_root function across different path scenarios
  - Windows path handling test cases (backslashes, drive letters)
  - Unit tests for template download and version detection
  - Test coverage for path normalization logic

#### 📦 Components

- **CLI Tool Version**: v1.5.3
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.2

---

### [1.5.2] - 2025-12-25

#### 🐛 Fixed

- **Template Download** - Fixed template download to use templates-v* tags
  - Changed from fetching `/releases/latest` to `/tags` endpoint
  - Filters for tags starting with `templates-v` prefix
  - Downloads latest template release (templates-v2.5.1)
  - Displays template version in UI during download

#### 🧪 Testing

- **Added Unit Tests** - Created comprehensive test suite for download functionality
  - Tests template tag filtering and selection
  - Mocks GitHub API responses
  - Verifies correct tag is downloaded

#### 📦 Components

- **CLI Tool Version**: v1.5.2
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.5.1

---

### [1.5.1] - 2025-12-24

#### 🔧 Improved

- **Version Alignment** - Patch release to align CLI version with template v2.4.1
  - No functional changes to CLI code
  - Ensures version consistency across components

#### 📦 Components

- **CLI Tool Version**: v1.5.1
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.4.1

---

### [1.5.0] - 2025-12-24

#### 🚀 Added

- **PowerShell Script Support** - Added `--script` option to choose between bash and PowerShell
  - `--script sh` (default): Installs bash scripts to `.specify/scripts/bash/`
  - `--script ps`: Installs PowerShell scripts to `.specify/scripts/powershell/`
  - Agent commands automatically updated to reference correct script paths
  - Consistent with spec-kit's `specify init --script` behavior

- **Enhance Workflow Integration** - Added support for new enhance workflow
  - Installs enhance command templates for all supported agents
  - Copies create-enhance.sh and create-enhance.ps1 scripts
  - Updates enabled.conf with enhance workflow option

#### 🔧 Changed/Improved

- **Script Installation Logic** - Changed to either/or behavior (breaking change)
  - Previously: Always installed bash, optionally added PowerShell
  - Now: Installs ONLY the selected script type via `--script` flag
  - Matches spec-kit's behavior where `--script ps` excludes bash entirely
  - More consistent and prevents confusion from mixed installations

#### 📦 Components

- **CLI Tool Version**: v1.5.0
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.4.0

---

### [1.4.4] - 2025-12-23

#### 🔧 Improved

- **Cleanup Workflow Guidance** - Updated cleanup workflow instructions to separate automatic vs agent-driven fixes, with confirm-before-apply and verify-via-`--dry-run` steps. No functional CLI code changes; release aligns with Extension Templates v2.3.1.

#### 📦 Components

- **CLI Tool Version**: v1.4.4
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.3.1

---

### [1.4.3] - 2025-12-23

#### 🐛 Fixed

- **Cleanup Workflow Script** - Fixed premature exit issues in `create-cleanup.sh` when run with `--json` flag
  - Root cause: `validate_workflow_directory` function had implicit non-zero return codes at lines 117 and 160
  - Fix: Explicitly return 0 from early return statements to prevent `set -e` from terminating the script prematurely
  - Impact: Script now correctly produces JSON output when requested instead of exiting without output

#### 📦 Components

- **CLI Tool Version**: v1.4.3
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.3.0

---

### [1.4.1] - 2025-12-23

#### 🔧 Improved

- **Version Bump Automation** - Added automated version bumping script (`bump-version.sh`)
  - Updates version in `specify_extend.py` and `pyproject.toml`
  - Creates git tag with appropriate prefix (`cli-v` for CLI tool)
  - Automatically updates CHANGELOG.md with version and date
  - Supports manual trigger in release workflow
- **Code Formatting** - Fixed formatting inconsistencies in README and scripts for better maintainability

#### 📦 Components

- **CLI Tool Version**: v1.4.1
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.3.0

---

### [1.3.9] - 2025-12-22

#### 🐛 Fixed

- Cleanup workflow numbering now checks for duplicates within each workflow directory instead of across all workflows.
- Top-level numbered specs under specs/ are handled as features without triggering invalid-name errors.

#### 📦 Components

- **CLI Tool Version**: v1.3.9
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.3.0

### [1.3.8] - 2025-12-22

#### 🚀 Added

- **Baseline Workflow** - New `/speckit.baseline` workflow for project context establishment
  - Added `baseline` to `AVAILABLE_EXTENSIONS` list
  - Automatic detection and installation of baseline workflow templates
  - Updated constitution template with baseline quality gates
  - Enhanced workflow selection detection to include baseline patterns

#### 📦 Components

- **CLI Tool Version**: v1.3.8
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.3.0

---

### [1.3.7] - 2025-12-22

#### 🚀 Added

- **Cleanup Workflow** - New `/speckit.cleanup` workflow for validating and reorganizing spec-kit artifacts
  - Added `cleanup` to `AVAILABLE_EXTENSIONS` list
  - Automatic detection and installation of cleanup workflow templates

#### 📦 Components

- **CLI Tool Version**: v1.3.7
- **Compatible Spec Kit Version**: v0.0.80+
- **Extension Templates Version**: v2.2.0

---

### [1.3.6] - 2025-12-16

#### 🚀 Added

- **Multi-Agent Installation** - Install commands for multiple AI agents in a single repository
  - New `--agents` flag accepts a comma-separated list (e.g. `--agents claude,copilot,cursor-agent`)
  - Keeps `--agent` for backward compatibility (mutually exclusive with `--agents`)
- **Symlink Mode (Opt-in)** - New `--link` flag to symlink agent command files instead of copying
  - Useful for monorepos or local development workflows
  - Falls back to copying on Windows

#### \ud83d\udce6 Components

- **CLI Tool Version**: v1.3.6
- **Compatible Spec Kit Version**: v0.0.80+

---

### [1.3.5] - 2025-12-16

#### 🔧 Changed

- **Spec-kit Compatibility** - Patch spec-kit's `scripts/bash/update-agent-context.sh` to keep Copilot instructions compatible while using `AGENTS.md` as canonical guidance
  - Rewrites Copilot target file to `.github/copilot-instructions.md`
  - Keeps `AGENTS.md` as the primary instructions source for Copilot coding agent
  - Avoids divergence between spec-kit context updates and spec-kit-extensions workflow command files

#### 📦 Components

- **CLI Tool Version**: v1.3.5
- **Compatible Spec Kit Version**: v0.0.80+

---

### [1.3.4] - 2025-12-15

#### 🐛 Fixed

- **Backward Compatibility** - Added fallback to support both `speckit.*` and `specify.*` naming conventions
  - Ensures compatibility when downloading from older releases
  - Gracefully handles transition period between naming conventions

#### 📦 Components

- **CLI Tool Version**: v1.3.4
- **Compatible Spec Kit Version**: v0.0.80+

---

### [1.3.3] - 2025-12-15

#### 🔧 Changed

- **Naming Convention** - Standardized command file naming from `specify.*` to `speckit.*`
  - Renamed all command files to use `speckit` prefix (e.g., `speckit.bugfix.md`, `speckit.modify.md`)
  - Updated Copilot agent files to `speckit.{ext}.agent.md` format
  - Updated Copilot prompt files to `speckit.{ext}.prompt.md` format
  - Fixed prompt file references to correctly point to agent files
  - Updated all documentation to reflect new naming convention

#### 📦 Components

- **CLI Tool Version**: v1.3.3
- **Compatible Spec Kit Version**: v0.0.80+

---

### [1.3.1] - 2025-12-14

#### 🐛 Fixed

- **common.sh Patching Compatibility** - Fixed patching to support parameterized `check_feature_branch()` function
  - Now handles both parameterized `check_feature_branch(branch, has_git_repo)` and non-parameterized signatures
  - Patched function supports optional parameters for backward compatibility
  - Resolves "function format has changed" error when patching newer common.sh versions

#### 📦 Components

- **CLI Tool Version**: v1.3.1
- **Compatible Spec Kit Version**: v0.0.80+

---

### [1.3.0] - 2025-12-14

#### 🚀 Improved

- **Directory Structure Organization** - Changed from flat directory naming to subdirectory organization
  - Bugfix, refactor, hotfix, and deprecate workflows now create subdirectories: `specs/bugfix/###-description/` instead of `specs/bugfix-###-description/`
  - Branch naming updated to use forward slashes: `bugfix/###-description` instead of `bugfix-###-description`
  - Cleaner organization with workflows grouped into their own subdirectories
  - Modify workflow continues to use feature-specific structure: `specs/###-feature/modifications/###-/`

- **Robust common.sh Patching** - Improved patching strategy for spec-kit's common.sh
  - Renames original `check_feature_branch()` to `check_feature_branch_old()` instead of in-place replacement
  - Appends new function to end of file for better compatibility
  - More resilient to changes in original function implementation
  - Easier to debug and compare old vs new implementations

#### 📦 Components

- **CLI Tool Version**: v1.3.0
- **Compatible Spec Kit Version**: v0.0.80+

---

## Extension Templates

### [2.2.0] - 2025-12-22

#### 🚀 Added

- **Cleanup Workflow** - New workflow for validating and reorganizing spec-kit artifacts
  - Command: `/speckit.cleanup [--dry-run] [--auto-fix] "reason"`
  - Validates sequential numbering (001, 002, 003, etc.)
  - Detects gaps, duplicates, and incorrect directory locations
  - Automatically renumbers directories with `--auto-fix`
  - Generates detailed cleanup reports in `specs/cleanup/NNN-cleanup-report/`
  - **Safety guarantee**: Only moves/renames documentation in `specs/`, never touches code files
  - Use cases: Pre-release validation, post-merge cleanup, periodic maintenance

#### 📦 Components

- **Extension Templates Version**: v2.2.0
- **Compatible Spec Kit Version**: v0.0.80+

---

### [2.1.1] - 2025-12-08

#### 🔧 Improved

- **Constitution Template Streamlining** - Reduced `constitution-template.md` to workflow-specific content only, removing redundant sections already present in base constitutions
  - Removed 70+ lines of duplicate content (metadata, project structure, etc.)
  - Template now focuses on workflow selection and quality gates sections only
  - Results in cleaner, more maintainable constitution files

#### 📦 Components

- **Extension Templates Version**: v2.1.1
- **Compatible Spec Kit Version**: v0.0.80+

---

## CLI Tool (specify-extend)

### [1.2.0] - 2025-12-12

#### ✨ Features

- **Extension Branch Pattern Support** - Automatically patches spec-kit's `common.sh` to support extension branch naming patterns
  - Patches `check_feature_branch()` to accept both standard and extension patterns
  - Standard pattern: `###-description` (e.g., `001-add-feature`)
  - Extension patterns:
    - `bugfix/###-description` (e.g., `bugfix/001-fix-login`)
    - `modify/###^###-description` (e.g., `modify/001^002-update-api`)
    - `refactor/###-description` (e.g., `refactor/003-cleanup-utils`)
    - `hotfix/###-description` (e.g., `hotfix/004-security-patch`)
    - `deprecate/###-description` (e.g., `deprecate/005-remove-legacy`)
  - Creates `.specify/scripts/bash/common.sh.backup` before patching
  - Gracefully handles already-patched files
  - Skips if `common.sh` doesn't exist (e.g., fresh installations)

#### 🔧 Improved

- **Installation Flow** - Now includes automatic `common.sh` patching after template installation
- **Error Messages** - Enhanced branch validation error to list all supported patterns
- **Backward Compatibility** - Preserves non-git repository behavior and standard spec-kit patterns

### [1.1.2] - 2025-12-12

#### 🔒 Security & Reliability

- **SSL/TLS Verification** - Added proper SSL certificate verification for HTTPS connections
  - Created default SSL context using `ssl.create_default_context()`
  - Updated httpx Client to use SSL verification
  - Matches spec-kit's secure connection handling

- **GitHub Authentication** - Added comprehensive GitHub token authentication support
  - New `--github-token` CLI option for authenticated requests
  - Checks `GH_TOKEN` and `GITHUB_TOKEN` environment variables
  - Authenticated requests get 5,000/hour rate limit vs 60/hour unauthenticated
  - Bearer token authorization headers

- **Rate Limit Handling** - Improved error handling with detailed rate limit information
  - Parse and display GitHub rate limit headers
  - Show remaining requests and reset time in local timezone
  - User-friendly error messages with troubleshooting tips
  - Guidance for CI/corporate environments

- **HTTP Improvements** - Enhanced reliability of network requests
  - Added timeout parameters (30s for API, 60s for downloads)
  - Better error handling with status code validation
  - JSON parsing error handling
  - Detailed error messages with Rich Panel formatting

### [1.1.1] - 2025-12-08

#### 🐛 Fixed

- **GitHub Copilot Prompt File Naming** - Corrected prompt file naming pattern to `speckit.*.prompt.md`
  - Previous: `.github/prompts/speckit.{workflow}.md`
  - Now: `.github/prompts/speckit.{workflow}.prompt.md`
  - Matches GitHub Copilot's expected naming convention

- **Removed Unsupported Scripts Section** - Removed `scripts:` frontmatter from all command files
  - GitHub Copilot does not support the `scripts:` section in agent/prompt files
  - Replaced `{SCRIPT}` template variables with explicit script paths
  - Commands now reference scripts directly (e.g., `.specify/scripts/bash/create-bugfix.sh`)

### [1.1.0] - 2025-12-08

#### ✨ Added

- **LLM-Enhanced Constitution Updates** - New `--llm-enhance` flag for intelligent constitution merging
  - Creates one-time prompt/command that uses AI to intelligently merge quality gates
  - For GitHub Copilot: Creates both `.github/agents/` and `.github/prompts/` files (matching spec-kit pattern)
  - For other agents: Creates command file (e.g., `.claude/commands/speckit.enhance-constitution.md`)
  - Prompt files for regular workflows are pointers to agent files (`agent: speckit.{workflow}`)
  - Self-destruct instructions included to prevent accidental re-use

- **GitHub Copilot Agent + Prompt Support** - Proper dual-file installation for GitHub Copilot
  - All workflow commands now create both `.github/agents/` and `.github/prompts/` files
  - Prompt files are lightweight pointers to agent files (following spec-kit pattern)
  - Matches spec-kit's implementation for better Copilot integration

#### 📝 Documentation

- Added comprehensive documentation for `--llm-enhance` feature
- Updated examples to show Copilot-specific usage patterns
- Clarified difference between prompt files and agent files

#### 📦 Components

- **CLI Tool Version**: v1.1.0
- **Installation**: `pip install specify-extend` or `uvx specify-extend`

### [1.0.1] - 2025-12-08

#### 🔧 Improved

- **Intelligent Section Numbering** - Enhanced `specify_extend.py` to detect and continue existing section numbering schemes
  - Automatically detects Roman numerals (I, II, III) or numeric (1, 2, 3) section numbering
  - Continues the sequence when adding workflow selection and quality gates sections
  - Ensures proper integration with existing project constitutions without manual renumbering

#### 🐛 Fixed

- **Edge Case Handling** - Improved section detection and parsing robustness
  - Better handling of edge cases in section formatting
  - Enhanced error handling for malformed constitution files
  - More reliable section insertion logic

#### 📝 Documentation

- **Code Quality Improvements** - Refactored with named constants and enhanced documentation
  - Added clear constant definitions for better code maintainability
  - Improved inline documentation and code comments
  - Better structured code for future enhancements

#### 📦 Components

- **CLI Tool Version**: v1.0.1
- **Installation**: `pip install specify-extend` or `uvx specify-extend`

### [1.0.0] - 2025-12-06

#### ✨ Added

- Initial release of `specify-extend` CLI tool
- PyPI package publication
- Automatic agent detection and installation
- GitHub release integration
- Constitution update with section numbering

#### 📦 Components

- **CLI Tool Version**: v1.0.0

---

## Combined Release History

Prior to v2.1.1/v1.0.1, templates and CLI were versioned together.

### [2.1.0] - 2025-12-05

### ✨ Added

- **VS Code Agent Config Support** - Added `handoffs` frontmatter to all command files to align with spec-kit v0.0.80+ and enable VS Code agent integration support
  - All five extension commands (`bugfix`, `modify`, `refactor`, `hotfix`, `deprecate`) now include handoff configurations
  - Handoffs provide quick navigation to next steps (`speckit.plan`, `speckit.tasks`) directly from within supported AI agents
  - Improves workflow continuity and discoverability for users

### 🔧 Technical Details

- **Compatible Spec Kit Version**: v0.0.80+ (was v0.0.18+)
- **Affected Files**: All 5 command files in `commands/` directory
- **Feature**: Handoffs enable AI agents to suggest natural next steps in the workflow

## [2.0.0] - 2025-10-08

### 🎯 Major Changes

**Checkpoint-Based Workflow Redesign** - All extension workflows now use a multi-phase checkpoint approach that gives users review and control points before implementation.

**Why this change?** User testing revealed 0% success rate (2/2 failures) with the previous auto-implementation design. Users were not given the opportunity to review or adjust the intended approach before execution, leading to incorrect fixes and wasted time.

### ✨ New Workflow Pattern

All workflows now follow this checkpoint-based pattern:

1. **Initial Analysis** - Run workflow command (e.g., `/speckit.bugfix`) to create analysis/documentation
2. **User Review** - Review the analysis, make adjustments as needed
3. **Planning** - Run `/speckit.plan` to create implementation plan
4. **Plan Review** - Review and adjust the plan
5. **Task Breakdown** - Run `/speckit.tasks` to break down into specific tasks
6. **Task Review** - Review tasks, ensure nothing is missed
7. **Implementation** - Run `/speckit.implement` to execute

### 🔄 Changed Workflows

#### Bugfix Workflow (`/speckit.bugfix`)
- **Before**: Auto-generated 21 tasks immediately after command
- **After**: Creates `bug-report.md` → User reviews → `/speckit.plan` → User reviews → `/speckit.tasks` → User reviews → `/speckit.implement`
- **Benefit**: Users can adjust the fix approach before implementation, preventing incorrect solutions

#### Modify Workflow (`/speckit.modify`)
- **Before**: Auto-generated 36 tasks with impact analysis
- **After**: Creates `modification-spec.md` + `impact-analysis.md` → User reviews → `/speckit.plan` → User reviews → `/speckit.tasks` → User reviews → `/speckit.implement`
- **Benefit**: Users can review impact analysis (~80% accurate) and catch missed dependencies before making breaking changes

#### Refactor Workflow (`/speckit.refactor`)
- **Before**: Auto-generated 36 tasks after metrics capture
- **After**: Creates `refactor-spec.md` + `metrics-before.md` → User captures baseline → `/speckit.plan` → User reviews → `/speckit.tasks` → User reviews → `/speckit.implement`
- **Benefit**: Users ensure baseline metrics are captured and plan is incremental before starting refactoring

#### Hotfix Workflow (`/speckit.hotfix`)
- **Before**: Auto-generated 28 tasks for emergency fix
- **After**: Creates `hotfix.md` → Quick assessment → `/speckit.plan` (fast-track) → Quick review → `/speckit.tasks` → Quick sanity check → `/speckit.implement`
- **Benefit**: Even in emergencies, a 2-minute review prevents making the outage worse

#### Deprecate Workflow (`/speckit.deprecate`)
- **Before**: Auto-generated 58 tasks across all phases
- **After**: Creates `deprecation.md` + `dependencies.md` → Stakeholder review → `/speckit.plan` → Approval → `/speckit.tasks` → Review → `/speckit.implement`
- **Benefit**: Multi-month deprecations require stakeholder alignment; checkpoints ensure proper planning

### 🚨 Breaking Changes

#### Command Names Updated
All extension commands now require the `/speckit.` prefix to align with spec-kit v0.0.18+:

- `/bugfix` → `/speckit.bugfix`
- `/modify` → `/speckit.modify`
- `/refactor` → `/speckit.refactor`
- `/hotfix` → `/speckit.hotfix`
- `/deprecate` → `/speckit.deprecate`

**Migration**: Update any scripts, documentation, or habits to use the new command names.

#### Workflow Process Changed
Auto-implementation has been removed. Users must now:

1. Run initial command to create analysis
2. Review the analysis
3. Run `/speckit.plan` to create implementation plan
4. Review the plan
5. Run `/speckit.tasks` to create task breakdown
6. Review the tasks
7. Run `/speckit.implement` to execute

**Migration**: Expect to review and approve at each checkpoint rather than having tasks auto-generated and immediately executed.

#### File Structure Updated
Each workflow now creates files in phases:

**Before** (v1.0.0):
```
specs/bugfix/001/
├── bug-report.md
└── tasks.md         # Created immediately
```

**After** (v2.0.0):
```
specs/bugfix/001/
├── bug-report.md    # Created by /speckit.bugfix
├── plan.md          # Created by /speckit.plan
└── tasks.md         # Created by /speckit.tasks
```

**Migration**: Expect additional files (`plan.md`) that weren't present before.

### 📦 Added

- **Checkpoint reminders** - Each command now shows "Next Steps" to guide users through the checkpoint workflow
- **Plan documents** - All workflows now generate `plan.md` with implementation strategy
- **Review prompts** - Documentation emphasizes what to review at each checkpoint
- **Why checkpoints matter** - Each workflow README explains the rationale for the checkpoint approach

### ❌ Removed

- **tasks-template.md** - No longer needed since tasks are created by `/speckit.tasks` command, not template expansion
- **Auto-implementation** - Workflows no longer auto-generate and execute tasks immediately
- **Single-command execution** - Users must now run 4 commands (analysis → plan → tasks → implement) instead of 1

### 📝 Updated Documentation

- **5 workflow READMEs** - All updated with checkpoint-based workflow sections
- **extensions/README.md** - Updated command names and architecture description
- **Main documentation** - README.md, QUICKSTART.md, EXAMPLES.md all reflect checkpoint workflow
- **Command files** - All `.claude/commands/speckit.*.md` files updated with checkpoint instructions

### 🎓 Lessons Learned

**Problem**: Auto-implementation had 0% success rate because users couldn't review or adjust the approach before execution.

**Solution**: Checkpoint-based workflow gives users control at each phase, leading to better outcomes and less wasted effort.

**Tradeoff**: More commands to run (4 instead of 1), but much higher success rate and user satisfaction.

### 🔧 Technical Details

- **Extension System Version**: 2.0.0 (was 1.0.0)
- **Compatible Spec Kit Version**: v0.0.18+ (was v0.0.30+)
- **Affected Files**: ~30 files updated across all 5 extension workflows
- **Lines Changed**: ~500 lines of documentation updated

### 📚 Resources

- See individual workflow READMEs for detailed checkpoint workflow descriptions:
  - `extensions/workflows/bugfix/README.md`
  - `extensions/workflows/modify/README.md`
  - `extensions/workflows/refactor/README.md`
  - `extensions/workflows/hotfix/README.md`
  - `extensions/workflows/deprecate/README.md`

---

## [1.0.0] - 2025-09-15

### Initial Release

- Bugfix workflow with regression-test-first approach
- Modify workflow with impact analysis
- Refactor workflow with metrics tracking
- Hotfix workflow for emergencies
- Deprecate workflow with 3-phase sunset
- All workflows with auto-generated task breakdowns
- Command names without `/speckit.` prefix
- Compatible with spec-kit v0.0.30+

---

[2.0.0]: https://github.com/martybonacci/spec-kit-extensions/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/martybonacci/spec-kit-extensions/releases/tag/v1.0.0
