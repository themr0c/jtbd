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
