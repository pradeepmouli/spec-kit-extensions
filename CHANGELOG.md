# Changelog

All notable changes to the Specify Extension System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Note**: This project has two versioned components:
- **Extension Templates** (workflows, commands, scripts) - Currently at v2.5.4
- **CLI Tool** (`specify-extend`) - Currently at v1.5.5

---

## Extension Templates

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

#### 📦 Components

- **Extension Templates Version**: v2.4.0
- **Compatible Spec Kit Version**: v0.0.80+
- **Compatible specify-extend**: v1.5.0+

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
