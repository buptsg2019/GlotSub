# GlotSub 构建和打包指南

## 快速打包

### 方法1：使用批处理脚本（推荐）

```powershell
# 1. 安装依赖（如果尚未安装）
pip install --user -r requirements.txt
pip install --user pyinstaller

# 2. 打包程序
python -m PyInstaller --onefile --windowed --name GlotSub main.py

# 3. 创建安装包
.\create_installer.bat
```

### 方法2：手动打包

```powershell
# 1. 打包
python -m PyInstaller --onefile --windowed --name GlotSub main.py

# 2. 测试
.\test_exe.bat

# 3. 创建安装包目录
mkdir installer\GlotSub
copy dist\GlotSub.exe installer\GlotSub\
copy README.md installer\GlotSub\
copy INSTALL.md installer\GlotSub\
copy LICENSE installer\GlotSub\
```

## 打包参数说明

- `--onefile`: 打包为单个可执行文件
- `--windowed`: 隐藏控制台窗口（GUI应用）
- `--name GlotSub`: 指定生成的可执行文件名称

## 打包结果

打包完成后，文件位于：
- **可执行文件**: `dist/GlotSub.exe` (约67MB)
- **构建文件**: `build/` 目录（可删除）
- **规格文件**: `GlotSub.spec`（可保留用于自定义打包）

## 创建安装程序

### 选项1：ZIP 安装包（最简单）

运行 `create_installer.bat` 脚本，会自动创建：
- `installer/GlotSub/` - 安装目录
- `installer/GlotSub_安装包.zip` - ZIP 安装包

### 选项2：Inno Setup 安装程序（专业）

1. 下载安装 Inno Setup: https://jrsoftware.org/isdl.php
2. 打开 `setup.iss` 文件
3. 在 Inno Setup 中编译脚本
4. 生成的安装程序位于 `installer/` 目录

### 选项3：NSIS 安装程序

1. 下载安装 NSIS: https://nsis.sourceforge.io/Download
2. 创建安装脚本
3. 编译生成安装程序

## 测试打包结果

### 基本测试

```powershell
# 测试可执行文件
.\test_exe.bat

# 或直接运行
.\dist\GlotSub.exe
```

### 完整测试清单

- [ ] 程序能正常启动
- [ ] 界面显示正常
- [ ] 能选择识别区域
- [ ] 能识别字幕（需要 Tesseract OCR）
- [ ] 字幕列表功能正常
- [ ] 复制和导出功能正常

## 文件大小优化

当前打包大小约 67MB，如需优化：

1. **排除不需要的模块**
   ```powershell
   python -m PyInstaller --onefile --windowed --name GlotSub --exclude-module matplotlib --exclude-module scipy main.py
   ```

2. **使用虚拟环境打包**（减小依赖）
   ```powershell
   python -m venv venv_build
   venv_build\Scripts\activate
   pip install -r requirements.txt pyinstaller
   python -m PyInstaller --onefile --windowed --name GlotSub main.py
   ```

3. **启用 UPX 压缩**（已默认启用）

## 依赖说明

### 已打包的依赖

以下依赖已打包进 exe 文件：
- Python 运行时
- Tkinter GUI 库
- Pillow 图像处理
- OpenCV 图像处理
- NumPy 数值计算
- pytesseract OCR 接口
- mss 屏幕截图
- pyperclip 剪贴板操作

### 需要单独安装的依赖

- **Tesseract OCR** - 必须单独安装，无法打包
  - 下载：https://github.com/UB-Mannheim/tesseract/wiki
  - 需要添加到系统 PATH

## 常见问题

### Q: 打包后程序无法运行？

A: 检查以下几点：
1. 是否安装了 Tesseract OCR
2. Tesseract 是否在系统 PATH 中
3. 杀毒软件是否拦截
4. 是否有必要的系统 DLL（通常 Windows 10/11 都有）

### Q: 打包文件太大？

A: 67MB 是正常大小，包含了所有 Python 依赖。可以：
- 使用虚拟环境减少不必要的依赖
- 排除不需要的模块
- 使用 UPX 压缩（已启用）

### Q: 如何创建自动安装程序？

A: 使用 Inno Setup 或 NSIS：
- Inno Setup: 使用提供的 `setup.iss` 脚本
- NSIS: 需要自行编写安装脚本

## 发布检查清单

- [ ] 打包成功，生成 exe 文件
- [ ] 测试程序基本功能
- [ ] 创建安装包目录
- [ ] 包含所有必要文档
- [ ] 创建安装说明文件
- [ ] 测试安装包解压和运行
- [ ] 检查文件大小是否合理
- [ ] 准备发布说明

## 版本信息

- 当前版本：1.0.0
- Python 版本：3.11.5
- PyInstaller 版本：6.17.0
- 打包日期：2026-01-05

