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
