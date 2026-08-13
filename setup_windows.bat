@echo off
echo ========================================
echo MaskDNS Windows Setup Script
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.11+
    pause
    exit /b 1
)
echo.

echo Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Trying alternative method...
    python -m pip install --user virtualenv
    python -m virtualenv .venv
)
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Initializing database...
python -c "from app import init_db; init_db()"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Run: .venv\Scripts\activate.bat
echo   2. Run: python app.py
echo   3. Open browser: http://localhost:5000
echo.
echo Default admin password: admin123
echo ========================================
pause
