@echo off
chcp 65001 >nul
echo ========================================
echo    FastDanbooruDataset Launcher
echo ========================================
echo.

REM Check if Python is installed
echo [1/4] Checking Python environment...
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not detected!
    echo.
    echo Please install Python 3.7 or higher:
    echo 1. Visit https://www.python.org/downloads/
    echo 2. Download the latest Python version
    echo 3. During installation, check "Add Python to PATH"
    echo 4. Run this script again after installation
    echo.
    pause
    exit /b 1
)

echo Python environment OK
py --version
echo.

REM Upgrade pip
echo [2/4] Upgrading pip to latest version...
py -m pip install --upgrade pip >nul 2>&1
echo Pip upgrade completed
echo.

REM Check and install dependencies
echo [3/4] Checking dependencies...
py -c "import flask, werkzeug" >nul 2>&1
if errorlevel 1 (
    echo Missing dependencies detected, installing...
    echo Installing: Flask, Werkzeug, gallery-dl
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Installation failed! Trying with China mirror...
        pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
        if errorlevel 1 (
            echo.
            echo Installation failed!
            echo Possible solutions:
            echo 1. Check network connection
            echo 2. Run this script as administrator
            echo 3. Manually run: pip install -r requirements.txt
            echo.
            pause
            exit /b 1
        )
    )
    echo.
    echo Dependencies installed successfully!
    echo.
    echo Installed components:
    pip list | findstr "Flask Werkzeug gallery-dl"
    echo.
else (
    echo Dependencies check completed - All required packages found
)

echo.
echo [4/4] Starting WebUI server...
echo WebUI will be available at: http://localhost:5678
echo Press Ctrl+C to stop server
echo ========================================
echo.

py app.py

echo.
echo Server stopped
echo Thank you for using FastDanbooruDataset WebUI!
pause