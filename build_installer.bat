@echo off
chcp 65001 >nul

REM 切换到脚本所在目录
cd /d "%~dp0"

echo ========================================
echo GlotSub 完整构建和打包脚本
echo ========================================
echo.
echo 当前工作目录: %CD%
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 此脚本需要管理员权限！
    echo [提示] 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)
python --version
echo [成功] Python 环境正常
echo.

echo [2/5] 安装/更新 Python 依赖...
if not exist "requirements.txt" (
    echo [错误] 找不到 requirements.txt 文件！
    echo [提示] 请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

pip install --user -r "%CD%\requirements.txt" --quiet
if errorlevel 1 (
    echo [警告] 某些依赖安装失败，继续执行...
)
pip install --user pyinstaller --quiet
echo [完成] Python 依赖已准备
echo.

echo [3/5] 检查 Tesseract OCR...
where tesseract >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到 Tesseract OCR，正在使用 Chocolatey 安装...
    choco install tesseract -y --params="'/Language:chi_sim /Language:eng'"
    if errorlevel 1 (
        echo [警告] Chocolatey 安装失败，安装程序将尝试自动安装
    ) else (
        echo [成功] Tesseract OCR 安装完成
        echo [提示] 更新当前会话的环境变量...
        REM 手动添加 Tesseract 到 PATH（Chocolatey 已添加到系统 PATH，但当前会话需要更新）
        set "PATH=%PATH%;C:\Program Files\Tesseract-OCR"
        REM 验证安装
        timeout /t 2 >nul
        if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
            echo [成功] Tesseract OCR 可执行文件已找到
            "C:\Program Files\Tesseract-OCR\tesseract.exe" --version 2>nul
        ) else (
            echo [警告] 无法验证 Tesseract 安装，但 Chocolatey 报告安装成功
        )
    )
) else (
    tesseract --version
    echo [成功] Tesseract OCR 已安装
)
echo.

echo [4/5] 打包 Python 程序...
echo 工作目录: %CD%

REM 确保在正确目录
if not exist "main.py" (
    echo [错误] 找不到 main.py 文件！
    echo [提示] 当前目录: %CD%
    pause
    exit /b 1
)

python -m PyInstaller --onefile --windowed --name GlotSub --clean main.py
if errorlevel 1 (
    echo [错误] 打包失败！
    pause
    exit /b 1
)
echo [成功] 程序打包完成
echo.

echo [5/5] 检查 Inno Setup...
where iscc >nul 2>&1
if errorlevel 1 (
    echo [警告] 未找到 Inno Setup 编译器 (iscc)
    echo [提示] 请安装 Inno Setup: https://jrsoftware.org/isdl.php
    echo [提示] 安装后将 Inno Setup 的安装目录添加到系统 PATH
    echo.
    echo [提示] 或者手动编译安装脚本：
    echo         1. 打开 Inno Setup Compiler
    echo         2. 打开文件: setup.iss
    echo         3. 点击 Build - Compile
    echo.
    pause
    exit /b 1
)

REM 确保 setup.iss 存在
if not exist "setup.iss" (
    echo [错误] 找不到 setup.iss 文件！
    echo [提示] 当前目录: %CD%
    pause
    exit /b 1
)

echo [提示] 正在编译安装程序...
iscc "%CD%\setup.iss"
if errorlevel 1 (
    echo [错误] 安装程序编译失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 构建完成！
echo ========================================
echo.
echo 安装程序位置: installer\GlotSub_Setup.exe
echo.
echo 下一步：
echo   1. 测试安装程序
echo   2. 分发安装程序给用户
echo.
pause

