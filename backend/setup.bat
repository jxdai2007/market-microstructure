@echo off
REM Setup script for Windows

echo Setting up Market Microstructure Analysis Backend
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH
    echo Please install Python 3.11 or higher
    exit /b 1
)

REM Create virtual environment
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Full installation failed. Trying minimal installation...
    pip install -r requirements-minimal.txt
    if errorlevel 1 (
        echo Installation failed. Please see TROUBLESHOOTING.md
        exit /b 1
    )
    echo Minimal dependencies installed successfully
)

echo.
echo Setup complete!
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python run.py
echo.
pause
