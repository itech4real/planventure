#!/bin/bash
set -e

echo "🚀 Setting up PlanVenture development environment..."

# Install Python dependencies for API
if [ -f "planventure-api/requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    cd planventure-api
    pip install --user -r requirements.txt
    cd ..
fi

# Install Node dependencies for Web
if [ -f "planventure-web/package.json" ]; then
    echo "📦 Installing Node dependencies..."
    cd planventure-web
    npm install
    cd ..
fi

echo "✅ Development environment is ready!"
echo ""
echo "🎯 Quick Start Commands:"
echo "  - API:  cd planventure-api && python app.py"
echo "  - Web:  cd planventure-web && npm run dev"
echo "  - Test: cd planventure-api && python -m pytest"
echo ""
echo "🌐 Services:"
echo "  - API will be available at: http://localhost:5000"
echo "  - Web will be available at: http://localhost:3000"
echo "  - PostgreSQL will be available at: localhost:5432"
