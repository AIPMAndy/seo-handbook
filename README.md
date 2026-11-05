# SEO Handbook V2｜从 0 到搜索增长与真实获客（2026）

> 免费开源、可离线阅读、可用 GitHub Pages 部署的 SEO 实战课程。**不是只讲排名：从客户需求，到真实页面，再到抓取、索引、搜索点击、有效咨询和订单。**

![SEO 保姆级教程网站预览](assets/site-preview.png)

**作者：AI酋长 Andy** ｜ [个人网站](https://metaver.vip/) ｜ [开源主页](https://github.com/AIPMAndy)

- 预定 GitHub 仓库：`https://github.com/AIPMAndy/seo-handbook`
- 预定 GitHub Pages：`https://aipmandy.github.io/seo-handbook/`
- **发布状态**：本项目源码与本地构建可独立运行；上面两个地址只有在真正创建仓库、推送并完成 Pages 部署后才可访问。不要把预定地址当作已上线。

## 一眼看懂项目

| 部分 | 已实现内容 | 验收方式 |
|---|---|---|
| 课程 | **41 章、164 条课程动作**，每条都有操作、完成标准、卡住怎么办 | 每章独立 HTML，且可直接访问 |
| 行动 | **30 天逐日计划**，每一天关联具体章节、凭证 | `plan.html` 勾选与持久化 |
| SEO 可发现性 | **62 个独立静态 HTML**、各页 title/description/H1/canonical/JSON-LD、sitemap | `python3 scripts/site_audit.py _site` |
| 工具箱 | 选题优先级、收入情景模拟、搜索摘要预览、本地进度导出/导入 | `tools.html` 手工交互 |
| 路线选择 | 6 类起点，42 个逐日任务，有完成凭证、对应章节与 30/90 天目标 | `routes.html` |
| SOP | **13 套深度操作指引，65 个实操步骤**，含失败回退 | `sops.html` 和 `sops/*.html` |
| 交互诊断 | 5 问定位流量阶段、推荐路线、导出 Markdown 清单 | `diagnose.html` |
| GSC 实操分析 | 浏览器本地 CSV 解析、手工审查任务导出；两期数据 CLI 对比 | `opportunities.html`、`scripts/gsc_compare.py` |
| 长期执行 | 13 周约 90 天操作、验收与停/改/扩标准 | `plan-90.html` |
| 模板 | 需求表、关键词地图、内容 Brief、周报、技术审计、迁移映射、实验与沟通模版 | `templates/` |
| 真实与假设 | 官方资料、模拟案例（明确标注）、证据边界 | `docs/sources.md`、`examples/` |
| 质量与自动发布 | Python 构建、源码校验、链接/元数据审计、GitHub Actions + Pages | CI 执行与 Pages 实际访问 |
| 对抗式审核 | 新手、SEO 工程师、内容编辑、客户、开发者五视角；阻断与修复记录 | `docs/red-team.md` |

## 立即开始｜运行网站不需要 Node

### 方式 A：直接看离线网站

1. 下载本项目 ZIP 并解压。
2. 打开 `_site/index.html`，从第一章或 30 天计划开始。若浏览器限制 `file://` 的本地保存功能，请改用下方的本地静态服务器，确保进度正常保存。
3. 勾选执行进度，工具箱可导出本地记录。

### 方式 B：本地运行并修改源码

```bash
python3 scripts/build.py          # 生成 _site/ 静态文件
python3 scripts/site_audit.py _site
python3 -m unittest discover -s tests -v
node tests/check_client.js         # 可选：若安装 Node 22，额外验证浏览器端核心算法
python3 scripts/verify_release.py    # 检验下载包文件未缺失或变化
python3 -m http.server 8080 -d _site
# 浏览器访问 http://localhost:8080
```

**建站、Python 测试与 CLI 均无第三方 Python 包依赖**，Python 3.10+ 即可；Node 只用于补充的 JavaScript 算法测试，运行网站无需安装。课程内容以 `data/chapters.json`、`data/routes.json`、`data/sops.json`、`data/sources.json` 为**唯一内容源**；修改后运行 build。不要运行旧版 V1 的 `seed_content.py`（V2 已移除该脚本，避免覆盖更新内容）。

## 不同人直接从适合的路线开始

- **完全新手**：先用 [`diagnose.html`](_site/diagnose.html)，选择“没有网站”，执行 7 天路线。
- **新站没收录**：使用 [`SOP：页面未被收录`](_site/sops/not-indexed.html)，不要只反复提交 URL。
- **已有数据的站点**：将实际 GSC CSV 拖进 [`机会分析`](_site/opportunities.html)，再运行 `python3 scripts/gsc_compare.py templates/gsc-before.csv templates/gsc-after.csv --output gsc-diff.csv` 练习同口径比较。
- **企业咨询服务**：先看 [`B2B 七天路线`](_site/routes.html#route-b2b) 与 [`案例：AI 专业服务 90 天路线`](examples/04-andy-seo-business.md)。
- **本地与跨境业务**：分别从 `routes.html` 的 local/global-ai 路线进入。

## 面向三种读者的入口

**完全新手**：从第 01 章开始，先定义目标、获取站点权限、验证 Search Console，再做关键词研究。没有真实网站也可以先用 `_site/` 项目练习，但**练习站的数据不等于你业务网站的流量**。

**已有网站的运营者**：从第 04、06、16、27 章开始。优先利用现有 GSC 页面与查询数据，改有展示且有业务价值的页面。

**企业与 B2B 顾问**：第 01、05、10、13、37、40 章优先。目标指标是**合格线索与实际订单**，不是总浏览量。

## 完整课程分组

1. 起步：网站、目标、搜索过程、GSC/Bing/事件追踪。
2. 调研：用户原话、免费选词、SERP 意图、竞争差距、聚类、商业优先级。
3. 建站：信息架构、Title/Meta、内容 Brief、原创正文、内链、旧文更新。
4. 技术：HTTP、Sitemap、Canonical、Robots/noindex、JSON-LD、媒体、迁移、Core Web Vitals、JavaScript、移动端。
5. 数据：Search Console、转化事件、Bing/IndexNow、CTR、实验、流量下降排查。
6. 增长：真实引用、本地/国际/电商/B2B、AI 搜索、内容规模化、转化、90 天复盘。
7. 中国大陆百度实操补充：站点验证、普通收录、流量与索引诊断，见 [docs/baidu-seo.md](docs/baidu-seo.md)。

每章正文都是**直接写在静态 HTML 里**，不是客户端 JavaScript 才能出现的文本。课程页有独立的自指 canonical，便于用这个仓库本身演示正确的基础 SEO。

## 2026 Google AI Search 最新测量

Google 生成式 AI 搜索表现报告已于 **2026-08-31 面向全球站点推出**，可查看 AI Overviews / AI Mode 的展示、页面、国家、设备等维度；如果展示量不足，报表可能不出现。Bing AI Performance 报告衡量其支持 AI 体验中的引用。**Google AI 展示量不等于 Bing AI 引用量，也不等于成交。** 详见 [逐步照做文档](docs/google-ai-search-2026.md)、[官方来源](docs/sources.md)。

## 数据与观点边界

- Google 不保证网页收录，更不保证排名第一；sitemap、结构化数据、提交 URL 也不是收录承诺。
- Google 的 AI Overviews / AI Mode 无需额外专属 schema 或 llms.txt 作为出现的前提；基础 SEO 仍然有效。详情见 [2026 年 Google 官方指南](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)。
- `robots.txt` 控制抓取，不等于阻止索引；公开但不想索引的页面应按情况使用可被抓取识别的 `noindex`。
- **GitHub Pages 项目子路径不能控制 `github.io` 域名根目录的 robots.txt**。本项目不会伪造可生效的子目录 robots 规则。
- `examples/` 中的商业案例、工具箱默认数字都是**教学假设**，不是对外宣称真实客户成果。
- 本项目 MIT 只覆盖原创源码和文字。链接的 Google/Bing 官方网页不因本仓库协议取得转授权。

## 目录结构

```text
seo-handbook/
├── README.md, START-HERE.md, PUBLISH.md, LICENSE
├── CHANGELOG.md, CONTRIBUTING.md, RELEASE_NOTES.md
├── data/                         # 课程、路线、SOP 与官方来源（唯一内容源）
│   ├── chapters.json             # 41 章 × 4 操作
│   ├── routes.json               # 6 条 7 天路径
│   ├── sops.json                 # 13 套详细 SOP
│   └── sources.json              # 来源及核验记录
├── assets/                       # 样式、浏览器交互、图标及网站图片
├── scripts/
│   ├── build.py                  # 生成独立 HTML（无需 Node）
│   ├── site_audit.py             # title、canonical、JSON-LD、站内链接、sitemap 审计
│   ├── gsc_opportunities.py      # GSC 数据观察排序
│   ├── gsc_compare.py            # 同口径两期 CSV 比较
│   ├── check_url.py              # 单页技术 SEO 检查
│   ├── verify_release.py         # 发布文件 SHA256 完整性校验
│   └── publish.sh                # Git 推送辅助脚本
├── templates/                    # 可复制模板与演示数据
├── examples/                     # 假设案例与演示方案，明确标记
├── docs/                         # 官方指南、排障、研究、竞争对标、审计记录
├── tests/                        # Python + Node 核心算法与故障注入测试
├── .github/workflows/            # GitHub Actions 自动审核、Pages 发布
├── MANIFEST.sha256               # 发布快照 SHA256
└── _site/                        # 62 个独立 HTML 的成品静态网站
```

## GitHub Pages 自动部署

阅读 [PUBLISH.md](PUBLISH.md)。简要步骤：先创建同名 Public 空仓库，再在本地执行 `bash scripts/publish.sh`（或按 GitHub 页面手动上传）并将 Settings → Pages → Source 设为 **GitHub Actions**。随后检查 `verify`、`deploy` 和公开网页是否真实可访问。**只看到 Actions 成功还不算最终上线验收**。

## 维护与贡献

- **修事实**：提交带官方证据、核验日期和具体 URL 的 Issue/PR。
- **修教程**：每个关键动作必须写清“怎么做 → 凭证 → 卡住怎么办”。
- **修代码**：附测试或复现步骤；发布前运行构建与审计。
- 变更记录与更新频率参见 [docs/maintenance.md](docs/maintenance.md)。

## License

原创内容与代码采用 [MIT License](LICENSE) 开源。欢迎复用、提交改进或为真实操作增加有来源的案例。

## 工具验收快照（2026-11-05）

- 62 个公开静态页面，`scripts/site_audit.py` 检查结果：0 errors、0 warnings。
- Python 24 项测试通过；Node 10 组核心客户端算法输入测试通过（本地）。
- **浏览器端 V2 人机交互与手机视觉验收尚未完成**：当前执行环境阻止自动浏览器访问本地构建，需实际部署后人工验收。不能把 JS 单元测试当作移动端实测。
- GitHub 远程仓库与 Pages 尚未创建/部署，不将预定 URL 作为已在线服务。
- ZIP 包含 SHA-256 文件清单；修改源代码或重新 build 后，请先重新测试再运行 `python3 scripts/verify_release.py --write` 更新发布清单。
- 竞品功能对照、尚未完成的真实业务验证详见 [docs/benchmark.md](docs/benchmark.md)。
