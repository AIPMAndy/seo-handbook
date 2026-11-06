#!/usr/bin/env python3
"""Dependency-free, SEO-first static site builder for GitHub Pages."""
from __future__ import annotations
import html, json, os, shutil
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'_site'
if OUT.exists():
    shutil.rmtree(OUT)  # Rebuild cleanly: deleted/renamed chapters must not leave indexable stale URLs.
BASE = os.environ.get('SITE_URL','https://aipmandy.github.io/seo-handbook/').strip().rstrip('/')+'/'
parsed=urlparse(BASE)
if parsed.scheme!='https' or not parsed.netloc or parsed.query or parsed.fragment:
    raise SystemExit('SITE_URL must be a public https URL without query/fragment')
CHAPTERS=json.loads((ROOT/'data/chapters.json').read_text(encoding='utf-8'))
SOURCES={x['id']:x for x in json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))}
SOPS=json.loads((ROOT/'data/sops.json').read_text(encoding='utf-8'))
ROUTES=json.loads((ROOT/'data/routes.json').read_text(encoding='utf-8'))
STAGES=['起步','调研','建站','技术','数据','增长']
H=lambda x:html.escape(str(x),quote=True)

def full_url(path):return BASE if path=='index.html' else BASE+path

def a(path,label):return f'<a href="{H(path)}">{H(label)}</a>'

def head(title,desc,path,kind='WebPage',extra=None):
    url=full_url(path)
    data={'@context':'https://schema.org','@type':kind,'name':title,'url':url,'inLanguage':'zh-CN','description':desc}
    if kind=='Article':
        data.update({'headline':title,'author':{'@type':'Person','name':'AI酋长 Andy','url':'https://metaver.vip/'},'mainEntityOfPage':url})
    if extra:data.update(extra)
    js=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    rel='../' if path.startswith(('lessons/','sops/')) else ''
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#f5f6f8"><title>{H(title)}｜SEO保姆级教程</title><meta name="description" content="{H(desc)}"><link rel="canonical" href="{H(url)}"><meta property="og:type" content="website"><meta property="og:image" content="{H(full_url("assets/social-preview.png"))}"><meta property="og:title" content="{H(title)}"><meta property="og:description" content="{H(desc)}"><meta property="og:url" content="{H(url)}"><meta property="og:locale" content="zh_CN"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="{rel}assets/favicon.svg"><link rel="stylesheet" href="{rel}assets/style.css"><script type="application/ld+json">{js}</script><script src="{rel}assets/app.js" defer></script></head><body><div class="progressline" id="readProgress" aria-hidden="true"></div><header class="nav"><nav class="nav-in" aria-label="主导航"><a class="brand" href="{rel}index.html" aria-label="SEO保姆级教程首页"><span class="brandmark">S</span><span>SEO Handbook <span style="font-weight:450;color:#6b7585">/ by Andy</span></span></a><div class="links"><a class="optional" href="{rel}routes.html">选择路线</a><a class="nav-compact" href="{rel}plan.html">30天实操</a><a class="nav-compact" href="{rel}tools.html">免费工具</a><a class="optional" href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">Andy 官网 ↗</a><a class="navcta nav-github" href="https://github.com/AIPMAndy/seo-handbook" rel="noopener noreferrer">GitHub ↗</a><a class="navcta nav-contact" href="{rel}contact.html">加微信</a></div></nav></header>'''

def author_banner(rel=''):
    """Consistent, unobtrusive author attribution and contact on every page."""
    return f'''<aside class="author-strip" aria-label="作者与咨询服务"><div class="wrap author-strip-inner"><div class="author-copy"><span class="eyebrow">AI 酋长 Andy · 官方联系渠道</span><h2>这套教程免费。需要落地帮助，可以找我。</h2><p>从 SEO 到 AI 产品化、内容获客与商业转化，把方法放进真实项目里验证。</p></div><div class="author-actions"><a class="btn" href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">访问个人官网 ↗</a><a class="btn secondary" href="https://metaver.vip/services" target="_blank" rel="noopener noreferrer">了解咨询服务 ↗</a><div class="wechat-line"><span>个人微信：<strong>AIPMAndy</strong></span><button class="copy-wechat" type="button" data-copy-wechat data-wechat="AIPMAndy">复制微信号</button><span class="copy-feedback" role="status" aria-live="polite"></span></div><a class="contact-secondary" href="{rel}contact.html">查看详细联系方式与添加步骤 →</a></div></div></aside>'''

def footer(rel=''):
    return author_banner(rel)+f'''<footer class="footer"><div class="footer-in"><div><b>SEO Handbook · by AI酋长 Andy</b><div>开源、免费、按证据更新。付费咨询为可选服务，和免费课程相互独立。</div></div><div>{a(rel+'index.html','首页')} &nbsp;·&nbsp; {a(rel+'plan.html','30天计划')} &nbsp;·&nbsp; {a(rel+'tools.html','工具箱')} &nbsp;·&nbsp; {a(rel+'routes.html','路线')} &nbsp;·&nbsp; {a(rel+'diagnose.html','诊断')} &nbsp;·&nbsp; {a(rel+'contact.html','联系 Andy')} &nbsp;·&nbsp; <a href="https://github.com/AIPMAndy/seo-handbook" rel="noopener noreferrer">源码</a> &nbsp;·&nbsp; <a href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">个人官网</a></div></div></footer></body></html>'''

