# spec-kit Extensions

**5 production-tested workflows that extend [spec-kit](https://github.com/github/spec-kit) to cover the complete software development lifecycle.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What Is This?

**spec-kit** provides excellent structured workflows for feature development (`/specify → /plan → /tasks → /implement`). These extensions add 5 additional workflows for the remaining ~75% of software development work:

- **`/bugfix`** - Fix bugs with regression-test-first approach
- **`/modify`** - Modify existing features with automatic impact analysis
- **`/refactor`** - Improve code quality with metrics tracking
- **`/hotfix`** - Handle production emergencies with expedited process
- **`/deprecate`** - Sunset features with phased 3-step rollout

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
| **New Feature** | ✅ `/specify` workflow | ✅ Same |
| **Bug Fix** | ❌ Ad-hoc | ✅ `/bugfix` with regression tests |
| **Modify Feature** | ❌ Ad-hoc | ✅ `/modify` with impact analysis |
| **Refactor Code** | ❌ Ad-hoc | ✅ `/refactor` with metrics |
| **Production Fire** | ❌ Panic | ✅ `/hotfix` with post-mortem |
| **Remove Feature** | ❌ Hope | ✅ `/deprecate` with 3-phase sunset |

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
/bugfix --help

# Should see:
# Usage: /bugfix "bug description"
# Creates a bugfix workflow with regression-test-first approach
```

## Usage

### Quick Decision Tree

**What are you doing?**

```
Building something new?
└─ Use `/specify "description"`

Fixing broken behavior?
├─ Production emergency?
│  └─ Use `/hotfix "incident description"`
└─ Non-urgent bug?
   └─ Use `/bugfix "bug description"`

Changing existing feature?
├─ Adding/modifying behavior?
│  └─ Use `/modify 014 "change description"`
└─ Improving code without changing behavior?
   └─ Use `/refactor "improvement description"`

Removing a feature?
└─ Use `/deprecate 014 "deprecation reason"`
```

### Example: Fix a Bug

```bash
/bugfix "profile form crashes when submitting without image upload"

# This creates:
# - Branch: bugfix/001-profile-form-crashes
# - Directory: specs/bugfix-001-profile-form-crashes/
# - Files: bug-report.md, tasks.md

# Follow tasks.md:
# 1. Reproduce bug
# 2. Write failing test (BEFORE fix)
# 3. Apply fix
# 4. Verify test passes
# 5. Document prevention measures
```

### Example: Modify Existing Feature

```bash
/modify 014 "make profile fields optional instead of required"

# This creates:
# - Branch: 014-mod-001-make-profile-fields
# - Directory: specs/014-edit-profile-form/modifications/001-make-profile-fields/
# - Files: modification-spec.md, impact-analysis.md (auto-generated), tasks.md

# Impact analysis automatically identifies:
# - Files that will need updates
# - Backward compatibility concerns
# - Dependent features
```

## Workflow Cheat Sheet

| Workflow | Command | Key Feature | Test Strategy |
|----------|---------|-------------|---------------|
| **Feature** | `/specify "..."` | Full spec + design | TDD (test before code) |
| **Bugfix** | `/bugfix "..."` | Regression test | Test before fix |
| **Modify** | `/modify 014 "..."` | Impact analysis | Update affected tests |
| **Refactor** | `/refactor "..."` | Baseline metrics | Tests unchanged |
| **Hotfix** | `/hotfix "..."` | Post-mortem | Test after (only exception) |
| **Deprecate** | `/deprecate 014 "..."` | 3-phase sunset | Remove tests last |

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

- ✅ **spec-kit v0.0.30+** (tested)
- ✅ Fully compatible with core spec-kit workflows
- ✅ Non-breaking (can be added/removed without affecting existing features)

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
