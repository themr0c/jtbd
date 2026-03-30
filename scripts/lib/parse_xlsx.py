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
