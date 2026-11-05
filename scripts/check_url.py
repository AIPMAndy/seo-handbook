#!/usr/bin/env python3
"""Lightweight, single-URL on-page checker; not a crawler or rank checker."""
from __future__ import annotations
import argparse,json,sys,urllib.error,urllib.request
from urllib.parse import urlparse
from site_audit import Inspect

def check(url):
    parsed=urlparse(url)
    if parsed.scheme not in ('http','https') or not parsed.netloc:raise ValueError('请传入 http/https 完整网页 URL')
    req=urllib.request.Request(url,headers={'User-Agent':'SEOHandbookAudit/1.0 (+https://github.com/AIPMAndy/seo-handbook)'})
    with urllib.request.urlopen(req,timeout=12) as resp:
        body=resp.read(3_000_001)
        if len(body)>3_000_000:raise ValueError('页面超过 3MB HTML 检查上限')
        ctype=resp.headers.get('Content-Type','')
        if 'html' not in ctype.lower():raise ValueError(f'响应不是 HTML: {ctype}')
        encoding=resp.headers.get_content_charset() or 'utf-8'
        text=body.decode(encoding,errors='replace')
        page=Inspect();page.feed(text)
        result={
           'requested_url':url,'final_url':resp.geturl(),'http_status':resp.status,
           'title':page.title.strip(),'h1':page.h1,'meta_description':page.meta.get('description',''),
           'meta_robots':page.meta.get('robots',''),
           'x_robots_tag':resp.headers.get('X-Robots-Tag',''),
           'canonical':page.canonical,'html_lang':page.lang,'internal_links_detected':len(page.links),
           'schema_blocks':len(page.jsons),
           'important_warnings':[]
        }
        if resp.geturl()!=url:result['important_warnings'].append('URL 有跳转；请核对最终页面和重定向类型')
        if not page.title:result['important_warnings'].append('缺少 title')
        if len(page.h1)!=1:result['important_warnings'].append('H1 数量不是 1，建议人工检查语义结构')
        if not page.meta.get('description'):result['important_warnings'].append('缺少 description')
        if not page.canonical:result['important_warnings'].append('未声明 canonical（不代表一定有错误）')
        if len(page.canonical)>1:result['important_warnings'].append('存在多个 canonical')
        if 'noindex' in (result['meta_robots']+' '+result['x_robots_tag']).lower():result['important_warnings'].append('页面被标为 noindex，请确认是否符合意图')
        if not page.lang:result['important_warnings'].append('缺少 html lang')
        return result

def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument('url',help='你有权限诊断的单个公开网页 URL');args=ap.parse_args(argv)
    try:result=check(args.url)
    except (ValueError,urllib.error.URLError,TimeoutError,UnicodeError) as e:print('检查失败：',e,file=sys.stderr);return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    print('注意：此脚本不能证明 Google 已抓取、收录或排名。请在 GSC 网址检查中确认。')
    return 0
if __name__=='__main__':sys.exit(main())
