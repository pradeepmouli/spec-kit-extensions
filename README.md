# spec-kit Extensions

**5 production-tested workflows that extend [spec-kit](https://github.com/github/spec-kit) to cover the complete software development lifecycle.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What Is This?

**spec-kit** provides excellent structured workflows for feature development (`/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement`). These extensions add 5 additional workflows for the remaining ~75% of software development work:

- **`/speckit.bugfix`** - Fix bugs with regression-test-first approach
- **`/speckit.modify`** - Modify existing features with automatic impact analysis
- **`/speckit.refactor`** - Improve code quality with metrics tracking
- **`/speckit.hotfix`** - Handle production emergencies with expedited process
- **`/speckit.deprecate`** - Sunset features with phased 3-step rollout

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
| **New Feature** | ✅ `/speckit.specify` workflow | ✅ Same |
| **Bug Fix** | ❌ Ad-hoc | ✅ `/speckit.bugfix` with regression tests |
| **Modify Feature** | ❌ Ad-hoc | ✅ `/speckit.modify` with impact analysis |
| **Refactor Code** | ❌ Ad-hoc | ✅ `/speckit.refactor` with metrics |
| **Production Fire** | ❌ Panic | ✅ `/speckit.hotfix` with post-mortem |
| **Remove Feature** | ❌ Hope | ✅ `/speckit.deprecate` with 3-phase sunset |

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

**Option 1: Use as Template (New Projects)**
```bash
# Create new project from this template
git clone https://github.com/[your-username]/spec-kit-extensions.git my-project
cd my-project
rm -rf .git
git init
# Rearrange files per INSTALLATION.md
```

**Option 2: Copy into Existing Project**
```bash
# Clone this repo
git clone https://github.com/[your-username]/spec-kit-extensions.git /tmp/extensions

# Copy files into your project
cd your-project
cp -r /tmp/extensions/extensions/* .specify/extensions/
cp -r /tmp/extensions/scripts/* .specify/scripts/bash/
cp -r /tmp/extensions/commands/* .claude/commands/

# Merge constitution sections
cat /tmp/extensions/docs/constitution-template.md >> .specify/memory/constitution.md

# Clean up
rm -rf /tmp/extensions
```

**Option 3: Git Submodule (Team Projects)**
```bash
cd your-project
git submodule add https://github.com/[your-username]/spec-kit-extensions.git .specify/extensions-source
# Create symlinks per INSTALLATION.md
```

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

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
Building something new?
└─ Use `/speckit.specify "description"`

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
| **Bugfix** | `/speckit.bugfix "..."` | Regression test | Test before fix |
| **Modify** | `/speckit.modify 014 "..."` | Impact analysis | Update affected tests |
| **Refactor** | `/speckit.refactor "..."` | Baseline metrics | Tests unchanged |
| **Hotfix** | `/speckit.hotfix "..."` | Post-mortem | Test after (only exception) |
| **Deprecate** | `/speckit.deprecate 014 "..."` | 3-phase sunset | Remove tests last |

## Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Step-by-step installation for all scenarios
- **[AI-AGENTS.md](AI-AGENTS.md)** - Setup guides for different AI coding agents
- **[EXAMPLES.md](EXAMPLES.md)** - Real examples from Tweeter project
- **[QUICKSTART.md](extensions/QUICKSTART.md)** - 5-minute tutorial
- **[Extension README](extensions/README.md)** - Detailed workflow documentation
- **[Architecture](docs/architecture.md)** - How the system works
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute improvements

## Compatibility

### AI Agents

These extensions work with any AI agent that supports spec-kit:

- ✅ **Claude Code** (fully tested, native commands)
- ✅ **GitHub Copilot** (via `.github/copilot-instructions.md`)
- ✅ **Cursor** (via `.cursorrules`)
- ✅ **Windsurf** (via project rules)
- ✅ **Gemini CLI** (via specify CLI)
- ✅ **Other CLI tools** (Qwen, opencode, Codex)
- ✅ **Any AI agent** (universal fallback via bash scripts)

**See [AI-AGENTS.md](AI-AGENTS.md) for detailed setup guides for each agent.**

### spec-kit Versions

- ✅ **spec-kit v0.0.18+** (updated for new `/speckit.` prefix)
- ✅ Fully compatible with core spec-kit workflows
- ✅ Non-breaking (can be added/removed without affecting existing features)
- ⚠️ **Breaking change from v0.0.17**: All commands now use `/speckit.` prefix

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
│   │       ├── bugfix/
│   │       ├── modify/
│   │       ├── refactor/
│   │       ├── hotfix/
│   │       └── deprecate/
│   ├── scripts/bash/
│   │   ├── create-bugfix.sh     # Extension scripts
│   │   ├── create-modification.sh
│   │   ├── create-refactor.sh
│   │   ├── create-hotfix.sh
│   │   └── create-deprecate.sh
│   └── memory/
│       └── constitution.md      # Updated with workflow quality gates
└── .claude/commands/            # If using Claude Code
    ├── bugfix.md
    ├── modify.md
    ├── refactor.md
    ├── hotfix.md
    └── deprecate.md
```

## FAQ

### Do I need to use all 5 workflows?

No! Enable only what you need via `.specify/extensions/enabled.conf`. Common combinations:
- **Minimal**: Just `/bugfix` (most teams need this)
- **Standard**: `/bugfix` + `/modify` (covers most scenarios)
- **Complete**: All 5 workflows (full lifecycle coverage)

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

- **Issues**: [GitHub Issues](https://github.com/[your-username]/spec-kit-extensions/issues)
- **Discussions**: [GitHub Discussions](https://github.com/[your-username]/spec-kit-extensions/discussions)
- **spec-kit**: [Original spec-kit repo](https://github.com/github/spec-kit)

---

**Ready to try it?** → [Installation Guide](INSTALLATION.md) → [5-Minute Tutorial](extensions/QUICKSTART.md)