def write(path,s):
    file=OUT/path;file.parent.mkdir(parents=True,exist_ok=True);file.write_text(s,encoding='utf-8')

def lesson_file(chap):return f"lessons/{chap['slug']}.html"

# Home page: all lessons linked in normal HTML, even when JS is disabled.
cards=''.join(f'''<a class="tile" data-course data-stage="{H(c['stage'])}" data-search="{H(c['title']+' '+c['outcome']+' '+c['stage'])}" href="{H(lesson_file(c))}"><span class="n">CHAPTER {H(c['id'])} &nbsp; · &nbsp; {H(c['stage'])}</span><h3>{H(c['title'])}</h3><p>{H(c['outcome'])}</p><div class="foot"><span>{len(c['steps'])} 个动作 · {c['minutes']} 分钟</span><span style="color:#2269f2">开始学习 ↗</span></div></a>''' for c in CHAPTERS)
filterbtn=''.join(f'<button type="button" class="filter {"active" if s=="全部" else ""}" data-filter="{H(s)}">{H(s)}</button>' for s in ['全部']+STAGES)
count=sum(len(x['steps']) for x in CHAPTERS)
home=head('从零做到可验证增长','41 章、164 项具体动作、30 天计划。从关键词、技术 SEO 到 Search Console 和商业转化，每步有验收与卡点处理。','index.html',kind='WebSite')+f'''<main><section class="hero"><div class="wrap"><div class="kicker">OPEN SOURCE · PRACTICAL SEO · 2026</div><h1>不是学会 SEO 术语。<br><span class="grad">是亲手做出搜索增长。</span></h1><p class="lead">给零基础用户的完整操作手册：找到真实需求，做出可抓取的网站，发布有证据的内容，读取搜索数据，再把合适的访问变成咨询或订单。每一步都告诉你怎么做、如何验收、卡住怎么办。</p><div class="hero-actions"><a class="btn" href="lessons/{CHAPTERS[0]['slug']}.html">从第一章开始 <span aria-hidden="true">↗</span></a><a class="btn secondary" href="routes.html">先选适合我的路线</a></div><div class="stats"><div class="stat"><strong>{len(CHAPTERS)}</strong><span>系统课程</span></div><div class="stat"><strong>{count}</strong><span>可执行动作</span></div><div class="stat"><strong>30</strong><span>逐日任务</span></div><div class="stat"><strong>0 元</strong><span>开源课程费用</span></div></div><div class="progress-panel"><div><h3>你的执行进度</h3><p>只存当前浏览器，可在工具箱导出备份。刷新不丢。</p></div><div style="flex:1;max-width:280px"><div id="currentProgress" data-total="{count+30}" style="text-align:right;font-size:13px;margin-bottom:8px">0 / {count+30} 项</div><div class="bar"><div id="progressBar"></div></div></div></div></div></section>
<section class="section section-white"><div class="wrap"><div class="heading"><div><div class="eyebrow">THE METHOD</div><h2>先让人找到，再让人相信。</h2><p>SEO 是“需求 → 页面 → 抓取 → 展示 → 点击 → 行动”的完整系统。排名只是其中一个环节。</p></div></div><div class="trio"><div><span class="tag">01 · 发现需求</span><h3>找对问题</h3><p>从真实用户语言和搜索结果出发，先验证值得做什么。</p></div><div><span class="tag">02 · 交付答案</span><h3>写出真正有用的页面</h3><p>代码、正文、证据和内部链接都能让人直接使用。</p></div><div><span class="tag">03 · 验证商业</span><h3>用数据决定下一步</h3><p>看查询、有效咨询和订单，不被漂亮的流量报表误导。</p></div></div></div></section>
<section class="section section-white"><div class="wrap"><div class="heading"><div><div class="eyebrow">YOUR PATH FIRST</div><h2>6 种起点，不必从头学完。</h2><p>新站查收录，老站查数据，B2B 查线索，本地门店查实际订单。用路线选择器找到现在该做的第一件事。</p></div><a class="btn" href="routes.html">选我的 7 天路线</a></div><div class="trio"><div><span class="tag">诊断</span><h3>先确定问题在哪一层</h3><p>5 个问题定位抓取、内容与商业转化卡点。<a href="diagnose.html">打开诊断 →</a></p></div><div><span class="tag">数据</span><h3>直接导入 GSC 数据</h3><p>本地分析 CSV，找出需要人工核查的页面。<a href="opportunities.html">打开分析 →</a></p></div><div><span class="tag">执行</span><h3>13 套可核验 SOP</h3><p>每套写清输入、操作、证据和失败回退。<a href="sops.html">查看 SOP →</a></p></div></div></div></section><section class="section home-author" aria-labelledby="meet-andy"><div class="wrap"><div class="home-author-card"><div class="home-author-content"><div class="eyebrow">FROM THE AUTHOR · AI 酋长 Andy</div><h2 id="meet-andy">SEO 学会了，怎么用它带来客户？</h2><p>我是 AI 酋长 Andy，持续开源 AI 与增长实操教程。课程免费开放；如果你正在做 AI 产品、专业服务或企业获客，希望有人一起诊断并推进落地，也可以直接联系我。</p><div class="hero-actions"><a class="btn" href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">看我的个人官网 ↗</a><a class="btn secondary" href="contact.html">添加个人微信 · AIPMAndy</a></div></div><div class="home-author-note"><span>直接联系</span><strong>AIPMAndy</strong><span>微信搜索这个 ID</span><button type="button" class="copy-wechat" data-copy-wechat data-wechat="AIPMAndy">复制微信号</button><span class="copy-feedback" role="status" aria-live="polite"></span><a href="https://metaver.vip/services" target="_blank" rel="noopener noreferrer">咨询服务介绍 ↗</a></div></div></div></section><section class="section" id="courses"><div class="wrap"><div class="heading"><div><div class="eyebrow">FULL CURRICULUM</div><h2>完整课程，照着执行</h2><p>按阶段学习或搜索当前卡点。每章至少 4 个动作，附验收标准和失败处理。</p></div><span id="filterCount" class="small">{len(CHAPTERS)} 章</span></div><div class="searchbar"><label class="sr-only" for="courseSearch">搜索课程标题或内容</label><input id="courseSearch" placeholder="搜索：关键词、收录、canonical、流量……" type="search" autocomplete="off"></div><div class="filters" role="group" aria-label="课程阶段">{filterbtn}</div><div class="grid">{cards}</div></div></section><section class="section section-white"><div class="wrap"><div class="heading"><div><div class="eyebrow">ZERO TO ONE</div><h2>走完 30 天，留下可检查的作品。</h2><p>不是每天读一篇文章，而是每天产出关键词表、Brief、独立页面、站点地图、数据报告等具体文件。</p></div><a class="btn" href="plan.html">打开逐日执行清单</a></div></section></main>'''+footer()
write('index.html',home)

