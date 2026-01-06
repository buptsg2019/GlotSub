@echo off
chcp 65001 >nul
echo ========================================
echo 测试 GlotSub.exe 可执行文件
echo ========================================
echo.

if not exist "dist\GlotSub.exe" (
    echo 错误：找不到 dist\GlotSub.exe
    echo 请先运行打包命令
    pause
    exit /b 1
)

echo 正在启动 GlotSub.exe...
echo 注意：如果系统未安装 Tesseract OCR，程序会显示错误提示
echo.
echo 按任意键启动程序...
pause >nul

start "" "dist\GlotSub.exe"

echo.
echo 程序已启动（如果窗口已打开）
echo 如果程序无法运行，请检查：
echo   1. 是否安装了 Tesseract OCR
echo   2. Tesseract OCR 是否在系统 PATH 中
echo   3. 杀毒软件是否拦截
echo.

