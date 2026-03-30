# JTBD Workflow Design

**Date:** 2026-03-30
**Status:** Approved

## Context

The JTBD (Jobs To Be Done) effort transforms RHDH documentation headings from topic-oriented to outcome-oriented. 27 jobs have been identified in a Google Sheet. The sheet is mostly filled in and needs validation before handoff to writers.

Multiple stakeholders with different tool preferences:

- **Content Strategist (CS):** authors in Google Sheets
- **Stakeholders:** validate headings and scope (approval happens in the Sheet; some will want to go deeper into content mapping)
- **Technical writers:** pick up tasks from Jira, implement in rhdh-docs via Git
- **Claude:** works in Markdown in this repository

## Design principle

Markdown files in `docs/jobs/` are the pivot point between all tools. In phase 1 they are generated from the sheet. In phase 2 the CS may edit them directly. The Jira pipeline is identical in both phases — no rework required on transition.

## Architecture

Four scripts, one data flow:

```
Google Sheet → XLSX export → [extract] → data/jobs.json
                                                    ↓
rhdh-docs main ──────────── [check-current-state] ──┘
                                                    ↓
                             [generate-plans] → docs/plan.md
                                             → docs/jobs/job-NN.md
                                                    ↓
                              [create-jiras] → Jira tasks (children of JTBD epic)
```

The JTBD Jira epic already exists. All tasks are created as children of that epic.

## Script: `extract`

**Input:** `data/*.xlsx` (latest file, or path argument)
**Output:** `data/jobs.json`

Refactors the parsing logic already in `scripts/import-jobs` into a standalone step. Reads two tabs:

- **"Phase 3 Jobs":** job number, name, statement, category, priority
- **"Phase 3 JTBD - All-in Proposal":** source content → proposed heading mapping per job

Produces a structured JSON file consumed by the downstream scripts.

## Script: `check-current-state`

**Input:** `data/jobs.json`, rhdh-docs local clone
**Output:** `data/current-state-report.json`

**Purpose:** detect when source content references in the sheet no longer match the rhdh-docs `main` branch (headings renamed, files moved, sections removed).

**Steps:**

1. Use a local clone of `red-hat-developers-documentation-rhdh` (clone path configurable, e.g. via `RHDH_DOCS_PATH` env var or `--docs-path` flag).
2. For each job, extract source content references from `jobs.json`.
3. Search the clone for those references: first exact heading match, then fuzzy match against all headings in `.adoc` files.
4. For each reference, output one of:
   - ✅ **found** — exact match, file path recorded
   - ⚠️ **ambiguous** — fuzzy match found (confidence score + suggested heading), CS must confirm
   - ❌ **not found** — no reasonable match, CS must update the sheet

The report is consumed by `generate-plans` to annotate per-title briefs.

## Script: `generate-plans`

**Input:** `data/jobs.json`, `data/current-state-report.json`
**Output:** `docs/plan.md`, `docs/jobs/job-NN.md` (one per job)

### General plan — `docs/plan.md`

Priority-sorted table of all jobs with: job number, title, category, priority, current-state flag, status, and link to per-title brief. Also shows a summary of how many jobs have stale references needing CS review.

Serves as the CS's progress tracker throughout the effort.

### Per-title brief — `docs/jobs/job-NN.md`

Fixed structure:

```markdown
# Job NN — <Job title>

## Metadata

| Field | Value |
|---|---|
| Category | … |
| Priority | … |
| Jira | (blank until create-jiras runs) |
| Sheet row | Job #NN |
| Status | Not started |

## Job statement

<Job Statement from sheet>

## Current state

<✅/⚠️/❌ status from check-current-state>
- Sheet reference: "…"
- Match: <file path, heading, confidence if fuzzy>
- Published URL: <link to published doc>
- CS action: <confirm / update sheet>

## Target structure

| Source section | Proposed JTBD heading |
|---|---|
| … | … |

## Rewrite instructions

Each heading must express an action + outcome (why the reader does this step).
Replace noun-phrase titles with outcome-oriented equivalents.
Keep all technical steps intact — only headings change.

Apply to: <adoc file path(s)>

## Acceptance criteria

- [ ] All headings follow action + outcome pattern
- [ ] No heading is a noun phrase only
- [ ] Source sections from the table above are all addressed
- [ ] PR linked to this Jira task
```

## Script: `create-jiras`

**Input:** `docs/jobs/job-NN.md` files, `docs/plan.md` (for epic key)
**Output:** Jira tasks created/updated via `jirha`; Jira key written back into each `job-NN.md` metadata block

**Behavior:**

- **Create:** if `Jira:` field in metadata is blank → call `jirha create`, write key back into the file
- **Update:** if `Jira:` field is populated → call `jirha update` to sync summary, priority, description
- **Parent:** reads epic key from `docs/plan.md` header; also accepts `--parent` flag override
- **Idempotent:** safe to run repeatedly; will not create duplicates

Jira task content:
- **Summary:** job title
- **Description:** job statement + target structure table + rewrite instructions + acceptance criteria (Jira wiki markup)
- **Priority:** from metadata
- **Labels:** `jtbd`, `job-NN`, category label
- **Component:** Documentation

## Directory structure

```
data/
  *.xlsx                        # XLSX exports (not committed if large)
  jobs.json                     # extracted structured data
  current-state-report.json     # stale-ref flags

docs/
  plan.md                       # general plan (priority overview + progress)
  jobs/
    job-01.md
    job-02.md
    …
    job-27.md

scripts/
  import-jobs                   # existing (kept for reference / one-shot use)
  extract                       # new: XLSX → jobs.json
  check-current-state           # new: jobs.json + rhdh-docs → report
  generate-plans                # new: jobs.json + report → Markdown
  create-jiras                  # new: Markdown → Jira tasks
```

## Phase 2: CS abandons the sheet

When the CS decides to work directly in this repository:

1. `docs/jobs/job-NN.md` files become the authoring environment (edit directly, propose changes via PR)
2. Stakeholder validation moves to GitHub PR comments (line-level commenting is better for heading review than Jira task comments)
3. `extract` and `check-current-state` are no longer needed as inputs to `generate-plans`
4. `create-jiras` is unchanged — it still reads from Markdown

The only change required: CS and stakeholders need GitHub access (they likely already have it for rhdh-docs).

## Configuration

| Variable | Default | Description |
|---|---|---|
| `RHDH_DOCS_PATH` | `../red-hat-developers-documentation-rhdh` | Local clone of rhdh-docs |
| `JTBD_EPIC` | (required) | Jira epic key, e.g. `RHIDP-XXXX` |

## Repository

GitHub: https://github.com/themr0c/jtbd

`create-jiras` includes a link to the per-title brief in each Jira task description:
`https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-NN.md`

This also enables the phase 2 stakeholder review flow: CS opens a PR against `main`, stakeholders comment on specific lines in the brief, link is shared in the Jira task.
