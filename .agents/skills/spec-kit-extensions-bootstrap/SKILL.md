---
name: spec-kit-extensions-bootstrap
description: Use when installing, upgrading, bootstrapping, or repairing spec-kit-extensions in a project. Triggers on requests like "install spec-kit-extensions", "set up speckit workflows", "upgrade specify-extend", "bootstrap spec-kit workflows", or "fix spec-kit-extensions install".
user-invocable: true
---

# Spec-Kit Extensions Bootstrap

Use this skill when the task is specifically about getting spec-kit-extensions installed or upgraded correctly.

## Purpose

This skill gives an agent a reliable install and upgrade procedure for spec-kit-extensions without relying on stale assumptions about native spec-kit extension upgrade behavior.

## Default Path

For most projects, use this sequence:

```bash
# 1. Install or update spec-kit CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 2. Initialize spec-kit in the target repo if needed
specify init . --ai claude

# 3. Install or upgrade spec-kit-extensions
pip install -U specify-extend
specify-extend --all
```

## Core Rules

1. Prefer `specify-extend --all` over raw `specify extension add`.
2. For upgrades of an already-installed `workflows` extension, do not depend on `specify extension add` succeeding.
3. If the user wants multiple agents reconciled, use:

```bash
specify-extend --agents claude,copilot --all
```

4. If the user wants curated workflow packages too, use:

```bash
specify-extend --all --with-workflows recommended
```

5. If the user wants curated companion extensions, use:

```bash
specify-extend --all --with-community recommended
```

## Upgrade Guidance

When the target project already has `.specify/extensions/workflows/extension.yml`, treat the operation as an upgrade.

Recommended command:

```bash
pip install -U specify-extend
specify-extend --all
```

Important:

- Do not tell the user to upgrade the existing workflows extension by manually re-running `specify extension add workflows ...`.
- Native `specify extension add` can fail on re-install or upgrade of an existing extension.
- `specify-extend --all` is the supported path because it can patch branch validation and use compatibility upgrade behavior when needed.

## Local Development Bootstrap

When validating a local checkout of spec-kit-extensions against another repo:

```bash
specify-extend --all --extension-source ../spec-kit-extensions
```

If workflow packages should also come from the local checkout:

```bash
specify-extend --all --extension-source ../spec-kit-extensions --with-workflows recommended
```

## Advanced Manual Path

Use this only when the user explicitly wants native spec-kit install behavior and understands the tradeoffs:

```bash
specify extension add workflows --from https://github.com/pradeepmouli/spec-kit-extensions/archive/refs/heads/main.zip
specify-extend --patch
```

Caveat:

- This manual path is acceptable for first-time installation.
- It is not the preferred upgrade path for an already-installed workflows extension.

## Verification

After install or upgrade, verify with:

```bash
specify extension list
```

Then validate a command is available:

```text
/speckit.bugfix "test bug"
```

## Troubleshooting Checklist

If install fails, check these in order:

1. `specify` is on `PATH`
2. `.specify/` exists in the target repo
3. The repo was initialized with `specify init`
4. The user is using `specify-extend --all` instead of manually re-adding an existing extension
5. If using local dev mode, the path passed to `--extension-source` contains `extension.yml`

## What Not To Do

- Do not assume `.claude/skills/` or `.github/skills/` are created by this repo.
- Do not tell the user to manually copy bundled skills as part of normal extension installation.
- Do not treat `specify extension add` as the default upgrade mechanism for an already-installed workflows extension.