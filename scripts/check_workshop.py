"""Regression checks for the production workshop homepage."""
from pathlib import Path
import re
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / 'public/index.html').read_text()
assert 'Make the unknowns<br>easier to discuss.' in html, 'Approved workshop homepage missing'
assert '<style' not in html and ' style=' not in html
assert 'unsafe-inline' not in (ROOT / 'scripts/build.py').read_text()
for text in ('noindex', 'Local design', 'comparison gallery', 'DESIGN DRAFT', 'interactive prototype', 'blueprint v3'):
    assert text not in html, text
assert 'href="/contact/"' in html
assert 'href="/privacy/"' in html
assert 'href="/assets/workshop.css"' in html
# naming: the guided session is Owl Laboratory; retired name must not appear
assert 'Owl Laboratory is a guided cybersecurity conversation from Taute Group for business teams.' in html
# /Bundi/ URL is preserved by design; only the visible retired name must not appear
import re as _re
visible=_re.sub(r'href="/Bundi/"','',html)
assert 'Bundi' not in visible, 'Retired service name must not appear'
# concise copy budget (readable prose, excluding svg artwork labels)
main = html[html.find('<main'):html.find('</main>')]
nosvg = re.sub(r'<svg.*?</svg>', '', main, flags=re.S)
words = len(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', nosvg)).strip().split())
assert 220 <= words <= 395, f'Homepage prose budget breached: {words} words'
# required boundary statement and consistent CTA
assert 'No scanner. No score. No promise to find everything.' in html
assert html.count('Discuss your priorities') >= 2
# process shown in four brief steps
assert len(re.findall(r'<span class="num">0\d</span>', html)) == 4
print('Passed: Owl Laboratory homepage, concise copy budget, boundaries and consistent CTA.')
