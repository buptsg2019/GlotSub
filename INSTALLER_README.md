# GlotSub 安装程序构建指南

## 概述

本指南说明如何构建包含 Tesseract OCR 自动安装功能的 GlotSub 安装程序。

## 构建前准备

### 必需软件

1. **Python 3.7+**
   - 下载：https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **Chocolatey**（用于自动安装 Tesseract）
   - 下载：https://chocolatey.org/install
   - 或运行：`Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`

3. **Inno Setup 6+**（用于创建安装程序）
   - 下载：https://jrsoftware.org/isdl.php
   - 安装后将安装目录添加到系统 PATH（通常为 `C:\Program Files (x86)\Inno Setup 6`）

### 本地环境准备

1. **安装 Tesseract OCR**（本地构建时）
   ```powershell
   # 以管理员权限运行
   choco install tesseract -y --params="'/Language:chi_sim /Language:eng'"
   ```

   或者手动下载安装：
   - 下载：https://github.com/UB-Mannheim/tesseract/wiki
   - 安装时勾选中文语言包

## 构建步骤

### 方法1：使用自动化脚本（推荐）

1. **以管理员身份运行 PowerShell**

2. **执行构建脚本**
   ```powershell
   .\build_installer.bat
   ```

   脚本将自动：
   - 检查 Python 环境
   - 安装 Python 依赖
   - 使用 Chocolatey 安装 Tesseract（如需要）
   - 打包 Python 程序
   - 编译 Inno Setup 安装脚本

3. **获取安装程序**
   - 位置：`installer\GlotSub_Setup.exe`

### 方法2：手动构建

#### 步骤1：安装依赖

```powershell
# 安装 Python 依赖
pip install --user -r requirements.txt
pip install --user pyinstaller

# 安装 Tesseract（如需要）
choco install tesseract -y --params="'/Language:chi_sim /Language:eng'"
```

#### 步骤2：打包程序

```powershell
python -m PyInstaller --onefile --windowed --name GlotSub main.py
```

#### 步骤3：编译安装程序

**选项A：使用命令行**
```powershell
iscc setup.iss
```

**选项B：使用 Inno Setup Compiler GUI**
1. 打开 Inno Setup Compiler
2. 文件 → 打开 → 选择 `setup.iss`
3. 构建 → 编译

## 安装程序功能

### 自动检测和安装 Tesseract OCR

安装程序在运行时会：

1. **自动检测** Tesseract OCR 是否已安装
2. **提示用户** 如果未安装
3. **提供两个安装选项**：
   - **选项1**：使用 Chocolatey 自动安装（如果系统已安装 Chocolatey）
   - **选项2**：自动下载并安装 Tesseract 安装程序（需要网络连接）

### 安装流程

1. 用户运行 `GlotSub_Setup.exe`
2. 安装向导启动
3. 检测 Tesseract OCR：
   - ✅ 已安装 → 继续安装 GlotSub
   - ❌ 未安装 → 提示用户是否自动安装
4. 安装 GlotSub 主程序
5. 创建桌面快捷方式（可选）
6. 完成安装

## 安装程序特性

- ✅ **自动检测 Tesseract OCR**
- ✅ **支持 Chocolatey 自动安装**
- ✅ **支持下载并自动安装 Tesseract**
- ✅ **友好的中文界面**
- ✅ **完整的错误处理**
- ✅ **桌面快捷方式选项**
- ✅ **自动添加到开始菜单**

## 文件结构

构建完成后：

```
GlotSub/
├── dist/
│   └── GlotSub.exe              # 打包的程序
├── installer/
│   └── GlotSub_Setup.exe        # 最终安装程序
├── setup.iss                     # Inno Setup 脚本
├── build_installer.bat          # 自动化构建脚本
└── ...
```

## 测试安装程序

### 基本测试

1. **在干净的 Windows 系统上测试**
   - 虚拟机或全新系统
   - 未安装 Tesseract OCR

2. **测试场景**
   - 场景1：系统已安装 Tesseract → 应直接安装 GlotSub
   - 场景2：系统未安装 Tesseract → 应提示并自动安装
   - 场景3：网络不可用 → 应给出手动安装提示

### 测试步骤

1. 运行 `GlotSub_Setup.exe`
2. 按照安装向导操作
3. 验证 Tesseract OCR 自动安装功能
4. 验证 GlotSub 程序运行正常

## 故障排查

### 构建时问题

**Q: Chocolatey 安装 Tesseract 失败？**
- A: 确保以管理员权限运行脚本
- A: 检查网络连接
- A: 手动安装 Tesseract，构建脚本仍可继续

**Q: Inno Setup 编译失败？**
- A: 检查 `setup.iss` 语法
- A: 确保 `dist\GlotSub.exe` 存在
- A: 检查 Inno Setup 是否正确安装

**Q: 打包的程序无法运行？**
- A: 检查所有依赖是否正确安装
- A: 在命令行运行查看错误信息
- A: 检查杀毒软件是否拦截

### 安装程序问题

**Q: 自动安装 Tesseract 失败？**
- A: 用户需要管理员权限
- A: 需要网络连接下载安装程序
- A: 提供手动安装指南

**Q: 安装后程序无法运行？**
- A: 检查 Tesseract OCR 是否正确安装
- A: 检查系统 PATH 环境变量
- A: 查看程序错误日志

## 分发建议

### 最小分发包

只需分发：
- `installer\GlotSub_Setup.exe` - 单个安装程序文件

### 完整分发包

可以包含：
- `GlotSub_Setup.exe` - 安装程序
- `README.md` - 使用说明
- `INSTALL.md` - 安装指南（备用）

### 安装程序大小

- **仅 GlotSub**: 约 67 MB
- **包含自动安装功能**: 约 67 MB（Tesseract 需要单独下载）

## 更新和维护

### 更新版本号

编辑 `setup.iss`：
```pascal
#define MyAppVersion "1.0.1"  // 修改版本号
```

### 更新 Tesseract 下载链接

编辑 `setup.iss` 中的 `DownloadUrl`：
```pascal
DownloadUrl := 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.0.20241111.exe';
```

## 相关文件

- `setup.iss` - Inno Setup 安装脚本
- `build_installer.bat` - 自动化构建脚本
- `BUILD.md` - 详细构建文档
- `INSTALL.md` - 用户安装指南

## 许可证

安装程序遵循与主程序相同的许可证。

