@echo off
REM Quick server launch script
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo ========================================
echo TRADE OPPORTUNITIES API SERVER
echo ========================================
echo Server starting on http://localhost:8000
echo Swagger UI: http://localhost:8000/docs
echo.
echo DO NOT CLOSE THIS WINDOW!
echo ========================================
echo.
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
