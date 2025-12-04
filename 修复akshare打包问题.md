# 🔧 修复akshare打包问题

## 问题原因
akshare库包含数据文件(如calendar.json),打包时需要特别处理。

---

## ✅ 解决方案: 更新build.yml配置

### 在GitHub上编辑 `.github/workflows/build.yml` 文件

将打包命令部分改为:

```yaml
    - name: 获取akshare数据文件路径
      run: |
        python -c "import akshare; import os; print(os.path.dirname(akshare.__file__))" > akshare_path.txt
        type akshare_path.txt
    
    - name: 打包图形界面版本
      run: |
        pyinstaller --onefile --windowed --name "股票查询工具" ^
          --hidden-import akshare ^
          --hidden-import pandas ^
          --hidden-import requests ^
          --hidden-import py_mini_racer ^
          --collect-all akshare ^
          --collect-data akshare ^
          股票查询工具_图形界面版.py
    
    - name: 打包命令行版本
      run: |
        pyinstaller --onefile --console --name "股票查询工具_命令行" ^
          --hidden-import akshare ^
          --hidden-import pandas ^
          --hidden-import requests ^
          --hidden-import py_mini_racer ^
          --collect-all akshare ^
          --collect-data akshare ^
          股票查询工具_命令行版.py
```

---

## 📋 完整的修复后的build.yml文件

复制以下内容,替换GitHub上的build.yml:

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
      uses: actions/checkout@v4
    
    - name: 设置Python环境
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: 打包图形界面版本
      run: |
        pyinstaller --onefile --windowed --name "股票查询工具" ^
          --hidden-import akshare ^
          --hidden-import pandas ^
          --hidden-import requests ^
          --hidden-import py_mini_racer ^
          --collect-all akshare ^
          --collect-data akshare ^
          股票查询工具_图形界面版.py
    
    - name: 打包命令行版本
      run: |
        pyinstaller --onefile --console --name "股票查询工具_命令行" ^
          --hidden-import akshare ^
          --hidden-import pandas ^
          --hidden-import requests ^
          --hidden-import py_mini_racer ^
          --collect-all akshare ^
          --collect-data akshare ^
          股票查询工具_命令行版.py
    
    - name: 上传可执行文件
      uses: actions/upload-artifact@v4
      with:
        name: Windows可执行文件
        path: |
          dist/股票查询工具.exe
          dist/股票查询工具_命令行.exe
        retention-days: 30
```

---

## 🎯 关键修改点

1. **`--collect-all akshare`** - 收集akshare所有文件
2. **`--collect-data akshare`** - 收集akshare数据文件
3. **添加更多hidden-import** - 确保依赖库都打包进去

---

## 📝 操作步骤

1. 访问: https://github.com/452766147/stock-query-tool/blob/main/.github/workflows/build.yml
2. 点击右上角的 ✏️ 编辑按钮
3. 全选内容,删除
4. 粘贴上面的完整配置
5. 点击 "Commit changes"
6. 等待重新构建(约5-10分钟)
7. 下载新的exe文件测试

---

## ⚠️ 注意

- 打包后的exe文件会比之前大(可能100-150MB)
- 这是正常的,因为包含了akshare的所有数据文件
- 但运行时不会再有找不到文件的错误

---

现在就去GitHub修改build.yml文件吧! 🚀
