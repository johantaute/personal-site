"""Regression checks for the public, explicitly fictional sample report."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.findings = []
        self.ids = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'article' and 'data-risk' in attrs:
            self.findings.append(attrs)

text = (ROOT / 'public/sample-report/index.html').read_text()
p = ReportParser()
p.feed(text)
assert 'fictional company' in text, 'The example must explicitly identify a fictional company'
assert len(p.findings) == 6, 'Expected six detailed, scored illustrative findings'
assert len(p.ids) == len(set(p.ids)), 'Duplicate anchor IDs'
for finding in p.findings:
    assert int(finding['data-score']) == int(finding['data-likelihood']) * int(finding['data-impact'])
assert sorted(int(f['data-score']) for f in p.findings) == [6, 9, 12, 12, 16, 16]
for section in ['summary', 'scope', 'baseline', 'scoring', 'findings', 'roadmap', 'decisions', 'evidence']:
    assert section in p.ids, f'Missing report section: {section}'
for phrase in ['not an industry benchmark', 'not a compliance certification', 'Closure evidence', 'Illustrative evidence register']:
    assert phrase in text, f'Missing safety or action context: {phrase}'
print('Passed: fictional labelling, 6 findings, scoring arithmetic, section anchors and closure context.')
