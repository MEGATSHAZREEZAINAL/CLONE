#!/bin/bash

# OpenManus Startup Script
set -e

echo "🚀 Starting OpenManus..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Install Playwright browsers
    echo "🌐 Installing Playwright browsers..."
    playwright install chromium
    
    # Mark dependencies as installed
    touch venv/.dependencies_installed
    echo "✅ Dependencies installed successfully!"
fi

# Check configuration
if [ ! -f "config/config.toml" ]; then
    echo "⚙️ Creating config file from example..."
    cp config/config.example.toml config/config.toml
    echo "⚠️  Please edit config/config.toml and add your API keys before running!"
    exit 1
fi

# Check if API keys are configured
if grep -q "REPLACE_WITH_YOUR_API_KEY" config/config.toml; then
    echo "⚠️  API keys not configured!"
    echo "   Please edit config/config.toml and replace 'REPLACE_WITH_YOUR_API_KEY' with your actual API key"
    echo "   For OpenAI: Get from https://platform.openai.com/api-keys"
    echo "   For Claude: Get from https://console.anthropic.com/"
    exit 1
fi

# Run the application
echo "🎯 Launching OpenManus..."
echo "   Type your prompt when prompted, or Ctrl+C to exit"
echo ""

python main.py