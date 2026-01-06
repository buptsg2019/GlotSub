# 安装指南

本指南详细说明 GlotSub 字幕识别工具的安装步骤。

## 快速安装

### Windows 用户

1. **安装 Python 3.7+**
   - 访问 https://www.python.org/downloads/
   - 下载并运行安装程序
   - **重要**：安装时勾选 "Add Python to PATH"

2. **安装 Tesseract OCR**
   - 下载地址：https://github.com/UB-Mannheim/tesseract/wiki
   - 运行安装程序（推荐版本：tesseract-ocr-w64-setup-5.x.x.exe）
   - 安装路径建议：`C:\Program Files\Tesseract-OCR`
   - **重要**：安装时务必勾选以下语言包：
     - ✅ Chinese Simplified (chi_sim)
     - ✅ Chinese Traditional (chi_tra)
     - ✅ English (eng)
   - 将安装目录添加到系统 PATH：
     ```
     C:\Program Files\Tesseract-OCR
     ```

3. **安装 Python 依赖**
   ```powershell
   cd D:\Software\GlotSub
   pip install -r requirements.txt
   ```

4. **验证安装**
   ```powershell
   python main.py
   ```

### Linux 用户

```bash
# 1. 安装 Python（如果未安装）
sudo apt update
sudo apt install python3 python3-pip

# 2. 安装 Tesseract OCR 及语言包
sudo apt install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng

# 3. 安装 Python 依赖
pip3 install -r requirements.txt

# 4. 运行程序
python3 main.py
```

### macOS 用户

```bash
# 1. 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装 Tesseract OCR
brew install tesseract tesseract-lang

# 3. 安装 Python 依赖
pip3 install -r requirements.txt

# 4. 运行程序
python3 main.py
```

## 详细安装步骤

### Tesseract OCR 安装详解

#### Windows 安装选项说明

安装程序会提供以下选项：

- **安装路径**：默认 `C:\Program Files\Tesseract-OCR`（推荐）
- **组件选择**：
  - Tesseract OCR executable（必需）
  - Language data（必需）
    - English（英文，默认已选）
    - Chinese Simplified（简体中文，**必须勾选**）
    - Chinese Traditional（繁体中文，可选）
  - Additional language data（其他语言，根据需要选择）

#### 验证 Tesseract 安装

打开命令提示符（CMD）或 PowerShell，输入：

```bash
tesseract --version
```

如果显示版本信息，说明安装成功。

#### 验证语言包安装

```bash
tesseract --list-langs
```

应该能看到 `chi_sim` 和 `eng` 在列表中。

### Python 依赖说明

主要依赖包及作用：

- **pytesseract** (0.3.10+)：Python 的 Tesseract OCR 接口
- **Pillow** (9.0.0+)：图像处理库
- **opencv-python** (4.5.0+)：图像预处理（提高OCR准确率）
- **numpy** (1.21.0+)：数值计算支持
- **mss** (6.1.0+)：高效的屏幕截图库
- **pyperclip** (1.8.2+)：剪贴板操作

### 使用虚拟环境（推荐）

为避免依赖冲突，建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 故障排查

### 问题1：找不到 tesseract 命令

**Windows 解决方案：**
1. 确认 Tesseract 安装路径
2. 添加到系统 PATH：
   - 控制面板 → 系统 → 高级系统设置 → 环境变量
   - 编辑"系统变量"中的 Path
   - 添加：`C:\Program Files\Tesseract-OCR`
3. 重启命令提示符或 PowerShell

**Linux/macOS 解决方案：**
```bash
# 查找安装位置
which tesseract

# 如果未找到，重新安装
# Ubuntu/Debian:
sudo apt install tesseract-ocr

# macOS:
brew install tesseract
```

### 问题2：提示找不到语言包

**Windows：**
- 重新运行安装程序，确保勾选了中文语言包
- 或手动下载语言包：https://github.com/tesseract-ocr/tessdata
- 将 `.traineddata` 文件复制到：`C:\Program Files\Tesseract-OCR\tessdata`

**Linux：**
```bash
sudo apt install tesseract-ocr-chi-sim
```

**macOS：**
```bash
brew install tesseract-lang
```

### 问题3：Python 模块导入错误

```bash
# 确认已安装所有依赖
pip list

# 重新安装依赖
pip install --upgrade -r requirements.txt

# 如果使用虚拟环境，确保已激活
```

### 问题4：程序运行时错误

1. **检查 Python 版本**：
   ```bash
   python --version
   ```
   需要 3.7 或更高版本

2. **检查所有依赖是否正确安装**：
   ```bash
   python -c "import pytesseract; import cv2; import mss; import pyperclip; print('所有依赖正常')"
   ```

3. **查看错误日志**：
   程序会在控制台输出详细错误信息，根据错误信息进行排查

## 性能优化建议

1. **减小识别区域**：只选择字幕显示的最小区域
2. **调整识别频率**：编辑 `main.py` 中的 `time.sleep(0.5)` 值
   - 值越大，识别频率越低，CPU占用越小
   - 值越小，识别频率越高，实时性越好
3. **关闭其他占用资源的程序**

## 获取帮助

如果遇到问题，可以：
1. 查看 README.md 中的常见问题部分
2. 提交 Issue 到项目仓库
3. 检查 Tesseract OCR 官方文档

