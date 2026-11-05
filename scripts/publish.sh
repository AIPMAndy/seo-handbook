#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
repo="AIPMAndy/seo-handbook"
command -v git >/dev/null || { echo '请先安装 Git'; exit 2; }
command -v gh >/dev/null || { echo '请安装 GitHub CLI 并运行 gh auth login，或改用 GitHub Desktop'; exit 2; }
gh auth status >/dev/null || { echo '请先 gh auth login'; exit 2; }
gh repo view "$repo" >/dev/null || { echo "仓库 $repo 尚不存在；先访问 https://github.com/new 创建 Public 空仓库"; exit 2; }
python3 scripts/build.py
python3 scripts/site_audit.py _site
python3 -m unittest discover -s tests -v
if [ ! -d .git ]; then git init -b main; fi
if ! git remote get-url origin >/dev/null 2>&1; then git remote add origin "https://github.com/$repo.git"; fi
current="$(git remote get-url origin)"
case "$current" in *github.com/AIPMAndy/seo-handbook* ) ;; *) echo "origin 不符合预期：$current"; exit 2;; esac
git add -A
git commit -m 'Publish SEO handbook with audited lessons and Pages' || echo '没有需要提交的改动'
git branch -M main
git push -u origin main
echo '源码已推送。下一步：Settings → Pages → Source → GitHub Actions；随后实测网站。'
