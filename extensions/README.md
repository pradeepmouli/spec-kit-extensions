# Specify Extension System

The extension system provides additional workflow types beyond the core `/specify` workflow for feature development.

## Available Workflows

### Core Workflow (Built-in)
- **`/specify`** - Create new features from scratch (greenfield development)

### Extension Workflows
- **`/bugfix`** - Quick bug remediation with regression tests
- **`/modify`** - Extend or modify existing features with impact analysis
- **`/refactor`** - Improve code quality while preserving behavior
- **`/hotfix`** - Emergency production fixes with expedited process
- **`/deprecate`** - Planned sunset of features with migration guides

## Enabling Extensions

Extensions are enabled by default in this project. To disable an extension, edit `.specify/extensions/enabled.conf` and comment out the workflow.

## Workflow Selection Guide

| Scenario | Use This Workflow |
|----------|------------------|
| Building new feature | `/specify` |
| Fixing a bug | `/bugfix` |
| Adding fields to existing feature | `/modify` |
| Extracting duplicate code | `/refactor` |
| Production is down | `/hotfix` |
| Removing old feature | `/deprecate` |

## Extension Structure

Each workflow extension contains:
- **Template files** - Markdown templates for specs and documentation
- **Command definition** - `.claude/commands/{workflow}.md` for AI agents
- **Bash scripts** - `.specify/scripts/bash/create-{workflow}.sh` for automation
- **Tasks template** - Customized task breakdown for the workflow type

## Creating Custom Extensions

See `docs/extension-development.md` for guide on creating your own workflow extensions.

## Compatibility

These extensions are designed to be:
- **Agent-agnostic** - Work with Claude Code, GitHub Copilot, Gemini CLI, etc.
- **Non-breaking** - Don't modify core Specify functionality
- **Spec Kit compatible** - Follow GitHub Spec Kit conventions for future contribution

## Version

Extension System Version: 1.0.0
Compatible with Specify Core: v0.0.30+

## License

Same license as parent project (Specify/Spec Kit)