# Lesson pages: semantically complete and independent static HTML documents.
for i,ch in enumerate(CHAPTERS):
    rel='../';path=lesson_file(ch)
    sidebar=''.join(f'<a class="side-link {"current" if c["id"]==ch["id"] else ""}" href="{H(c["slug"])}.html">{c["id"]} · {H(c["title"][:18])}</a>' for c in CHAPTERS)
    steps=''.join(f'''<section class="step" id="step-{j}"><div class="step-head"><span class="step-num">{j}</span><div><h3>{H(s['do'])}</h3><p class="step-meta"><strong>验收：</strong>{H(s['done'])}</p><p class="step-meta"><strong>卡住怎么办：</strong>{H(s['stuck'])}</p><label class="checklabel"><input type="checkbox" data-task="lesson-{H(ch['id'])}-{j}"> 我已经完成，并保留了验收证据</label></div></div></section>''' for j,s in enumerate(ch['steps'],1))
    links=''.join(f'<li><a target="_blank" rel="noopener noreferrer" href="{H(SOURCES[k]["url"])}">{H(SOURCES[k]["title"])} ↗</a> <span class="small">（官方来源）</span></li>' for k in ch['sources'])
    prev=a(CHAPTERS[i-1]['slug']+'.html','← 上一章') if i else '<span></span>'
    nextlink=a(CHAPTERS[i+1]['slug']+'.html','下一章 →') if i<len(CHAPTERS)-1 else a('../plan.html','进入30天实操 →')
    desc=ch['outcome']
    htmlpage=head(ch['title'],desc,path,'Article')+f'''<main class="wrap reading"><aside class="sidebar" aria-label="课程目录"><div class="side-title">全部章节 · {len(CHAPTERS)}</div>{sidebar}</aside><article class="article"><nav class="breadcrumb"><a href="../index.html">首页</a> / {H(ch['stage'])} / 第 {H(ch['id'])} 章</nav><div style="margin-top:28px"><span class="tag">{H(ch['stage'])}</span> &nbsp; <span class="small">约 {ch['minutes']} 分钟 · {len(ch['steps'])} 个验收动作</span></div><h1>{H(ch['title'])}</h1><p class="intro">{H(ch['outcome'])}</p><div class="example"><strong>实际场景</strong><div>{H(ch['example'])}</div></div><div class="notice">操作方式：照着完成一个动作 → 保留结果 → 勾选完成。这里给出的工具和政策以实际官方界面为准；模拟情景不代表真实客户结果。</div><h2>逐步照做</h2>{steps}<h2>本章交付物</h2><p>{H(ch['deliverable'])}</p><h2>核验资料</h2><ul class="ref-list">{links}</ul><aside class="lesson-author-cta" aria-label="与作者交流"><span class="eyebrow">免费教程 · 作者答疑与咨询</span><h2>把这一章用到你自己的项目。</h2><p>个人网站和微信都在这里。课程可以独立免费学习；如需针对具体业务的诊断与陪跑，再选择咨询服务。</p><div class="lesson-author-actions"><a href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">Andy 个人官网 ↗</a><a href="../contact.html">联系 Andy · 微信 AIPMAndy →</a></div></aside><div class="prevnext">{prev}{nextlink}</div></article></main>'''+footer(rel)
    write(path,htmlpage)

