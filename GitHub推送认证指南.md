# 🔐 GitHub推送认证指南

## 问题: 权限被拒绝

你遇到了认证问题,有两个简单的解决方案:

---

## ✅ 方案1: 使用GitHub Desktop (最简单!推荐)

### 1. 下载GitHub Desktop
访问: https://desktop.github.com/
下载并安装 GitHub Desktop

### 2. 登录你的GitHub账号
打开GitHub Desktop,点击左上角 "File" → "Options" → "Accounts" → 登录

### 3. 添加本地仓库
1. 点击 "File" → "Add Local Repository"
2. 选择文件夹: `/Users/liliwen/Projects/快速获取股价`
3. GitHub Desktop会自动检测到这是一个Git仓库

### 4. 发布到GitHub
1. 点击顶部的 "Publish repository"
2. 确认仓库名为: `stock-query-tool`
3. 点击 "Publish repository"

**搞定!** 几分钟后就能在Actions看到自动构建了!

---

## ✅ 方案2: 使用Personal Access Token (命令行)

### 1. 创建Token
1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. Note: 填写 "股票查询工具"
4. Expiration: 选择 "No expiration" (永不过期)
5. 勾选权限: **repo** (勾选整个repo)
6. 点击底部绿色按钮 "Generate token"
7. **⚠️ 重要**: 复制生成的token (只显示一次!)

### 2. 使用Token推送

```bash
# 在终端执行(替换YOUR_TOKEN为你的实际token)
git remote set-url origin https://YOUR_TOKEN@github.com/452766147/stock-query-tool.git

# 推送
git push -u origin main
```

---

## ✅ 方案3: 使用VS Code (如果你用VS Code)

### 1. 在VS Code中打开项目
```bash
code /Users/liliwen/Projects/快速获取股价
```

### 2. 使用Source Control
1. 点击左侧的 "Source Control" 图标
2. 点击 "..." 菜单
3. 选择 "Push to..." → "origin"
4. 会弹出GitHub登录窗口,完成认证
5. 推送成功!

---

## 🎯 我的推荐

### 最简单: 方案1 - GitHub Desktop
- ✅ 图形界面,无需命令行
- ✅ 自动处理认证
- ✅ 点几下鼠标就完成

### 最快: 方案2 - Personal Access Token  
- ✅ 命令行一行搞定
- ✅ 适合技术人员

---

## 📋 临时方案: 手动上传 (1分钟完成!)

如果上面都太麻烦,可以直接在GitHub网页上传:

### 步骤:
1. 访问: https://github.com/452766147/stock-query-tool
2. 点击 "uploading an existing file"
3. 把项目文件夹拖进去
4. 点击 "Commit changes"
5. 自动触发Actions构建!

**重要文件必须包括:**
- `股票查询工具_图形界面版.py`
- `股票查询工具_命令行版.py`
- `requirements.txt`
- `.github/workflows/build.yml`

---

## 🚀 推荐操作

### 现在立即执行 (选一个):

**最简单 → 方案1: 下载GitHub Desktop**
1. https://desktop.github.com/
2. 登录后添加本地仓库
3. 点击发布

**最快 → 方案2: 创建Token**
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. 勾选repo权限
4. 复制token
5. 执行命令(替换YOUR_TOKEN):
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/452766147/stock-query-tool.git
git push -u origin main
```

---

选哪个? 我帮你执行! 😊
