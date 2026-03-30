# CLAUDE.md — JTBD: Jobs To Be Done

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Import and manage JTBD jobs from the scoring spreadsheet into Jira.

## Setup

```bash
pip install -r requirements.txt   # installs openpyxl
# jirha must be on PATH (see ~/src/gh/themr0c/jirha)
```

## Pipeline

Run in sequence. Each step's output feeds the next.

```bash
# Step 1: Extract sheet data (requires XLSX export in data/)
scripts/extract "data/[WIP] RHDH TOC mapping - JTBD Effort.xlsx"
# → data/jobs.json

# Step 2: Check current state against rhdh-docs (requires local clone)
export RHDH_DOCS_PATH=../red-hat-developers-documentation-rhdh
scripts/check-current-state
# → data/current-state-report.json

# Step 3: Generate Markdown plans
scripts/generate-plans --epic RHIDP-XXXX
# → docs/plan.md + docs/jobs/job-NN.md (one per job)

# Step 4: Create/update Jira tasks (children of JTBD epic)
scripts/create-jiras                 # dry run (default)
scripts/create-jiras --exec          # create/update issues
```

`scripts/import-jobs` is superseded by this pipeline but kept for reference.

## Tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```
