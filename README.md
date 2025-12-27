> **👉 Claude Code users: Visit [github.com/MartyBonacci/specswarm](https://github.com/MartyBonacci/specswarm) for the best experience**
>
> **Using other AI tools?** Continue with this repository - it's designed to work universally across AI coding assistants. Note that our development focus is shifting to SpecSwarm for Claude Code.

**9 production-tested workflows that extend [spec-kit](https://github.com/github/spec-kit) to cover the complete software development lifecycle.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What Is This?

**spec-kit** provides excellent structured workflows for feature development (`/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement`). These extensions add 8 additional **workflow extensions** and 1 **command extension** to cover the remaining ~75% of software development work:

### Workflow Extensions (create specs, plans, and tasks)

- **`/speckit.baseline`** - Establish project baseline and track all changes by workflow type
- **`/speckit.bugfix`** - Fix bugs with regression-test-first approach
- **`/speckit.enhance`** - Make minor enhancements with streamlined single-doc workflow
- **`/speckit.modify`** - Modify existing features with automatic impact analysis
- **`/speckit.refactor`** - Improve code quality with metrics tracking
- **`/speckit.hotfix`** - Handle production emergencies with expedited process
- **`/speckit.deprecate`** - Sunset features with phased 3-step rollout
- **`/speckit.cleanup`** - Clean up codebase with automated scripts

### Command Extensions (provide commands without workflow structure)

- **`/speckit.review`** - Review completed work with structured feedback
- **`/speckit.incorporate`** - Incorporate documents into workflows and advance stages
## Why Use These Extensions?

### The Problem

With vanilla spec-kit, you get structure for ~25% of your work (new features), but the remaining 75% happens ad-hoc:

- **Bugs**: No systematic approach → regressions happen
- **Feature changes**: No impact analysis → breaking changes
- **Code quality**: No metrics → unclear if refactor helped
- **Emergencies**: No process → panic-driven development
- **Feature removal**: No plan → angry users
- **Codebase Cleanup**: No automation → manual effort
- **Work Review**: No structure → inconsistent feedback
- **Document Integration**: Manual copy-paste → context lost, inconsistent

### The Solution

These extensions bring spec-kit's structured approach to all development activities:

| Activity | Without Extensions | With Extensions |
|----------|-------------------|-----------------|
| **New Feature** | ✅ `/speckit.specify` workflow | ✅ Same |
| **Project Baseline** | ❌ Ad-hoc | ✅ `/speckit.baseline` with comprehensive docs |
| **Bug Fix** | ❌ Ad-hoc | ✅ `/speckit.bugfix` with regression tests |
| **Minor Enhancement** | ❌ Ad-hoc | ✅ `/speckit.enhance` with streamlined planning |
| **Modify Feature** | ❌ Ad-hoc | ✅ `/speckit.modify` with impact analysis |
| **Refactor Code** | ❌ Ad-hoc | ✅ `/speckit.refactor` with metrics |
| **Production Fire** | ❌ Panic | ✅ `/speckit.hotfix` with post-mortem |
| **Remove Feature** | ❌ Hope | ✅ `/speckit.deprecate` with 3-phase sunset |
| **Codebase Cleanup** | ❌ Manual | ✅ `/speckit.cleanup` with automation |
| **Work Review** | ❌ Inconsistent | ✅ `/speckit.review` with structured feedback |
| **Document Integration** | ❌ Manual copy-paste | ✅ `/speckit.incorporate` with smart stage advancement |
## Real-World Validation

These workflows are **production-tested** on a React Router v7 Twitter clone ("Tweeter") with:

- ✅ 14 features implemented
- ✅ 3 modifications (with impact analysis that caught dependencies)
- ✅ 2 bugfixes (regression tests prevented recurrence)
- ✅ 1 refactor (metrics showed 15% code duplication reduction)
- ✅ 100% build success rate across all workflows

See [EXAMPLES.md](EXAMPLES.md) for detailed real-world examples.

## Quick Start

### Prerequisites

- **spec-kit** installed ([installation guide](https://github.com/github/spec-kit))
- **AI coding agent** (Claude Code, GitHub Copilot, Gemini CLI, Cursor, etc.)
- **Git** repository with `.specify/` directory

### Installation

spec-kit-extensions works with any AI agent that supports spec-kit. Installation is a two-step process:

**Step 1: Initialize spec-kit** (creates `.specify/` structure):
```bash
specify init --here --ai claude
# or for PowerShell: specify init --here --ai claude --script ps
```

**Step 2: Install extensions**:
```bash
specify-extend --all
```

This will:
- Detect your configured AI agent
- Install all 8 workflow extensions and 1 command extension into `.specify/`
- Set up quality gates
- Configure branch naming patterns

**Optional: Install GitHub integration**:
```bash
specify-extend --all --github-integration
```

The `--github-integration` flag will interactively prompt you to select GitHub features:
- **Review enforcement workflows** - Automatically require reviews before merge
- **Review reminder workflow** - Auto-comment on PRs with instructions
- **PR template** - Structured PR template with review checklist
- **Issue templates** - 9 templates for all workflow types
- **GitHub Copilot config** - PR review configuration
- **CODEOWNERS template** - Automatic reviewer assignment
- **Documentation** - Complete guide for all features

You can select individual features or install all with `all`. Non-interactive: `specify-extend --all --github-integration --no-interactive`

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md).

**Alternative: Install the CLI tool manually**
```bash
# 1. Initialize spec-kit in your project
cd your-project
specify init .

# 2. Install specify-extend tool from PyPI
pip install specify-extend

# Or use with uvx (no installation needed)
uvx specify-extend --all

# Or run directly with Python
python -m specify_extend --all

# 3. Install extensions (auto-detects your agent)
specify-extend --all
specify-extend --all --script ps  # Optional: install PowerShell workflows

# Or install specific extensions
specify-extend bugfix modify refactor
```

The `specify-extend` tool automatically:
- ✅ Downloads latest extensions from GitHub
- ✅ Detects your AI agent (Claude, Gemini, Copilot, Cursor, Qwen, opencode, Codex, Amazon Q, etc.)
- ✅ Installs extensions matching your setup
- ✅ Configures agent-specific commands
- ✅ Updates constitution with quality gates
- ✅ Patches spec-kit's `common.sh` to support extension branch patterns

**Optional: LLM-Enhanced Constitution Updates**

For intelligent merging of quality gates into your existing constitution (instead of simple appending):

```bash
specify-extend --all --llm-enhance
```

This creates a one-time prompt that uses your AI agent to intelligently merge quality gates while preserving your constitution's style and structure. The prompt/command includes instructions to delete itself after use.

**GitHub Copilot**: Reference `.github/prompts/speckit.enhance-constitution.md` in Copilot Chat (also creates matching agent file)
**Other agents**: Run `/speckit.enhance-constitution`

See [specify-extend documentation](docs/specify-extend.md) for details.

**Manual install (copy files)**

If you prefer manual installation or need more control:

**Option 1: Copy into Existing Project**
```bash
# Clone this repo
git clone https://github.com/pradeepmouli/spec-kit-extensions.git /tmp/extensions

# Copy files into your project
cd your-project
cp -r /tmp/extensions/extensions/* .specify/extensions/
cp -r /tmp/extensions/scripts/* .specify/scripts/bash/
# Optional (PowerShell): copy only if you want PowerShell workflows
mkdir -p .specify/scripts/powershell/
cp -r /tmp/extensions/scripts/powershell/* .specify/scripts/powershell/
cp -r /tmp/extensions/commands/* .claude/commands/

# Merge constitution sections
cat /tmp/extensions/docs/constitution-template.md >> .specify/memory/constitution.md

# Clean up
rm -rf /tmp/extensions
```

**Option 2: Git Submodule (Team Projects)**
```bash
cd your-project
git submodule add https://github.com/pradeepmouli/spec-kit-extensions.git .specify/extensions-source
# Create symlinks per INSTALLATION.md
```

See [INSTALLATION.md](INSTALLATION.md) for detailed manual installation instructions.

### Verify Installation

```bash
# In your project, try:
/speckit.bugfix --help

# Should see:
# Usage: /speckit.bugfix "bug description"
# Creates a bugfix workflow with regression-test-first approach
```

## Usage

### Quick Decision Tree

**What are you doing?**

```
Starting with spec-kit?
└─ Use `/speckit.baseline` to establish project context

Building something new?
├─ Major feature (multi-phase, complex)?
│  └─ Use `/speckit.specify "description"`
└─ Minor enhancement (simple, quick)?
   └─ Use `/speckit.enhance "description"`

Fixing broken behavior?
├─ Production emergency?
│  └─ Use `/speckit.hotfix "incident description"`
└─ Non-urgent bug?
   └─ Use `/speckit.bugfix "bug description"`

Changing existing feature?
├─ Adding/modifying behavior?
│  └─ Use `/speckit.modify 014 "change description"`
└─ Improving code without changing behavior?
   └─ Use `/speckit.refactor "improvement description"`

Removing a feature?
└─ Use `/speckit.deprecate 014 "deprecation reason"`

Reviewing completed work?
└─ Use `/speckit.review [task-id]`
```

### Example: Fix a Bug

```bash
# Step 1: Create bug report
/speckit.bugfix "profile form crashes when submitting without image upload"
# Creates: bug-report.md with initial analysis
# Shows: Next steps to review and investigate

# Step 2: Investigate and update bug-report.md with root cause

# Step 3: Create fix plan
/speckit.plan
# Creates: Detailed fix plan with regression test strategy

# Step 4: Break down into tasks
/speckit.tasks
# Creates: Task list (reproduce, write regression test, fix, verify)

# Step 5: Execute fix
/speckit.implement
# Runs all tasks including regression-test-first approach
```

### Example: Modify Existing Feature

```bash
# Step 1: Create modification spec with impact analysis
/speckit.modify 014 "make profile fields optional instead of required"
# Creates: modification-spec.md + impact-analysis.md
# Shows: Impact summary and next steps

# Step 2: Review modification spec and impact analysis
# - Check affected files and contracts
# - Assess backward compatibility
# - Refine requirements if needed

# Step 3: Create implementation plan
/speckit.plan
# Creates: Detailed plan for implementing changes

# Step 4: Break down into tasks
/speckit.tasks
# Creates: Task list (update contracts, update tests, implement)

# Step 5: Execute changes
/speckit.implement
# Runs all tasks in correct order
```

## Workflow Cheat Sheet

| Workflow | Command | Key Feature | Test Strategy |
|----------|---------|-------------|---------------|
| **Feature** | `/speckit.specify "..."` | Full spec + design | TDD (test before code) |
| **Baseline** | `/speckit.baseline` | Context tracking | No tests (doc only) |
| **Bugfix** | `/speckit.bugfix "..."` | Regression test | Test before fix |
| **Enhance** | `/speckit.enhance "..."` | Single-doc workflow | Tests for new behavior |
| **Modify** | `/speckit.modify 014 "..."` | Impact analysis | Update affected tests |
| **Refactor** | `/speckit.refactor "..."` | Baseline metrics | Tests unchanged |
| **Hotfix** | `/speckit.hotfix "..."` | Post-mortem | Test after (only exception) |
| **Deprecate** | `/speckit.deprecate 014 "..."` | 3-phase sunset | Remove tests last |
| **Review** | `/speckit.review [task-id]` | Structured feedback | Verify tests |
| **Cleanup** | `/speckit.cleanup` | Automated scripts | Manual verification |

- **[INSTALLATION.md](INSTALLATION.md)** - Step-by-step installation for all scenarios
- **[AI-AGENTS.md](AI-AGENTS.md)** - Setup guides for different AI coding agents
- **[EXAMPLES.md](EXAMPLES.md)** - Real examples from Tweeter project
- **[QUICKSTART.md](extensions/QUICKSTART.md)** - 5-minute tutorial
- **[Extension README](extensions/README.md)** - Detailed workflow documentation
- **[Architecture](docs/architecture.md)** - How the system works
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute improvements

## Compatibility

### AI Agents

These extensions work with any AI agent that supports spec-kit. Command files are installed per agent:

| Agent | Command directory | Format |
|-------|-------------------|--------|
| Claude Code | `.claude/commands` | Markdown |
| GitHub Copilot | `.github/agents` | Markdown |
| Cursor | `.cursor/commands` | Markdown |
| Windsurf | `.windsurf/workflows` | Markdown |
| Gemini CLI | `.gemini/commands` | TOML |
| Qwen Code | `.qwen/commands` | TOML |
| opencode | `.opencode/commands` | Markdown |
| Codex CLI | `.codex/commands` | Markdown |
| Amazon Q Developer CLI | `.q/commands` | Markdown |
| Manual/Generic | None (use scripts directly) | N/A |

Detection also recognizes:
- Copilot: `.github/copilot-instructions.md`
- Cursor: `.cursorrules`

If no agent is detected, you can pass `--agent` explicitly or use the scripts directly.

**See [AI-AGENTS.md](AI-AGENTS.md) for detailed setup guides for each agent.**

### spec-kit Versions

- ✅ **spec-kit v0.0.80+** (includes VS Code agent config support with handoffs)
- ✅ **spec-kit v0.0.18+** (updated for new `/speckit.` prefix)
- ✅ Fully compatible with core spec-kit workflows
- ✅ Non-breaking (can be added/removed without affecting existing features)
- ⚠️ **Breaking change from v0.0.17**: All commands now use `/speckit.` prefix

### Component Versions

This project has two independently versioned components:

- **Extension Templates** (v2.5.1) - Workflow templates, commands, and scripts
  - See [CHANGELOG.md](CHANGELOG.md) for template version history
- **CLI Tool** (v1.5.2) - `specify-extend` installation tool
  - Check version with `specify-extend --version`
  - See [CHANGELOG.md](CHANGELOG.md) for CLI version history

Both components are released together but versioned separately to allow independent updates.

## Optional GitHub Integration

**New in vX.Y.Z**: spec-kit-extensions now includes optional GitHub workflows, issue templates, and AI agent configuration to enhance your development workflow.

### Features

- **🔒 Review Enforcement** - Automatically require code reviews before merging spec-kit branches
- **💬 Review Reminders** - Auto-comment on PRs with helpful review instructions
- **📝 PR Template** - Structured PR template with review checklist
- **👥 CODEOWNERS** - Automatic reviewer assignment based on workflow type
- **🤖 Copilot for PRs** - GitHub Copilot integration for AI-assisted code review
- **📋 Issue Templates** - Structured templates for all 9 workflow types
- **✅ Review Helper** - Tools to check review status and validate branches

### What's Included

1. **GitHub Actions Workflows** (3 workflows)
   - `spec-kit-review-required.yml` - Enforces review completion before merge
   - `spec-kit-review-helper.yml` - Manual tools for checking review status
   - `spec-kit-review-reminder.yml` - Auto-comments on PRs with review instructions

2. **GitHub Code Review Integration**
   - `pull_request_template.md` - Structured PR template with review checklist
   - `CODEOWNERS.example` - Automatic reviewer assignment configuration
   - `copilot.yml` - GitHub Copilot for PRs configuration with spec-kit awareness

3. **Issue Templates** (9 templates)
   - Feature Request, Bug Report, Enhancement Request
   - Modification Request, Refactoring Request, Hotfix Request
   - Deprecation Request, Cleanup Request, Baseline/Documentation Request

4. **AI Agent Configuration**
   - `copilot-instructions.md` - GitHub Copilot workflow guidance
   - Includes review requirements and best practices

### Installation (Optional)

**Option 1: Automated Installation (Recommended)**

Use the `--github-integration` flag during installation:

```bash
specify-extend --all --github-integration
```

This will:
- Interactively prompt you to select which GitHub features to install
- Download and install selected features from the latest release
- Set up the `.github/` directory automatically

Available features to select:
- `review-enforcement` - Review requirement enforcement workflow
- `review-reminder` - PR review reminder workflow
- `review-helper` - Manual review checking tools
- `pr-template` - Pull request template
- `issue-templates` - 9 issue templates for all workflows
- `copilot-config` - GitHub Copilot configuration
- `codeowners` - CODEOWNERS template
- `documentation` - Complete docs
- `all` - Install everything

Non-interactive mode (installs all features):
```bash
specify-extend --all --github-integration --no-interactive
```

**Option 2: Manual Installation**

If you prefer manual control, first obtain the spec-kit-extensions files:

```bash
# Clone the spec-kit-extensions repository
git clone https://github.com/pradeepmouli/spec-kit-extensions.git /tmp/spec-kit-extensions

# Or download a specific release
# wget https://github.com/pradeepmouli/spec-kit-extensions/archive/refs/tags/vX.Y.Z.tar.gz
# tar -xzf vX.Y.Z.tar.gz
```

Then copy the desired files to your project:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Copy workflows (recommended for review enforcement)
cp /tmp/spec-kit-extensions/.github/workflows/spec-kit-review-*.yml .github/workflows/

# Copy PR template (recommended for structured PRs)
cp /tmp/spec-kit-extensions/.github/pull_request_template.md .github/

# Copy issue templates (optional)
cp -r /tmp/spec-kit-extensions/.github/ISSUE_TEMPLATE .github/

# Copy GitHub Copilot configuration (optional, for Copilot users)
cp /tmp/spec-kit-extensions/.github/copilot-instructions.md .github/
cp /tmp/spec-kit-extensions/.github/copilot.yml.example .github/
# NOTE: copilot.yml.example is instructional. Configure it for your GitHub Copilot
# setup according to the actual Copilot configuration schema, then rename to
# copilot.yml to activate (if applicable to your Copilot version).

# Copy CODEOWNERS template (optional, for teams)
cp /tmp/spec-kit-extensions/.github/CODEOWNERS.example .github/CODEOWNERS
# IMPORTANT: Edit .github/CODEOWNERS to replace placeholder values

# Commit the files
git add .github/
git commit -m "Add spec-kit GitHub workflows and code review integration"
git push
```

### Usage

**Complete Review Workflow**:
1. Implement your work using spec-kit workflows
2. Run `/speckit.review` before creating a PR (REQUIRED)
3. Commit the review file to your branch
4. Create PR - fill out the PR template checklist
5. GitHub Actions automatically:
   - Post reminder comment with review instructions
   - Validate review file exists and is approved
   - Add appropriate labels
   - Request reviewers (via CODEOWNERS)
   - Block merge if review missing or not approved
6. GitHub Copilot assists with PR review (if configured)
7. Human reviewers perform additional review
8. Merge when both AI review + human review approved

**Issue Templates**:
1. Click "New Issue" → Select appropriate template
2. Fill out structured form
3. Use suggested workflow commands to start implementation

**Review Helper**:
- Go to Actions → Spec-Kit Review Helper → Run workflow
- Check status, list pending reviews, or validate branches

**GitHub Copilot for PRs** (if configured):
- Ask Copilot to "Review this PR for spec-kit workflow compliance"
- Copilot checks review completion, specification alignment, and code quality
- Works alongside `/speckit.review` for comprehensive coverage

### Documentation

See [.github/README.md](.github/README.md) for complete documentation including:
- Detailed workflow descriptions
- Configuration options
- Troubleshooting guide
- Examples and best practices

### Benefits

- **Consistent Quality** - All code reviewed before merge
- **Automated Enforcement** - No manual checking needed
- **Better Documentation** - Reviews committed with code
- **Structured Issues** - Complete information from the start

**Note**: These are entirely optional. Use what helps your workflow!

## Project Structure

After installation, your project will have:

```
your-project/
├── .specify/
│   ├── extensions/              # Extension workflows
│   │   ├── README.md
│   │   ├── QUICKSTART.md
│   │   ├── enabled.conf         # Enable/disable workflows
│   │   └── workflows/
│   │       ├── baseline/
│   │       ├── bugfix/
│   │       ├── enhance/
│   │       ├── modify/
│   │       ├── refactor/
│   │       ├── hotfix/
│   │       ├── deprecate/
│   │       ├── cleanup/
│   │       └── review/
│   ├── scripts/bash/            # Bash scripts (Linux/Mac/Git Bash)
│   │   ├── create-baseline.sh
│   │   ├── create-bugfix.sh
│   │   ├── create-enhance.sh
│   │   ├── create-modification.sh
│   │   ├── create-refactor.sh
│   │   ├── create-hotfix.sh
│   │   ├── create-deprecate.sh
│   │   ├── create-cleanup.sh
│   │   └── mark-task-status.sh
│   ├── scripts/powershell/      # PowerShell scripts (Windows)
│   │   ├── create-baseline.ps1
│   │   ├── create-bugfix.ps1
│   │   ├── create-enhance.ps1
│   │   ├── create-modification.ps1
│   │   ├── create-refactor.ps1
│   │   ├── create-hotfix.ps1
│   │   ├── create-deprecate.ps1
│   │   └── create-cleanup.ps1
│   └── memory/
│       └── constitution.md      # Updated with workflow quality gates
└── .claude/commands/            # Example: Claude Code command files
    ├── speckit.baseline.md
    ├── speckit.bugfix.md
    ├── speckit.enhance.md
    ├── speckit.modify.md
    ├── speckit.refactor.md
    ├── speckit.hotfix.md
    ├── speckit.deprecate.md
    ├── speckit.cleanup.md
    └── speckit.review.md
```

**Note**: `specify-extend` installs **either** bash or PowerShell scripts based on `--script` (default: bash). Bash scripts work on Linux, macOS, and Windows (via Git Bash or WSL).

## FAQ

### Do I need to use all 9 workflows?

No! Enable only what you need via `.specify/extensions/enabled.conf`. Common combinations:
- **Minimal**: Just `/bugfix` (most teams need this)
- **Standard**: `/bugfix` + `/enhance` + `/modify` (covers most scenarios)
- **Complete**: All 9 workflows (full lifecycle coverage + maintenance)

### Can I customize the workflows?

Yes! See [Extension Development Guide](extensions/DEVELOPMENT.md) for creating custom workflows or modifying existing ones.

### What if I pick the wrong workflow?

No problem! Create the correct workflow and copy your work over. The worst case is having the wrong template.

### Do these work without Claude Code?

Yes! The workflows are **agent-agnostic**. They work with any AI agent that supports spec-kit, or even manually if you prefer following the templates yourself.

### Will these be contributed to spec-kit?

That's the plan! We've opened [an issue](https://github.com/github/spec-kit/issues/[NUMBER]) proposing these extensions be incorporated upstream. Until then, use this repo.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Bug reports
- Feature requests
- New workflow ideas
- Documentation improvements
- Real-world usage examples

## License

MIT License - Same as spec-kit

See [LICENSE](LICENSE) for details.

## Credits

Built with ❤️ for the spec-kit community by developers who wanted structured workflows for more than just new features.

**Special Thanks**:
- [GitHub spec-kit team](https://github.com/github/spec-kit) for the foundation
- Anthropic Claude Code team for excellent AI agent integration
- Early adopters who tested these workflows in production

## Support

- **Issues**: [GitHub Issues](https://github.com/pradeepmouli/spec-kit-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pradeepmouli/spec-kit-extensions/discussions)
- **spec-kit**: [Original spec-kit repo](https://github.com/github/spec-kit)

---

**Ready to try it?** → [Installation Guide](INSTALLATION.md) → [5-Minute Tutorial](extensions/QUICKSTART.md)
