# JTBD Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build four scripts (`extract`, `check-current-state`, `generate-plans`, `create-jiras`) that transform a Google Sheet XLSX export into Jira tasks via Markdown briefs, with automatic detection of stale content references in rhdh-docs.

**Architecture:** Linear pipeline — XLSX → `data/jobs.json` → (check rhdh-docs) → `data/current-state-report.json` → `docs/jobs/job-NN.md` → Jira tasks. Shared parsing logic lives in `scripts/lib/`. The Markdown briefs are the canonical source for Jira whether generated from the sheet (phase 1) or edited directly by the CS (phase 2).

**Tech Stack:** Python 3, openpyxl (existing), difflib (stdlib), jirha CLI (existing), pytest

---

## File Map

**New files:**
- `scripts/lib/__init__.py` — empty package marker
- `scripts/lib/parse_xlsx.py` — XLSX parsing extracted from `scripts/import-jobs`
- `scripts/lib/current_state.py` — fuzzy heading matching against rhdh-docs `.adoc` files
- `scripts/lib/plan_renderer.py` — Markdown template rendering for plan and briefs
- `scripts/lib/parse_markdown.py` — parse job-NN.md briefs; write Jira key back to metadata
- `scripts/extract` — XLSX → `data/jobs.json`
- `scripts/check-current-state` — `data/jobs.json` + rhdh-docs clone → `data/current-state-report.json`
- `scripts/generate-plans` — JSON → `docs/plan.md` + `docs/jobs/job-NN.md`
- `scripts/create-jiras` — `docs/jobs/*.md` → Jira tasks via jirha
- `tests/conftest.py` — empty (pytest discovery)
- `tests/fixtures/sample.adoc` — fixture AsciiDoc with known headings
- `tests/fixtures/sample_brief.md` — fixture job brief with known content
- `tests/test_parse_xlsx.py`
- `tests/test_current_state.py`
- `tests/test_plan_renderer.py`
- `tests/test_parse_markdown.py`
- `tests/test_create_jiras_helpers.py`

**Modified files:**
- `requirements.txt` — add `pytest>=8.0`
- `.claude/CLAUDE.md` — document the pipeline

---

### Task 1: Shared XLSX parsing library + `extract` script

**Files:**
- Create: `scripts/lib/__init__.py`
- Create: `scripts/lib/parse_xlsx.py`
- Create: `tests/conftest.py`
- Create: `tests/test_parse_xlsx.py`
- Create: `scripts/extract`
- Modify: `requirements.txt`

- [ ] **Step 1.1: Write failing tests**

Create `tests/conftest.py` (empty):
```python
```

Create `tests/test_parse_xlsx.py`:
```python
import sys
from pathlib import Path
import openpyxl
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from lib.parse_xlsx import _cell, parse_jobs, parse_proposal


def _wb(jobs_rows, proposal_rows=None):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Phase 3 Jobs'
    for row in jobs_rows:
        ws.append(row)
    if proposal_rows is not None:
        ws2 = wb.create_sheet('Phase 3 JTBD - All-in Proposal')
        for row in proposal_rows:
            ws2.append(row)
    return wb


def test_cell_none():
    assert _cell(None) == ''


def test_cell_float():
    assert _cell(3.0) == '3'


def test_cell_string_stripped():
    assert _cell('  hello  ') == 'hello'


def test_parse_jobs_basic():
    header = ['Job #', 'Job', 'Job Statement', 'Job Category ', 'Job Priority (calculated)']
    row1 = [1, 'Install RHDH', 'When I install...', 'Install', 'high']
    jobs = parse_jobs(_wb([header, row1]))
    assert len(jobs) == 1
    assert jobs[0]['num'] == '1'
    assert jobs[0]['name'] == 'Install RHDH'
    assert jobs[0]['priority'] == 'Major'
    assert jobs[0]['category_label'] == 'install'


def test_parse_jobs_skips_empty_num():
    header = ['Job #', 'Job', 'Job Statement', 'Job Category ', 'Job Priority (calculated)']
    jobs = parse_jobs(_wb([header, [None, 'No number', '', '', '']]))
    assert jobs == []


def test_parse_proposal_returns_empty_when_sheet_missing():
    wb = openpyxl.Workbook()
    wb.active.title = 'Phase 3 Jobs'
    assert parse_proposal(wb) == {}
```

- [ ] **Step 1.2: Run — expect failure**

```bash
cd /home/ffloreth/src/gh/themr0c/jtbd
python -m pytest tests/test_parse_xlsx.py -v 2>&1 | head -15
```

Expected: `ModuleNotFoundError: No module named 'lib'`

- [ ] **Step 1.3: Create `scripts/lib/__init__.py`**

```bash
mkdir -p scripts/lib
touch scripts/lib/__init__.py
```

- [ ] **Step 1.4: Create `scripts/lib/parse_xlsx.py`**

