#!/bin/bash

# Development setup script for Sanic + Next.js Template
echo "🚀 Setting up development environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python 3.12 is installed
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 is not installed. Please install Python 3.12 first."
    echo "   This template requires Python 3.12 for Vercel compatibility."
    exit 1
fi

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Create Python virtual environment with Python 3.12
echo "🐍 Setting up Python virtual environment with Python 3.12..."
cd api
python3.12 -m venv venv
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
echo "⚠️  Important: This template uses Python 3.12 for Vercel compatibility."
echo ""
echo "🌐 Application will be available at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs (if using FastAPI in future)"
