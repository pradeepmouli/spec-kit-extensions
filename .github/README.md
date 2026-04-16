# GitHub Workflows & Automation for spec-kit-extensions

This directory contains optional GitHub workflows, issue templates, and AI agent configuration to enhance your spec-kit development experience.

## 📋 Table of Contents

- [Overview](#overview)
- [GitHub Actions Workflows](#github-actions-workflows)
- [GitHub Code Review Integration](#github-code-review-integration)
- [Issue Templates](#issue-templates)
- [AI Agent Integration](#ai-agent-integration)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Overview

These optional GitHub configurations provide:

1. **Review Enforcement** - Automatically require code reviews before merging spec-kit branches
2. **Review Reminders** - Auto-comment on PRs with review instructions
3. **Pull Request Template** - Structured PR template with review checklist
4. **CODEOWNERS Integration** - Automatic reviewer assignment
5. **GitHub Copilot for PRs** - AI-assisted code review with spec-kit awareness
6. **Issue Templates** - Structured templates for each workflow type
7. **Review Helper** - Tools to check review status and validate branches
8. **AI Agent Instructions** - Configuration for GitHub Copilot and other AI agents

## GitHub Actions Workflows

### 1. Spec-Kit Review Required (`spec-kit-review-required.yml`)

**Purpose**: Enforces that spec-kit workflow branches have completed code reviews before merging.

**Triggers**: Runs on pull requests to main/master/develop branches

**What it does**:
- Detects spec-kit branch patterns (bugfix/, modify/, refactor/, etc.)
- Searches for review files in the spec directory
- Validates review status (must be "Approved" or "Approved with Notes")
- Blocks merge if review is missing or shows "Needs Changes"

**Example output**:
```
✅ Spec-kit review check passed!
Branch has been properly reviewed and approved.
```

or

```
❌ Spec-Kit Review Required

This pull request is from a spec-kit workflow branch but does not have
a completed code review.

To complete this PR, please:
1. Run '/speckit.review' command to perform code review
2. Ensure the review status is 'Approved' or 'Approved with Notes'
3. Commit the review file to your branch
4. Push the changes
```

**Branch patterns recognized**:
- `bugfix/001-description`
- `modify/001^002-description`
- `refactor/001-description`
- `hotfix/001-description`
- `deprecate/001-description`
- `cleanup/001-description`
- `baseline/001-description`
- `enhance/001-description`
- `001-feature-name` (standard features)

### 2. Spec-Kit Review Helper (`spec-kit-review-helper.yml`)

**Purpose**: Manual workflow to check review status and validate branches

**Triggers**: Manual dispatch only

**Actions available**:

1. **check-status** - Check review status for current or specified branch
   ```
   🔍 Checking review status for bugfix/001
   ✓ Found spec directory: specs/bugfix/001-login-fix
   ✓ Found review file: specs/bugfix/001-login-fix/review.md
   ✅ Review Status: APPROVED
   This branch is ready to merge!
   ```

2. **list-pending** - List all specs missing reviews
   ```
   🔍 Searching for branches without reviews...
   ⚠️  specs/bugfix/002-auth-issue
      Missing review file - run /speckit.review
   ```

3. **validate-branch** - Validate spec-kit branch has all required files
   ```
   🔍 Validating spec-kit branch: bugfix/001-login-fix
   ✓ Spec directory: specs/bugfix/001-login-fix
   ✓ Found: spec.md
   ✓ Found: plan.md
   ✓ Found: tasks.md
   ✓ Found: review.md
   ✅ Branch validation passed!
   ```

**Usage**:
- Go to Actions tab → Spec-Kit Review Helper → Run workflow
- Select action and optionally specify branch name

### 3. Spec-Kit Review Reminder (`spec-kit-review-reminder.yml`)

**Purpose**: Automatically comments on PRs to remind about review requirements and integrates with GitHub's code review system.

**Triggers**: Runs when PRs are opened or reopened

**What it does**:
- Detects spec-kit workflow branches
- Checks if review file exists and is approved
- Posts helpful comment with review instructions
- Automatically adds labels (`spec-kit:{workflow-type}`, `needs-review`, `review-approved`)
- Optionally requests reviewers (configurable)

**Example comment**:
```markdown
📋 Spec-Kit Review Reminder

## 📋 Review Required

This PR is from a spec-kit workflow branch but doesn't have a completed code review yet.

### Before merging this PR:

1. Complete the code review:
   /speckit.review

2. Verify review status:
   - Review file should be created in your spec directory
   - Status should be "✅ Approved" or "⚠️ Approved with Notes"

3. Commit the review file:
   git add specs/*/review.md
   git commit -m "Add code review"
   git push

💡 Tip: You can run the review helper workflow to check your review status
```

**Features**:
- Provides clear instructions for completing review
- Links to documentation
- Shows workflow-specific guidance
- Auto-labels PRs for tracking
- Integrates with CODEOWNERS for reviewer assignment

## GitHub Code Review Integration

### 4. Pull Request Template (`pull_request_template.md`)

**Purpose**: Structured PR template that guides developers through the spec-kit review process.

**Features**:
- Workflow type selection (bugfix, enhance, modify, etc.)
- Required spec-kit review checklist
- Review file path and status fields
- Testing checklist
- Documentation checklist
- Quality gates checklist

**Key sections**:
- **Spec-Kit Review Completed** - Forces acknowledgment of review requirement
- **Review File Path** - Documents where review is located
- **Review Status** - Documents approval status
- **Pre-Review Checklist** - Ensures review is done before requesting human review

**Integration**:
- Works with automated review enforcement workflow
- Provides context for human reviewers
- Ensures both AI review (/speckit.review) and human review are completed

### 5. CODEOWNERS Configuration (`CODEOWNERS.example`)

**Purpose**: Example configuration for automatic reviewer assignment based on file paths and workflow types.

**Features**:
- Automatic reviewer assignment for different workflow types
- Path-based reviewer assignment (frontend, backend, security, etc.)
- Integration with spec-kit directory structure
- Team and individual reviewer support

**Example patterns**:
```
# Bug fixes reviewed by QA and senior engineers
specs/bugfix/                   @your-org/qa-team @your-org/senior-engineers

# Hotfixes reviewed by engineering leads
specs/hotfix/                   @your-org/engineering-leads

# Frontend code reviewed by frontend team
src/components/                 @your-org/frontend-team

# Security-sensitive files require security team review
src/auth/                       @your-org/security-team
```

**Usage**:
1. Rename `CODEOWNERS.example` to `CODEOWNERS`
2. Replace `@your-org/team-name` with your actual teams
3. Customize patterns for your project structure
4. Commit to `.github/CODEOWNERS`

**How it works with spec-kit**:
1. Developer runs `/speckit.review` (AI review)
2. Developer commits review file and creates PR
3. GitHub automatically requests human reviewers via CODEOWNERS
4. Automated workflow checks AI review is approved
5. Human reviewers perform additional review
6. Both AI + human approval required for merge

### 6. GitHub Copilot for PRs (`copilot.yml`)

**Purpose**: Configures GitHub Copilot to assist with pull request reviews, understanding spec-kit workflows.

**Features**:
- Copilot understands spec-kit workflow types
- Provides review instructions specific to each workflow
- Checks for spec-kit review completion
- Reviews for specification alignment
- Workflow-specific review checklists

**Review instructions include**:
- **Spec-Kit Review Completion** - Verify `/speckit.review` was run
- **Specification Alignment** - Compare implementation to spec.md
- **Workflow-Specific Checks** - Different checks for bugfix vs refactor vs modify
- **Code Quality** - Best practices, security, performance
- **Testing** - Coverage, edge cases, regression tests

**Suggested prompts**:
- "Review this PR for spec-kit workflow compliance"
- "Check if the spec-kit review is completed and approved"
- "Compare this implementation to the specification in specs/"
- "Look for security vulnerabilities in this PR"
- "Check test coverage for this PR"

**Integration**:
- Works with GitHub Copilot for Pull Requests feature
- Complements `/speckit.review` AI review
- Provides context-aware code review assistance
- Helps human reviewers focus on architecture and UX

## Issue Templates

Structured issue templates for each spec-kit workflow type:

### Available Templates

| Template | Label | Workflow Command |
|----------|-------|------------------|
| 🚀 Feature Request | `enhancement`, `spec-kit:feature` | `/speckit.specify` |
| 🐛 Bug Report | `bug`, `spec-kit:bugfix` | `/speckit.bugfix` |
| ✨ Enhancement Request | `enhancement`, `spec-kit:enhance` | `/speckit.enhance` |
| 🔄 Modification Request | `modification`, `spec-kit:modify` | `/speckit.modify` |
| 🔨 Refactoring Request | `refactoring`, `spec-kit:refactor` | `/speckit.refactor` |
| 🚨 Hotfix Request | `hotfix`, `priority:critical`, `spec-kit:hotfix` | `/speckit.hotfix` |
| ⚠️ Deprecation Request | `deprecation`, `spec-kit:deprecate` | `/speckit.deprecate` |
| 🧹 Cleanup Request | `cleanup`, `tech-debt`, `spec-kit:cleanup` | `/speckit.cleanup` |
| 📋 Baseline/Documentation | `documentation`, `baseline`, `spec-kit:baseline` | `/speckit.baseline` |

### Template Features

Each template includes:

- **Structured fields** - Guides users to provide complete information
- **Acceptance criteria** - Checkbox lists for defining completion
- **Priority/severity levels** - Categorize importance
- **Pre-submission checklist** - Ensures quality issues
- **Workflow guidance** - Shows relevant spec-kit commands
- **Auto-labeling** - Automatically adds appropriate labels

### Using Issue Templates

1. Click "New Issue" in your repository
2. Select the appropriate template
3. Fill out all required fields
4. Submit the issue
5. Use the suggested workflow commands to start implementation

## AI Agent Integration

### GitHub Copilot Configuration

**Files**:

- `.github/copilot-instructions.md`
- `.github/copilot.yml.example`

GitHub Copilot support is split across:

- Repository-wide instructions in `.github/copilot-instructions.md`
- Optional PR review configuration in `.github/copilot.yml.example`
- Project-level command agents and prompts generated in user repositories when spec-kit/specify-extend installs Copilot integration

**Key features**:

- Gives Copilot explicit workflow entry points through agents and prompts
- Preserves repository-wide workflow guidance and review requirements
- Supports PR review configuration separately from command execution
- Keeps Copilot aligned with current spec-kit command and review patterns

### Other AI Agents

These configurations are agent-agnostic and work with:
- **GitHub Copilot** - Uses `.github/copilot-instructions.md` here, plus generated `.github/agents/` and `.github/prompts/` in installed target projects
- **Claude Code** - Can read workflow files and issue templates
- **Cursor** - Can use issue templates and workflow patterns
- **Any spec-kit compatible agent**

## Installation

### For New Projects Using spec-kit-extensions

When you install spec-kit-extensions with `specify-extend --all`, these GitHub configurations are **NOT** automatically installed (to keep repositories clean).

To add GitHub workflows and templates to your project:

1. **Copy workflows** (recommended):
   ```bash
   cp path/to/spec-kit-extensions/.github/workflows/spec-kit-review-*.yml .github/workflows/
   ```

2. **Copy PR template** (recommended):
   ```bash
   cp path/to/spec-kit-extensions/.github/pull_request_template.md .github/
   ```

3. **Copy issue templates** (optional):
   ```bash
   cp -r path/to/spec-kit-extensions/.github/ISSUE_TEMPLATE .github/
   ```

4. **Copy GitHub Copilot configuration** (optional, for Copilot users):
   ```bash
   cp path/to/spec-kit-extensions/.github/copilot-instructions.md .github/
   cp path/to/spec-kit-extensions/.github/copilot.yml.example .github/copilot.yml
   ```

   Workflow command agents and prompt files are generated in the target project by the spec-kit/specify-extend installation flow; they are not copied from this repository's `.github/` directory.

5. **Copy CODEOWNERS template** (optional, for teams):
   ```bash
   cp path/to/spec-kit-extensions/.github/CODEOWNERS.example .github/
   # Then customize and rename:
   mv .github/CODEOWNERS.example .github/CODEOWNERS
   # Edit .github/CODEOWNERS to replace @your-org/team-name with actual teams
   ```

6. **Commit the files**:
   ```bash
   git add .github/
   git commit -m "Add spec-kit GitHub workflows and code review integration"
   git push
   ```

### For This Repository (spec-kit-extensions itself)

These files are already present in the repository.

## Usage

### Enforcing Code Reviews

Once `spec-kit-review-required.yml` is installed:

1. **Create a spec-kit branch** and implement your work:
   ```bash
   /speckit.bugfix "fix login issue"
   # ... implement fix ...
   ```

2. **Run code review** (REQUIRED):
   ```bash
   /speckit.review
   ```

3. **Commit the review file**:
   ```bash
   git add specs/bugfix/001-*/review.md
   git commit -m "Add code review for login fix"
   git push
   ```

4. **Create pull request**:
   - The workflow will automatically check for review
   - PR will be blocked if review is missing or not approved
   - PR will pass if review shows "Approved" or "Approved with Notes"

### Checking Review Status

Use the review helper workflow:

1. Go to **Actions** tab in GitHub
2. Select **Spec-Kit Review Helper**
3. Click **Run workflow**
4. Choose action:
   - `check-status` - Check review status for a branch
   - `list-pending` - Find all specs without reviews
   - `validate-branch` - Verify all required files exist
5. Optionally specify branch name
6. Click **Run workflow**

### Creating Issues

1. Go to **Issues** tab
2. Click **New Issue**
3. Select template matching your work type
4. Fill out the form completely
5. Submit
6. Use the suggested commands to start work

## Configuration

### Customizing Review Requirements

Edit `.github/workflows/spec-kit-review-required.yml`:

**Change target branches**:
```yaml
on:
  pull_request:
    branches:
      - main
      - develop
      - staging  # Add custom branches
```

**Change approval patterns**:
```yaml
# Line ~140: Modify grep patterns to match your review format
if grep -qiE '\*\*Status\*\*:?\s*Approved' "$REVIEW_FILE"; then
```

**Add custom branch patterns**:
```yaml
# Line ~30: Add your custom patterns
if [[ "$BRANCH_NAME" =~ ^(bugfix|custom-pattern)/ ]]; then
```

### Customizing Issue Templates

Edit files in `.github/ISSUE_TEMPLATE/`:

**Add custom fields**:
```yaml
- type: input
  id: custom_field
  attributes:
    label: Custom Field
    description: Your custom field description
  validations:
    required: true
```

**Modify labels**:
```yaml
labels: ["bug", "spec-kit:bugfix", "your-custom-label"]
```

**Add new templates**:
Create new `.yml` file in `.github/ISSUE_TEMPLATE/` following the existing format.

### Customizing Copilot Instructions

Edit the Copilot configuration that matches what you want to change:

- `.github/copilot-instructions.md` for repository-wide instructions
- `.github/copilot.yml` if you enable PR review configuration from the example file

If you are customizing a target project after installation, you may also edit generated `.github/agents/*.agent.md` and `.github/prompts/*.prompt.md` files there.

Typical customizations:

- Add project-specific workflow patterns
- Customize review requirements
- Add team conventions
- Include project-specific examples

## Branch Protection Rules (Recommended)

To fully enforce reviews, add branch protection rules:

1. Go to **Settings** → **Branches**
2. Add rule for `main` (or your default branch)
3. Enable:
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - Select: `Check Spec-Kit Review Completion`
4. Optionally enable:
   - Require pull request reviews
   - Require approvals
5. Save changes

This ensures:
- All PRs must pass the review check
- Spec-kit branches must have completed reviews
- Additional human reviews can be required too

## Troubleshooting

### Review Check Failing

**Problem**: PR blocked with "No review file found"

**Solution**:
1. Run `/speckit.review` in your working directory
2. Ensure review.md is created in the spec directory
3. Commit and push the review file
4. Re-run the check

### Review Check Not Finding Spec Directory

**Problem**: "Could not find spec directory"

**Solution**:
1. Verify your branch name matches spec-kit patterns
2. Check spec directory exists in `specs/{workflow-type}/{number}-*/`
3. Ensure directory structure matches spec-kit conventions

### Review Status Not Recognized

**Problem**: Review file exists but status not detected

**Solution**:
Ensure review file contains one of these formats:
```markdown
**Status**: ✅ Approved
```
or
```markdown
**Status**: ⚠️ Approved with Notes
```
or
```markdown
Status: Approved
```

### Issue Templates Not Appearing

**Problem**: Templates don't show up when creating issues

**Solution**:
1. Ensure files are in `.github/ISSUE_TEMPLATE/` directory
2. Verify YAML syntax is valid
3. Push changes to main branch
4. Refresh the New Issue page

## Examples

### Complete Workflow Example

```bash
# 1. Create issue using bug report template (via GitHub UI)

# 2. Start work
/speckit.bugfix "fix authentication timeout"

# 3. Implement the fix
# ... code changes ...

# 4. Run review (REQUIRED)
/speckit.review

# 5. Review creates file: specs/bugfix/001-fix-authentication-timeout/review.md
# Ensure it shows: **Status**: ✅ Approved

# 6. Commit review
git add specs/bugfix/001-*/review.md
git commit -m "Add code review for authentication timeout fix"
git push

# 7. Create PR
gh pr create --title "Fix authentication timeout" --body "Fixes #123"

# 8. GitHub Actions automatically checks for review
# ✅ Spec-kit review check passed!

# 9. Merge PR
gh pr merge
```

### Checking Review Status Example

```bash
# Via GitHub Actions UI
Actions → Spec-Kit Review Helper → Run workflow
- Action: check-status
- Branch: bugfix/001-auth-fix
- Run workflow

# Output:
# ✓ Found spec directory: specs/bugfix/001-auth-fix
# ✓ Found review file: specs/bugfix/001-auth-fix/review.md
# ✅ Review Status: APPROVED
# This branch is ready to merge!
```

## Benefits

### For Teams

- **Consistent quality** - All code is reviewed before merge
- **Clear tracking** - Issue templates provide complete information
- **Automated enforcement** - No manual checking needed
- **Better documentation** - Reviews are committed with code

### For Solo Developers

- **Self-review structure** - Organized review process
- **Quality gates** - Catch issues before merge
- **Documentation** - Review history in git
- **AI assistance** - Copilot helps follow workflows

### For Projects

- **Audit trail** - All work has review documentation
- **Quality metrics** - Track review approvals
- **Process compliance** - Automated enforcement
- **Reduced errors** - Reviews catch bugs early

## Contributing

To improve these workflows:

1. Test changes locally first
2. Create an issue describing the improvement
3. Submit a PR with changes
4. Include examples and documentation

## Support

For questions or issues:

- **GitHub Issues**: [Project issues](../issues)
- **Discussions**: [Project discussions](../discussions)
- **Documentation**: [Main README](../README.md)

## License

These configurations are part of spec-kit-extensions and use the same license as the main project.

---

**Remember**: These are **optional** configurations. You can:
- Use all of them
- Use only what you need
- Customize for your project
- Skip them entirely

The choice is yours!