```python
"""Parse JTBD XLSX export. Logic extracted from scripts/import-jobs."""

JOBS_SHEET = 'Phase 3 Jobs'
PROPOSAL_SHEET = 'Phase 3 JTBD - All-in Proposal'

PRIORITY_MAP = {
    'high': 'Major',
    'medium': 'Normal',
    'low': 'Minor',
    '': 'Normal',
}


def _cell(v):
    if v is None:
        return ''
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v).strip()


def _row_cells(row, n=5):
    return tuple(_cell(row[i]) if i < len(row) else '' for i in range(n))


def _clean_heading(heading):
    return heading.split('\n')[0].strip() if heading else ''


def _entry(source, heading, sp=''):
    return {'source': source, 'heading': _clean_heading(heading), 'sp': sp}


def _flush(proposals, job, entries):
    if job and entries:
        proposals[job] = entries


def _parse_simple_row(row):
    source = _cell(row[2]) if len(row) > 2 else ''
    heading = _cell(row[3]) if len(row) > 3 else ''
    sp = _cell(row[4]) if len(row) > 4 else ''
    if source or heading:
        return _entry(source, heading, sp)
    return None


def _parse_detailed_row(a, b, row):
    if a and b:
        if b.startswith(('Chapter', '(')):
            return _entry(b, _cell(row[2]) if len(row) > 2 else '',
                          _cell(row[3]) if len(row) > 3 else '')
        return _entry(a, b, _cell(row[2]) if len(row) > 2 else '')
    if not a and b:
        return _entry(b, _cell(row[2]) if len(row) > 2 else '',
                      _cell(row[3]) if len(row) > 3 else '')
    return None


def parse_proposal(wb):
    """Parse All-in Proposal tab. Returns {job_name: [{source, heading, sp}]}."""
    if PROPOSAL_SHEET not in wb.sheetnames:
        return {}
    ws = wb[PROPOSAL_SHEET]
    rows = list(ws.iter_rows(values_only=True))
    proposals, current_job, current_entries, mode = {}, None, [], None

    for row in rows:
        a, b, *_ = _row_cells(row)
        if a.startswith('Category:'):
            _flush(proposals, current_job, current_entries)
            current_job, current_entries, mode = None, [], None
            continue
        if a == 'Parent Topic (Job)' and b == 'Job Statement':
            mode = 'simple'
            continue
        if a.startswith('Job') and ':' in a and not a.startswith('Job Statement'):
            _flush(proposals, current_job, current_entries)
            current_job = a.split(':', 1)[1].strip()
            current_entries, mode = [], 'detailed'
            continue
        if a.startswith('Job Statement:'):
            continue
        if mode == 'detailed' and a in ('Original Source Content', 'Parent Topic', 'Mapped Content (Source)'):
            continue
        if mode == 'simple':
            if a:
                _flush(proposals, current_job, current_entries)
                current_job, current_entries = a, []
            entry = _parse_simple_row(row)
            if entry:
                current_entries.append(entry)
        elif mode == 'detailed':
            entry = _parse_detailed_row(a, b, row)
            if entry:
                current_entries.append(entry)

    _flush(proposals, current_job, current_entries)
    return proposals


def parse_jobs(wb):
    """Parse 'Phase 3 Jobs' tab. Returns list of job dicts."""
    import sys
    if JOBS_SHEET not in wb.sheetnames:
        print(f'ERROR: tab "{JOBS_SHEET}" not found.', file=sys.stderr)
        sys.exit(1)
    ws = wb[JOBS_SHEET]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [str(h).strip() if h else '' for h in rows[0]]
    jobs = []
    for row in rows[1:]:
        cells = dict(zip(headers, row))
        job_num = cells.get('Job #')
        job = cells.get('Job', '')
        if not job_num or not job:
            continue
        job_num = _cell(job_num)
        job = str(job).strip()
        category = str(cells.get('Job Category ', '') or cells.get('Job Category', '') or '').strip()
        priority_raw = str(cells.get('Job Priority (calculated)', '') or '').strip().lower()
        jobs.append({
            'num': job_num,
            'name': job,
            'summary': f'JTBD - {job}',
            'statement': str(cells.get('Job Statement', '') or '').strip(),
            'category': category,
            'category_label': category.lower().replace(' ', '-'),
            'priority': PRIORITY_MAP.get(priority_raw, 'Normal'),
        })
    return jobs
```

- [ ] **Step 1.5: Run — expect all pass**

```bash
python -m pytest tests/test_parse_xlsx.py -v
```

Expected:
```
tests/test_parse_xlsx.py::test_cell_none PASSED
tests/test_parse_xlsx.py::test_cell_float PASSED
tests/test_parse_xlsx.py::test_cell_string_stripped PASSED
tests/test_parse_xlsx.py::test_parse_jobs_basic PASSED
tests/test_parse_xlsx.py::test_parse_jobs_skips_empty_num PASSED
tests/test_parse_xlsx.py::test_parse_proposal_returns_empty_when_sheet_missing PASSED
6 passed
```

- [ ] **Step 1.6: Create `scripts/extract`**

```python
#!/usr/bin/env python3
"""Extract JTBD jobs from XLSX to data/jobs.json."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import openpyxl
from lib.parse_xlsx import parse_jobs, parse_proposal


def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <xlsx-file> [output.json]', file=sys.stderr)
        sys.exit(1)
    xlsx_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'data/jobs.json'

    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    proposals = parse_proposal(wb)
    jobs = parse_jobs(wb)
    wb.close()

    for job in jobs:
        job['entries'] = proposals.get(job['name'], [])

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump({'jobs': jobs}, f, indent=2, ensure_ascii=False)

    print(f'Extracted {len(jobs)} jobs → {output_path}')


if __name__ == '__main__':
    main()
```

```bash
chmod +x scripts/extract
```

- [ ] **Step 1.7: Smoke-test with real XLSX**

```bash
python scripts/extract "data/[WIP] RHDH TOC mapping - JTBD Effort.xlsx"
```

