#!/bin/bash

# Patchamomma Quick Setup Script for macOS/Linux

echo ""
echo "===================================="
echo "  Patchamomma Setup Script"
echo "===================================="
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/5] Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Generating sample transcripts..."
python scripts/download_ami_corpus.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to generate sample transcripts"
    exit 1
fi

echo "[5/5] Configuring environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "WARNING: .env created from template"
    echo "Please edit .env and add your GEMINI_API_KEY"
    echo "Get it from: https://aistudio.google.com"
    echo ""
fi

echo ""
echo "===================================="
echo "  Setup Complete!"
echo "===================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your GEMINI_API_KEY"
echo "  2. Start backend: python main.py"
echo "  3. In another terminal:"
echo "     - cd frontend"
echo "     - npm install"
echo "     - npm start"
echo "  4. Open http://localhost:3000"
echo ""
echo "For more info, see README.md"
echo ""
