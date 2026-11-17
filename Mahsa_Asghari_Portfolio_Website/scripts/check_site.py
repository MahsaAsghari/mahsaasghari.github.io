#!/usr/bin/env python3
"""Validate public scope, standalone assets, links, figures and the embedded PDF."""
import base64,hashlib,json,re,io
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.refs=[];self.images=[];self.scripts=[];self.styles=[];self.projects=0;self.details=0;self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):
            assert a['id'] not in self.ids,'Duplicate ID '+a['id']
            self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='a' and a.get('href'):self.refs.append(a['href'])
        if tag=='img' and a.get('src'):self.images.append(a)
        if tag=='script' and a.get('src'):self.scripts.append(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet':self.styles.append(a.get('href'))
        if tag=='article' and 'data-category' in a:self.projects+=1
        if tag=='details' and 'study-detail' in a.get('class',''):self.details+=1
def main():
    html=(ROOT/'index.html').read_text()
    page=Page();page.feed(html)
    assert page.h1==1 and page.projects==4 and page.details==4
    assert not page.scripts and not page.styles,'External CSS or JS in the standalone page'
    assert not re.search(r'@@[A-Z_]+@@',html),'Unresolved template'
    for ref in page.refs:
        if ref.startswith('#'):assert ref[1:] in page.ids,'Broken fragment '+ref
    for image in page.images:
        assert image['src'].startswith('data:image/'),'Non-embedded image'
        for field in ['alt','width','height']:assert image.get(field),'Missing image '+field
        assert not re.search(r'\b(?:OCT|PS-OCT|Linnik)\b',image['alt'],re.I),'Unpublished-work image'
    for url in re.findall(r'url\("([^"]+)"\)',html.split('</style>')[0]):
        assert url.startswith('data:'),'External CSS asset'
    for word in ['172.86','730 nm','Linnik','Four-step','full-field PS-OCT','dual-channel full-field']:
        for p in [ROOT/'index.html',ROOT/'scripts/site_content.json',ROOT/'projects/polarization-sensitive-oct.html']:
            assert word.lower() not in p.read_text().lower(),'Unpublished detail in '+str(p)
    manifest=json.loads((ROOT/'assets/asset-manifest.json').read_text())
    assert len(manifest)==19 and not any(i['name'].startswith('oct-') for i in manifest)
    for i in manifest:assert (ROOT/i['file']).is_file()
    for project in json.loads((ROOT/'scripts/site_content.json').read_text())['projects']:
        slug=project['slug']
        assert 'study-'+slug in page.ids
        assert '../index.html#study-'+slug in (ROOT/f'projects/{slug}.html').read_text()
    pdfdata=re.search(r'<script id="portfolio-data" type="application/json">(.*?)</script>',html,re.S).group(1)
    decoded=base64.b64decode(json.loads(pdfdata)['base64'])
    assert decoded==(ROOT/'assets/documents/Mahsa_Asghari_Portfolio.pdf').read_bytes()
    assert decoded.startswith(b'%PDF-')
    # Optional checks use the existing PDF/image toolchain when available.
    try:
        from PIL import Image
        for image in page.images:
            Image.open(io.BytesIO(base64.b64decode(image['src'].split(',',1)[1]))).verify()
        for p in (ROOT/'assets/images').rglob('oct-*'):
            with Image.open(p) as im:assert im.size==(1,1),'Legacy image not cleared: '+str(p)
    except ImportError:pass
    try:
        import fitz
        pdf=fitz.open(stream=decoded,filetype='pdf')
        assert len(pdf)==5
        text=' '.join(p.get_text() for p in pdf)
        for term in ['OCT','172.86','Linnik','730 nm']:
            assert term.lower() not in text.lower(),'Unpublished detail in PDF'
    except ImportError:pass
    print('PASS: 4 published studies, standalone images/fonts/styles/scripts, working fragments, public-only data, empty legacy images, and matching embedded PDF.')
if __name__=='__main__':main()
