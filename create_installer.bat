@echo off
chcp 65001 >nul
echo ========================================
echo GlotSub 安装包创建脚本
echo ========================================
echo.

REM 创建安装包目录
if not exist "installer" mkdir installer
if not exist "installer\GlotSub" mkdir installer\GlotSub

echo [1/4] 复制可执行文件...
copy /Y "dist\GlotSub.exe" "installer\GlotSub\GlotSub.exe"
if errorlevel 1 (
    echo 错误：找不到 dist\GlotSub.exe
    echo 请先运行打包命令：python -m PyInstaller --onefile --windowed --name GlotSub main.py
    pause
    exit /b 1
)

echo [2/4] 复制文档文件...
copy /Y "README.md" "installer\GlotSub\README.md" >nul 2>&1
copy /Y "INSTALL.md" "installer\GlotSub\INSTALL.md" >nul 2>&1
copy /Y "LICENSE" "installer\GlotSub\LICENSE" >nul 2>&1

echo [3/4] 复制安装说明...
copy /Y "installer\安装说明.txt" "installer\GlotSub\安装说明.txt" >nul 2>&1

echo [4/4] 创建安装包 ZIP 文件...
cd installer
if exist "GlotSub_安装包.zip" del "GlotSub_安装包.zip"
powershell -Command "Compress-Archive -Path GlotSub\* -DestinationPath GlotSub_安装包.zip -Force"
cd ..

echo.
echo ========================================
echo 安装包创建完成！
echo ========================================
echo.
echo 安装包位置：installer\GlotSub_安装包.zip
echo 安装目录：installer\GlotSub\
echo.
echo 安装包内容：
echo   - GlotSub.exe (主程序)
echo   - README.md (使用说明)
echo   - INSTALL.md (安装指南)
echo   - 安装说明.txt (快速安装说明)
echo.
pause

