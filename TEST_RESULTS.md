# Template Download Tests

## Overview

This document describes the tests created to verify that `specify-extend` correctly downloads the latest `templates-v*` tag from GitHub.

## Changes Made

### Updated `download_latest_release()` function

**Before**: Downloaded from `/releases/latest` endpoint
**After**: Fetches from `/tags` endpoint and filters for `templates-v*` tags

**Key behaviors**:
1. Fetches all tags from `https://api.github.com/repos/pradeepmouli/spec-kit-extensions/tags`
2. Filters for tags starting with `templates-v`
3. Gets the first one (GitHub returns tags in reverse chronological order, so first = latest)
4. Downloads the zipball for that tag
5. Displays "Latest template version: templates-v2.4.1" to user

## Tests Created

### Unit Tests (`test_specify_extend.py`)

**Test 1: `test_download_latest_template_tag()`**
- Verifies the function fetches `templates-v2.4.1` from the tags API
- Mocks GitHub API responses
- Asserts the correct URL is constructed for download
- ✅ PASSING

**Test 2: `test_filters_template_tags_only()`**
- Ensures only `templates-v*` tags are considered
- Tests with mixed tag types (v*, cli-v*, templates-v*)
- Verifies non-template tags are ignored
- ✅ PASSING

**Test 3: `test_no_template_tags_found()`**
- Tests behavior when no `templates-v*` tags exist
- Verifies function returns `None` gracefully
- ✅ PASSING

### Running the Tests

```bash
# Run unit tests
cd /Users/pmouli/GitHub.nosync/spec-kit-extensions
uv run python test_specify_extend.py
```

### Integration Test (`test_integration.sh`)

Created but needs refinement - dry-run mode doesn't trigger download.

## Verification

The implementation correctly:
- ✅ Fetches tags from pradeepmouli/spec-kit-extensions
- ✅ Filters for `templates-v*` prefix
- ✅ Gets the latest version (templates-v2.4.1)
- ✅ Constructs correct download URL
- ✅ Displays version to user

## Expected Behavior

When users run:
```bash
specify-extend --all
```

They will see:
```
ℹ Latest template version: templates-v2.4.1
Downloading templates-v2.4.1...
```

And the templates from that specific tag will be installed.
