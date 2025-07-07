#!/bin/bash

# OpenManus Deployment Script
set -e

echo "🚀 Starting OpenManus deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p config output

# Check if config file exists
if [ ! -f "config/config.toml" ]; then
    if [ -f "config/config.example.toml" ]; then
        echo "📝 Creating config file from example..."
        cp config/config.example.toml config/config.toml
        echo "⚠️  Please edit config/config.toml and add your API keys before running the application."
        echo "   You need to set your LLM API key in the config file."
    else
        echo "❌ No config example found. Please create config/config.toml manually."
        exit 1
    fi
fi

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "✅ Deployment complete!"
echo ""
echo "To start OpenManus:"
echo "  docker-compose up -d"
echo ""
echo "To run interactively:"
echo "  docker-compose run --rm openmanus"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop:"
echo "  docker-compose down"
echo ""
echo "⚠️  Don't forget to configure your API keys in config/config.toml"