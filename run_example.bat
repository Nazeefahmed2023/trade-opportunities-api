@echo off
REM Run example API client
echo Running example client...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requests if not already installed
pip install requests >nul 2>&1

REM Run example
python example_client.py

pause
