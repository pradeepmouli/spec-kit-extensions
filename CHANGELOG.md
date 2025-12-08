# Changelog

All notable changes to the Specify Extension System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Note**: This project has two versioned components:
- **Extension Templates** (workflows, commands, scripts) - Currently at v2.1.1
- **CLI Tool** (`specify-extend`) - Currently at v1.1.1

---

## Extension Templates

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
specs/bugfix-001/
├── bug-report.md
└── tasks.md         # Created immediately
```

**After** (v2.0.0):
```
specs/bugfix-001/
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
