# 贡献指南：让新手真正照着做完

欢迎更正事实、补充可验证的案例、改进代码与课程。

## 问题报告（Issue）

请提供：**章节/链接、当前错误、你实际点击/输入了什么、你看到的结果、期望的完成状态、可公开截图或原始资料、核验日期**。不要上传账号 Token、客户合同、后台访问密钥或私人信息。

## 修复教程（PR）

1. 课程直接编辑 `data/chapters.json`，路线编辑 `data/routes.json`，SOP 编辑 `data/sops.json`，官方出处编辑 `data/sources.json`。这四份 JSON 是唯一内容源，不存在会覆盖内容的另一个 seed 脚本。
2. 每个教程步骤必须有 `do / done / stuck` 三项，其中 `done` 是能复核的完成凭证。
3. 涉及搜索引擎规则，要更新 `data/sources.json` 和 `docs/sources.md`，写明官方原始来源与核查日期。
4. 运行 `python3 scripts/build.py && python3 scripts/site_audit.py _site && python3 -m unittest discover -s tests -v && node tests/check_client.js`；发布 ZIP 时再执行 `python3 scripts/verify_release.py --write` 更新 SHA-256 清单。
5. 在 PR 中附变更前后对比与测试结论。若未实机测试，请明确写未完成，而非宣称通过。

## 可接受的新内容

新手的真实失败路径、不同 CMS 的操作界面与版本、可公开且有原始证据的案例、非操纵性的推广实践、政策更新、网站访问性修复。

## 不接受

虚构流量或收入、只改写别人教程的无价值批量内容、买卖传递排名信用的链接、自动批量查询 Google 搜索、秘密绕过平台规定的内容、上传真实客户敏感资料。

## V2 专项贡献方向

- **真实跟做记录**：选择 `data/routes.json` 其中一条路线，记录每天任务、证据、阻碍与复测；个人资料和客户隐私请自行去标识。
- **搜索规则更新**：优先给 Google/Bing/百度官方出处、发布日期、影响范围和代码/课程具体修改行。
- **SOP 质量**：不能只有概念；必须给可重复操作、完成证据及失败备选路径。
- **数据工具**：变更 CSV 解析时加 `tests/check_client.js` 输入用例；修改 Python 脚本时加 unittest。
- **商业结果**：不要把模拟案例写成真实客户成交，也不要把观察性流量变化写成已证明的收益提升。
