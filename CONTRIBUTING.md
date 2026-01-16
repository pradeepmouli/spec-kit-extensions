# Contributing to spec-kit-extensions

Thank you for your interest in contributing! These extensions were built by the community for the community, and we welcome all contributions.

## Ways to Contribute

### 1. Report Bugs

Found a bug? Please [open an issue](https://github.com/[your-username]/spec-kit-extensions/issues/new) with:

- **Clear title**: "Bug: workflow_name - brief description"
- **Steps to reproduce**: Exact commands and context
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**:
  - spec-kit version
  - AI agent (Claude Code, Copilot, etc.)
  - OS and version

**Example**:
```markdown
## Bug: /modify fails when parent feature has spaces in name

### Steps to Reproduce
1. Create feature: /specify "user profile"
2. Try to modify: /modify 001 "add avatar"

### Expected
Creates branch: 001-mod-001-add-avatar

### Actual
Error: "Feature directory not found"

### Environment
- spec-kit: v0.0.30
- Claude Code: v1.2.0
- macOS: 14.1
```

### 2. Request Features

Have an idea for a new workflow or improvement? [Start a discussion](https://github.com/[your-username]/spec-kit-extensions/discussions/new?category=ideas) with:

- **Use case**: What problem does this solve?
- **Proposed solution**: How would it work?
- **Alternative**: What do people do today without this?
- **Impact**: How many projects would benefit?

**Example**:
```markdown
## New Workflow: /security-audit

### Use Case
Need systematic approach for security reviews before releases.

### Proposed Solution
- Checklist-based workflow
- Automated security scanning integration
- Sign-off tracking

### Current Alternative
Ad-hoc security reviews, often skipped under pressure.

### Impact
Every production deployment should have this.
```

### 3. Improve Documentation

Documentation improvements are always welcome:

- Fix typos or unclear instructions
- Add examples from your projects
- Improve installation guides
- Translate documentation
- Add troubleshooting tips

**Small fixes**: Open PR directly
**Large changes**: Open issue first to discuss approach

### 4. Share Real-World Examples

Using these workflows in production? Share your experience!

1. [Start a discussion](https://github.com/[your-username]/spec-kit-extensions/discussions/new?category=show-and-tell)
2. Include:
   - What workflow you used
   - What problem it solved
   - Metrics (time saved, bugs prevented, etc.)
   - Lessons learned

We may feature your example in [EXAMPLES.md](EXAMPLES.md)!

### 5. Contribute Code

#### Small Fixes

For typos, small bugs, or minor improvements:

1. Fork the repository
2. Create a branch: `git checkout -b fix/description`
3. Make your changes
4. Test thoroughly
5. Submit PR with clear description

#### New Workflows

Want to contribute a new workflow (e.g., `/performance-audit`, `/security-review`)?

**Before writing code**:

1. [Open a discussion](https://github.com/[your-username]/spec-kit-extensions/discussions/new?category=ideas) proposing the workflow
2. Get feedback from maintainers
3. Wait for approval before starting implementation

**After approval**:

1. Follow the [Extension Development Guide](extensions/DEVELOPMENT.md)
2. Create:
   - Workflow template files
   - Bash creation script
   - Command definition (for Claude Code)
   - Tasks template
   - README for the workflow
3. Test on real project
4. Submit PR with examples

#### Workflow Improvements

Improving existing workflows:

1. [Open an issue](https://github.com/[your-username]/spec-kit-extensions/issues/new) describing the improvement
2. Explain why it's better than current approach
3. Share examples where current approach falls short
4. Wait for maintainer feedback
5. Submit PR

#### New AI Agent Support

Want to add support for a new AI coding agent?

1. Review the [AGENTS.md](AGENTS.md) guide for maintainers
2. [Open an issue](https://github.com/[your-username]/spec-kit-extensions/issues/new) proposing the new agent
3. Follow the steps in AGENTS.md to:
   - Update agent configuration in `specify_extend.py`
   - Add detection logic
   - Create command templates
   - Update documentation (README.md, AI-AGENTS.md)
4. Test the integration thoroughly
5. Submit PR with examples

## Development Setup

### Prerequisites

- Git
- Bash (Linux, macOS, or WSL2 on Windows)
- A test project with spec-kit installed

### Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/spec-kit-extensions.git
cd spec-kit-extensions

# 2. Create development symlinks (for testing in this repo)
# This mimics the structure that 'specify init' creates
mkdir -p .specify/scripts/bash .specify/scripts/powershell .specify/extensions/workflows
ln -s "$(pwd)/common.sh" .specify/scripts/bash/common.sh
ln -s "$(pwd)"/scripts/*.sh .specify/scripts/bash/
ln -s "$(pwd)"/scripts/powershell/*.ps1 .specify/scripts/powershell/
ln -s "$(pwd)"/extensions/workflows/* .specify/extensions/workflows/

# 3. Test in this repo directly
.specify/scripts/bash/create-refactor.sh --json "test refactoring"

# OR: Install into a separate test project
cd /tmp
mkdir test-project && cd test-project
git init

# 4. Initialize spec-kit (creates .specify/ structure)
specify init --here --ai claude
# or for PowerShell scripts:
# specify init --here --ai claude --script ps

# 5. Install your local extensions into test project
cp -r ~/spec-kit-extensions/extensions/* .specify/extensions/
cp ~/spec-kit-extensions/scripts/* .specify/scripts/bash/
# or for PowerShell:
# cp ~/spec-kit-extensions/scripts/powershell/* .specify/scripts/powershell/
cp ~/spec-kit-extensions/commands/* .claude/commands/

# 6. Test workflows in test project
/bugfix "test bug"
# ... verify it works
```

**Note**:
- The `.specify/` directory is created by **spec-kit's `specify init`**, not by specify-extend
- `specify init --script ps` uses PowerShell scripts, `--script sh` (default) uses Bash
- The `.specify/` directory and `specs/` are git-ignored in this repo to avoid committing test artifacts

### Testing Changes

**Test every workflow** before submitting PR:

```bash
# Test /bugfix
/bugfix "test bug description"
# Verify: branch created, files generated, tasks make sense

# Test /modify
/modify 001 "test modification"
# Verify: nested under parent, impact analysis runs

# Test /refactor
/refactor "test refactor description"
# Verify: metrics template created

# Test /hotfix
/hotfix "test incident"
# Verify: expedited tasks, post-mortem reminder

# Test /deprecate
/deprecate 001 "test reason"
# Verify: 3-phase plan, dependency scan
```

**Test edge cases**:
- Feature with spaces in name
- Missing parent feature (for /modify)
- Non-existent feature number
- Invalid characters in description
- Empty repository

## Code Style

### Bash Scripts

```bash
#!/usr/bin/env bash
# Script description here

# Exit on error
set -e

# Use absolute paths
REPO_ROOT=$(git rev-parse --show-toplevel)

# Clear error messages
error() {
    echo "ERROR: $1" >&2
    exit 1
}

# Validate inputs
if [ $# -lt 1 ]; then
    error "Usage: $0 <required_param>"
fi
```

### Markdown

- Use ATX-style headers (`#` not `===`)
- Code blocks have language specified: ` ```bash `
- Lists use `-` for unordered, `1.` for ordered
- Keep lines under 120 characters when possible
- Add blank line after headers

### Templates

- Use placeholder syntax: `{{VARIABLE_NAME}}`
- Include comments explaining optional sections
- Provide examples inline
- Keep templates under 300 lines

## PR Guidelines

### Before Submitting

- [ ] Test on real project
- [ ] Update relevant documentation
- [ ] Add entry to CHANGELOG.md (if significant)
- [ ] Verify all workflows still work
- [ ] Check for typos and formatting

### PR Description Template

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Testing
How did you test this?
- [ ] Tested /bugfix workflow
- [ ] Tested /modify workflow
- [ ] Tested on real project
- [ ] Added/updated tests

## Screenshots (if applicable)
Show before/after for UI changes

## Breaking Changes
List any breaking changes and migration path

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] CHANGELOG.md updated (if needed)
```

### PR Review Process

1. **Automated checks**: Must pass before review
2. **Maintainer review**: 1-2 business days typically
3. **Feedback**: Address comments and update PR
4. **Approval**: At least 1 maintainer approval required
5. **Merge**: Maintainer merges when ready

## Release Process

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New workflows or features
- **PATCH** (0.0.1): Bug fixes

Releases happen when:
- Significant new feature merged
- Critical bug fixed
- Requested by community

## Community Guidelines

### Code of Conduct

- **Be respectful**: Treat everyone with respect
- **Be constructive**: Criticism should be constructive
- **Be patient**: Maintainers are volunteers
- **Be collaborative**: Work together, not against

### Response Times

- **Bug reports**: 2-3 business days
- **Feature requests**: 1 week for initial feedback
- **PRs**: 1-2 business days for initial review
- **Security issues**: 24 hours

## Recognition

Contributors are recognized in:

- **README.md** - Credits section
- **Release notes** - For significant contributions
- **EXAMPLES.md** - Real-world usage examples

Top contributors may be invited to become maintainers.

## Questions?

- **General questions**: [Discussions](https://github.com/[your-username]/spec-kit-extensions/discussions)
- **Bug reports**: [Issues](https://github.com/[your-username]/spec-kit-extensions/issues)
- **Security issues**: Email [security@example.com]
- **Direct contact**: [Maintainer contact info]

---

Thank you for contributing to spec-kit-extensions! 🎉
