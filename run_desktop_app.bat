@echo off
echo Starting College Voting System Desktop App...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating...
    python -m venv .venv
    echo.
)

REM Activate virtual environment and run
call .venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.

REM Launch the desktop app
echo Launching application...
python app_desktop.py

pause
