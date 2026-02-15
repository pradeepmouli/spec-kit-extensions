# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**spec-kit-extensions** extends GitHub's spec-kit with 7 additional production-tested workflows that cover the complete software development lifecycle beyond just feature development.

**Architecture (v2.3.0+)**: Native spec-kit extension format
- **Extension Manifest**: `extension.yml` declares all commands and configuration
- **Workflow Templates**: Stored in `workflows/` directory
- **Scripts**: Located in `scripts/` directory (including `common.sh`)
- **Configuration**: YAML-based (`config-template.yml`)
- **Installation**: Via `specify extension add spec-kit-workflows` (native) or legacy `specify-extend` CLI

The project is designed to be **agent-agnostic**, working with Claude Code, GitHub Copilot, Cursor, and any AI coding assistant that supports spec-kit.

## Development Commands

### Testing the Native Extension

```bash
# Test in a fresh spec-kit project
cd /tmp
mkdir test-project && cd test-project
git init
specify init .

# Install extension in dev mode
specify extension add --dev /path/to/spec-kit-extensions

# Verify installation
specify extension list
# Should show: spec-kit-workflows (v2.3.0)

# Test a workflow
/speckit.workflows.bugfix "test bug"
git branch  # Should show: bugfix/001-test-bug
ls specs/bugfix/  # Should show: 001-test-bug/

# Test JSON output
.specify/extensions/spec-kit-workflows/scripts/create-bugfix.sh --json "test"
```

### Legacy CLI Testing (Deprecated)

The `specify-extend` CLI tool is deprecated but still maintained for spec-kit < 0.0.93:

```bash
# Install the CLI tool locally for development
pip install -e .

# Run the CLI tool (from source)
python specify_extend.py --help
python specify_extend.py --version
python specify_extend.py --list

# Test installation in a separate spec-kit project
cd /path/to/test-project
specify init .
specify-extend --all --dry-run
specify-extend --all
```

### Version Management

**IMPORTANT**: This project now uses a single version number for the native extension format:

1. **Extension version** in `extension.yml` (`version: "2.3.0"`)
2. **Extension templates version** documented in `CHANGELOG.md`
3. **Legacy CLI version** (deprecated) in `pyproject.toml` and `specify_extend.py`

When updating versions:
- Update version in `extension.yml`
- Document changes in CHANGELOG.md under "Extension Templates" section
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Legacy CLI versions are frozen at v1.5.12

### Git Workflow

```bash
# This repo uses standard git workflows (no spec-kit workflows on itself)
git status
git add .
git commit -m "Description"
git push

# Create tags for releases
git tag -a v1.3.9 -m "Release version 1.3.9"
git push origin v1.3.9
```

## Architecture

### Core Components (Native Format v2.3.0+)

1. **`extension.yml`** - Extension manifest
   - Declares all 11 commands (8 workflows + 3 command extensions)
   - Specifies requirements (spec-kit >= 0.0.93)
   - Defines hooks (e.g., `after_tasks` → `speckit.review`)
   - Sets default configuration

2. **`config-template.yml`** - Configuration template
   - Enables/disables individual workflows
   - Branch validation settings
   - Constitution update preferences
   - Copied to `.specify/extensions/spec-kit-workflows/config.yml` on install

3. **`scripts/common.sh`** - Shared bash utilities
   - `generate_branch_name()` - Smart branch naming with stop words filtering
   - `get_repo_root()`, `get_current_branch()` - Git utilities
   - `find_feature_dir_by_prefix()` - Supports multiple branches per spec

4. **`scripts/`** - Workflow creation scripts
   - `create-baseline.sh`, `create-bugfix.sh`, `create-modification.sh`, etc.
   - Each script creates branch, directory structure, and templates
   - All scripts support `--json` flag for programmatic output

5. **`commands/`** - Agent command files
   - `speckit.baseline.md`, `speckit.bugfix.md`, etc.
   - Used by Claude Code, Copilot, Cursor, etc.
   - Native system handles agent-specific format conversion

6. **`workflows/`** - Workflow templates
   - Each workflow has: templates, README, and helper scripts
   - Templates use `{{PLACEHOLDER}}` syntax
   - Installed to `.specify/extensions/spec-kit-workflows/workflows/`

7. **`scripts/validate-branch.sh`** - Branch validation hook
   - Validates branch names match workflow patterns
   - Replaces common.sh patching from legacy system