# An authored 30-day route: task + proof + chapter mapping.
daily=[
('定义服务与 SEO 目标','写 1 页目标人群、核心服务、页面与转化动作','目标表 4 项完整',1),
('拿到网站权限','核对域名、DNS、CMS、统计权限，能访问公开首页','权限表 + 网站 URL',3),
('验证 GSC 和 Bing','完成站点所有权验证，记录账号与属性','两张验证状态截图',4),
('保存数据基线','导出 GSC 当前索引和效果情况，新站填 0','带日期基线表',2),
('收集客户原话','访谈或整理 10 条可匿名的真实需求','需求原话 10 行',5),
('扩展搜索短语','把真实问题拓展成候选关键词并标注来源','关键词池至少 20 个',6),
('判断用户意图','手查搜索结果，为候选关键词分配页面类型','前 10 个词的 SERP 表',7),
('竞争对手内容拆解','选 3 个 SERP 页面找证据差距','竞争差距表',8),
('做关键词地图','按搜索意图聚类，标注现有/新建 URL','至少 5 个主题簇/页面',9),
('优先级取舍','挑 5 个能真正交付的选题并排期','有负责人的 5 题计划',10),
('画网站结构','确定栏目、主要成交页、知识页内链关系','站点层级树',11),
('写第一个服务页 Brief','把受众、目标、证据、CTA 填完整','Brief 1 份',13),
('发布服务页','写清对象、交付内容、真实证据与咨询入口','URL + 手机截图',14),
('发布第 1 篇回答型文章','从用户高频真实问题切入，写完整操作','文章 URL + 原始证据',14),
('发布第 2 篇文章','回答不同搜索意图，避免同题重复','文章 URL + 差异说明',14),
('写唯一的标题摘要','给这三页设置准确 title、H1、description','页面源代码记录',12),
('补网站内链','从首页/文章/服务页建立真实文字入口','链接路径图',15),
('检查 HTTP 与可访问性','抽查核心 URL 状态码、HTTPS、手机正文','状态码列表',17),
('生成与提交 Sitemap','确认正式 URL、XML 可用并提交 GSC','sitemap URL + 提交截图',18),
('核对 Canonical','排除旧 URL 和参数导致的重复问题','页面自指 canonical 检查表',19),
('排查 robots/noindex','确认线上正式页面未误阻断','检查截图/日志',20),
('添加合适的结构化数据','只添加与页面可见事实一致的类型','验证结果链接/截图',21),
('优化图片与移动体验','压缩图、alt、预留尺寸、修手机端布局','优化前后截图',22),
('检查真实网页性能','用 PSI 检查 LCP/INP/CLS，先修最大瓶颈','性能基线与一个修复记录',24),
('确保 HTML 正文可抓取','查看源代码，核对重要正文与真实 href','源码检查记录',25),
('GSC 第一次复盘','下载查询/页面数据，并明确无数据的原因','查询+页面表',27),
('验证自然搜索转化事件','做 3 次成功+1 次失败表单测试','事件与后台对照',28),
('修复一页高价值内容','基于真实用户反馈或 GSC 查询改善页面','修改前后对比',16),
('做商业漏斗检查','统计展示、点击、有效咨询、成交的可得数据','漏斗表；缺项标未知',40),
('完成第一轮红队审计','查 10 大误区、修最严重 3 条，制定下一轮周期','审计记录 + 60/90 天计划',41),
]
assert len(daily)==30
schedule=''.join(f'''<section class="day" data-day><div class="daytop"><span class="eyebrow">DAY {j:02d}</span><label class="checklabel" style="margin:0"><input class="daycheck" data-task="day-{j:02d}" type="checkbox"> 完成</label></div><h3>{H(d[0])}</h3><p>{H(d[1])}</p><div class="proof"><b>验收凭证：</b>{H(d[2])}<div style="margin-top:9px"><a href="lessons/{CHAPTERS[d[3]-1]['slug']}.html" style="color:#2565cb">对应课程 第 {d[3]} 章 ↗</a></div></div></section>''' for j,d in enumerate(daily,1))
plan=head('30 天逐日 SEO 实操计划','每天一个具体任务，提供验收凭证、对应课程和浏览器本地勾选；零基础从第一天照做。','plan.html')+f'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">30-DAY EXECUTION</div><h1>30 天，不再停留在“学习”。</h1><p>每天完成一件可检查的事。新站数据可能为零，目标是完整的执行与可验证的基线，而不是承诺 30 天排名。</p><div class="notice">本地进度只保存在当前设备浏览器。可以前往<a href="tools.html" style="color:#1d62d0">工具箱导出/导入进度</a>。</div></div></section><section class="section" style="padding-top:15px"><div class="wrap"><div class="schedule">{schedule}</div></div></section></main>'''+footer()
write('plan.html',plan)