Expected: `Extracted 27 jobs → data/jobs.json`

```bash
python -c "import json; d=json.load(open('data/jobs.json')); print(len(d['jobs']), 'jobs')"
```

Expected: `27 jobs`

- [ ] **Step 1.8: Add pytest to requirements.txt**

Replace contents of `requirements.txt`:
```
openpyxl>=3.1
pytest>=8.0
```

- [ ] **Step 1.9: Commit**

```bash
git add scripts/lib/ scripts/extract requirements.txt \
        tests/conftest.py tests/test_parse_xlsx.py data/jobs.json
git commit -m "feat: add extract script and shared XLSX parsing library"
```

---

### Task 2: `check-current-state` — fuzzy heading matching

**Files:**
- Create: `scripts/lib/current_state.py`
- Create: `tests/fixtures/sample.adoc`
- Create: `tests/test_current_state.py`
- Create: `scripts/check-current-state`

- [ ] **Step 2.1: Create fixture AsciiDoc**

Create `tests/fixtures/sample.adoc`:
```adoc
= Installing Red Hat Developer Hub on OpenShift Container Platform

== Before you begin

Prerequisites text.

== Installing the Operator

Procedure text.

=== Verifying the installation

Check it works.
```

- [ ] **Step 2.2: Write failing tests**

Create `tests/test_current_state.py`:
```python
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from lib.current_state import load_headings, fuzzy_match, check_reference

FIXTURES = Path(__file__).parent / 'fixtures'


def test_load_headings_finds_all():
    headings = load_headings(FIXTURES)
    texts = [h for h, _ in headings]
    assert 'Installing Red Hat Developer Hub on OpenShift Container Platform' in texts
    assert 'Before you begin' in texts
    assert 'Installing the Operator' in texts
    assert 'Verifying the installation' in texts


def test_load_headings_records_file():
    headings = load_headings(FIXTURES)
    assert any('sample.adoc' in f for _, f in headings)


def test_fuzzy_match_exact():
    headings = [('Installing the Operator', 'assembly.adoc')]
    results = fuzzy_match('Installing the Operator', headings)
    assert results[0][0] == 1.0


def test_fuzzy_match_partial():
    headings = [('Installing the Operator', 'assembly.adoc'), ('Unrelated topic', 'other.adoc')]
    results = fuzzy_match('Install the Operator', headings)
    assert results[0][1] == 'Installing the Operator'
    assert results[0][0] >= 0.6


def test_fuzzy_match_below_threshold_excluded():
    headings = [('Completely unrelated heading', 'assembly.adoc')]
    results = fuzzy_match('Installing RHDH on OpenShift', headings, threshold=0.6)
    assert results == []


def test_check_reference_found():
    headings = [('Installing the Operator', 'assembly.adoc')]
    result = check_reference('Installing the Operator', headings)
    assert result['status'] == 'found'
    assert result['confidence'] == 1.0


def test_check_reference_ambiguous():
    headings = [('Installing the Operator on OpenShift', 'assembly.adoc')]
    result = check_reference('Installing the Operator', headings)
    assert result['status'] == 'ambiguous'
    assert 0.6 <= result['confidence'] < 1.0


def test_check_reference_not_found():
    headings = [('Completely unrelated content here', 'assembly.adoc')]
    result = check_reference('Installing RHDH', headings)
    assert result['status'] == 'not_found'
    assert result['match'] is None
```

- [ ] **Step 2.3: Run — expect failure**

```bash
python -m pytest tests/test_current_state.py -v 2>&1 | head -10
```

Expected: `ModuleNotFoundError: No module named 'lib.current_state'`

- [ ] **Step 2.4: Create `scripts/lib/current_state.py`**

```python
"""Check rhdh-docs headings against sheet source references."""
import re
from difflib import SequenceMatcher
from pathlib import Path


def load_headings(docs_path):
    """Return list of (heading_text, relative_file_path) from all .adoc files."""
    docs = Path(docs_path)
    results = []
    for adoc in sorted(docs.rglob('*.adoc')):
        rel = str(adoc.relative_to(docs))
        for line in adoc.read_text(errors='ignore').splitlines():
            m = re.match(r'^={1,6}\s+(.+)$', line)
            if m:
                results.append((m.group(1).strip(), rel))
    return results


def fuzzy_match(reference, headings, threshold=0.6):
    """Return sorted list of (score, heading, file) with score >= threshold."""
    ref_lower = reference.lower()
    scored = []
    for heading, file in headings:
        score = SequenceMatcher(None, ref_lower, heading.lower()).ratio()
        if score >= threshold:
            scored.append((score, heading, file))
    return sorted(scored, reverse=True)


def check_reference(reference, headings):
    """Return status dict: found / ambiguous / not_found."""
    for heading, file in headings:
        if reference.lower() == heading.lower():
            return {'status': 'found', 'match': heading, 'confidence': 1.0, 'file': file}
    matches = fuzzy_match(reference, headings)
    if not matches:
        return {'status': 'not_found', 'match': None, 'confidence': 0.0, 'file': None}
    best_score, best_heading, best_file = matches[0]
    return {
        'status': 'ambiguous',
        'match': best_heading,
        'confidence': round(best_score, 2),
        'file': best_file,
    }
```

- [ ] **Step 2.5: Run — expect all pass**

```bash
python -m pytest tests/test_current_state.py -v
```

Expected: 8 passed.

- [ ] **Step 2.6: Create `scripts/check-current-state`**

