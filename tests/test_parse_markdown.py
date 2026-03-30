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
