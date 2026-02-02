@echo off
echo.
echo ====================================
echo  Molecular Data Converter
echo  Author: Bei Chen
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Starting molecular data converter...
echo.

REM Run the starter script
python start_here.py

echo.
echo Conversion process completed!
pause
