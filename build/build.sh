#!/bin/bash

echo "🏗️  Building InventoryPro Lab..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed"
    exit 1
fi

# Build the application
echo "📦 Building Docker container..."
cd "$(dirname "$0")/../deploy"
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully"
    echo "🚀 To start the lab, run: docker-compose up -d"
    echo "🌐 Application will be available at: http://localhost:3206"
else
    echo "❌ Build failed"
    exit 1
fi