```python
#!/usr/bin/env python3
"""Check sheet source references against rhdh-docs main branch headings."""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.current_state import load_headings, check_reference

DEFAULT_DOCS_PATH = os.environ.get(
    'RHDH_DOCS_PATH',
    str(Path(__file__).parent.parent.parent / 'red-hat-developers-documentation-rhdh'),
)


def _git_commit(docs_path):
    try:
        r = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                           cwd=docs_path, capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return 'unknown'


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('jobs_json', nargs='?', default='data/jobs.json')
    parser.add_argument('--output', default='data/current-state-report.json')
    parser.add_argument('--docs-path', default=DEFAULT_DOCS_PATH)
    args = parser.parse_args()

    docs_path = Path(args.docs_path)
    if not docs_path.exists():
        print(f'ERROR: rhdh-docs not found at {docs_path}', file=sys.stderr)
        print('Set RHDH_DOCS_PATH env var or use --docs-path', file=sys.stderr)
        sys.exit(1)

    with open(args.jobs_json) as f:
        jobs = json.load(f)['jobs']

    print(f'Loading headings from {docs_path} …')
    headings = load_headings(docs_path)
    print(f'  {len(headings)} headings indexed')

    report = {
        'generated': date.today().isoformat(),
        'docs_path': str(docs_path),
        'docs_commit': _git_commit(docs_path),
        'jobs': {},
    }

    flagged = 0
    for job in jobs:
        entries_report = []
        for entry in job.get('entries', []):
            source = entry.get('source', '')
            if not source:
                continue
            result = check_reference(source, headings)
            result['source'] = source
            entries_report.append(result)
        is_flagged = any(e['status'] != 'found' for e in entries_report)
        if is_flagged:
            flagged += 1
        report['jobs'][job['num']] = {'flagged': is_flagged, 'entries': entries_report}

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f'{flagged}/{len(jobs)} jobs flagged → {args.output}')


if __name__ == '__main__':
    main()
```

```bash
chmod +x scripts/check-current-state
```

- [ ] **Step 2.7: Commit**

```bash
git add scripts/lib/current_state.py scripts/check-current-state \
        tests/fixtures/sample.adoc tests/test_current_state.py
git commit -m "feat: add check-current-state with fuzzy heading matching"
```

---

### Task 3: `generate-plans` — Markdown templates

**Files:**
- Create: `scripts/lib/plan_renderer.py`
- Create: `tests/test_plan_renderer.py`
- Create: `scripts/generate-plans`

- [ ] **Step 3.1: Write failing tests**

Create `tests/test_plan_renderer.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from lib.plan_renderer import render_general_plan, render_job_brief

JOB = {
    'num': '3',
    'name': 'Install RHDH on OpenShift',
    'summary': 'JTBD - Install RHDH on OpenShift',
    'statement': 'When I install RHDH, I want clear steps.',
    'category': 'Install',
    'category_label': 'install',
    'priority': 'Major',
    'entries': [
        {'source': 'Chapter 3 - Installing', 'heading': 'Installing RHDH so your team can use it', 'sp': ''},
    ],
}

REPORT_FOUND = {
    'jobs': {'3': {'flagged': False, 'entries': [
        {'source': 'Chapter 3 - Installing', 'status': 'found',
         'match': 'Installing the Operator', 'confidence': 1.0, 'file': 'assemblies/install.adoc'},
    ]}}
}

REPORT_AMBIGUOUS = {
    'jobs': {'3': {'flagged': True, 'entries': [
        {'source': 'Chapter 3 - Installing', 'status': 'ambiguous',
         'match': 'Installing RHDH on OCP', 'confidence': 0.78, 'file': 'assemblies/install.adoc'},
    ]}}
}


def test_general_plan_table_header():
    result = render_general_plan([JOB], REPORT_FOUND, 'RHIDP-1234')
    assert '| # | Job |' in result
    assert 'RHIDP-1234' in result


def test_general_plan_links_brief():
    result = render_general_plan([JOB], REPORT_FOUND, 'RHIDP-1234')
    assert 'job-03.md' in result


def test_general_plan_flag_when_ambiguous():
    result = render_general_plan([JOB], REPORT_AMBIGUOUS, 'RHIDP-1234')
    assert '⚠️' in result
    assert 'Jobs affected:' in result


def test_brief_has_all_sections():
    result = render_job_brief(JOB, REPORT_FOUND['jobs']['3'], 'RHIDP-1234')
    for section in ['## Metadata', '## Job statement', '## Current state',
                    '## Target structure', '## Rewrite instructions', '## Acceptance criteria']:
        assert section in result, f'Missing: {section}'


def test_brief_warning_for_ambiguous():
    result = render_job_brief(JOB, REPORT_AMBIGUOUS['jobs']['3'], 'RHIDP-1234')
    assert '⚠️' in result
    assert '78%' in result


def test_brief_checkmark_for_found():
    result = render_job_brief(JOB, REPORT_FOUND['jobs']['3'], 'RHIDP-1234')
    assert '✅' in result


def test_brief_blank_jira_key():
    result = render_job_brief(JOB, REPORT_FOUND['jobs']['3'], 'RHIDP-1234')
    assert '| Jira |  |' in result
```

- [ ] **Step 3.2: Run — expect failure**

```bash
python -m pytest tests/test_plan_renderer.py -v 2>&1 | head -10
```

Expected: `ModuleNotFoundError: No module named 'lib.plan_renderer'`

