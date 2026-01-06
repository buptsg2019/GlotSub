@echo off
chcp 65001 >nul
echo ========================================
echo 准备 Tesseract OCR 文件
echo ========================================
echo.

REM 创建Tesseract目录
if not exist "tesseract_files" mkdir tesseract_files

echo [提示] 正在尝试使用 Chocolatey 安装 Tesseract OCR...
echo.

REM 尝试使用Chocolatey安装（需要管理员权限）
choco install tesseract -y --params="'/Language:chi_sim /Language:eng'"
if errorlevel 1 (
    echo.
    echo [警告] Chocolatey 安装失败，可能需要管理员权限
    echo [提示] 请手动下载 Tesseract OCR 安装包
    echo [提示] 下载地址: https://github.com/UB-Mannheim/tesseract/wiki
    echo [提示] 或使用管理员权限运行此脚本
    echo.
    pause
    exit /b 1
)

echo.
echo [成功] Tesseract OCR 安装完成
echo [提示] 正在查找 Tesseract 安装位置...

REM 查找Tesseract安装位置
set TESSERACT_PATH=
for /f "tokens=*" %%i in ('where tesseract 2^>nul') do set TESSERACT_PATH=%%~dpi

if "%TESSERACT_PATH%"=="" (
    REM 尝试常见安装路径
    if exist "C:\Program Files\Tesseract-OCR" set TESSERACT_PATH=C:\Program Files\Tesseract-OCR\
    if exist "C:\Program Files (x86)\Tesseract-OCR" set TESSERACT_PATH=C:\Program Files (x86)\Tesseract-OCR\
)

if "%TESSERACT_PATH%"=="" (
    echo [错误] 无法找到 Tesseract OCR 安装路径
    pause
    exit /b 1
)

echo [成功] 找到 Tesseract OCR: %TESSERACT_PATH%
echo.

REM 复制Tesseract文件到准备目录
echo [1/3] 复制 Tesseract 可执行文件...
xcopy /E /I /Y "%TESSERACT_PATH%*" "tesseract_files\"
if errorlevel 1 (
    echo [警告] 复制失败，可能需要管理员权限
    pause
    exit /b 1
)

echo [2/3] 验证语言包...
if exist "tesseract_files\tessdata\chi_sim.traineddata" (
    echo [成功] 找到简体中文语言包
) else (
    echo [警告] 未找到简体中文语言包 (chi_sim.traineddata)
)

if exist "tesseract_files\tessdata\eng.traineddata" (
    echo [成功] 找到英文语言包
) else (
    echo [警告] 未找到英文语言包 (eng.traineddata)
)

echo.
echo [3/3] 完成！
echo.
echo Tesseract 文件已准备在: tesseract_files\
echo 这些文件将被包含在安装程序中
echo.
pause

