@echo off
REM Windows setup script for Trade Opportunities API
echo ====================================
echo Trade Opportunities API - Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [5/5] Checking .env file...
if not exist .env (
    echo WARNING: .env file not found
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your GEMINI_API_KEY
    echo You can get it from: https://makersuite.google.com/app/apikey
    echo.
)

echo.
echo ====================================
echo Setup Complete! ✓
echo ====================================
echo.
echo Next steps:
echo 1. Edit .env file and add your GEMINI_API_KEY
echo 2. Run: start_server.bat
echo.
echo To get Gemini API key:
echo Visit: https://makersuite.google.com/app/apikey
echo.
pause