- [ ] **Step 3.3: Create `scripts/lib/plan_renderer.py`**

```python
"""Render Markdown plan and job brief files."""
from datetime import date

GITHUB_BASE = 'https://github.com/themr0c/jtbd/blob/main'

PRIORITY_EMOJI = {'Major': '🔴', 'Normal': '🟡', 'Minor': '🟢'}


def render_general_plan(jobs, report, epic_key):
    """Render content for docs/plan.md."""
    today = date.today().isoformat()
    flagged_nums = [
        j['num'] for j in jobs
        if report.get('jobs', {}).get(j['num'], {}).get('flagged')
    ]
    lines = [
        '# JTBD Transformation Plan — RHDH Documentation', '',
        '## Status', '',
        f'Last updated: {today}',
        f'Epic: {epic_key}', '',
        '## Jobs by Priority', '',
        '| # | Job | Category | Priority | Status | Brief |',
        '| --- | --- | --- | --- | --- | --- |',
    ]
    for job in jobs:
        emoji = PRIORITY_EMOJI.get(job['priority'], '🟡')
        flag = ' ⚠️' if job['num'] in flagged_nums else ''
        num = job['num'].zfill(2)
        link = f'[job-{num}.md](jobs/job-{num}.md)'
        lines.append(
            f'| {job["num"]} | {job["name"]} | {job["category"]} '
            f'| {emoji} {job["priority"]} | Not started{flag} | {link} |'
        )
    if flagged_nums:
        lines += [
            '', '## Current-state flags', '',
            f'⚠️  {len(flagged_nums)} job(s) have source references that may be outdated.',
            f'Jobs affected: {", ".join(flagged_nums)}',
        ]
    lines += [
        '', '## Categories', '',
        'Discover · Plan · Install · Get Started · Configure · Secure · '
        'Extend · Develop · Administer · Observe · Upgrade · Reference',
    ]
    return '\n'.join(lines) + '\n'


def render_job_brief(job, job_report, epic_key):
    """Render content for docs/jobs/job-NN.md."""
    num = job['num'].zfill(2)

    cs_lines = []
    for entry in (job_report or {}).get('entries', []):
        source = entry.get('source', '')
        status = entry.get('status', 'not_found')
        match = entry.get('match')
        confidence = entry.get('confidence', 0)
        file = entry.get('file')
        if status == 'found':
            cs_lines += [f'- ✅ **{source}**', f'  - Found: `{file}`']
        elif status == 'ambiguous':
            cs_lines += [
                f'- ⚠️ **{source}**',
                f'  - Best match ({confidence:.0%}): "{match}" in `{file}`',
                f'  - CS action: confirm this is the right source before rewrite',
            ]
        else:
            cs_lines += [
                f'- ❌ **{source}**',
                f'  - No match found — CS action: update sheet reference',
            ]
    if not cs_lines:
        cs_lines = ['No source references recorded.']

    entries = job.get('entries', [])
    table = ['| Source section | Proposed JTBD heading |', '| --- | --- |']
    for e in entries:
        table.append(f'| {e["source"] or "—"} | {e["heading"] or "—"} |')

    adoc_files = sorted({
        e.get('file', '') for e in (job_report or {}).get('entries', []) if e.get('file')
    })
    apply_to = ', '.join(f'`{f}`' for f in adoc_files) if adoc_files else '_Confirm source file with CS_'
    github_link = f'{GITHUB_BASE}/docs/jobs/job-{num}.md'

    lines = [
        f'# Job {num} — {job["name"]}', '',
        '## Metadata', '',
        '| Field | Value |', '| --- | --- |',
        f'| Category | {job["category"]} |',
        f'| Priority | {PRIORITY_EMOJI.get(job["priority"], "🟡")} {job["priority"]} |',
        '| Jira |  |',
        f'| Sheet row | Job #{job["num"]} |',
        '| Status | Not started |', '',
        '## Job statement', '',
        job['statement'] or '_No statement recorded._', '',
        '## Current state', '',
    ] + cs_lines + ['', '## Target structure', ''] + table + [
        '', '## Rewrite instructions', '',
        'Each heading must express an action + outcome (why the reader does this step).',
        'Replace noun-phrase titles with outcome-oriented equivalents.',
        'Keep all technical steps intact — only headings change.',
        '', f'Apply to: {apply_to}', '',
        '## Acceptance criteria', '',
        '- [ ] All headings follow action + outcome pattern',
        '- [ ] No heading is a noun phrase only ("Installation", "Prerequisites")',
        '- [ ] Source sections from the table above are all addressed',
        '- [ ] PR linked to this Jira task',
        f'- [ ] Brief: {github_link}',
    ]
    return '\n'.join(lines) + '\n'
```

- [ ] **Step 3.4: Run — expect all pass**

```bash
python -m pytest tests/test_plan_renderer.py -v
```

Expected: 7 passed.

- [ ] **Step 3.5: Create `scripts/generate-plans`**

