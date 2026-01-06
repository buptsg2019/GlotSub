# GlotSub - 轻量级字幕自动识别工具

GlotSub 是一个轻量化、易打包安装的屏幕字幕识别工具，可以实时识别屏幕指定区域中的中英文字幕，并自动保存到列表中，支持复制和导出功能。

## 功能特性

- 🖱️ **区域选择**：通过鼠标拖动选择屏幕任意区域进行识别
- 🔍 **实时识别**：自动识别选中区域中的字幕内容（支持中文和英文）
- ⏸️ **暂停控制**：可随时暂停/继续识别过程
- 📝 **滚动列表**：识别到的字幕实时添加到滚动列表中显示
- 📋 **一键复制**：将所有识别的字幕复制到剪贴板
- 💾 **导出功能**：支持导出为文本文件（.txt）或字幕文件（.srt）
- 💻 **轻量高效**：使用Python + Tkinter构建，内存占用小，运行流畅

## 系统要求

- Windows 7/10/11 或 Linux 或 macOS
- Python 3.7 或更高版本
- Tesseract OCR 引擎

## 安装步骤

### 1. 安装 Python

如果尚未安装 Python，请从 [Python官网](https://www.python.org/downloads/) 下载并安装 Python 3.7+ 版本。

### 2. 安装 Tesseract OCR

#### Windows 系统

1. 从 [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装程序
2. 运行安装程序，建议安装到默认路径 `C:\Program Files\Tesseract-OCR`
3. 安装时**务必勾选中文语言包**（Chinese Simplified, Chinese Traditional）
4. 将 Tesseract 添加到系统 PATH 环境变量：
   - 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在系统变量中找到 Path，点击编辑
   - 添加：`C:\Program Files\Tesseract-OCR`

#### Linux 系统

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng

# Fedora
sudo dnf install tesseract tesseract-langpack-chi_sim tesseract-langpack-eng

# Arch Linux
sudo pacman -S tesseract tesseract-data-chi_sim tesseract-data-eng
```

#### macOS 系统

```bash
brew install tesseract tesseract-lang
```

### 3. 安装 Python 依赖

在项目目录下运行：

```bash
pip install -r requirements.txt
```

或使用国内镜像加速：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用方法

1. **启动程序**
   ```bash
   python main.py
   ```

2. **选择识别区域**
   - 点击"选择识别区域"按钮
   - 程序窗口会隐藏，屏幕会变暗
   - 在屏幕上拖动鼠标选择要识别的区域（黄色边框）
   - 释放鼠标完成选择，或按 ESC 取消

3. **开始识别**
   - 点击"开始识别"按钮
   - 程序会实时识别选中区域的字幕
   - 识别到的新字幕会自动添加到列表中

4. **控制识别**
   - 点击"暂停识别"可暂停识别过程
   - 再次点击"继续识别"恢复识别

5. **管理字幕**
   - **清空列表**：清除所有已识别的字幕
   - **复制全部**：将所有字幕复制到剪贴板
   - **导出文件**：将字幕保存为 .txt 或 .srt 格式文件

## 打包为可执行文件

使用 PyInstaller 打包为独立可执行文件：

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包程序
pyinstaller --onefile --windowed --name GlotSub --icon=NONE main.py

# 打包后的可执行文件在 dist 目录下
```

打包参数说明：
- `--onefile`：打包为单个可执行文件
- `--windowed`：隐藏控制台窗口（GUI应用）
- `--name`：指定生成的可执行文件名称

## 技术栈

- **GUI框架**：Tkinter（Python 内置，轻量级）
- **OCR引擎**：Tesseract OCR（开源，支持多语言）
- **图像处理**：Pillow, OpenCV, NumPy
- **屏幕截图**：mss（高效跨平台截图库）
- **剪贴板操作**：pyperclip

## 注意事项

1. **识别准确率**：OCR识别准确率受以下因素影响：
   - 字幕字体清晰度
   - 背景对比度
   - 字幕大小
   - 屏幕分辨率

2. **性能优化**：
   - 识别区域不宜过大，建议只选择字幕显示区域
   - 识别频率默认0.5秒一次，可根据需要调整

3. **语言支持**：
   - 默认支持中文（简体）和英文识别
   - 如需其他语言，请安装对应的 Tesseract 语言包

4. **系统兼容性**：
   - Windows：完全支持
   - Linux：需要X11图形界面
   - macOS：完全支持

## 常见问题

**Q: 提示找不到 Tesseract OCR？**  
A: 请确保 Tesseract 已正确安装并添加到系统 PATH 环境变量中。

**Q: 识别准确率低？**  
A: 尝试选择更清晰的区域，确保字幕与背景对比度高。可以调整识别区域大小。

**Q: 程序运行缓慢？**  
A: 减小识别区域面积可以提升性能。识别频率可在代码中调整（recognize_loop 函数中的 time.sleep 值）。

**Q: 不支持其他语言？**  
A: 请安装对应的 Tesseract 语言包，并在代码中修改 `ocr_config` 参数。

## 开发说明

项目结构：
```
GlotSub/
├── main.py              # 主程序文件
├── requirements.txt     # Python依赖列表
├── README.md           # 说明文档
└── LICENSE             # 许可证文件
```

## 许可证

本项目采用开源许可证，详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目！

## 更新日志

### v1.0.0 (2024)
- 初始版本发布
- 实现基本的区域选择和字幕识别功能
- 支持中英文识别
- 支持字幕列表管理和导出功能
