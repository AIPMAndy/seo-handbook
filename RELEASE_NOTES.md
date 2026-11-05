# SEO Handbook V2 · Release Notes (2026-11-05)

**用途**：让零基础站长、B2B 顾问、本地服务与海外工具团队，直接完成一次“需求→可用页面→可抓取→可测量→有效询盘→下一轮”的 SEO 实验。

## 交付清单

- 41 个核心课程章节、164 个步骤、30 天逐日计划。
- 6 条个性化 7 天路线、13 套深度 SOP（65 个操作节点）、13 周复盘。
- 62 个独立静态页面，源码含正文、规范网址、JSON-LD、XML sitemap。
- 关键词评分、利润假设、标题摘要预览、本地进度保存；新增 SEO 诊断器与 GSC CSV 浏览器本地分析。
- Python GSC 同口径两期比较器及静态网页审计。
- 2026 Google/Bing AI 可见度官方指标操作说明与竞品对标记录。

## 本地校验结果

```bash
python3 scripts/build.py
python3 scripts/site_audit.py _site
python3 -m unittest discover -s tests -v
node tests/check_client.js
```

结果：62 HTML pages; 0 errors, 0 warnings; Python 23 tests pass; Node 10 client-logic scenarios pass.

**尚未完成**：GitHub 远程提交、Pages 部署后的 HTTP 200 与人工手机交互测试，以及真实 GSC 索引/获客数据验证。

## 2026-11-05 封包完整性复审

- 课程 JSON 成为唯一内容源，删除 V1 过时的 seed 和升级中间脚本。
- 两期 GSC 对比对空白指标严格拒绝，不把缺失数值当 0。
- 新增 SHA256 校验脚本和发布清单；Python 回归测试共 24 项。