```python
#!/usr/bin/env python3
"""Generate docs/plan.md and docs/jobs/job-NN.md from jobs.json."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.plan_renderer import render_general_plan, render_job_brief


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('jobs_json', nargs='?', default='data/jobs.json')
    parser.add_argument('--report', default='data/current-state-report.json')
    parser.add_argument('--epic', required=True, help='Jira epic key e.g. RHIDP-1234')
    parser.add_argument('--output-dir', default='docs')
    args = parser.parse_args()

    with open(args.jobs_json) as f:
        jobs = json.load(f)['jobs']

    report = {'jobs': {}}
    report_path = Path(args.report)
    if report_path.exists():
        with open(report_path) as f:
            report = json.load(f)
    else:
        print(f'Warning: {args.report} not found — no current-state annotations', file=sys.stderr)

    out = Path(args.output_dir)
    (out / 'jobs').mkdir(parents=True, exist_ok=True)

    (out / 'plan.md').write_text(render_general_plan(jobs, report, args.epic))
    print(f'Written: {out}/plan.md')

    for job in jobs:
        num = job['num'].zfill(2)
        job_report = report.get('jobs', {}).get(job['num'], {})
        (out / 'jobs' / f'job-{num}.md').write_text(render_job_brief(job, job_report, args.epic))

    print(f'Written: {len(jobs)} briefs → {out}/jobs/')


if __name__ == '__main__':
    main()
```

```bash
chmod +x scripts/generate-plans
```

- [ ] **Step 3.6: Smoke-test**

```bash
python scripts/generate-plans data/jobs.json --epic RHIDP-PLACEHOLDER
```

Expected:
```
Written: docs/plan.md
Written: 27 briefs → docs/jobs/
```

```bash
head -20 docs/plan.md
head -40 docs/jobs/job-01.md
```

Verify: table present in plan, all sections present in brief.

- [ ] **Step 3.7: Commit**

```bash
git add scripts/lib/plan_renderer.py scripts/generate-plans \
        tests/test_plan_renderer.py docs/plan.md docs/jobs/
git commit -m "feat: add generate-plans with Markdown brief templates"
```

---

### Task 4: `create-jiras` — Markdown → Jira tasks

**Files:**
- Create: `scripts/lib/parse_markdown.py`
- Create: `tests/fixtures/sample_brief.md`
- Create: `tests/test_parse_markdown.py`
- Create: `tests/test_create_jiras_helpers.py`
- Create: `scripts/create-jiras`

- [ ] **Step 4.1: Create fixture brief**

Create `tests/fixtures/sample_brief.md`:
```markdown
# Job 03 — Install RHDH on OpenShift

## Metadata

| Field | Value |
| --- | --- |
| Category | Install |
| Priority | 🔴 Major |
| Jira | RHIDP-9999 |
| Sheet row | Job #3 |
| Status | Not started |

## Job statement

When I install RHDH, I want clear steps so I can complete it without help.

## Current state

- ✅ **Installing the Operator**
  - Found: `assemblies/assembly-install-rhdh-ocp.adoc`

## Target structure

| Source section | Proposed JTBD heading |
| --- | --- |
| Installing the Operator | Installing RHDH so your team can use it |

## Rewrite instructions

Each heading must express an action + outcome.

Apply to: `assemblies/assembly-install-rhdh-ocp.adoc`

## Acceptance criteria

- [ ] All headings follow action + outcome pattern
- [ ] No heading is a noun phrase only
- [ ] Source sections from the table above are all addressed
- [ ] PR linked to this Jira task
- [ ] Brief: https://github.com/themr0c/jtbd/blob/main/docs/jobs/job-03.md
```

- [ ] **Step 4.2: Write failing tests for `parse_markdown`**

Create `tests/test_parse_markdown.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from lib.parse_markdown import parse_brief, write_jira_key

FIXTURES = Path(__file__).parent / 'fixtures'
SAMPLE = FIXTURES / 'sample_brief.md'


def test_title():
    assert parse_brief(SAMPLE)['title'] == 'Job 03 — Install RHDH on OpenShift'


def test_jira_key():
    assert parse_brief(SAMPLE)['jira_key'] == 'RHIDP-9999'


def test_priority():
    p = parse_brief(SAMPLE)['priority']
    assert '🔴' in p and 'Major' in p


def test_job_statement():
    assert 'clear steps' in parse_brief(SAMPLE)['job_statement']


def test_blank_jira_key(tmp_path):
    content = SAMPLE.read_text().replace('| Jira | RHIDP-9999 |', '| Jira |  |')
    f = tmp_path / 'blank.md'
    f.write_text(content)
    assert parse_brief(f)['jira_key'] == ''


def test_write_jira_key(tmp_path):
    content = SAMPLE.read_text().replace('| Jira | RHIDP-9999 |', '| Jira |  |')
    f = tmp_path / 'test.md'
    f.write_text(content)
    write_jira_key(f, 'RHIDP-4242')
    assert parse_brief(f)['jira_key'] == 'RHIDP-4242'
```

- [ ] **Step 4.3: Run — expect failure**

```bash
python -m pytest tests/test_parse_markdown.py -v 2>&1 | head -10
```

Expected: `ModuleNotFoundError: No module named 'lib.parse_markdown'`

- [ ] **Step 4.4: Create `scripts/lib/parse_markdown.py`**

