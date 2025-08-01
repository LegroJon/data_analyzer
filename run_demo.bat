@echo off
REM Demo batch file for Data Analyzer

echo.
echo ====================================
echo    Data Analyzer - Demo
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Run the demo
echo Running demonstration...
echo.
python demo.py

echo.
echo ====================================
echo Demo completed.
echo Check the data\output\ directory for results.
echo ====================================
pause
