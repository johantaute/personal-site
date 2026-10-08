"""Check published pages and internal navigation using the standard library."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set();self.h1=0;self.main=0;self.title=0;self.meta=set();self.svg=0
    def handle_starttag(self, tag, attrs):
        if tag=='svg':self.svg+=1
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, 'Duplicate ID';self.ids.add(a['id'])
        self.h1+=tag=='h1';self.main+=tag=='main';self.title+=tag=='title' and self.svg==0
        if tag=='meta':self.meta.add(a.get('name',a.get('property')))
        if tag in ('a','link','img'):
            self.links.append(a.get('href',a.get('src','')))
        if tag=='img':assert 'alt' in a, 'Missing image alternative'
        assert tag not in ('form','iframe'), 'Unexpected active integration'
        if tag=='script':assert a=={'id':'email-copy-script'}, 'Unexpected script'
        assert not any(k.startswith('on') for k in a), 'Inline event handler'
    def handle_endtag(self,tag):
        if tag=='svg':self.svg-=1
pages={}
for file in ROOT.rglob('*.html'):
    html=file.read_text()
    if '<script' in html:
        assert file==ROOT/'contact/index.html' and html.count('<script')==1, 'Unexpected script placement'
        assert "navigator.clipboard.writeText('contact@tautegroup.co.za')" in html
    p=Page();p.feed(html);assert p.h1==p.main==p.title==1, str(file)
    assert {'description','viewport','og:title','og:description','og:url','og:image','twitter:card'}<=p.meta, str(file)
    pages[file]=p
for file,p in pages.items():
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        dest=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else file.parent/unquote(u.path)
        if not u.path:dest=file
        if dest.is_dir():dest=dest/'index.html'
        assert dest.is_file(), f'{file}: broken link {link}'
        if u.fragment:assert dest in pages and unquote(u.fragment) in pages[dest].ids, f'Broken anchor {link}'
assert not (ROOT/'original').exists()
assert "connect-src 'none'" in (ROOT/'_headers').read_text()
print(f'Passed: {len(pages)} pages, metadata, landmarks, image alternatives, internal links/anchors and public boundaries.')
