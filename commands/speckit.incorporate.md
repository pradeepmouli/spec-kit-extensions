---
description: "Incorporate documents into workflows and advance stages intelligently"
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

## Overview

Incorporate external documents (specs, plans, research, checklists, etc.) into existing workflows or initiate new workflows using the document as context. This command intelligently:

1. **Detects document type** - Identifies what kind of document it is
2. **Detects workflow context** - Determines if you're in a workflow and at what stage
3. **Advances workflow stages** - Automatically progresses to appropriate stage
4. **Leverages analysis** - Uses `/speckit.analyze` for intelligent incorporation

## Usage

```bash
/speckit.incorporate <document-path> [--type TYPE] [--workflow WORKFLOW] [--stage STAGE] [--enrich] [--dry-run]
```

**Options:**
- `--type TYPE` - Force document type (spec|plan|tasks|research|checklist|postmortem)
- `--workflow WORKFLOW` - Initiate specific workflow if not in one (baseline|bugfix|enhance|modify|refactor|hotfix|deprecate|cleanup)
- `--stage STAGE` - Target stage (auto|current|spec|plan|tasks)
- `--enrich` - Enrich current stage docs instead of advancing (default for research)
- `--dry-run` - Show what would be done without making changes

## Step 1: Load Workflow Context

First, get current workflow context:

```bash
cd "$(git rev-parse --show-toplevel)" && \
source .specify/scripts/bash/common.sh && \
CURRENT_BRANCH=$(get_current_branch) && \
echo "Current branch: $CURRENT_BRANCH" && \
get_feature_paths
```

This provides:
- `CURRENT_BRANCH` - Current git branch
- `FEATURE_DIR` - Feature directory path (if in workflow)
- `FEATURE_SPEC` - Main specification file
- `IMPL_PLAN` - Implementation plan file
- `TASKS` - Task list file

**Determine workflow stage:**
- If `FEATURE_DIR` not found → Not in workflow
- If only spec exists → Spec stage
- If spec + plan exist → Planning stage
- If spec + plan + tasks exist → Task stage

## Step 2: Analyze the Document

Use native spec-kit analyze to understand the document:

```bash
/speckit.analyze <document-path>
```

**From the analysis, identify:**
1. **Document Type** - What kind of document is this?
   - **Spec/Requirements** - Goals, acceptance criteria, architecture
   - **Plan/Approach** - Implementation steps, technical decisions
   - **Tasks** - Concrete action items, checklist format
   - **Research** - Background info, API docs, examples, findings
   - **Checklist** - Validation items, testing scenarios
   - **Post-mortem** - Incident analysis, lessons learned

2. **Key Content Areas** - Main sections and topics covered

3. **Completeness** - Is it comprehensive or partial?

4. **Conflicts** - Does it contradict existing workflow docs?

**Detection Patterns:**
- **Spec indicators**: "Requirements", "Goals", "Acceptance Criteria", "Architecture", "User Stories"
- **Plan indicators**: "Implementation", "Approach", "Technical Design", "Steps", "Strategy"
- **Tasks indicators**: Checkbox lists, numbered action items, "TODO", "Task", specific assignments
- **Research indicators**: "Background", "Investigation", "Findings", "Documentation", external links
- **Checklist indicators**: Validation lists, test scenarios, "Verify", "Ensure", "Check"

## Step 3: Determine Action Strategy

Based on workflow context and document type, choose strategy:

### Scenario A: Not in Workflow (No FEATURE_DIR)

**Action: Initiate Workflow**

1. If `--workflow` specified, use that. Otherwise, determine from document content:
   - Contains "bug", "fix", "regression" → bugfix
   - Contains "refactor", "cleanup code", "improve" → refactor
   - Contains "hotfix", "urgent", "production" → hotfix
   - Contains "deprecate", "sunset", "remove" → deprecate
   - Contains "baseline", "context", "current state" → baseline
   - Contains "enhance", "minor improvement" → enhance
   - Otherwise → Ask user for workflow type

2. Execute appropriate workflow creation script:
   ```bash
   # For bugfix example:
   .specify/scripts/bash/create-bugfix.sh "Description from document title"
   ```

3. Incorporate the document into the newly created workflow directory

### Scenario B: In Workflow - Document Type Matches Current Stage

**Action: Enrich Current Stage**

Append or merge document content into existing stage document:

```bash
# Example: In spec stage with research document
cat >> "$FEATURE_SPEC" << 'EOF'

## Additional Research

<content from research document>
EOF
```

### Scenario C: In Workflow - Document Type is Next Stage

**Action: Advance to Next Stage**

**C1: Have spec, document is plan**
```bash
# Use native spec-kit plan command with document as context
/speckit.plan

# Then incorporate plan content into plan.md
# The agent will use the provided document as primary reference
```

**C2: Have spec + plan, document is tasks**
```bash
# Use native spec-kit tasks command with document as context
/speckit.tasks

# Then incorporate task content into tasks.md
```

### Scenario D: In Workflow - Document Type Skips Stages

**Action: Create Intermediate Stages, Then Advance**

**Example: Have spec only, document is tasks**

1. First, create minimal plan:
   ```bash
   /speckit.plan
   # Agent creates basic plan to bridge the gap
   ```

2. Then, create tasks using document:
   ```bash
   /speckit.tasks
   # Agent uses provided document as primary task source
   ```

### Scenario E: Document Type is Research/Checklist

**Action: Enrich Most Relevant Stage Document**

Research and checklists are supplementary - don't advance stages, just enrich:

