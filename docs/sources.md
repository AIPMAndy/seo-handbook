# SEO 官方来源台账（2026-11-05 核对）

**原则**：来自 Google/Bing 的规则优先引用官方说明；可用性以实际网页为准。第三方经验、编辑建议、模拟计算与官方承诺严格区分。每次重大更新要更新 `data/sources.json` 的 `checked` 字段和这里的变更说明。

| 主题 | 原始官方链接 | 本教程采用的边界 |
|---|---|---|
| SEO 入门 | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | 没有确保第一名的技巧；先让用户与搜索引擎理解内容 |
| Search Console | https://developers.google.com/search/docs/monitor-debug/search-console-start | 用于检查搜索展示、点击、抓取和索引；不等于转化后台 |
| 以人为本的内容 | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | 原创性、经验、证据和完成用户任务优先 |
| 垃圾政策 | https://developers.google.com/search/docs/essentials/spam-policies | 禁止堆词、操纵性买链、滥用规模化内容等 |
| Sitemap | https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview | 可帮助发现，不保证索引；列出正式规范 URL |
| Canonical | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | canonical 是较强信号，不是强制命令；不要用 robots 处理重复 |
| Robots | https://developers.google.com/search/docs/crawling-indexing/robots/intro | robots.txt 主要控制抓取，不等于 noindex |
| 结构化数据 | https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data | 标记与可见正文一致；通过验证不保证富结果 |
| 核心网页指标 | https://developers.google.com/search/docs/appearance/core-web-vitals | LCP 2.5s、INP 200ms、CLS 0.1 是常见良好阈值 |
| 多语言站 | https://developers.google.com/search/docs/specialty/international/localized-versions | 互相指向的 hreflang、独立完整的当地内容 |
| AI 搜索（2026） | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | Google AI 搜索依然依赖基础 SEO；无需特殊专属 schema/llms.txt |
| Bing 提交 | https://www.bing.com/webmasters/help/?topicid=62f2860b | Bing 推荐 IndexNow；通知更新不代表完成收录 |
| 百度普通收录 | https://ziyuan.baidu.com/linksubmit | 提交可缩短发现时间，但无法保证收录 |
| 百度官方指南 | https://ziyuan.baidu.com/doc | 站点验证、抓取诊断、索引与搜索数据入口 |

## 需持续复核的风险点

1. 各 CMS 的 UI 和网站发布入口会改变，因此章节给出平台无关的验证方法，同时要求用户以所用平台官方说明为准。
2. Search Console 页面命名及指标展示可能变更，按最新官方页面/当前账号实际 UI 调整截图。
3. Google/Bing 收录与排名属于搜索引擎决策；本项目不使用“保证 7 天收录”“保证排名”等结论。
4. JavaScript 可渲染 ≠ 一定会被索引；优先保证正文 HTML 可用，但也不声称 JS 一律不能做 SEO。
5. IndexNow 有支持列表，不等于 Google URL 提交通道。
6. 此表是**2026-11-05 核对的参考文档集合**，不代表会自动随政策更新；以每次维护 PR 的最新核验为准。

## V2 新增：2026 年 Google / Bing AI 搜索可测量数据

- [Google 2026-06-03 发布的生成式 AI 搜索报告](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)：官方称 2026-08-31 已全球推出。
- [GSC 生成式 AI 搜索表现帮助](https://support.google.com/webmasters/answer/16984139?hl=en)：按曝光、页面、地区/设备、日期查看；展示不足时可能看不到报告。
- [Google 网站对生成式 AI 搜索的展示控制](https://blog.google/products-and-platforms/products/search/new-controls-website-owners/)：发布说明，最终以当前 GSC 后台为准。
- [Bing AI Performance 帮助](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c)：记录支持范围内的引用而非 Google AI 曝光。
- [Search Console 搜索效果报表](https://support.google.com/webmasters/answer/7576553?hl=en)：明确平均排名、点击、展示、不同维度汇总和导出限制。

对应 [详细可照做版：Google AI Search 2026](google-ai-search-2026.md)。
