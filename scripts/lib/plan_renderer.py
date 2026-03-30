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