- **Research** → Add to spec.md (background section) or plan.md (approach section)
- **Checklist** → Add to tasks.md (validation section) or create separate checklist.md

## Step 4: Intelligent Incorporation

When incorporating document content:

### 4.1 Check for Conflicts

Compare document with existing content:

```bash
# If conflicts detected by analyze
# Present to user:
echo "⚠️  Potential conflicts detected:"
echo "  - Document says X"
echo "  - Existing spec says Y"
echo ""
echo "Options:"
echo "  1. Keep existing (skip conflicting parts)"
echo "  2. Replace with new (update existing)"
echo "  3. Mark as NEEDS RECONCILIATION (both present)"
```

### 4.2 Detect Duplicates

If analyze indicates overlapping content:
- Skip truly duplicate content
- Merge complementary information
- Note: "Incorporated X from document, skipped Y (already covered)"

### 4.3 Structure Content

When adding to existing docs:
- Maintain document structure (use existing headers)
- Add new sections if needed
- Preserve formatting consistency
- Add source attribution: `<!-- Incorporated from: document-name.md -->`

### 4.4 Preserve Git History

Before making changes:
```bash
# Ensure changes are trackable
git diff --exit-code || echo "Uncommitted changes exist"
```

## Step 5: Provide Feedback

Clearly summarize what was done:

```
✅ Incorporated document: research-notes.md

Actions taken:
  • Detected document type: Research
  • Current workflow: bugfix/001-login-error
  • Current stage: Spec
  • Action: Enriched bug-report.md with research findings
  
Added sections:
  - Background on authentication flow
  - API documentation excerpts
  - Similar bug references

Next steps:
  - Review incorporated content in bug-report.md
  - Run: /speckit.plan (when ready to move to planning)
```

## Step 6: Suggest Next Actions

Based on workflow state after incorporation:

```
Workflow Progress:
  [✓] Spec      - bug-report.md (enriched)
  [ ] Plan      - Ready to create with: /speckit.plan
  [ ] Tasks     - Awaiting plan completion

Suggested: Review the enriched spec, then run /speckit.plan to continue.
```

## Examples

### Example 1: Incorporate Research into Existing Bugfix

```bash
# You're in bugfix/001-login-error with bug-report.md
/speckit.incorporate api-authentication-research.md

# Result:
# ✅ Detected: Research document
# ✅ Added to bug-report.md under "Background Research" section
# ✅ Spec stage enriched, ready for planning
```

### Example 2: Incorporate Plan to Advance Stage

```bash
# You're in enhance/023-improve-ui with enhancement-spec.md
/speckit.incorporate implementation-approach.md

# Result:
# ✅ Detected: Plan document
# ✅ Executed: /speckit.plan using implementation-approach.md
# ✅ Created: plan.md
# ✅ Advanced to planning stage
```

### Example 3: Initiate Workflow from Document

```bash
# Not in any workflow
/speckit.incorporate hotfix-analysis.md --workflow hotfix

# Result:
# ✅ Detected: Hotfix needed
# ✅ Executed: create-hotfix.sh "Issue from analysis"
# ✅ Created: hotfix/001-issue/
# ✅ Incorporated hotfix-analysis.md into hotfix-spec.md
```

### Example 4: Skip Stages with Task List

```bash
# You're in refactor/005-cleanup with refactor-spec.md only
/speckit.incorporate detailed-task-breakdown.md

# Result:
# ⚠️  Document is tasks, but no plan exists
# ✅ Creating minimal plan first...
# ✅ Created: plan.md (basic)
# ✅ Executing: /speckit.tasks using detailed-task-breakdown.md
# ✅ Created: tasks.md
# ✅ Advanced from spec → plan → tasks stage
```

### Example 5: Dry Run

```bash
/speckit.incorporate research.md --dry-run

# Result:
# 🔍 Dry Run - No changes will be made
# 
# Would perform:
#   • Document type: Research
#   • Current stage: Spec (bug-report.md)
#   • Action: Enrich bug-report.md
#   • New section: "Background Research"
#   • Lines to add: ~45 lines
#   
# To execute: /speckit.incorporate research.md
```

## Error Handling

### Document Not Found
```
❌ Error: Document not found: nonexistent.md
Please check the path and try again.
```

### Cannot Determine Workflow Type
```
❌ Cannot determine appropriate workflow type from document.
Please specify: /speckit.incorporate document.md --workflow [type]

Available workflows:
  baseline, bugfix, enhance, modify, refactor, hotfix, deprecate, cleanup
```

### Conflicts Detected
```
⚠️  Conflicts detected - user input required
Cannot auto-merge due to contradictions.

Please resolve manually or use:
  --force-append  (add as-is with conflict marker)
  --skip-conflicts (skip conflicting sections)
```

## Best Practices

1. **Use analyze first** for unfamiliar documents
2. **Review enriched docs** before advancing stages
3. **Commit after incorporation** to preserve history
4. **Use --dry-run** for complex incorporations
5. **Specify --type** if detection might be ambiguous
6. **Keep original documents** (don't delete after incorporation)

## Integration with Other Commands

- **`/speckit.analyze`** - Analyze document before incorporating
- **`/speckit.review`** - Review after incorporation to validate
- **`/speckit.plan`** - Called automatically when advancing to plan stage
- **`/speckit.tasks`** - Called automatically when advancing to tasks stage
- **Workflow creation scripts** - Called when initiating new workflows

---

**Note**: This is a command extension - it doesn't create workflow structures itself, but works with existing workflows and delegates to appropriate workflow commands/scripts.
