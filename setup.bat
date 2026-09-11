@echo off
REM Patchamomma Quick Setup Script for Windows

echo.
echo ====================================
echo  Patchamomma Setup Script
echo ====================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Generating sample transcripts...
python scripts/download_ami_corpus.py
if errorlevel 1 (
    echo ERROR: Failed to generate sample transcripts
    pause
    exit /b 1
)

echo [5/5] Configuring environment...
if not exist .env (
    copy .env.example .env
    echo WARNING: .env created from template
    echo Please edit .env and add your GEMINI_API_KEY
    echo Get it from: https://aistudio.google.com
    echo.
    pause
)

echo.
echo ====================================
echo  Setup Complete!
echo ====================================
echo.
echo Next steps:
echo   1. Edit .env and add your GEMINI_API_KEY
echo   2. Start backend: python main.py
echo   3. In another terminal:
echo      - cd frontend
echo      - npm install
echo      - npm start
echo   4. Open http://localhost:3000
echo.
echo For more info, see README.md
echo.
pause