8. **`scripts/migrate-to-native.sh`** - Migration helper
   - Migrates legacy installations to native format
   - Removes old patches and files

### Legacy Components (Deprecated)

**`specify_extend.py`** - Legacy CLI tool (deprecated, frozen at v1.5.12)
- Only needed for spec-kit < 0.0.93
- Native extension system replaces all functionality
- Maintained for backward compatibility

### Key Design Patterns

**Branch Naming = Workflow Type**
- Standard feature: `001-feature-name`
- Bugfix: `bugfix/001-description`
- Modify: `modify/001^002-description`
- Refactor: `refactor/001-description`
- Hotfix: `hotfix/001-description`
- Deprecate: `deprecate/001-description`
- Cleanup: `cleanup/001-description`
- Baseline: `baseline/001-description`

**Native Installation Flow**
1. `specify extension add spec-kit-workflows`
2. Native system reads `extension.yml`
3. Copies all files to `.specify/extensions/spec-kit-workflows/`
4. Registers commands via `CommandRegistrar`
5. Configures hooks from manifest

**Agent Detection & Support**

The native system handles agent detection automatically via `CommandRegistrar`. For details on how agents are supported, see [AGENTS.md](AGENTS.md).

**Branch Validation** (Native)
- Hook-based: `scripts/validate-branch.sh`
- No file patching required
- Registered in `extension.yml` hooks section

## Working with This Codebase

### Making Changes to Scripts

