#!/bin/bash
# 推送代码到GitHub

echo "🚀 准备推送代码到GitHub..."
echo ""
echo "⚠️  需要GitHub认证"
echo ""
echo "请选择推送方式:"
echo "1. 使用GitHub CLI (推荐)"
echo "2. 使用Personal Access Token"
echo ""

# 检查是否安装了GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ 检测到GitHub CLI"
    echo "正在推送..."
    gh auth login
    git push origin main
else
    echo "方法1: 安装GitHub CLI (最简单)"
    echo "  brew install gh"
    echo "  gh auth login"
    echo "  git push origin main"
    echo ""
    echo "方法2: 使用Token推送"
    echo "  1. 访问: https://github.com/settings/tokens"
    echo "  2. Generate new token (classic)"
    echo "  3. 勾选 repo 权限"
    echo "  4. 复制token"
    echo "  5. 执行命令:"
    echo "     git remote set-url origin https://YOUR_TOKEN@github.com/452766147/stock-query-tool.git"
    echo "     git push origin main"
fi
