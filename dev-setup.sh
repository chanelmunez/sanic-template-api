#!/bin/bash

# Development setup script for Sanic + Next.js Template
echo "🚀 Setting up development environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Create Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd api
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 To start development:"
echo "1. Frontend: npm run dev (in root directory)"
echo "2. Backend: npm run python-dev (in root directory)"
echo "   Or: cd api && source venv/bin/activate && python -m uvicorn main:app --reload --port 8000"
echo ""
echo "🌐 Application will be available at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs (if using FastAPI in future)"
