@echo off
REM Start API server on Windows
echo ====================================
echo Trade Opportunities API - Server
echo ====================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please create .env from .env.example and configure it
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server...
echo.
echo API will be available at:
echo - Local:   http://localhost:8000
echo - Docs:    http://localhost:8000/docs
echo - Health:  http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
