#!/bin/bash

# CDrive Insurance Management System - Quick Start Script

echo "🏢 CDrive Insurance Management System - Quick Start"
echo "================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ and try again."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Start the application
echo "🚀 Starting CDrive Insurance Management System..."
echo "   Access the application at: http://localhost:8501"
echo "   Press Ctrl+C to stop the application"
echo ""

streamlit run app.py

echo "👋 Application stopped. Thank you for using CDrive Insurance Management System!"