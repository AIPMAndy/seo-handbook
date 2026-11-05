# 将 SEO Handbook 真正开源到 GitHub（发布操作单）

> 正式仓库：`AIPMAndy/seo-handbook`。源码已发布到 `main`，GitHub Actions 的 `verify` 与 `deploy` 工作流通过；本文后续部署步骤保留为维护和重新发布指南。

## A. 创建空仓库（网页方式）

1. 登录 https://github.com/new ，选择 Owner `AIPMAndy`。
2. Repository name 填 `seo-handbook`，Description 可填 `从零到搜索流量与获客的 SEO 实战开源教程｜41章、164课程动作、13套SOP、6条路线、30/90天实操`。
3. Visibility 选 **Public**，**不要预先勾选** Add a README、.gitignore 或 License（本项目已包含）。
4. 点击 **Create repository**，确认页面显示 `AIPMAndy/seo-handbook`。

## B. 将源码一次性推送

将下载的 ZIP 解压后打开该目录。推荐本机已安装 Git、可以访问账号的环境：

```bash
cd seo-handbook
python3 scripts/build.py
python3 scripts/site_audit.py _site
python3 -m unittest discover -s tests -v
node tests/check_client.js
bash scripts/publish.sh
```

如未配置 Git 认证，请使用 GitHub Desktop，或登录 `gh auth login` 后重新执行。`scripts/publish.sh` **不会自动创建公开仓库**，会先检查它是否存在，避免误传到错误地址。

## C. 启用 GitHub Pages

1. 打开 `https://github.com/AIPMAndy/seo-handbook/settings/pages`。
2. 找到 Build and deployment → Source，选择 **GitHub Actions**。
3. 在仓库 Actions 页面观察 `verify` 和 `deploy`。若 deploy 因权限配置报错，检查仓库 Actions 权限和 Settings → Pages 的 Source。
4. 打开 `https://aipmandy.github.io/seo-handbook/`，再随机打开 3 个 `lessons/*.html` 页面与 `plan.html`、`tools.html`、`diagnose.html`、`routes.html`、`opportunities.html`、`sops/not-indexed.html`。

## D. 最终必须做的 10 项验收

- [ ] 首页、课程和工具页均返回 200；手机 390px 无明显横向溢出。
- [ ] 课程页面 HTML 源码能找到正文，而不是 JS 动态加载的空容器。
- [ ] 首页、两篇课程页 title、description、H1 不重复。
- [ ] 每页 canonical 指向当前实际 HTTPS 地址。
- [ ] `sitemap.xml` 能访问，条目与公开页面一致。
- [ ] 站点在手机浏览器能阅读，并且章节链接可点开。
- [ ] 30 天进度勾选刷新后保留、JSON 导入/导出可用。
- [ ] 选题评分器、收益假设模型、搜索结果预览都能正确响应输入。
- [ ] 六条路线按选择过滤；诊断表单能生成清单且可以下载。
- [ ] GSC 英文/中文 CSV 上传可计算，双引号和带逗号标签解析正常，错误文件有明确报错。
- [ ] 390px 手机宽度下测试新页面的横向滚动、操作按钮和表格；表格允许**局部**横向滚动，不允许整个页面横向溢出。
- [ ] GitHub Actions 的 CI 与 Pages deploy 均成功。
- [ ] GSC 验证完成或记录为待办；**不把“部署成功”说成“Google 已经收录”**。

**想部署到其他域名？** 使用 `SITE_URL=https://example.com/subpath/ python3 scripts/build.py`，并同步改 `.github/workflows/deploy.yml` 里的构建环境变量。若采用自定义域名根路径，设 `SITE_URL=https://example.com/` 并按 GitHub 官方文档配置 CNAME 与 DNS。更换域名后必须重新运行 sitemap/canonical 检查。
