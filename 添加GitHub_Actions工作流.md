# 📝 GitHub Actions工作流配置文件

## 🎯 需要添加的内容

### 文件路径:
`.github/workflows/build.yml`

### 完整内容 (复制下面所有内容):

```yaml
name: 构建Windows可执行文件

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    
    steps:
    - name: 检出代码
      uses: actions/checkout@v3
    
    - name: 设置Python环境
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: 打包图形界面版本
      run: |
        pyinstaller --onefile --windowed --name "股票查询工具" --hidden-import akshare --hidden-import pandas 股票查询工具_图形界面版.py
    
    - name: 打包命令行版本
      run: |
        pyinstaller --onefile --console --name "股票查询工具_命令行" --hidden-import akshare --hidden-import pandas 股票查询工具_命令行版.py
    
    - name: 上传可执行文件
      uses: actions/upload-artifact@v3
      with:
        name: Windows可执行文件
        path: |
          dist/股票查询工具.exe
          dist/股票查询工具_命令行.exe
        retention-days: 30
```

---

## 📋 操作步骤

### 方法1: 网页创建 (推荐)

1. **访问仓库首页**
   https://github.com/452766147/stock-query-tool

2. **创建新文件**
   - 点击 "Add file" → "Create new file"

3. **输入文件路径**
   在文件名输入框输入: `.github/workflows/build.yml`
   (注意: 输入时会自动创建文件夹)

4. **粘贴内容**
   复制上面的YAML内容,粘贴到编辑器

5. **提交**
   - 点击底部绿色按钮 "Commit changes"
   - 点击确认

6. **查看构建**
   - 点击 "Actions" 标签
   - 会自动开始构建!

---

### 方法2: 上传文件

如果上面的链接打开了创建页面:

1. 确认文件名是: `.github/workflows/build.yml`
2. 粘贴上面的YAML配置
3. 点击 "Commit new file"

---

## ⏱️ 构建时间

提交后:
- ✅ 立即触发构建
- ⏰ 等待 5-10分钟
- 📥 下载exe文件

---

## 🔍 检查文件是否正确

构建需要这4个文件:
- ✅ `股票查询工具_图形界面版.py`
- ✅ `股票查询工具_命令行版.py`
- ✅ `requirements.txt`
- ❓ `.github/workflows/build.yml` (现在要添加的)

---

现在就去创建这个文件吧! 创建后告诉我,我帮你查看构建进度! 🚀
