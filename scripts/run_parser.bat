@echo off
REM Data Analyzer - Task Parser
REM Easy execution script for Windows

echo.
echo ====================================
echo    Data Analyzer - Task Parser
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

REM Run the parser
echo Starting task parser...
echo.
python src\task_parser.py

echo.
echo ====================================
echo Process completed.
echo Check the data\output\ directory for results.
echo ====================================
pause
