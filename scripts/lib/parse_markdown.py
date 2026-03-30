"""Parse job-NN.md brief files; write Jira key back to metadata."""
import re
from pathlib import Path


def parse_brief(path):
    """Return dict of sections from a job-NN.md file."""
    text = Path(path).read_text()

    title_m = re.match(r'^# (.+)', text)
    title = title_m.group(1).strip() if title_m else ''

    metadata = {}
    meta_m = re.search(r'## Metadata\n\n[^\n]+\n[^\n]+\n((?:\|[^\n]+\n?)+)', text)
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
