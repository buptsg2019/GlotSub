@echo off
REM GlotSub 打包脚本 (Windows)
REM 使用 PyInstaller 打包为可执行文件

echo 正在检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 未找到 PyInstaller，正在安装...
    pip install pyinstaller
)

echo.
echo 开始打包 GlotSub...
echo.

pyinstaller --onefile --windowed --name GlotSub --add-data "requirements.txt;." main.py

if errorlevel 1 (
    echo.
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo 打包完成！
echo 可执行文件位于 dist 目录：dist\GlotSub.exe
echo.
pause