# Tools, three fully working client-side utilities + progress export/import.
tools=head('SEO 免费实操工具箱','关键词优先级评分、自然搜索商业情景模拟、搜索结果标题预览和 30 天进度导出。数据只在浏览器本地运算。','tools.html')+'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">PRACTICAL TOOLKIT</div><h1>4 个零成本工具。<br>现在就能用。</h1><p>没有账号和服务器要求。所有估算都是透明的情景模型，不会伪装成真实搜索量或真实收入。</p></div></section><section class="section" style="padding-top:10px"><div class="wrap"><div class="toolsgrid">
<div class="toolcard"><span class="tag">01 · 决策工具</span><h2>关键词选题优先级</h2><p>相关性 × 意图 × 独特证据 ÷ 制作成本。适合你自己的选题排序。</p><div class="fieldrow"><div class="field"><label for="relevance">业务相关性（0–5）</label><input id="relevance" type="number" min="0" max="5" value="4"></div><div class="field"><label for="intent">意图强度（0–5）</label><input id="intent" type="number" min="0" max="5" value="4"></div><div class="field"><label for="proof">能提供的独特证据（0–5）</label><input id="proof" type="number" min="0" max="5" value="3"></div><div class="field"><label for="cost">制作成本（1–5）</label><input id="cost" type="number" min="1" max="5" value="2"></div></div><div class="result" id="keywordResult" aria-live="polite">请输入参数。</div></div>
<div class="toolcard"><span class="tag">02 · 商业模型</span><h2>自然搜索到收入模拟</h2><p>先看到假设如何传导到咨询与订单。不是流量或收入预测。</p><div class="fieldrow"><div class="field"><label for="impressions">每月展示量（假设）</label><input id="impressions" type="number" min="0" value="10000"></div><div class="field"><label for="ctr">自然点击率 %</label><input id="ctr" type="number" min="0" max="100" value="3" step="0.1"></div><div class="field"><label for="leadRate">点击→有效线索率 %</label><input id="leadRate" type="number" min="0" max="100" value="2" step="0.1"></div><div class="field"><label for="closeRate">有效线索→成交率 %</label><input id="closeRate" type="number" min="0" max="100" value="10" step="0.1"></div><div class="field"><label for="price">客单收入（元）</label><input id="price" type="number" min="0" value="4500"></div><div class="field"><label for="deliveryCost">单笔履约成本（元）</label><input id="deliveryCost" type="number" min="0" value="1500"></div></div><div class="result" id="roiResult" aria-live="polite">请输入参数。</div></div>
<div class="toolcard"><span class="tag">03 · 编辑辅助</span><h2>搜索结果文字预览</h2><p>只是文字排版示意：Google 会自动选择或改写标题和摘要。</p><div class="field"><label for="snTitle">Title</label><input id="snTitle" value="SEO教程：从0到上线、收录、获客｜可执行指南"></div><div class="field" style="margin-top:12px"><label for="snDesc">Meta description</label><input id="snDesc" value="41章 SEO 保姆级教程，包含关键词调研、技术检查、Search Console、30天计划和可复制模板。"></div><div class="preview"><div class="url">https://example.com/seo-guide/</div><div class="serptitle" id="serpTitle">SEO教程</div><div class="serpdesc" id="serpDesc">SEO 实操指南</div></div><div class="small" id="snInfo" style="margin-top:8px"></div></div>
<div class="toolcard"><span class="tag">04 · 自主管理</span><h2>学习进度备份</h2><p>课程勾选与 30 天任务只存你当前浏览器。无需注册，也不会传给本项目服务器。</p><div style="display:flex;gap:12px;flex-wrap:wrap;margin:25px 0"><button class="btn" id="exportProgress" type="button">导出 JSON 进度</button><label class="btn secondary" style="cursor:pointer">导入进度 <input type="file" id="importProgress" accept=".json,application/json" hidden></label></div><p class="small">注：不同浏览器、无痕模式、清理站点数据都会影响本地记录。保存一份 JSON 即可迁移。</p><div class="callout"><b>真正的网站 SEO 审计</b><p>仓库还包含 <code>python3 scripts/site_audit.py _site</code>：检查标题、元数据、规范网址、结构化数据和本地链接。运行方式见 README。</p></div></div></div></div></section></main>'''+footer()
write('tools.html',tools)

# V2: public static, crawlable, role-oriented playbooks and on-device diagnostic tools.
source_list=lambda ids: '<ul class="ref-list">'+''.join(f'<li><a href="{H(SOURCES[k]["url"])}" target="_blank" rel="noopener noreferrer">{H(SOURCES[k]["title"])} ↗</a></li>' for k in ids)+'</ul>'
route_cards=''
for route in ROUTES:
    day_items=''.join(f'<li><strong>第 {j} 天 · {H(day[0])}</strong><p>{H(day[1])}</p><a href="lessons/{CHAPTERS[route["chapters"][j-1]-1]["slug"]}.html">查看对应课程 {route["chapters"][j-1]:02d} →</a></li>' for j,day in enumerate(route['daily'],1))
    route_cards+=f'''<section class="routecard" data-route="{H(route['id'])}" id="route-{H(route['id'])}"><div class="tag">7 天任务</div><h2>{H(route['title'])}</h2><p>{H(route['for'])}</p><p><strong>第 7 天验收：</strong>{H(route['goal'])}</p><ol class="routelist">{day_items}</ol><div class="milestones"><p><b>30 天目标：</b>{H(route['days30'])}</p><p><b>90 天目标：</b>{H(route['days90'])}</p></div></section>'''
route_options=''.join(f'<option value="{H(r["id"])}">{H(r["title"])}</option>' for r in ROUTES)
routes_html=head('6 种起点的 SEO 路线图','从零建站、新站不收录、老站停滞、B2B 咨询、本地实体门店和多语言 AI 工具：每条路线给出 7 天任务、验证凭证及 30/90 天目标。','routes.html')+f'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">PERSONAL ROUTES</div><h1>SEO 的第一步，取决于你现在在哪。</h1><p>选择自己最接近的情况。每天都有一个实实在在的交付物。不是把所有章节学完才动手。</p><label for="routeSelect" class="selectlabel">我的起点</label><select id="routeSelect" class="bigselect"><option value="all">显示所有路线</option>{route_options}</select></div></section><section class="section"><div class="wrap route-grid">{route_cards}</div></section><section class="section section-white"><div class="wrap"><h2>不知道选哪条？</h2><p>先用<a href="diagnose.html">SEO 问题诊断器</a>回答 5 个问题，再按结果选择路线。完成后进入<a href="plan-90.html">90 天验证计划</a>。</p></div></section></main>'''+footer()
write('routes.html',routes_html)

