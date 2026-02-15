# Migration Guide: Legacy → Native Extension System

This guide helps you migrate from the legacy `specify-extend` CLI tool to the native spec-kit v0.0.93+ extension system.

## Overview

**What's Changing**:
- **Installation**: `specify-extend --all` → `specify extension add spec-kit-workflows`
- **Location**: Files move from `.specify/extensions/workflows/` → `.specify/extensions/spec-kit-workflows/`
- **Configuration**: `enabled.conf` → `config.yml` (YAML format)
- **No more patching**: Extension uses hooks instead of patching `common.sh`

**Why Migrate**:
- ✅ Simpler installation and updates
- ✅ Native spec-kit integration
- ✅ Better compatibility with future spec-kit versions
- ✅ No more fragile file patching
- ✅ Standardized extension format

## Migration Paths

Choose the migration path that fits your situation:

### Path 1: Fresh Installation (Recommended)

**Best for**: New projects or when you want a clean slate

1. **Remove legacy installation**:
   ```bash
   # Uninstall old extension (if you have specify-extend installed)
   pip uninstall specify-extend

   # Or manually remove the old files
   rm -rf .specify/extensions/workflows
   rm -f .specify/extensions/enabled.conf

   # Restore original common.sh if patched
   cd .specify/scripts/bash
   if [ -f common.sh.backup ]; then
       mv common.sh.backup common.sh
   fi
   ```

2. **Install native extension**:
   ```bash
   # From catalog (requires spec-kit v0.0.93+)
   specify extension add spec-kit-workflows

   # Or directly from GitHub
   specify extension add --from https://github.com/pradeepmouli/spec-kit-extensions/releases/latest
   ```

3. **Verify installation**:
   ```bash
   specify extension list
   # Should show: spec-kit-workflows (v2.3.0)

   # Test a command
   /speckit.workflows.bugfix --help
   ```

### Path 2: Automated Migration

**Best for**: Existing installations with data you want to preserve

1. **Run migration script**:
   ```bash
   # Download migration script
   curl -sSL https://raw.githubusercontent.com/pradeepmouli/spec-kit-extensions/main/scripts/migrate-to-native.sh > migrate.sh
   chmod +x migrate.sh

   # Run migration
   ./migrate.sh
   ```

2. **Install native extension**:
   ```bash
   specify extension add spec-kit-workflows
   ```

3. **Verify migration**:
   ```bash
   # Check extension is installed
   specify extension list

   # Test workflows still work
   /speckit.workflows.bugfix "test migration"

   # Verify existing specs are still accessible
   ls specs/bugfix/  # Your existing workflow directories should still be there
   ```

### Path 3: Manual Migration

**Best for**: Custom setups or when you need full control

1. **Backup current installation**:
   ```bash
   cp -r .specify/extensions .specify/extensions-backup-$(date +%Y%m%d)
   ```

2. **Remove old extension files**:
   ```bash
   rm -rf .specify/extensions/workflows
   rm -f .specify/extensions/enabled.conf
   ```

3. **Restore original common.sh**:
   ```bash
   cd .specify/scripts/bash
   if [ -f common.sh.backup ]; then
       mv common.sh.backup common.sh
   fi
   ```

4. **Install native extension**:
   ```bash
   specify extension add spec-kit-workflows
   ```

5. **Migrate configuration** (if you customized `enabled.conf`):

   Old `enabled.conf`:
   ```
   baseline=true
   bugfix=true
   modify=false
   ```

   New `.specify/extensions/spec-kit-workflows/config.yml`:
   ```yaml
   workflows:
     baseline: true
     bugfix: true
     modify: false
   ```

## Configuration Changes

### Enabled Workflows

**Legacy** (`.specify/extensions/enabled.conf`):
```
baseline=true
bugfix=true
enhance=true
modify=true
refactor=true
hotfix=true
deprecate=false
cleanup=false
```

**Native** (`.specify/extensions/spec-kit-workflows/config.yml`):
```yaml
workflows:
  baseline: true
  bugfix: true
  enhance: true
  modify: true
  refactor: true
  hotfix: true
  deprecate: false
  cleanup: false
```

