"""Regression checks for the production workshop homepage."""
from pathlib import Path
import re
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'public/index.html').read_text()
assert 'Make the unknowns<br>easier to discuss.' in html, 'Approved workshop homepage missing'
assert 'workshop-script' in html
assert '<style' not in html and ' style=' not in html
assert 'unsafe-inline' not in (ROOT / 'scripts/build.py').read_text()
for text in ('noindex', 'Local design', 'comparison gallery', 'DESIGN DRAFT', 'interactive prototype', 'blueprint v3'):
    assert text not in html, text
assert 'href="/contact/"' in html
assert 'href="/privacy/"' in html
assert 'href="/assets/workshop.css"' in html
assert 'No scanner. No score. No promise to find everything.' in html
assert len(re.findall('data-choice=', html)) == 3
assert 'id="reset"' in html
print('Passed: approved workshop, production framing, real contact, static CSS and scenario controls.')