sop_cards=''.join(f'''<a class="tile" href="sops/{H(sp["id"])}.html"><span class="tag">{len(sp['steps'])} 步 · SOP</span><h3>{H(sp['title'])}</h3><p>{H(sp['entry'])}</p><div class="foot"><span>交付证据</span><span>开始 →</span></div></a>''' for sp in SOPS)
sops_index=head('13 套 SEO 实战 SOP','可交付的 SEO 标准操作：收录排障、关键词地图、B2B、本地、国际、AI 搜索、改版、数据和转化周报。','sops.html')+f'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">FIELD PLAYBOOKS</div><h1>13 套能直接照做的 SOP。</h1><p>不是泛泛讲知识。每个 SOP 都给出适用情境、操作、留存证据和失败处理。真实案例与模拟任务分开。</p></div></section><section class="section"><div class="wrap"><div class="grid">{sop_cards}</div></div></section></main>'''+footer()
write('sops.html',sops_index)
for sp in SOPS:
    path=f'sops/{sp["id"]}.html'
    steps=''.join(f'''<section class="step"><h3>{j:02d} · {H(step['do'])}</h3><p class="step-meta"><b>完成凭证：</b>{H(step['proof'])}</p><p class="step-meta"><b>如果做不到：</b>{H(step['stuck'])}</p></section>''' for j,step in enumerate(sp['steps'],1))
    sop_html=head(sp['title'],sp['deliverable'],path,'Article')+f'''<main class="wrap reading"><aside class="sidebar"><div class="side-title">SOP 目录 · {len(SOPS)}</div>{''.join(f'<a class="side-link" href="{H(x["id"])}.html">{H(x["title"][:20])}</a>' for x in SOPS)}<a class="side-link" href="../sops.html">全部 SOP →</a></aside><article class="article"><nav class="breadcrumb"><a href="../index.html">首页</a> / <a href="../sops.html">SOP</a></nav><span class="tag">可检查的标准操作</span><h1>{H(sp['title'])}</h1><p class="intro">适用：{H(sp['entry'])}</p><div class="notice"><b>最后必须交付：</b>{H(sp['deliverable'])}</div><h2>操作、证据与失败处理</h2>{steps}<h2>官方依据</h2>{source_list(sp['sources'])}<p><a class="btn secondary" href="../sops.html">返回 SOP 列表</a></p></article></main>'''+footer('../')
    write(path,sop_html)

diag_decisions=[
 ('不能访问网站或没有站点','先做第 03 章和“还没有网站”路线','no-site'),
 ('访问报错或未被发现','从状态码、robots、canonical、站点地图、真实内链检查','new-site'),
 ('已索引却没有展示','核对查询需求、搜索意图、页面价值与目标语言','new-site'),
 ('有展示但没有自然点击','按查询/页面/地区拆数据，核查标题与 SERP 意图','existing-site'),
 ('有点击但没有有效咨询','先验证事件和咨询路径；区分访客与有效客户','b2b'),
 ('有咨询但没有成交','检查交付定位、价格信息与客户匹配，不要只加内容量','b2b')]
decision_table=''.join(f'<tr><td>{H(a)}</td><td>{H(b)}</td><td><a href="routes.html#route-{H(c)}">对应路线</a></td></tr>' for a,b,c in diag_decisions)
diagnose=head('5 个问题快速诊断 SEO 卡点','从网站权限、搜索结果阶段、数据、商业目标和服务类型判断下一步，输出可下载的行动方案。','diagnose.html')+f'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">SEO TROUBLESHOOTER</div><h1>先定位问题，再选择正确动作。</h1><p>只需填写当前能确认的状态。工具在浏览器本地计算，不连接网站或读取任何账号。</p></div></section><section class="section"><div class="wrap"><div class="toolcard diagnostic"><form id="diagnosisForm"><div class="formgrid"><div class="field"><label for="diagSite">1. 你现在的网站</label><select id="diagSite" required><option value="none">还没有网站</option><option value="yes">有可公开访问的网站</option><option value="broken">网站无法稳定访问</option></select></div><div class="field"><label for="diagSearch">2. 搜索数据处于哪一层</label><select id="diagSearch"><option value="unknown">不知道 / 没有 Search Console</option><option value="notindex">明确未收录关键页</option><option value="noimp">已收录，几乎没有展示</option><option value="imp">有展示，点击很少</option><option value="clicks">有自然搜索点击</option></select></div><div class="field"><label for="diagLeads">3. 是否有有效商业线索</label><select id="diagLeads"><option value="unknown">没有记录 / 未验证事件</option><option value="no">有点击，但无有效线索</option><option value="yes">有有效线索</option></select></div><div class="field"><label for="diagBusiness">4. 主要业务类型</label><select id="diagBusiness"><option value="b2b">B2B / 专业服务</option><option value="local">实体门店</option><option value="global">跨境 / AI 工具</option><option value="content">内容网站 / 个人项目</option></select></div><div class="field"><label for="diagHours">5. 每周可投入的小时数</label><input id="diagHours" type="number" min="1" max="80" value="5" required></div></div><button type="submit" class="btn">生成我的下一步</button></form><section id="diagOutput" class="result" aria-live="polite" tabindex="-1"><b>当前建议：</b>填完后点击“生成我的下一步”。</section><button type="button" class="btn secondary" id="downloadDiagnosis" disabled>下载 Markdown 行动清单</button></div></div></section><section class="section section-white"><div class="wrap"><h2>没有任何数据时怎么判断？</h2><p>使用以下固定规则；不依赖 AI 生成猜测。诊断只根据你提供的已知状态给出下一步，不能取代 GSC 实测。</p><div class="table-wrap"><table class="deci-table"><thead><tr><th>已确认的情况</th><th>优先动作</th><th>路线</th></tr></thead><tbody>{decision_table}</tbody></table></div></div></section></main>'''+footer()
write('diagnose.html',diagnose)

