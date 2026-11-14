#!/usr/bin/env python3
"""Reproducible PDF edition generated from the same JSON that drives the website."""
from __future__ import annotations
import argparse, html, json
from pathlib import Path
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
SITE='https://aipmandy.github.io/seo-handbook/'
def read(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
def e(v):return html.escape(str(v),quote=True)
def a(url,label):return f'<a href="{e(url)}">{e(label)}</a>'
def action_list(steps):
    return ''.join(
        f'<li><p class="action"><strong>{i:02d}.</strong> {e(step["do"])}</p>'
        f'<p class="proof"><b>验收/凭证：</b>{e(step.get("done",step.get("proof","")))}</p>'
        f'<p class="fallback"><b>卡住怎么办：</b>{e(step["stuck"])}</p></li>'
        for i,step in enumerate(steps,1))
def source_list(ids,sources):
    return '<ul class="sources">'+''.join(
        '<li>'+a(sources[k]['url'],sources[k]['title'])+
        f'<span>官方资料 · 源数据核验日期 {e(sources[k].get("checked","未记录"))}</span></li>'
        for k in ids)+'</ul>'
def make_html():
    chapters,sops,routes=read('chapters.json'),read('sops.json'),read('routes.json')
    sources={s['id']:s for s in read('sources.json')}
    if len(chapters)<40 or len(sops)<10:raise ValueError('Refuse incomplete PDF source')
    missing={k for x in chapters+sops for k in x['sources']}-set(sources)
    if missing:raise ValueError(f'Missing references: {sorted(missing)}')
    toc=[];body=[];sop_toc=[];sop_body=[]
    for ch in chapters:
        anchor='ch-'+ch['id']
        toc.append(f'<li>{a("#"+anchor,ch["id"]+" / "+ch["title"])}</li>')
        body.append(f'''<section class="chapter" id="{e(anchor)}">
<div class="overline">PART I / 41 CHAPTERS / {e(ch['stage'])} / {e(ch['minutes'])} MIN</div>
<h2>{e(ch['id'])}. {e(ch['title'])}</h2><p class="outcome">本章交付目标：{e(ch['outcome'])}</p>
<div class="scenario"><b>教学场景（非真实客户结果）</b><p>{e(ch['example'])}</p></div>
<h3>逐步操作与验收</h3><ol class="steps">{action_list(ch['steps'])}</ol>
<div class="deliverable"><b>本章交付物</b><p>{e(ch['deliverable'])}</p></div>
<h3>官方核验资料</h3>{source_list(ch['sources'],sources)}</section>''')
    for i,sop in enumerate(sops,1):
        anchor='sop-'+sop['id']
        sop_toc.append(f'<li>{a("#"+anchor,f"{i:02d} / "+sop["title"])}</li>')
        sop_body.append(f'''<section class="chapter" id="{e(anchor)}">
<div class="overline">PART II / STANDARD OPERATING PROCEDURE / {i:02d}</div>
<h2>{e(sop['title'])}</h2><p class="outcome">适用情境：{e(sop['entry'])}</p>
<h3>操作、凭证与失败回退</h3><ol class="steps">{action_list(sop['steps'])}</ol>
<div class="deliverable"><b>最终交付物</b><p>{e(sop['deliverable'])}</p></div>
<h3>官方核验资料</h3>{source_list(sop['sources'],sources)}</section>''')
    routes_body=[]
    for rt in routes:
        daily=''.join(f'<li><b>第 {i} 天</b> {e(d[0])}<span>凭证：{e(d[1])}</span></li>'
                      for i,d in enumerate(rt['daily'],1))
        routes_body.append(f'''<section class="route"><h3>{e(rt['title'])}</h3>
<p><b>适用：</b>{e(rt['for'])}</p><p><b>7 天目标：</b>{e(rt['goal'])}</p>
<ol>{daily}</ol><p><b>30 天：</b>{e(rt['days30'])}</p>
<p><b>90 天：</b>{e(rt['days90'])}</p></section>''')
    css=r"""
@page{size:A4;margin:21mm 19mm 20mm;@top-left{content:"SEO HANDBOOK  /  AIPMAndy";font:9px "Noto Sans CJK SC",sans-serif;color:#667085}
@top-right{content:"OPEN SOURCE  /  2026";font:9px "Noto Sans CJK SC",sans-serif;color:#667085}
@bottom-left{content:"AI 酋长 Andy  ·  metaver.vip  ·  AIPMAndy";font:9px "Noto Sans CJK SC",sans-serif;color:#8a919d}
@bottom-right{content:counter(page);font:10px "Noto Sans CJK SC",sans-serif;color:#677080}}
@page cover{margin:0;@top-left{content:none}@top-right{content:none}@bottom-left{content:none}@bottom-right{content:none}}
html{font-family:"Noto Sans CJK SC","Noto Sans SC",sans-serif;color:#101828;font-size:10.2pt;line-height:1.72}
body{margin:0}h1,h2,h3,p,ol,ul{margin-top:0}
h1{font-weight:750;letter-spacing:-1px;font-size:37pt;line-height:1.35}
h2{font-size:20.5pt;line-height:1.43;letter-spacing:-.3px;margin:6mm 0 7mm}
h3{font-size:12.5pt;margin:9mm 0 3mm;color:#1a3b60;break-after:avoid}
p,li{orphans:2;widows:2}a{color:#1758a4;text-decoration:none;overflow-wrap:anywhere}
.cover{page:cover;break-after:page;height:297mm;box-sizing:border-box;padding:27mm 24mm 20mm;display:flex;flex-direction:column;background:#111a2b;color:#fff}
.cover .eyebrow{font-size:11pt;color:#a3b1cb;letter-spacing:3px}
.cover .rule{height:2px;width:38mm;background:#72a5f2;margin:18mm 0 35mm}
.cover h1{margin:0 0 12mm;color:white}.cover h1 em{font-style:normal;color:#b7d4ff}
.cover .subtitle{font-size:14pt;color:#d7e1ef;max-width:140mm;line-height:1.9}
.cover .edition{margin-top:auto;border-top:1px solid #40506a;padding-top:8mm;color:#c0c9db;font-size:10pt}
.intro,.contents{break-after:page}.intro h2,.contents h2{font-size:23pt}
.contents ol{padding-left:0;list-style:none;columns:2;column-gap:11mm}
.contents li{font-size:8.2pt;padding:3px 0;break-inside:avoid}
.contents a::after{content:"  " target-counter(attr(href),page);color:#77879c}
.contents .segment{font-weight:750;margin:8mm 0 2mm;color:#0d2f51}
.chapter{break-before:page}.overline{font-size:8pt;letter-spacing:1.45px;color:#4e78a8;margin:0 0 4mm}
.outcome{font-size:11pt;line-height:1.8;border-left:3px solid #2465b4;padding:3mm 4mm;background:#eff5fd}
.scenario,.deliverable{background:#f7f9fc;border:1px solid #dfe7f1;border-radius:3mm;padding:4mm 5mm;margin:5mm 0;break-inside:avoid}
.scenario b,.deliverable b{font-size:9pt;color:#164f8c}
.scenario p,.deliverable p{margin:2mm 0 0}
ol.steps{list-style:none;padding:0}
.steps li{border-top:1px solid #e5e9ef;padding:4mm 0 3.6mm;break-inside:avoid}
.steps .action{font-weight:650;color:#172a41;margin:0 0 1.5mm}
.steps .action strong{color:#2a6bad;margin-right:3mm}
.steps .proof,.steps .fallback{font-size:9.2pt;margin:1mm 0;color:#42516a}
.steps .fallback{color:#64748b}
.sources{padding-left:5mm;font-size:8.8pt}
.sources li{margin-bottom:2mm;overflow-wrap:anywhere}
.sources span{display:block;color:#6f7c90;font-size:8pt}
.routes-intro{break-before:page}
.route{break-inside:avoid;margin-bottom:8mm;padding-bottom:5mm;border-bottom:1px solid #dae3ee}
.route ol{padding-left:7mm}.route li{margin:2mm 0}
.route li span{display:block;color:#667085;font-size:9pt}
.contact{background:#eef4fd;border:1px solid #cfdef0;padding:6mm;border-radius:2mm}
.small{color:#59677a;font-size:9pt}
"""
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>SEO 实战保姆级攻略 · AI 酋长 Andy</title><style>{css}</style></head><body>
<section class="cover"><div class="eyebrow">STAR AWAKENING / PRACTICAL KNOWLEDGE SERIES</div>
<div class="rule"></div><h1>SEO<br><em>实战保姆级攻略</em></h1>
<p class="subtitle">41 章实操课程 · 13 套 SOP · 6 条 7 天路线<br>
从真实需求、可抓取页面到可核验的咨询与转化链路。</p>
<div class="edition">AI 酋长 Andy · 2026-11-15 版<br>免费开源 · 不承诺搜索排名、询盘数量或收入结果<br>微信：AIPMAndy</div></section>
<section class="intro"><div class="overline">READ THIS FIRST</div><h2>用事实替代流量幻觉</h2>
<p>本手册由 <b>data/chapters.json</b>、<b>data/sops.json</b>、<b>data/routes.json</b> 与
<b>data/sources.json</b> 自动生成。每项练习请保存日期、原始证据与结论边界。</p>
<p>全部“示例”均为<strong>教学模拟</strong>，不得当作真实客户业绩。官方来源的“核验日期”取自源数据，
不代表重新核实了今天的网页；平台规则可能变化，请以链接中的官方页面为准。</p>
<div class="contact"><b>作者与公开联系渠道</b><p>AI 酋长 Andy · 微信 <b>AIPMAndy</b><br>
个人官网：{a('https://metaver.vip/','https://metaver.vip/')}<br>
公司官网：{a('https://www.a6no1.cn/','https://www.a6no1.cn/')}<br>
咨询服务：{a('https://metaver.vip/services','https://metaver.vip/services')}<br>
开源仓库：{a('https://github.com/AIPMAndy/seo-handbook','github.com/AIPMAndy/seo-handbook')}<br>
在线工具：{a(SITE+'tools.html','SEO 诊断与可编辑工具')}</p></div>
<p class="small">PDF 是离线阅读手册；需要输入、计算和导出的工具请到在线网站。
阅读免费教程无需加微信。</p></section>
<section class="contents"><div class="overline">CONTENTS</div><h2>完整目录</h2>
<div class="segment">第一部分 · 41 章实操课程</div><ol>{''.join(toc)}</ol>
<div class="segment">第二部分 · 13 套 SOP</div><ol>{''.join(sop_toc)}</ol>
<div class="segment">第三部分 · 7 天路线</div><p>6 种起点与每日应保留的凭证。</p></section>
{''.join(body)}{''.join(sop_body)}
<section class="routes-intro"><div class="overline">PART III / EXECUTION ROUTES</div>
<h2>选择你的 7 天路线</h2><p>无需从第一页开始读。根据业务与搜索数据状况，挑一条合适的路线。</p></section>
{''.join(routes_body)}
<section class="contact"><h3>继续实操</h3><p>在线教程：{a(SITE,SITE)}<br>
咨询服务：{a('https://metaver.vip/services','https://metaver.vip/services')}<br>
公司官网：{a('https://www.a6no1.cn/','https://www.a6no1.cn/')} · 微信：AIPMAndy</p>
<p class="small">请保留变更记录、原始材料、失败复盘与证据链接。</p></section></body></html>'''
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',default='pdf/seo-handbook-guide.pdf')
    args=p.parse_args()
    out=Path(args.output)
    if not out.is_absolute():out=ROOT/out
    out.parent.mkdir(parents=True,exist_ok=True)
    HTML(string=make_html(),base_url=ROOT.as_uri()).write_pdf(out)
    print(f'Built searchable PDF: {out} ({out.stat().st_size} bytes)')
if __name__=='__main__':main()
