---
name: rrdocupdate
description: >
  Generate and update the RR documentation suite (rr_CHANGELOG, rr_CLAUDE_CONTEXT,
  rr_MANIFEST, rr_DATADICTIONARY, rr_DATAFLOW, rr_DEPLOY, rr_TESTING) in the project's
  docs/ folder. Use this skill whenever the user says "RRDocUpdate", "/rrdocupdate",
  or asks to update project documentation. Also use this skill automatically before
  any /commit to ensure docs are current. Triggers on: "update docs", "document changes",
  "RRDocUpdate", "refresh documentation", "update changelog", or any request to
  synchronize the rr_ documentation files with the current project state.
---

# RRDocUpdate - Documentation Artifact Generator

## Overview

Analyze the current project state and session changes, then create or update the standard RR documentation suite in the project's `/docs` folder. Apply changes directly and auto-stage them for git.

---

## Step 1: Establish Project Root and Docs Folder

1. Identify the project root (the git repository root, or the current working directory if not a git repo).
2. Check if a `docs/` folder exists at the project root. If not, create it.
3. Inventory which of the 7 standard `rr_` files exist in `docs/`:
   - `rr_CHANGELOG.md`
   - `rr_CLAUDE_CONTEXT.md`
   - `rr_DATADICTIONARY.md`
   - `rr_DATAFLOW.md`
   - `rr_DEPLOY.md`
   - `rr_MANIFEST.md`
   - `rr_TESTING.md`

---

## Step 2: Scaffold Missing Documents

For any `rr_` file that does NOT exist yet, create it by copying the corresponding template from `E:\local\claude\standard\` and filling in project-specific values:

- Replace `[DATE]` with today's date
- Replace `[PROJECT_NAME]` with the actual project/repo name
- Replace `[NAME]` with "Team" (or the git user.name if available)
- Scan the actual project structure and populate initial content where possible (e.g., directory tree for MANIFEST, detected database type for DATADICTIONARY, detected test framework for TESTING, etc.)

---

## Step 3: Smart Detection - Determine Which Documents Need Updating

Analyze what has changed in the current session. Use the following methods:
- Run `git diff --cached --name-only` and `git diff --name-only` to see staged and unstaged changes
- Run `git status` to see new/untracked files
- Review the conversation history for what was worked on this session

Apply this mapping to determine which documents to update:

| Change Type | Documents to Update |
|---|---|
| New, renamed, or deleted files | `rr_MANIFEST.md` |
| Database schema, model, or migration changes | `rr_DATADICTIONARY.md` |
| API endpoints, integrations, data flow changes | `rr_DATAFLOW.md` |
| Test file additions, test config changes | `rr_TESTING.md` |
| Deployment config, CI/CD, environment, Docker changes | `rr_DEPLOY.md` |
| **Any code changes at all** | `rr_CHANGELOG.md` AND `rr_CLAUDE_CONTEXT.md` |

**IMPORTANT:** `rr_CHANGELOG.md` and `rr_CLAUDE_CONTEXT.md` should ALWAYS be updated when there are any code changes.

---

## Step 4: Update Each Affected Document

### For `rr_MANIFEST.md`:
- Regenerate the directory structure tree from the actual project
- Update the File Registry tables (Source Files, Config Files, Test Files, Scripts, Data Files) with current file info
- Update file line counts and sizes
- Update the File Size Compliance section (flag files over 400 lines)
- Add entries to the Audit Log for files added/removed/renamed

### For `rr_DATADICTIONARY.md`:
- Update table definitions to match current schema/models
- Update column specs, constraints, indexes from actual code
- Update enumerations and constants from actual code
- Update validation patterns if new ones were added

### For `rr_DATAFLOW.md`:
- Update API contracts with new/modified endpoints
- Update sequence diagrams if workflows changed
- Update external system integrations if modified
- Update input/output specifications

### For `rr_TESTING.md`:
- Update test counts and coverage metrics
- Update test file listings
- Update the test execution commands if changed
- Note any new test types or fixtures added

### For `rr_DEPLOY.md`:
- Update software dependencies and versions
- Update environment variables if new ones added
- Update build/deploy commands if changed
- Update infrastructure details if modified

### For `rr_CHANGELOG.md` (ALWAYS on code changes):
- **Append** new entries under the `## [Unreleased]` section
- Categorize changes into: Added, Changed, Deprecated, Removed, Fixed, Security
- Add a Claude Sessions entry with today's date and a summary of the session work
- **NEVER** overwrite or remove existing changelog history

### For `rr_CLAUDE_CONTEXT.md` (ALWAYS on code changes):
- **Update** the "Current Project State" table (phase, health, last updated date)
- **Update** the "Immediate Priorities" section (move completed items, add new blockers/in-progress items)
- **Update** the "Active Branch" section
- **Append** a new entry to "Previous Session Notes" with:
  - What was accomplished
  - What was attempted but didn't work
  - Key decisions made
  - Open questions
- **Update** the "Session Handoff Checklist"
- **NEVER** overwrite existing session history

---

## Step 5: Auto-Stage Documentation

After all updates are written:

```bash
git add docs/rr_*.md
```

---

## Step 6: Report

Output a brief summary in this format:

```
--- RRDocUpdate Complete ---

Created:
- [list any newly scaffolded documents]

Updated:
- [list each updated document with a 1-line summary of what changed]

Staged:
- [count] documentation files staged for commit
```

---

## Important Rules

1. **Never delete existing content** in CHANGELOG or CLAUDE_CONTEXT - only append/update sections
2. **Always use the actual project state** - read real files, real git status, real directory structure
3. **Keep template structure intact** - maintain all section headers and table formats from the templates
4. **Date everything** - all new entries should include today's date
5. **Be concise but accurate** - document what actually changed, not boilerplate
6. **If this is triggered before a /commit**, complete all doc updates and staging BEFORE the commit is created
7. **Templates location**: `E:\documentation` contains the canonical templates for scaffolding new documents
