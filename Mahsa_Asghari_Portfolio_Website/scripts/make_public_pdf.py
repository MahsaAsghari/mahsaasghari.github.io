#!/usr/bin/env python3
"""Create the concise public portfolio from published-project data only."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'scripts/site_content.json').read_text())
INK='#0a191b';LIME='#c4ec92';PAPER='#f4f3ec';GRAY='#56665c'
def text(c,x,y,s,size=10,color=INK,font='PSans'):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,s)
def para(c,x,top,w,s,size=10,color=INK,font='PSans',leading=None):
    style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.6,textColor=HexColor(color))
    p=Paragraph(escape(s),style);_,h=p.wrap(w,900);p.drawOn(c,x,top-h);return top-h
def image(c,file,x,y,w,h):
    im=Image.open(file).convert('RGB');iw,ih=im.size;r=min(w/iw,h/ih)
    c.drawImage(ImageReader(str(file)),x+(w-iw*r)/2,y+(h-ih*r)/2,iw*r,ih*r)
def footer(c,n,dark=False):
    fg='#aebbb2' if dark else GRAY
    c.setStrokeColor(HexColor('#32443b' if dark else '#d4d9ce'));c.setLineWidth(.5);c.line(42,50,553,50)
    text(c,42,32,'MAHSA ASGHARI  /  SELECTED RESEARCH',7,fg)
    text(c,530,32,f'{n:02}',8,fg)
def main():
    for name,file in [('PSans','sans-regular'),('PBold','sans-bold'),('PSerif','serif-italic')]:
        pdfmetrics.registerFont(TTFont(name,str(ROOT/f'assets/fonts/{file}.ttf')))
    out=ROOT/'assets/documents/Mahsa_Asghari_Portfolio.pdf';out.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(out),pagesize=(595.28,841.89),pageCompression=1)
    c.setTitle('Mahsa Asghari - Selected Published Research');c.setAuthor('Mahsa Asghari')
    c.setFillColor(HexColor(INK));c.rect(0,0,596,842,fill=1,stroke=0)
    text(c,43,795,'RESEARCH PORTFOLIO  /  2026',8,LIME,'PBold')
    text(c,42,714,'Mahsa',55,PAPER);text(c,39,650,'Asghari.',58,LIME,'PSerif')
    text(c,44,604,'PhD in Physics / Optics',12,PAPER)
    para(c,44,568,242,DATA['introduction'],11,'#b5c2b8')
    image(c,ROOT/'assets/images/portrait-pdf.jpg',330,448,222,296)
    text(c,44,449,'KASSEL, GERMANY',8,LIME,'PBold')
    c.setStrokeColor(HexColor('#34463c'));c.line(43,414,553,414)
    for i,skill in enumerate(DATA['expertise']):
        x=44+i*175
        text(c,x,380,f'0{i+1} / {skill["title"].upper()}',8,LIME,'PBold')
        para(c,x,360,152,skill['text'],9,'#c7d0c7')
    text(c,44,269,'RESEARCH & EDUCATION',8,LIME,'PBold')
    para(c,44,249,507,'PhD in Physics (Optics), IASBS, 2016-2025. Highest distinction. Visiting PhD Researcher, University of Kassel, 2024-2025.',10,PAPER)
    text(c,44,184,'SCIENTIFIC PEER REVIEW',8,LIME,'PBold')
    para(c,44,165,507,'40+ manuscripts reviewed. IOP Publishing Outstanding Reviewer (2024) and Trusted Reviewer (2024, 2026).',10,'#c7d0c7')
    text(c,44,103,DATA['email'],11,PAPER)
    text(c,44,82,'Authorized to work full-time in Germany',8,'#b5c2b8')
    footer(c,1,True);c.showPage()
    manifest={i['name']:i for i in json.loads((ROOT/'assets/asset-manifest.json').read_text())}
    for n,p in enumerate(DATA['projects'],2):
        c.setFillColor(HexColor(PAPER));c.rect(0,0,596,842,fill=1,stroke=0)
        text(c,42,800,f'{p["number"]} / PUBLISHED RESEARCH',8,'#4d7134','PBold')
        titlebottom=para(c,42,775,511,p['title'],25,INK,leading=31)
        nexttop=para(c,42,titlebottom-15,511,p['deck'],10,GRAY,leading=15)
        text(c,42,nexttop-22,p['institution']+'  /  '+p['date']+'  /  '+p['role'],8,'#4b633e')
        c.setFillColor(HexColor('#ffffff'));c.rect(42,365,511,235,fill=1,stroke=0)
        image(c,ROOT/manifest[p['image']]['file'],54,378,487,209)
        para(c,42,352,511,manifest[p['image']]['caption'],8,GRAY,leading=12)
        text(c,42,310,'KEY OUTCOME',8,'#4d7134','PBold')
        y=para(c,42,292,511,p['result'],11,INK,leading=17)
        text(c,42,y-26,'REPORTED SCOPE',8,'#4d7134','PBold')
        para(c,42,y-41,511,p['scope'],9,GRAY,leading=14)
        text(c,42,158,'PUBLICATION',8,'#4d7134','PBold')
        para(c,42,142,511,p['publication'],10,INK,leading=15)
        text(c,42,94,'https://doi.org/'+p['doi'],8,GRAY)
        c.linkURL('https://doi.org/'+p['doi'],(42,88,553,105),relative=0)
        footer(c,n);c.showPage()
    c.save();print(out)
if __name__=='__main__':main()
