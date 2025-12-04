# 🚀 GitHub自动生成exe文件 - 操作步骤

## ✅ 第一步: 创建GitHub仓库

### 1. 访问GitHub
打开浏览器,访问: https://github.com/new

### 2. 填写仓库信息
```
Repository name: stock-query-tool
(或者其他你喜欢的名字)

Description: 股票平均价格查询工具
(可选)

☐ Public  ← 选择这个(免费)
☑ Private ← 或选这个(如果不想公开)

❌ 不要勾选 "Initialize this repository with a README"
❌ 不要勾选 "Add .gitignore"
❌ 不要勾选 "Choose a license"
```

### 3. 点击绿色按钮
点击 "Create repository"

---

## ✅ 第二步: 推送代码到GitHub

创建完仓库后,GitHub会显示一个页面,找到 "…or push an existing repository from the command line" 部分。

### 复制你的仓库地址:
格式类似: `https://github.com/你的用户名/stock-query-tool.git`

### 在Mac终端执行以下命令:

```bash
# 1. 添加远程仓库(替换成你的仓库地址!)
git remote add origin https://github.com/你的用户名/stock-query-tool.git

# 2. 推送代码
git branch -M main
git push -u origin main
```

**注意**: 
- 第一次推送可能需要输入GitHub用户名和密码
- 如果提示需要Personal Access Token,按照GitHub提示操作

---

## ✅ 第三步: 等待自动构建

### 1. 查看构建进度
推送成功后:
1. 访问你的GitHub仓库页面
2. 点击顶部的 "Actions" 标签
3. 会看到一个工作流正在运行: "构建Windows可执行文件"
4. 显示黄色圆圈 🟡 表示正在构建
5. 显示绿色勾号 ✅ 表示构建成功

### 2. 等待时间
- 预计需要 5-10分钟
- 可以点进去查看实时日志

---

## ✅ 第四步: 下载exe文件

### 构建成功后:

1. 在Actions页面,点击那个成功的工作流(绿色✅的那个)
2. 页面向下滚动,找到 "Artifacts" 部分
3. 点击下载 "Windows可执行文件"
4. 会下载一个zip文件

### 解压得到:
```
Windows可执行文件/
├── 股票查询工具.exe           ← 图形界面版(推荐)
└── 股票查询工具_命令行.exe    ← 命令行版
```

---

## ✅ 第五步: 发给领导

### 直接发送:
把 `股票查询工具.exe` 通过:
- 微信
- 邮件  
- 钉钉
- U盘

发给领导即可!

### 领导使用方法:
**双击运行,无需安装任何东西!**

---

## 📋 完整命令清单 (复制粘贴执行)

```bash
# 在Mac终端执行(已经在正确目录)

# 1. 添加远程仓库(⚠️ 替换成你的实际地址!)
git remote add origin https://github.com/你的用户名/stock-query-tool.git

# 2. 推送代码
git branch -M main
git push -u origin main
```

---

## ❓ 常见问题

### Q1: 没有GitHub账号?
**A**: 访问 https://github.com/signup 注册(免费,2分钟)

### Q2: 推送时要求输入密码?
**A**: 
- 如果有双重认证,需要使用Personal Access Token
- 访问: https://github.com/settings/tokens
- 点击 "Generate new token (classic)"
- 勾选 "repo" 权限
- 生成后复制token,作为密码使用

### Q3: 构建失败怎么办?
**A**: 
- 点进失败的工作流查看错误日志
- 通常是依赖库问题,检查requirements.txt
- 可以修改后重新推送

### Q4: 想重新构建?
**A**: 
- 在Actions页面,点击 "Run workflow" 按钮
- 或者修改任意文件后重新push

### Q5: exe文件太大?
**A**: 
- PyInstaller打包的exe通常50-100MB
- 这是正常的,包含了Python运行环境
- 如果觉得太大,可以用方案1(Python脚本)

---

## 🎯 下一步操作

### 现在就执行:

1. **打开浏览器** → https://github.com/new
2. **创建仓库** → 按上面步骤填写
3. **复制仓库地址** → 类似 `https://github.com/xxx/stock-query-tool.git`
4. **回到终端执行**:

```bash
# 替换成你的仓库地址!
git remote add origin https://github.com/你的用户名/stock-query-tool.git
git push -u origin main
```

5. **访问GitHub Actions** → 等待构建完成
6. **下载exe** → 发给领导!

---

## 💡 提示

如果不想折腾GitHub,也可以:
- 使用之前准备的 `股票查询工具_部署包.zip`
- 发给领导,让他运行 `Windows一键安装.bat`
- 虽然需要Python,但有自动安装脚本很简单

**但生成exe是最佳体验!领导无需安装任何东西!** 🏆

---

准备好了吗? 开始创建GitHub仓库吧! 🚀