**When modifying workflow scripts** (scripts/*.sh):
1. Test with `--json` flag: `./scripts/create-bugfix.sh --json "test"`
2. Verify branch creation works in non-git repos (uses fallback logic)
3. Ensure `generate_branch_name()` from common.sh is available
4. All scripts must source common.sh with fallback search logic (see create-bugfix.sh:5-36)

**Function existence checks** (added recently):
All scripts now verify required functions exist:
```bash
if ! declare -f generate_branch_name > /dev/null; then
    echo "Error: generate_branch_name function is not available" >&2
    exit 1
fi
```

### Making Changes to specify_extend.py

**Key functions to understand**:

- `detect_agent()` - Agent detection logic
- `patch_common_sh()` - Patches spec-kit's common.sh
- `update_constitution()` - Constitution update logic
- `parse_constitution_sections()` - Detects Roman/numeric section numbering
- `detect_existing_workflows()` - Checks which workflows already documented
- `download_latest_release()` - Downloads from GitHub with rate limit handling
- `prompt_for_workflows()` - Interactive workflow selection

**Testing changes**:
```bash
# Test agent detection
python specify_extend.py --agent claude --all --dry-run

# Test multi-agent support
python specify_extend.py --agents claude,copilot --all --dry-run

# Test interactive mode
python specify_extend.py --all

# Test with GitHub token (avoids rate limits)
python specify_extend.py --all --github-token ghp_xxx
```

### Testing Workflow Scripts

Create a test spec-kit project:
```bash
cd /tmp
mkdir test-project && cd test-project
git init
specify init .
python /path/to/spec-kit-extensions/specify_extend.py --all

# Test individual workflow
.specify/scripts/bash/create-bugfix.sh "test bug"
git branch  # Should show: bugfix/001-test-bug
ls specs/bugfix/  # Should show: 001-test-bug/
```

### Working with Templates

Templates are in `extensions/workflows/{workflow}/`:
- Use `{{PLACEHOLDER}}` syntax for variable substitution
- Test placeholders are replaced by creation scripts
- Keep consistent structure across workflows

### Constitution Updates

Two modes:
1. **Direct append** (`--no-llm-enhance`): Appends template to constitution
2. **LLM-enhanced** (`--llm-enhance`, default): Creates one-time command for intelligent merging

Constitution logic:
- Detects existing section numbering (Roman/numeric)
- Continues numbering from highest section
- Avoids duplicating already-present workflows
- Gracefully handles malformed Roman numerals

## Important Files

### Configuration Files

- **`pyproject.toml`** - Python package configuration, version, dependencies
- **`extensions/enabled.conf`** - Controls which workflows are active
- **`CHANGELOG.md`** - Version history for both CLI and templates

### Documentation Files

- **`README.md`** - Main project documentation
- **`INSTALLATION.md`** - Manual installation guide
- **`AI-AGENTS.md`** - Agent-specific setup guides
- **`EXAMPLES.md`** - Real-world usage examples
- **`docs/architecture.md`** - System architecture details
- **`extensions/README.md`** - Extension system overview
- **`extensions/DEVELOPMENT.md`** - Creating custom workflows

### Template Files

- **`docs/constitution-template.md`** - Quality gates template
- **`extensions/workflows/{workflow}/*-template.md`** - Workflow templates

## Common Tasks

### Updating Branch Name Generation

Edit `common.sh` function `generate_branch_name()` (lines 66-112):
- Stop words list: line 71
- Length filtering: lines 84-91
- Word count limits: lines 94-96

Recent improvements:
- Stop word filtering (v2.1.1)
- Length filtering for meaningful words
- Handles acronyms properly

### Adding a New Workflow

1. Create workflow directory: `extensions/workflows/{workflow}/`
2. Add templates: `*-template.md`, `README.md`
3. Create script: `scripts/create-{workflow}.sh`
4. Add command: `commands/speckit.{workflow}.md`
5. Update constitution template: `docs/constitution-template.md`
6. Update `AVAILABLE_EXTENSIONS` in specify_extend.py (line 63)
7. Add to enabled.conf
8. Update documentation

### Updating GitHub API Handling

GitHub API interaction in `specify_extend.py`:
- Rate limit handling: `_parse_rate_limit_headers()` (lines 157-177)
- Error formatting: `_format_rate_limit_error()` (lines 180-207)
- Download logic: `download_latest_release()` (lines 554-618)

Uses `httpx` with SSL verification and follows redirects.

### Handling Agent-Specific Changes

When a new AI agent needs support, see [AGENTS.md](AGENTS.md) for comprehensive instructions on:
- Adding to AGENT_CONFIG
- Updating detection logic
- Creating command templates
- Testing the integration

## Dependencies

**Python (3.11+)**:
- `typer` - CLI framework
- `rich` - Terminal formatting
- `httpx` - HTTP client with SSL support

**Bash**:
- Standard POSIX utilities: `grep`, `sed`, `find`, `git`
- No external bash dependencies

## Testing Considerations

**Non-git repository support**:
- All scripts have fallback logic for non-git repos
- Use `has_git()` checks before git operations
- Provide informative warnings, not errors

**Multiple branches per spec**:
- `find_feature_dir_by_prefix()` supports `bugfix/004-fix-a` and `bugfix/004-fix-b` sharing `specs/bugfix/004-*/`
- Numeric prefix is the key, not full branch name

**Cross-platform**:
- Windows symlink detection (specify_extend.py:884-888)
- Path handling works on Windows/Mac/Linux
- Line ending handling in templates

## Release Process

1. Update version in `pyproject.toml` and `specify_extend.py`
2. Update `CHANGELOG.md` with changes
3. Test installation: `python -m build && pip install dist/*.whl`
4. Create git tag: `git tag -a v1.3.9 -m "Release 1.3.9"`
5. Push: `git push && git push --tags`
6. GitHub Actions will create release automatically
7. Verify release appears on GitHub
8. Test installation from release: `specify-extend --all`

## Reinforcement Learning Process

This repo includes an internal process for improving workflows based on real-world usage data.

**Commands** (for use in this repo only):
- `/rl-intake` - Create an intake to collect usage data from another repository
- `/rl-analyze` - Analyze an intake to generate findings and optimization recommendations

**Documentation**:
- `docs/rl-intake-process.md` - Full process documentation
- `docs/rl-intake/` - Templates for intake, analysis, and optimization

**Workflow**:
1. Collect data from a repo that used spec-kit (chat logs, specs, commits, tests)
2. Create intake document in `specs/rl-intake/`
3. Analyze for prompt clarity, template effectiveness, workflow adherence
4. Generate specific fixes with before/after diffs
5. Apply changes and validate improvements

**Note**: The `specs/` directory is gitignored - intake data stays local.

## Notes for Claude Code

- This repo does NOT use spec-kit workflows on itself (it's the tool, not a project using the tool)
- When testing changes, always test in a separate spec-kit project
- The `--dry-run` flag is your friend for testing
- Constitution patching is the most complex part - be careful with changes
- Branch name generation affects user experience - test thoroughly
- Always verify both `--json` and human-readable output modes work
