# Windows 一键安装脚本（对于编程小白）
# 运行这个脚本会自动完成：
# 1. 检查 Python 是否安装
# 2. 创建虚拟环境
# 3. 安装依赖包
# 4. 构建 exe 文件
# 5. 创建桌面快捷方式

@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     🎙️  AI口播智能体 - Windows 安装程序                   ║
echo ║     Talking Agent - Windows Setup                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: ===== 第1步：检查 Python =====
echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ 错误：未检测到 Python 3.10+
    echo.
    echo 请先安装 Python：
    echo   1. 访问 https://www.python.org/downloads/
    echo   2. 下载 Python 3.10 或更高版本
    echo   3. 安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ 已检测到 Python !PYTHON_VERSION!
echo.

:: ===== 第2步：创建虚拟环境 =====
echo [2/4] 创建虚拟环境...
if exist venv (
    echo ⚠️  虚拟环境已存在，跳过创建
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✓ 虚拟环境创建成功
)
echo.

:: ===== 第3步：激活虚拟环境并安装依赖 =====
echo [3/4] 安装依赖包（这需要几分钟，请耐心等待...）
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败
    pause
    exit /b 1
)

pip install --upgrade pip setuptools wheel >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 安装依赖失败，请检查网络连接
    pause
    exit /b 1
)
echo ✓ 依赖包安装成功
echo.

:: ===== 第4步：构建 exe 文件 =====
echo [4/4] 构建可执行文件（这需要2-3分钟...）
python build\build_exe.py
if errorlevel 1 (
    echo ❌ 构建失败
    pause
    exit /b 1
)
echo ✓ 可执行文件构建成功
echo.

:: ===== 创建桌面快捷方式 =====
echo 创建桌面快捷方式...
set DESKTOP=%USERPROFILE%\Desktop
set EXE_PATH=%cd%\dist\Talking.exe
set SHORTCUT_PATH=%DESKTOP%\AI口播智能体.lnk

powershell -Command ^
  "$WshShell = New-Object -ComObject WScript.Shell; " ^
  "$Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); " ^
  "$Shortcut.TargetPath = '%EXE_PATH%'; " ^
  "$Shortcut.WorkingDirectory = '%cd%'; " ^
  "$Shortcut.Save()"

if errorlevel 1 (
    echo ⚠️  快捷方式创建失败（非致命错误）
) else (
    echo ✓ 桌面快捷方式创建成功
)
echo.

:: ===== 完成 =====
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║              ✅ 安装完成！                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📝 下一步：
echo    1. 查看桌面是否出现 "🎙️ AI口播智能体" 图标
echo    2. 双击运行
echo    3. 享受使用！
echo.
echo 📁 可执行文件位置：
echo    %EXE_PATH%
echo.
echo 💡 提示：
echo    - 首次运行会下载 AI 模型文件（约 2GB），请耐心等待
echo    - 建议在网络良好的地方运行
echo    - 确保硬盘有足够空间（至少 10GB）
echo.
pause
