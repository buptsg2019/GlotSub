@echo off
chcp 65001 >nul
REM GlotSub 打包脚本 (Windows)
REM 使用 PyInstaller 打包为可执行文件

echo ========================================
echo GlotSub 打包脚本
echo ========================================
echo.

REM 检查并关闭正在运行的GlotSub.exe
echo [1/4] 检查运行中的进程...
tasklist | findstr /I "GlotSub.exe" >nul 2>&1
if %errorlevel% == 0 (
    echo 检测到GlotSub.exe正在运行，正在关闭...
    taskkill /F /IM GlotSub.exe >nul 2>&1
    timeout /t 2 >nul
)

REM 删除旧的打包文件
echo [2/4] 清理旧文件...
if exist dist\GlotSub.exe (
    del /f /q dist\GlotSub.exe >nul 2>&1
)
if exist build (
    rmdir /s /q build >nul 2>&1
)

REM 检查 PyInstaller
echo [3/4] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 未找到 PyInstaller，正在安装...
    pip install pyinstaller
)

echo.
echo [4/4] 开始打包 GlotSub...
echo.

REM 使用spec文件打包
python -m PyInstaller --clean GlotSub.spec

if errorlevel 1 (
    echo.
    echo ========================================
    echo 打包失败！
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. GlotSub.exe 正在运行，请先关闭
    echo 2. 缺少必要的依赖包
    echo 3. PyInstaller 配置问题
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 可执行文件位于：dist\GlotSub.exe
echo.
pause