opportunities=head('免费 GSC CSV 机会分析','导入 Google Search Console 的查询或页面 CSV，本地计算观察优先级，区分指标与商业推断，并导出人工审查任务。','opportunities.html')+'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">GSC LAB · OFFLINE</div><h1>上传 CSV，不靠猜找下一步。</h1><p>从 Search Console 导出“查询”或“网页”报表 CSV。页面只在当前浏览器解析数据，不向任何服务器发送文件。</p></div></section><section class="section"><div class="wrap"><div class="toolcard"><h2>导入 Search Console 导出的 CSV</h2><p>支持常见中/英文字段，自动识别逗号分隔和 UTF-8 BOM；用于人工排查候选，不是流量预测。</p><div class="formgrid"><div class="field"><label for="gscFile">GSC 查询或页面 CSV（不超过 2 MB）</label><input id="gscFile" type="file" accept=".csv,text/csv"></div><div class="field"><label for="gscMin">最低展示次数</label><input id="gscMin" type="number" min="0" value="100"></div><div class="field"><label for="gscTop">最多展示行数</label><select id="gscTop"><option value="10">10</option><option value="20" selected>20</option><option value="50">50</option></select></div></div><button class="btn" id="gscRun" type="button">在本地分析</button> <button class="btn secondary" id="gscDownload" type="button" disabled>下载诊断任务 CSV</button><div id="gscStatus" role="status" class="notice" aria-live="polite">选择文件后开始。文件不会上传。</div><div class="table-wrap"><table id="gscTable" class="deci-table"><thead><tr><th>查询或页面</th><th>点击</th><th>展示</th><th>CTR</th><th>平均排名</th><th>观察分值*</th></tr></thead><tbody></tbody></table></div><p class="small">* 展示 × (1 − CTR) 是帮助安排人工检查顺序的启发式指标。它不是“丢失点击量”、搜索量估计、商业价值或涨量预测。不同排名、地区、品牌与 SERP 形态的 CTR 不应直接横比。</p></div><div class="notice"><strong>怎样读这个表：</strong>挑 3 行 → 打开对应查询/页面和 SERP → 写出用户意图与独特证据缺口 → 先做一个修复 → 14/28 天后同口径复盘。若 CSV 是“查询”报表，不要把这些查询当成独立页面。没有足够数据时从真实用户问题研究起步。</div></div></section></main>'''+footer()
write('opportunities.html',opportunities)

weeks=[
 ('目标和证据','定出一个业务闭环、搜索渠道基线、网站权限','目标表、权限记录、数据字典','若无法验证账号，就只读检查并请求授权'),
 ('真实需求与搜索意图','收集真实客户问题 20 条；做 10 条目标 SERP 观察','匿名问题库、搜索意图表','没有客户就做 3 个目标用户访谈'),
 ('关键词地图与服务架构','选择 5 个能证明独特价值的主题，规划页面类型','关键词→URL 地图、内部链接草图','已有相关页则升级而不是新建重复页'),
 ('上线第一批页面','发布至少 1 个服务/核心功能页与 1–2 个问题页','URL、原始证据、手机可用性测试','新页面有反复跳转、404 时先修技术'),
 ('技术审核与收录观察','查 HTTP、canonical、robots、sitemap、图片与 HTML','审计日志、GSC URL 检查截图','索引可能尚未发生；记录实际状态'),
 ('线索事件与体验','完成表单、预约、试用等关键行动的真实测试','成功/失败的端到端测试记录','没有后端证据不把按钮点击算成有效线索'),
 ('搜索报告首轮','按页面、查询、地区设备看数据，标出缺数据项','第一份 GSC 周报、候选页面名单','低量新站转去补内容和需求样本'),
 ('内容与证据升级','选高价值页面增加实测、流程、真实案例材料','修改前后对比、页面事实来源','不是增加字数就一定更好'),
 ('内部链接与真实引用','修复断链、加上下文内链，寻找合理的被引用机会','内链图、引用联系与成果记录','拒绝买链/机器量产外联'),
 ('对抗式质量测试','外部新手跟做、内容可信度、技术、转化四类审查','问题清单、阻断修复、复测记录','无外部用户时标明仅内部测试'),
 ('扩大有效主题','根据真实查询和需求决定扩写、合并、暂停哪个主题','投资组合表、已砍选题原因','低商业关联但高展示不自动加预算'),
 ('归因与投入决策','统计自然搜索、有效线索、订单与制作/维护成本','周报和测算表，未知项保留','不能直接从时间相关性推导 SEO 增收'),
 ('90 天复盘与下一轮','复核证据、决定继续做/改/停，确定下季 3 个优先事项','90 天复盘、90 天后资源计划','若无有效样本，保留假设和下一验证动作')]
