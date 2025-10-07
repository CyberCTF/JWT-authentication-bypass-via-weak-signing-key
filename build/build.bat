@echo off

echo 🏗️  Building InventoryPro Lab...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is required but not installed
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is required but not installed
    exit /b 1
)

REM Build the application
echo 📦 Building Docker container...
cd /d "%~dp0\..\deploy"
docker-compose build

if %errorlevel% equ 0 (
    echo ✅ Build completed successfully
    echo 🚀 To start the lab, run: docker-compose up -d
    echo 🌐 Application will be available at: http://localhost:3206
) else (
    echo ❌ Build failed
    exit /b 1
)
