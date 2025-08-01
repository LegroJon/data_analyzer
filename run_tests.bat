@echo off
REM Test runner batch file for Windows

echo.
echo ====================================
echo    Data Analyzer - Test Suite
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

REM Run the test suite
echo Running comprehensive test suite...
echo.
python run_tests.py

echo.
echo ====================================
echo Test run completed.
echo ====================================
pause
