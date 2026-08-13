@echo off
echo ========================================
echo Starting MaskDNS Server
echo ========================================
echo.

if not exist .venv (
    echo Virtual environment not found!
    echo Please run setup_windows.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.

echo Starting Flask application...
echo Access the app at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.
python app.py
