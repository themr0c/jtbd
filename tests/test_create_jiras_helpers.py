import importlib.util
import sys
import types
from pathlib import Path


def _load():
    script_path = Path(__file__).parent.parent / 'scripts' / 'create-jiras'
    loader = importlib.machinery.SourceFileLoader('create_jiras', str(script_path))
    spec = importlib.util.spec_from_loader('create_jiras', loader)
    mod = types.ModuleType('create_jiras')
    mod.__file__ = str(script_path)
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
