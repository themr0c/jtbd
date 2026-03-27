# JTBD — Jobs To Be Done

Import and manage JTBD jobs from the scoring spreadsheet into Jira.

## import-jobs

Parses the JTBD XLSX export and creates Jira tasks via `jirha`.

```bash
scripts/import-jobs "data/[WIP] RHDH TOC mapping - JTBD Effort.xlsx"                             # preview
scripts/import-jobs "data/[WIP] RHDH TOC mapping - JTBD Effort.xlsx" --parent RHIDP-XXXX --exec   # create issues
```

Requires `openpyxl` (`pip install -r requirements.txt`) and `jirha` on PATH.
