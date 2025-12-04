; 股票查询工具 NSIS 安装脚本 - 修复版
; 正确处理 PyInstaller --onedir 输出结构

;--------------------------------
; 包含现代UI
!include "MUI2.nsh"

;--------------------------------
; 常量定义
!define PRODUCT_NAME "股票查询工具"
!define PRODUCT_VERSION "2.1"
!define PRODUCT_PUBLISHER "Stock Query Tool"
!define PRODUCT_WEB_SITE "https://github.com/452766147/stock-query-tool"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"

;--------------------------------
; 安装包基本设置
Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "股票查询工具安装包_v${PRODUCT_VERSION}.exe"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
InstallDirRegKey HKLM "Software\${PRODUCT_NAME}" "Install_Dir"
RequestExecutionLevel admin

;--------------------------------
; 界面设置
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\nsis.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\win.bmp"

;--------------------------------
; 安装页面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

; 完成页面 - 提供启动选项
!define MUI_FINISHPAGE_RUN "$INSTDIR\股票查询工具.exe"
!define MUI_FINISHPAGE_RUN_TEXT "立即运行股票查询工具"
!define MUI_FINISHPAGE_SHOWREADME ""
!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
!define MUI_FINISHPAGE_SHOWREADME_TEXT "创建桌面快捷方式"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION CreateDesktopShortcut
!insertmacro MUI_PAGE_FINISH

;--------------------------------
; 卸载页面
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

;--------------------------------
; 语言设置
!insertmacro MUI_LANGUAGE "SimpChinese"

;--------------------------------
; 版本信息
VIProductVersion "2.1.0.0"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "Comments" "专业的股票价格查询与分析工具"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "LegalCopyright" "Copyright (C) 2024"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileDescription" "${PRODUCT_NAME} 安装程序"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileVersion" "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "ProductVersion" "${PRODUCT_VERSION}"

;--------------------------------
; 安装部分
Section "主程序" SEC01
  SectionIn RO  ; 必选
  
  ; 设置输出路径到安装目录
  SetOutPath "$INSTDIR"
  
  ; 【关键修复】复制图形界面版本
  ; PyInstaller --onedir 输出结构: dist/股票查询工具/
  ;   ├─ 股票查询工具.exe
  ;   └─ _internal/
  
  ; 方法1: 使用 /r 递归复制整个目录内容(不包括目录本身)
  File "dist\股票查询工具\股票查询工具.exe"
  File /r "dist\股票查询工具\_internal"
  
  ; 复制命令行版本到子目录
  SetOutPath "$INSTDIR\命令行版"
  File "dist\股票查询工具_命令行\股票查询工具_命令行.exe"
  File /r "dist\股票查询工具_命令行\_internal"
  
  ; 写入安装路径到注册表
  WriteRegStr HKLM "Software\${PRODUCT_NAME}" "Install_Dir" "$INSTDIR"
  
  ; 写入卸载信息
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\股票查询工具.exe"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegDWORD HKLM "${PRODUCT_UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${PRODUCT_UNINST_KEY}" "NoRepair" 1
  
  ; 创建卸载程序
  SetOutPath "$INSTDIR"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; 创建开始菜单快捷方式
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\股票查询工具.lnk" "$INSTDIR\股票查询工具.exe"
  CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\股票查询工具_命令行.lnk" "$INSTDIR\命令行版\股票查询工具_命令行.exe"
  CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\卸载.lnk" "$INSTDIR\Uninstall.exe"
  
  ; 显示完成消息
  DetailPrint "安装完成！"
  DetailPrint "程序已安装到: $INSTDIR"
  
SectionEnd

;--------------------------------
; 创建桌面快捷方式函数
Function CreateDesktopShortcut
  CreateShortcut "$DESKTOP\股票查询工具.lnk" "$INSTDIR\股票查询工具.exe" "" "$INSTDIR\股票查询工具.exe" 0
FunctionEnd

;--------------------------------
; 卸载部分
Section "Uninstall"
  
  ; 删除注册表键
  DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "Software\${PRODUCT_NAME}"
  
  ; 删除快捷方式
  Delete "$DESKTOP\股票查询工具.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\*.*"
  RMDir "$SMPROGRAMS\${PRODUCT_NAME}"
  
  ; 删除程序文件
  RMDir /r "$INSTDIR\_internal"
  RMDir /r "$INSTDIR\命令行版"
  Delete "$INSTDIR\股票查询工具.exe"
  Delete "$INSTDIR\Uninstall.exe"
  
  ; 删除安装目录
  RMDir "$INSTDIR"
  
  ; 显示完成消息
  MessageBox MB_OK "股票查询工具已成功卸载！"
  
SectionEnd
