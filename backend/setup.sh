#!/usr/bin/env bash
# Setup script for market microstructure analysis backend

set -e  # Exit on error

echo "🚀 Setting up Market Microstructure Analysis Backend"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

echo "✓ Found Python $PYTHON_VERSION"

# Check if Python version meets requirement
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Error: Python 3.11 or higher is required"
    echo "   Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel

# Try installing full requirements first
echo ""
echo "📥 Installing dependencies..."
if pip install -r requirements.txt; then
    echo "✓ All dependencies installed successfully"
else
    echo ""
    echo "⚠️  Full installation failed. Trying minimal installation..."
    echo ""
    if pip install -r requirements-minimal.txt; then
        echo "✓ Minimal dependencies installed successfully"
        echo ""
        echo "ℹ️  Note: Some optional dependencies (FastAPI, Pydantic) were skipped"
        echo "   The core WebSocket functionality will still work"
    else
        echo "❌ Installation failed. Please see TROUBLESHOOTING.md"
        exit 1
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python run.py"
echo ""
echo "To deactivate virtual environment later: deactivate"