```python
"""Parse job-NN.md brief files; write Jira key back to metadata."""
import re
from pathlib import Path


def parse_brief(path):
    """Return dict of sections from a job-NN.md file."""
    text = Path(path).read_text()

    title_m = re.match(r'^# (.+)', text)
    title = title_m.group(1).strip() if title_m else ''

    metadata = {}
    meta_m = re.search(r'## Metadata\n\n\|.*?\|\n\|.*?\|\n((?:\|.*?\|\n?)+)', text)
    if meta_m:
        for row in meta_m.group(1).strip().splitlines():
            parts = [p.strip() for p in row.split('|') if p.strip()]
            if len(parts) == 2:
                metadata[parts[0]] = parts[1]

    def section(name):
        m = re.search(
            rf'^## {re.escape(name)}\n\n(.*?)(?=\n^## |\Z)',
            text, re.MULTILINE | re.DOTALL,
        )
        return m.group(1).strip() if m else ''

    return {
        'title': title,
        'jira_key': metadata.get('Jira', '').strip(),
        'category': metadata.get('Category', '').strip(),
        'priority': metadata.get('Priority', '').strip(),
        'sheet_row': metadata.get('Sheet row', '').strip(),
        'status': metadata.get('Status', '').strip(),
        'job_statement': section('Job statement'),
        'current_state': section('Current state'),
        'target_structure': section('Target structure'),
        'rewrite_instructions': section('Rewrite instructions'),
        'acceptance_criteria': section('Acceptance criteria'),
        'path': str(path),
        'raw': text,
    }


def write_jira_key(path, key):
    """Write a Jira issue key into the Metadata table."""
    text = Path(path).read_text()
    updated = re.sub(r'(\| Jira \|)(.*?)(\|)', rf'\1 {key} \3', text, count=1)
    Path(path).write_text(updated)
```

- [ ] **Step 4.5: Run — expect all pass**

```bash
python -m pytest tests/test_parse_markdown.py -v
```

Expected: 6 passed.

- [ ] **Step 4.6: Write failing tests for `create-jiras` helpers**

Create `tests/test_create_jiras_helpers.py`:
```python
import importlib.util
import sys
import types
from pathlib import Path


def _load():
    spec = importlib.util.spec_from_file_location(
        'create_jiras', Path(__file__).parent.parent / 'scripts' / 'create-jiras'
    )
    mod = types.ModuleType('create_jiras')
    spec.loader.exec_module(mod)
    return mod


mod = _load()
_table_to_jira = mod._table_to_jira
_checklist_to_jira = mod._checklist_to_jira
get_epic_key = mod.get_epic_key


def test_table_converts_header():
    md = '| Source | Heading |\n| --- | --- |\n| Sec A | Do this |'
    result = _table_to_jira(md)
    assert result.startswith('||Source||Heading||')


def test_table_converts_rows():
    md = '| Source | Heading |\n| --- | --- |\n| Sec A | Do this |'
    assert '|Sec A|Do this|' in _table_to_jira(md)


def test_table_empty():
    assert '(No content mapping available.)' in _table_to_jira('')


def test_checklist_converts():
    result = _checklist_to_jira('- [ ] Check one\n- [x] Check two')
    assert '* Check one' in result
    assert '* Check two' in result


def test_get_epic_key(tmp_path):
    p = tmp_path / 'plan.md'
    p.write_text('# Plan\n\nEpic: RHIDP-5678\n')
    assert get_epic_key(str(p)) == 'RHIDP-5678'


def test_get_epic_key_missing(tmp_path):
    p = tmp_path / 'plan.md'
    p.write_text('# Plan\n\nNo epic here.\n')
    assert get_epic_key(str(p)) is None
```

- [ ] **Step 4.7: Run — expect failure**

```bash
python -m pytest tests/test_create_jiras_helpers.py -v 2>&1 | head -10
```

