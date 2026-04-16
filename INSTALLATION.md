# Installation Guide

This guide covers the supported ways to install `spec-kit-extensions` in a spec-kit project.

## Prerequisites

Before installing, ensure you have:

- `spec-kit` installed from source with extension support
  ```bash
  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
  ```
- A Git repository initialized for your project
- An AI coding agent configured with `specify init --ai ...` if you want agent-specific commands installed automatically

## Recommended Install

The recommended path is to use `specify-extend`. It installs the workflows extension through native spec-kit commands, reconciles requested agent integrations, and patches spec-kit's branch validation so typed workflow branches such as `bugfix/...` and `refactor/...` work correctly.

```bash
# 1. Initialize spec-kit in your project
cd your-project
specify init --here --ai claude

# 2. Install the CLI tool
pip install specify-extend
# or run it without a persistent install:
# uvx specify-extend --all

# 3. Install this extension pack
specify-extend --all

# 4. Verify installation
specify extension list
```

What this does:

- Detects or reconciles your target agent integrations
- Installs the workflows extension through native `specify extension add`
- Installs workflow scripts and command files for the active agent(s)
- Updates constitution and enabled workflow state
- Patches `common.sh` for extension branch patterns

## Common Variants

### Multiple agents

```bash
specify-extend --agents claude,copilot,cursor-agent --all
```

### Local development source

Use this when validating local, unpushed changes from a checkout of this repository.

```bash
specify-extend --all --extension-source ../spec-kit-extensions
```

`specify-extend` stages a sanitized temporary copy of that checkout and installs it via native `specify extension add --dev`, which avoids copying generated `.specify` state back into the install.

### Curated companion extensions

```bash
specify-extend --list-community
specify-extend --all --with-community recommended
```

### Curated workflow packages

```bash
specify-extend --list-workflows
specify-extend --all --with-workflows recommended
```

### PowerShell scripts

```bash
specify-extend --all --script ps
```

### Git hooks and GitHub integration

```bash
specify-extend --all --hooks --github-integration
```

## Native Install Without The CLI

This path is supported, but it does not patch spec-kit's branch validation on its own. Use it only if you explicitly want native extension installation behavior and are prepared to patch branch handling separately.

```bash
# Install the workflows extension directly
specify extension add workflows --from https://github.com/MartyBonacci/spec-kit-extensions/archive/refs/heads/main.zip

# Then patch branch validation for typed workflow branches
specify-extend --patch
```

## Verification

After installation, verify everything works:

```bash
# Extension should be listed
specify extension list

# A workflow command should resolve
/speckit.workflows.bugfix "test bug"

# Alias should also resolve
/speckit.bugfix "test bug"
```

You can also verify installed files directly:

```bash
ls .specify/extensions/
ls .specify/scripts/bash/create-*.sh
ls .specify/scripts/powershell/create-*.ps1 2>/dev/null || true
ls .claude/commands/*.md 2>/dev/null || true
ls .github/agents/*.agent.md 2>/dev/null || true
ls .github/prompts/*.prompt.md 2>/dev/null || true
```

## Installed Layout

After a standard install, your project will contain the extension under `.specify/extensions/workflows/` plus agent-specific command assets.

Typical layout:

```text
your-project/
├── .specify/
│   ├── extensions/
│   │   └── workflows/
│   │       ├── extension.yml
│   │       ├── commands/
│   │       ├── scripts/
│   │       └── templates/
│   ├── scripts/
│   │   ├── bash/
│   │   └── powershell/
│   └── memory/
│       └── constitution.md
├── .claude/commands/
├── .github/agents/
└── .github/prompts/
```

The exact agent-specific directories depend on the configured agent:

- Claude Code installs command files under `.claude/commands/`
- GitHub Copilot installs agent and prompt files under `.github/agents/` and `.github/prompts/`
- Cursor installs command files under `.cursor/commands/`
- Gemini CLI and Qwen install Markdown command files under their command directories

## Configuration

### Enable or disable workflows

Edit `.specify/extensions/enabled.conf` to control which workflows are active.

```bash
bugfix
# refactor
```

### Customize templates

Workflow templates live under `.specify/extensions/workflows/templates/` in installed projects.

```bash
nano .specify/extensions/workflows/templates/bugfix/bug-report-template.md
```

### Review constitution updates

`specify-extend` updates `.specify/memory/constitution.md` with extension quality gates. Review that file if your project has a customized constitution.

## Troubleshooting

### `No .specify directory found`

Initialize spec-kit first:

```bash
specify init --here --ai claude
```

### Agent commands were not installed where I expected

Force the target agent explicitly:

```bash
specify-extend --ai claude --all
specify-extend --ai copilot --all
specify-extend --ai cursor-agent --all
```

For multi-agent repos, use:

```bash
specify-extend --agents claude,copilot --all
```

### Local extension source validation failed

`--extension-source` must point at the repository root containing `extension.yml`, `commands/`, `scripts/`, and `templates/`.

```bash
specify-extend --all --extension-source /path/to/spec-kit-extensions
```

### Scripts are not executable

```bash
chmod +x .specify/scripts/bash/create-*.sh
```

### Native install worked, but workflow branches are rejected

Patch spec-kit's branch validation:

```bash
specify-extend --patch
```

### Commands do not work for my AI agent

See [AI-AGENTS.md](AI-AGENTS.md) for agent-specific expectations and setup details. In current installs:

- GitHub Copilot uses `.github/agents/` and `.github/prompts/`
- Cursor uses `.cursor/commands/`
- Manual fallback is always available by running the generated scripts directly

## Updating

Check current versions:

```bash
specify-extend --version
grep -n "version:" .specify/extensions/workflows/extension.yml
```

This project has two independently versioned parts:

- Extension templates and workflow pack
- The `specify-extend` CLI

To update using the published source:

```bash
pip install --upgrade specify-extend
specify-extend --all
```

To update from a local checkout:

```bash
specify-extend --all --extension-source /path/to/spec-kit-extensions
```

## Uninstalling

To remove the extension from a project:

```bash
rm -rf .specify/extensions/
rm -f .specify/scripts/bash/create-{baseline,bugfix,cleanup,deprecate,enhance,hotfix,modification,refactor}.sh
rm -f .specify/scripts/powershell/create-{baseline,bugfix,cleanup,deprecate,enhance,hotfix,modification,refactor}.ps1
rm -f .claude/commands/speckit.*.md
rm -f .github/agents/speckit.*.agent.md
rm -f .github/prompts/speckit.*.prompt.md
rm -f .cursor/commands/speckit.*.md
```

Then manually review `.specify/memory/constitution.md` if you want to remove previously added workflow quality-gate text.

## Next Steps

After installation:

1. Read [extensions/QUICKSTART.md](extensions/QUICKSTART.md)
2. Try a real workflow such as `/speckit.workflows.bugfix` or `/speckit.workflows.enhance`
3. Review [AI-AGENTS.md](AI-AGENTS.md) if you are working in a multi-agent setup
4. Review [docs/specify-extend.md](docs/specify-extend.md) for advanced CLI usage

## Getting Help

- Installation and usage guidance: [README.md](README.md)
- Agent-specific guidance: [AI-AGENTS.md](AI-AGENTS.md)
- Advanced CLI reference: [docs/specify-extend.md](docs/specify-extend.md)
- Core spec-kit issues: https://github.com/github/spec-kit
