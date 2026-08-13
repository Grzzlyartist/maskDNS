#!/bin/bash

echo "========================================"
echo "MaskDNS Setup Script (Git Bash/Windows)"
echo "========================================"
echo ""

# Check Python
echo "Checking Python installation..."
python --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python not found! Please install Python 3.11+"
    exit 1
fi
echo ""

# Clean up old venv if exists
if [ -d ".venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf .venv
    echo ""
fi

# Create virtual environment
echo "Creating virtual environment..."
python -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

# Initialize database
echo "Initializing database..."
python -c "from app import init_db; init_db()"
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  1. Run: source .venv/Scripts/activate"
echo "  2. Run: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "Default admin password: admin123"
echo "========================================"
