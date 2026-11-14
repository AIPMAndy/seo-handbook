#!/usr/bin/env python3
"""Render every PDF page; enforce text, source coverage, clickable brand links and page bounds.
A contact sheet is automated evidence, not a human 100% zoom or phone-device sign-off.
"""
import argparse,json
from pathlib import Path
import fitz
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('pdf',type=Path)
    ap.add_argument('--qa-dir',type=Path,default=Path('qa/pdf'))
    args=ap.parse_args()
    chapters=json.loads((ROOT/'data/chapters.json').read_text(encoding='utf-8'))
    sops=json.loads((ROOT/'data/sops.json').read_text(encoding='utf-8'))
    doc=fitz.open(args.pdf);issues=[];links=[];thumbs=[]
    if not 55<=len(doc)<=450:issues.append(f'Unexpected page count {len(doc)}')
    if args.pdf.stat().st_size<100000:issues.append('PDF unexpectedly small')
    whole='\n'.join(p.get_text() for p in doc)
    for needle in ('AIPMAndy','metaver.vip','a6no1.cn','教学场景'):
        if needle not in whole:issues.append(f'Missing text {needle}')
    for ch in chapters:
        if ch['title'] not in whole:issues.append('Missing chapter '+ch['title'])
    for sop in sops:
        if sop['title'] not in whole:issues.append('Missing SOP '+sop['title'])
    for i,page in enumerate(doc):
        if not page.get_text().strip():issues.append(f'Blank/image-only page {i+1}')
        if page.rect.width<500 or page.rect.height<700:issues.append(f'Unexpected paper size p{i+1}')
        for block in page.get_text('blocks'):
            x0,y0,x1,y1,*_=block
            if min(x0,y0)<-2 or x1>page.rect.width+2 or y1>page.rect.height+2:
                issues.append(f'Out-of-bounds text block p{i+1}')
        for l in page.get_links():
            if l.get('uri'):links.append(l['uri'])
        pix=page.get_pixmap(matrix=fitz.Matrix(.65,.65),alpha=False)
        thumb=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        thumb.thumbnail((175,230),Image.Resampling.LANCZOS)
        thumbs.append(thumb)
    for link in ['https://metaver.vip/','https://metaver.vip/services','https://www.a6no1.cn/',
                 'https://github.com/AIPMAndy/seo-handbook']:
        if link not in links:issues.append('Missing clickable URL '+link)
    out=args.qa_dir;out.mkdir(parents=True,exist_ok=True)
    w,h,columns=198,270,8
    sheet=Image.new('RGB',(w*columns,h*((len(thumbs)+columns-1)//columns)),'#e9eef5')
    draw=ImageDraw.Draw(sheet)
    for i,thumb in enumerate(thumbs):
        x=i%columns*w+11;y=i//columns*h+7
        sheet.paste(ImageOps.expand(thumb,border=1,fill='#aebccc'),(x,y))
        draw.text((x,y+239),str(i+1),fill='#334155')
    sheet.save(out/'all-pages-contact-sheet.jpg',quality=84,optimize=True)
    report={'status':'passed' if not issues else 'failed','pages':len(doc),
        'chapters':len(chapters),'sops':len(sops),'links':len(links),
        'rendered_pages':len(thumbs),'text_characters':len(whole),
        'fonts':sorted({x[3] for p in doc for x in p.get_fonts()}),
        'errors':issues,'limitations':['Automatic contact sheet is not high-resolution human approval',
        'Safari/iOS and Android physical device QA still required',
        'Official links retain source dates; this does not recheck their current validity']}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','pages','chapters','sops','links','rendered_pages','text_characters','errors')},ensure_ascii=False))
    if issues:raise SystemExit(1)
if __name__=='__main__':main()