Expected: `FileNotFoundError` (script doesn't exist yet).

- [ ] **Step 4.8: Create `scripts/create-jiras`**

```python
#!/usr/bin/env python3
"""Create or update Jira tasks from docs/jobs/job-NN.md briefs."""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.parse_markdown import parse_brief, write_jira_key

GITHUB_BASE = 'https://github.com/themr0c/jtbd/blob/main'


def _table_to_jira(md_table):
    lines = [l for l in md_table.splitlines() if '|' in l and '---' not in l]
    if not lines:
        return '(No content mapping available.)'
    result = []
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        sep = '||' if i == 0 else '|'
        result.append(sep + sep.join(cells) + sep)
    return '\n'.join(result)


def _checklist_to_jira(md):
    return '\n'.join(re.sub(r'^- \[[ x]\] ', '* ', l) for l in md.splitlines())


def get_epic_key(plan_path='docs/plan.md'):
    try:
        m = re.search(r'Epic: (RHIDP-\w+)', Path(plan_path).read_text())
        return m.group(1) if m else None
    except FileNotFoundError:
        return None


def _parse_priority(priority_field):
    for key in ('Major', 'Normal', 'Minor'):
        if key in priority_field:
            return key
    return 'Normal'


def _parse_job_num(sheet_row):
    m = re.search(r'#(\d+)', sheet_row)
    return m.group(1).zfill(2) if m else '00'


def _build_description(brief):
    rel = Path(brief['path']).relative_to(Path.cwd())
    link = f'{GITHUB_BASE}/{rel}'
    return (
        f'h1. Job Statement\n\n{brief["job_statement"]}\n\n'
        f'h2. Target Structure\n\n{_table_to_jira(brief["target_structure"])}\n\n'
        f'h2. Rewrite Instructions\n\n{brief["rewrite_instructions"]}\n\n'
        f'h2. Acceptance Criteria\n\n{_checklist_to_jira(brief["acceptance_criteria"])}\n\n'
        f'h2. References\n\n* [Full brief|{link}]\n'
    )


def _run(cmd, label):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'  ERROR {label}: {r.stderr.strip()}', file=sys.stderr)
        return None
    return r.stdout


def create_or_update(brief, parent, dry_run=False):
    priority = _parse_priority(brief['priority'])
    job_num = _parse_job_num(brief['sheet_row'])
    category_label = brief['category'].lower().replace(' ', '-')
    desc = _build_description(brief)

    if brief['jira_key']:
        if dry_run:
            print(f'  [dry-run] UPDATE {brief["jira_key"]} — {brief["title"]}')
            return brief['jira_key']
        cmd = ['jirha', 'update', brief['jira_key'],
               '-s', brief['title'], '--desc', desc, '--priority', priority]
        out = _run(cmd, f'update {brief["jira_key"]}')
        if out is not None:
            print(f'  Updated {brief["jira_key"]} — {brief["title"]}')
        return brief['jira_key'] if out is not None else None

    if dry_run:
        print(f'  [dry-run] CREATE — {brief["title"]} (parent: {parent})')
        return None

    cmd = ['jirha', 'create', 'RHIDP', brief['title'],
           '--type', 'Task', '--priority', priority,
           '--component', 'Documentation', '--desc', desc, '--parent', parent]
    out = _run(cmd, 'create')
    if out is None:
        return None
    for line in out.splitlines():
        if line.startswith('Created '):
            key = line.split(':')[0].replace('Created ', '').strip()
            print(f'  Created {key} — {brief["title"]}')
            return key
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--jobs-dir', default='docs/jobs')
    parser.add_argument('--plan', default='docs/plan.md')
    parser.add_argument('--parent', help='Override epic key from plan.md')
    parser.add_argument('--exec', action='store_true', dest='execute')
    args = parser.parse_args()

    parent = args.parent or get_epic_key(args.plan)
    if not parent:
        print('ERROR: epic key not found in plan.md — use --parent RHIDP-XXXX', file=sys.stderr)
        sys.exit(1)

    briefs = sorted(Path(args.jobs_dir).glob('job-*.md'))
    if not briefs:
        print(f'No job-NN.md files found in {args.jobs_dir}', file=sys.stderr)
        sys.exit(1)

    if not args.execute:
        print('--- DRY RUN (pass --exec to create/update issues) ---\n')

    created, updated, failed = 0, 0, 0
    for brief_path in briefs:
        brief = parse_brief(brief_path)
        was_new = not brief['jira_key']
        key = create_or_update(brief, parent, dry_run=not args.execute)
        if key is None and args.execute:
            failed += 1
        elif key and args.execute:
            if was_new:
                write_jira_key(brief_path, key)
                job_num = _parse_job_num(brief['sheet_row'])
                category_label = brief['category'].lower().replace(' ', '-')
                for label in ['jtbd', f'job-{job_num}', category_label]:
                    subprocess.run(['jirha', 'update', key, '--add-label', label],
                                   capture_output=True, text=True)
                created += 1
            else:
                updated += 1

    if args.execute:
        print(f'\n--- Summary: {created} created, {updated} updated, {failed} failed ---')


if __name__ == '__main__':
    main()
```

```bash
chmod +x scripts/create-jiras
```

- [ ] **Step 4.9: Run all tests**

```bash
python -m pytest tests/ -v
```

Expected: all tests pass (no failures).

- [ ] **Step 4.10: Dry-run smoke test**

```bash
python scripts/create-jiras --plan docs/plan.md --parent RHIDP-PLACEHOLDER
```

Expected: 27 `[dry-run] CREATE` lines.

- [ ] **Step 4.11: Commit**

```bash
git add scripts/lib/parse_markdown.py scripts/create-jiras \
        tests/fixtures/sample_brief.md \
        tests/test_parse_markdown.py tests/test_create_jiras_helpers.py
git commit -m "feat: add create-jiras with Markdown parsing and idempotent Jira sync"
```

---

### Task 5: Update CLAUDE.md and final smoke test

**Files:**
- Modify: `.claude/CLAUDE.md`

- [ ] **Step 5.1: Replace `.claude/CLAUDE.md` content**

Replace the `## import-jobs` section with:

```markdown
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

# Step 4: Create/update Jira tasks (children of epic)
scripts/create-jiras                 # dry run (default)
scripts/create-jiras --exec          # create/update issues
```

`scripts/import-jobs` is superseded by this pipeline but kept for reference.
```

- [ ] **Step 5.2: Run full test suite**

```bash
python -m pytest tests/ -v
```

All tests must pass.

- [ ] **Step 5.3: Final commit**

```bash
git add .claude/CLAUDE.md
git commit -m "docs: update CLAUDE.md with pipeline documentation"
```

---

## Self-Review

**Spec coverage:**

| Spec requirement | Task |
| --- | --- |
| `extract` XLSX → JSON | Task 1 |
| `check-current-state` with fuzzy match, suggest closest, CS decides | Task 2 |
| Clone rhdh-docs locally | Task 2 (`--docs-path` / `RHDH_DOCS_PATH`) |
| `generate-plans` general plan + per-title brief | Task 3 |
| Jira key written back to brief after create | Task 4 (`write_jira_key`) |
| Idempotent create/update | Task 4 (jira_key check) |
| JTBD epic as parent | Task 4 (`--parent` / `get_epic_key`) |
| GitHub link in Jira description | Task 4 (`_build_description`) |
| Phase 2 transition documented | Spec doc + CLAUDE.md |

**No placeholders found.**

**Type consistency:** `parse_brief` returns `jira_key` (string). `create_or_update` reads `brief['jira_key']`. `write_jira_key` takes path + string key. All consistent across tasks.
