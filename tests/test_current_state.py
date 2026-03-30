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
