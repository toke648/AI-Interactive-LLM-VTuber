@echo off
chcp 65001 >nul
echo [INFO] 正在检查 Python 环境...

:: 检测 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未检测到 Python，请安装 Python 并添加到环境变量。
    pause
    exit /b
)

echo [INFO] 设置工作目录...
cd /d "%~dp0"

echo [INFO] 创建并激活虚拟环境 (venv)...
if not exist "venv" (
    python -m venv venv
    echo [INFO] 虚拟环境已创建。
)

call venv\Scripts\activate

echo [INFO] 确保 pip 版本最新...
python -m ensurepip
python -m pip install --upgrade pip

echo [INFO] 检查并安装 PyAudio 依赖 (Windows 适配)...
pip show pyaudio >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] 安装 PyAudio...
    pip install --no-cache-dir pyaudio
)

echo [INFO] 安装 wheel 依赖包...
pip install --no-cache-dir wheel

echo [INFO] 安装 Python 依赖...
if not exist "requirements.txt" (
    echo [ERROR] 缺少 requirements.txt，请检查文件。
    pause
    exit /b
)
pip install --no-cache-dir -r requirements.txt

echo [INFO] 检查端口 5000 是否被占用...
netstat -ano | findstr :5000 >nul
if %errorlevel% == 0 (
    echo [ERROR] 端口 5000 已被占用，请手动关闭相关进程后重试。
    pause
    exit /b
)

echo [INFO] 启动 Python 服务器
python server.py