### Branch Validation

**Legacy**: Patched `common.sh` to add validation

**Native**: Hook-based validation (automatic)
```yaml
branch_validation:
  enabled: true
  extra_prefixes: []
```

### Constitution Updates

**Legacy**: Manual or LLM-enhanced CLI flags

**Native**: Configuration-driven
```yaml
constitution:
  auto_update: true
  numbering_style: "auto"
```

## Path Changes

All file paths have changed to use the new extension structure:

| Old Path | New Path |
|----------|----------|
| `.specify/scripts/bash/create-bugfix.sh` | `.specify/extensions/spec-kit-workflows/scripts/create-bugfix.sh` |
| `.specify/extensions/workflows/bugfix/bug-report-template.md` | `.specify/extensions/spec-kit-workflows/workflows/bugfix/bug-report-template.md` |
| `.specify/scripts/bash/common.sh` (patched) | `.specify/extensions/spec-kit-workflows/scripts/common.sh` |

**Important**: These path changes are handled automatically by the native extension system. You don't need to update your existing workflow directories or specs.

## Troubleshooting

### Issue: Commands not found after installation

**Solution**: Verify extension is installed and enabled
```bash
specify extension list
specify extension enable spec-kit-workflows
```

### Issue: Scripts reference old paths

**Solution**: This shouldn't happen with the native extension. If it does:
```bash
# Reinstall the extension
specify extension remove spec-kit-workflows
specify extension add spec-kit-workflows
```

### Issue: Branch validation not working

**Solution**: Check validation hook configuration
```bash
# Edit config to enable validation
vim .specify/extensions/spec-kit-workflows/config.yml

# Ensure branch_validation.enabled is true
```

### Issue: Constitution not updated

**Solution**:
```bash
# Check constitution config
vim .specify/extensions/spec-kit-workflows/config.yml

# Set constitution.auto_update to true
# Or manually run constitution update command
/speckit.workflows.enhance-constitution
```

### Issue: Old patched common.sh causing conflicts

**Solution**: Restore original
```bash
cd .specify/scripts/bash
if [ -f common.sh.backup ]; then
    cp common.sh.backup common.sh
    rm common.sh.backup
fi
```

## Version Compatibility

| Extension Version | Requires spec-kit | Notes |
|-------------------|-------------------|-------|
| v2.3.0+ (native) | >= 0.0.93 | Native extension format |
| v2.1.x (legacy) | >= 0.0.80 | Uses `specify-extend` CLI |
| v2.0.x (legacy) | >= 0.0.70 | Legacy format |

## Rollback

If you need to rollback to the legacy system:

1. **Remove native extension**:
   ```bash
   specify extension remove spec-kit-workflows
   ```

2. **Restore backup**:
   ```bash
   # If you created a backup
   cp -r .specify/extensions-backup-YYYYMMDD .specify/extensions
   ```

3. **Reinstall legacy version**:
   ```bash
   pip install specify-extend==2.1.1
   specify-extend --all
   ```

## Getting Help

- **Migration issues**: [Open an issue](https://github.com/pradeepmouli/spec-kit-extensions/issues)
- **spec-kit questions**: [spec-kit repo](https://github.com/github/spec-kit)
- **Documentation**: [README.md](README.md) and [INSTALLATION.md](INSTALLATION.md)

## FAQ

**Q: Do I need to migrate my existing spec directories?**
A: No! Your `specs/` directories are not affected by this migration. Only the installation structure changes.

**Q: Can I use both legacy and native at the same time?**
A: No, you should use one or the other. The native format is recommended for all new installations.

**Q: Will my existing workflows still work?**
A: Yes, the workflows themselves are identical. Only the installation method and file locations change.

**Q: What about my custom modifications?**
A: Custom workflow templates and scripts can be preserved by copying them to the new location after installation. See the native extension's documentation for customization guidelines.

**Q: Do agent commands change?**
A: Yes for native installs. Native commands use `/speckit.workflows.*` (e.g. `/speckit.workflows.bugfix`). Legacy installs keep `/speckit.*`.

---

*For the complete migration plan and technical details, see [plan.md](plan.md)*
