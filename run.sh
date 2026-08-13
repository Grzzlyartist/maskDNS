#!/bin/bash

echo "========================================"
echo "Starting MaskDNS Server"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run: bash setup.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate
echo ""

# Start the application
echo "Starting Flask application..."
echo "Access the app at: http://localhost:5000"
echo "Press CTRL+C to stop the server"
echo ""
python app.py