weekhtml=''.join(f'''<section class="day"><div class="eyebrow">WEEK {j:02d}</div><h3>{H(w[0])}</h3><p>{H(w[1])}</p><p class="proof"><b>验收：</b>{H(w[2])}</p><p class="small"><b>没有进展：</b>{H(w[3])}</p></section>''' for j,w in enumerate(weeks,1))
plan90=head('SEO 90 天：从上线到商业验证','13 周分阶段执行：需求、上线、技术、线索、实验与经济性，每周有明确的交付物和失败处理。','plan-90.html')+f'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">13-WEEK OUTCOME PLAN</div><h1>90 天，围绕真实结果做 13 次验收。</h1><p>前 30 天做出能被访问、可测量的作品；中间 30 天发现问题；后 30 天围绕有效线索和订单做取舍。每周只选最有价值的 1–3 件事。</p><div class="hero-actions"><a href="routes.html" class="btn secondary">先选个人路线</a><a href="plan.html" class="btn secondary">30 天每日计划</a></div></div></section><section class="section"><div class="wrap"><div class="schedule">{weekhtml}</div><div class="notice"><b>停止继续投入的信号：</b>连续两个复盘周期没有可验证的目标客户需求，或者网站无真实交付能力，或者跟踪数据无法证实任何有效客户行为。优先修验证链路，而不是继续批量发文章。<br><b>扩大的信号：</b>有可复核的高质量需求、稳定的页面体验、可归因或明确标注不确定性的商机，且边际投入仍值得。</div></div></section></main>'''+footer()
write('plan-90.html',plan90)

# A standalone, indexable author/contact page. WeChat is a searchable ID, not an invented QR code.
contact=head('联系 AI 酋长 Andy｜个人微信与官网','AI 酋长 Andy 的个人官网 metaver.vip、咨询服务介绍和个人微信 AIPMAndy；教程免费、咨询可选。','contact.html',extra={'about':{'@type':'Person','name':'AI酋长 Andy','url':'https://metaver.vip/'}})+'''<main><section class="minihero"><div class="wrap"><div class="eyebrow">CONTACT THE AUTHOR</div><h1>联系 AI 酋长 Andy</h1><p>SEO、AI 产品和内容获客问题，可以从公开教程开始实践；需要面向具体项目的诊断，再通过下面的渠道联系。</p></div></section><section class="section"><div class="wrap"><div class="contact-grid"><article class="contact-card primary"><span class="eyebrow">01 · 个人微信</span><h2>微信搜索：<span class="contact-wechat">AIPMAndy</span></h2><p>打开微信 → 添加朋友 → 搜索 <strong>AIPMAndy</strong> → 发送你的业务问题和网站地址。</p><div class="contact-actions"><button type="button" class="btn" data-copy-wechat data-wechat="AIPMAndy">复制微信号</button><span class="copy-feedback" role="status" aria-live="polite"></span></div><p class="small">目前提供的是微信 ID 文字入口，不使用未经核验的二维码。</p></article><article class="contact-card"><span class="eyebrow">02 · 官方网站</span><h2>metaver.vip</h2><p>了解 Andy 的 AI 产品化、内容与增长项目、公开资料和服务信息。</p><div class="contact-actions"><a class="btn" href="https://metaver.vip/" target="_blank" rel="noopener noreferrer">访问个人官网 ↗</a><a class="btn secondary" href="https://metaver.vip/services" target="_blank" rel="noopener noreferrer">查看咨询服务 ↗</a></div></article></div><div class="notice contact-clarity"><strong>关于这套教程：</strong>SEO Handbook 的课程、工具和模板仍可免费使用。微信与个人官网是作者的公开联系渠道，不影响课程访问和功能使用。具体合作内容以实际沟通为准。</div><div class="contact-back"><a href="index.html">← 返回教程首页</a> <a href="routes.html">选择 7 天实操路线 →</a></div></div></section></main>'''+footer()
write('contact.html',contact)

# Generated artifacts are all deployable; GitHub Pages project paths are relative.
(OUT/'assets').mkdir(exist_ok=True)
for asset in (ROOT/'assets').iterdir():
    if asset.is_file():shutil.copy2(asset,OUT/'assets'/asset.name)
files=['index.html','contact.html','plan.html','plan-90.html','routes.html','sops.html','diagnose.html','opportunities.html','tools.html']+[lesson_file(x) for x in CHAPTERS]+[f'sops/{x["id"]}.html' for x in SOPS]
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{xml_escape(full_url(p))}</loc></url>\n' for p in files)+'</urlset>\n'
write('sitemap.xml',sitemap)
# NOTE: project GitHub Pages cannot own root /robots.txt on github.io. No misleading nested robots file.
write('.nojekyll','')
print(f'Built {len(files)} HTML pages, {len(CHAPTERS)} chapters, {len(SOPS)} SOPs, {len(ROUTES)} routes at {OUT} (base={BASE})')
