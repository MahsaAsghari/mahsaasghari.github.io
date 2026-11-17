#!/usr/bin/env python3
"""Generate the self-contained public website; no build is needed for publishing."""
from pathlib import Path
from html import escape as E
import json, base64, mimetypes, re
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'scripts/site_content.json').read_text())
IMAGES={i['name']:i for i in json.loads((ROOT/'assets/asset-manifest.json').read_text())}
def uri(path):
    mime=mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(Path(path).read_bytes()).decode()
ARROW='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" stroke-width="1.5"/></svg>'
RIGHT='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6" stroke="currentColor" stroke-width="1.5"/></svg>'
DOWN='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4" stroke="currentColor" stroke-width="1.5"/></svg>'
MARK='<svg width="40" height="40" viewBox="0 0 44 44" fill="none" aria-hidden="true"><circle cx="22" cy="22" r="19"/><ellipse cx="22" cy="22" rx="8" ry="19"/><path d="M0 22h44"/><circle cx="22" cy="22" r="3" fill="currentColor" stroke="none"/></svg>'
def image(name,cls='',eager=False):
    i=IMAGES[name]
    return f'<img class="{cls}" src="{uri(ROOT/i["file"])}" width="{i["width"]}" height="{i["height"]}" alt="{E(i["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def figure(name,index):
    i=IMAGES[name]
    return f'<figure class="science-figure"><div class="figure-frame">{image(name)}<button class="enlarge" type="button" data-enlarge aria-label="Enlarge: {E(i["caption"])}" hidden>{ARROW}</button></div><figcaption><span>{index:02}</span> {E(i["caption"])}</figcaption></figure>'
def project(p):
    figures=''
    n=0
    for group in p['groups']:
        for name in group['images']:
            n+=1;figures+=figure(name,n)
    contributions=''.join('<li>'+E(t)+'</li>' for t in p['contribution'])
    facts=''.join('<div><dt>'+E(k)+'</dt><dd>'+E(v)+'</dd></div>' for k,v in p['facts'])
    slug=p['slug']
    return f'''<article class="project" data-category="{p['category']}" aria-labelledby="title-{slug}">
<a class="project-media" href="#study-{slug}" aria-label="Explore {E(p['title'])}">{image(p['image'])}<span class="image-index">{p['number']} / PUBLISHED STUDY</span><span class="image-open">{ARROW}</span></a>
<div class="project-summary"><div class="project-journal"><span>{E(p['institution'])}</span><span>{p['date']}</span></div><span class="project-role">{E(p['role'])}</span><h3 id="title-{slug}"><a href="#study-{slug}">{E(p['title'])}</a></h3><p>{E(p['deck'])}</p><div class="project-actions"><a href="#study-{slug}" class="study-link">Explore study {RIGHT}</a><a href="https://doi.org/{p['doi']}" class="paper-link" target="_blank" rel="noopener noreferrer">Read paper {ARROW}</a></div></div>
<details class="study-detail" id="study-{slug}"><summary><span>Inside the experiment</span><span class="detail-plus" aria-hidden="true">+</span></summary><div class="study-body"><div class="study-overview"><div><p class="eyebrow">THE RESEARCH QUESTION</p><h4>{E(p['question'])}</h4><dl>{facts}</dl></div><aside><p class="eyebrow">MY CONTRIBUTION</p><ul>{contributions}</ul></aside></div><div class="outcome"><span class="eyebrow">KEY OUTCOME</span><p>{E(p['result'])}</p><small>{E(p['scope'])}</small></div><div class="figure-grid">{figures}</div><a class="publication-link" href="https://doi.org/{p['doi']}" target="_blank" rel="noopener noreferrer"><span>VIEW THE PUBLICATION</span><strong>{E(p['publication'])}</strong>{ARROW}</a></div></details></article>'''
def main():
    style=(ROOT/'assets/style.css').read_text()
    for font in ['sans-regular','sans-bold','serif-italic']:
        style=style.replace('@@'+font.upper().replace('-','_')+'@@',uri(ROOT/f'assets/fonts/{font}.woff'))
    timeline=''
    for role in DATA['background']:
        body=f'<p>{E(role["text"])}</p>' if role['text'] else ''
        timeline+=f'<li><span class="timeline-year">{E(role["date"])}</span><div><h3>{E(role["title"])}</h3><span class="institution">{E(role["organization"])}</span>{body}</div></li>'
    favicon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#0a191b"/><g stroke="#c4ec92" fill="none" stroke-width="1.5"><circle cx="32" cy="32" r="22"/><ellipse cx="32" cy="32" rx="9" ry="22"/><path d="M5 32h54"/></g><circle cx="32" cy="32" r="3" fill="#c4ec92"/></svg>'
    values={'STYLE':style,'SCRIPT':(ROOT/'assets/site.js').read_text(),'INTRO':E(DATA['introduction']),'BIOGRAPHY':E(DATA['biography']),'EMAIL':E(DATA['email']),'PORTRAIT':uri(ROOT/'assets/images/portrait.webp'),'PDF_DATA':json.dumps({'base64':base64.b64encode((ROOT/'assets/documents/Mahsa_Asghari_Portfolio.pdf').read_bytes()).decode()}),'FAVICON':'data:image/svg+xml;base64,'+base64.b64encode(favicon.encode()).decode(),'PROJECTS':''.join(project(p) for p in DATA['projects']),'TIMELINE':timeline,'MARK':MARK,'ARROW':ARROW,'DOWNLOAD':DOWN}
    html=(ROOT/'scripts/templates/home.html').read_text()
    for key,value in values.items():html=html.replace('@@'+key+'@@',value)
    if re.search(r'@@[A-Z_]+@@',html):raise ValueError('Unresolved template token')
    (ROOT/'index.html').write_text(html,encoding='utf-8')
    # Keep existing published URLs useful without duplicating the research pages.
    for p in DATA['projects']:
        (ROOT/f'projects/{p["slug"]}.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=../index.html#study-{p["slug"]}"><link rel="canonical" href="https://mahsaasghari.github.io/#study-{p["slug"]}"><title>{E(p["title"])} | Mahsa Asghari</title><a href="../index.html#study-{p["slug"]}">Open this published study</a></html>')
    # Overwrite the previous public URL with only the concept-level statement.
    concept='Polarization-sensitive OCT. An unpublished research concept.'
    stub=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Research interest | Mahsa Asghari</title><style>body{{margin:0;background:#0a191b;color:#f4f3ec;font:18px/1.8 Arial,sans-serif;min-height:100vh;display:grid;place-items:center}}main{{max-width:620px;padding:30px}}small,a{{color:#c4ec92}}h1{{font-weight:400;font-size:42px;line-height:1.2}}a{{display:inline-block;margin-top:20px}}</style><main><small>MAHSA ASGHARI / RESEARCH INTEREST</small><h1>Polarization-sensitive OCT.</h1><p>An unpublished research concept.</p><a href="../index.html#about">Return to portfolio →</a></main></html>'
    (ROOT/'projects/polarization-sensitive-oct.html').write_text(stub)
    print('Built the self-contained website, four compatibility links, and a minimal unpublished-concept page.')
if __name__=='__main__':main()
