#!/usr/bin/env python3
"""Audit a generated static SEO site. Stdlib only; no external HTTP required."""
from __future__ import annotations
import argparse, json, sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__();self.title='';self.h1=[];self.links=[];self.assets=[];self.images=[];self.meta={};self.canonical=[];self.lang='';self.in_title=False;self.in_h1=False;self.in_json=False;self.jsons=[];self.buffer='';self.h1_buffer=''
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='html':self.lang=d.get('lang','')
        if tag=='title':self.in_title=True
        if tag=='h1':self.in_h1=True;self.h1_buffer=''
        if tag=='meta':
            key=d.get('name') or d.get('property')
            if key:self.meta[key]=d.get('content','')
        if tag=='link' and d.get('rel')=='canonical':self.canonical.append(d.get('href',''))
        if tag=='a' and 'href' in d:self.links.append(d['href'])
        if tag=='link' and d.get('rel') in ('stylesheet','icon') and 'href' in d:self.assets.append(d['href'])
        if tag=='script' and d.get('src'):self.assets.append(d['src'])
        if tag=='img':self.images.append(d)
        if tag=='script' and d.get('type')=='application/ld+json':self.in_json=True;self.buffer=''
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.in_h1:self.h1_buffer+=data
        if self.in_json:self.buffer+=data
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='h1':self.in_h1=False;self.h1.append(self.h1_buffer.strip())
        if tag=='script' and self.in_json:self.in_json=False;self.jsons.append(self.buffer)

def audit(folder:Path,site_url='https://aipmandy.github.io/seo-handbook/'):
    errors=[];warnings=[];pages=sorted(folder.rglob('*.html'));titles=defaultdict(list);canonicals=defaultdict(list)
    if not pages:return ['No HTML pages found'],[],0
    for p in pages:
        rel=p.relative_to(folder).as_posix();parser=Inspect()
        try:parser.feed(p.read_text(encoding='utf-8'))
        except Exception as e:errors.append(f'{rel}: cannot parse HTML: {e}');continue
        if not parser.title:errors.append(f'{rel}: missing title')
        else:titles[parser.title].append(rel)
        if len(parser.h1)!=1:errors.append(f'{rel}: expected exactly one H1, found {len(parser.h1)}')
        if not parser.meta.get('description'):errors.append(f'{rel}: missing meta description')
        if not parser.lang:errors.append(f'{rel}: missing html lang')
        if 'noindex' in parser.meta.get('robots','').lower():errors.append(f'{rel}: accidental noindex')
        if len(parser.canonical)!=1:errors.append(f'{rel}: expected one canonical, found {len(parser.canonical)}')
        else:
            expected=site_url.rstrip('/')+'/' if rel=='index.html' else site_url.rstrip('/')+'/'+rel
            if parser.canonical[0]!=expected:errors.append(f'{rel}: canonical mismatch expected={expected}')
            canonicals[parser.canonical[0]].append(rel)
        if not parser.jsons:errors.append(f'{rel}: JSON-LD missing')
        for script in parser.jsons:
            try:
                parsed=json.loads(script)
                if parsed.get('@context')!='https://schema.org':errors.append(f'{rel}: unexpected schema.org context')
            except Exception as e:errors.append(f'{rel}: JSON-LD parse failed: {e}')
        for img in parser.images:
            if 'alt' not in img:errors.append(f'{rel}: image missing alt')
        for href in parser.links+parser.assets:
            parsed=urlparse(href)
            if parsed.scheme or parsed.netloc or href.startswith('#') or href.startswith('mailto:'):continue
            if not parsed.path:continue
            target=(p.parent/unquote(parsed.path)).resolve()
            if not target.is_relative_to(folder.resolve()):errors.append(f'{rel}: broken/outside relative path {href}');continue
            if target.is_dir():target=target/'index.html'
            if not target.is_file():errors.append(f'{rel}: broken internal href {href}')
        if len(p.read_text(encoding='utf-8'))<650:warnings.append(f'{rel}: unusually short HTML')
    for title,paths in titles.items():
        if len(paths)>1:errors.append('Duplicate title: '+', '.join(paths))
    for link,paths in canonicals.items():
        if len(paths)>1:errors.append('Duplicate canonical: '+', '.join(paths))
    sm=folder/'sitemap.xml'
    if not sm.exists():errors.append('No sitemap.xml')
    else:
        try:
            tree=ET.parse(sm)
            locs=[el.text for el in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
            known={site_url.rstrip('/')+'/' if p.relative_to(folder).as_posix()=='index.html' else site_url.rstrip('/')+'/'+p.relative_to(folder).as_posix() for p in pages}
            if set(locs)!=known:errors.append(f'Sitemap URL mismatch missing={len(known-set(locs))} extra={len(set(locs)-known)}')
            if len(locs)!=len(set(locs)):errors.append('Sitemap duplicate loc')
        except Exception as e:errors.append(f'Invalid sitemap: {e}')
    if (folder/'robots.txt').exists() and '/seo-handbook/' in site_url:
        warnings.append('GitHub Pages project subpath robots.txt cannot control host root; review root robots semantics')
    return errors,warnings,len(pages)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('site',nargs='?',default='_site');ap.add_argument('--base',default='https://aipmandy.github.io/seo-handbook/');args=ap.parse_args()
    errors,warnings,count=audit(Path(args.site).resolve(),args.base)
    print(f'Checked {count} HTML pages; {len(errors)} errors, {len(warnings)} warnings')
    for msg in errors:print('ERROR:',msg)
    for msg in warnings:print('WARNING:',msg)
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
