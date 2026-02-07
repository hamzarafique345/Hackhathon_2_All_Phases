@echo off
REM ========================================
REM   Todo Application - Quick Start Script
REM   Kubernetes Deployment with Ingress
REM ========================================

echo.
echo ========================================
echo   Todo Application - Starting...
echo ========================================
echo.

REM Check if Docker is running
echo [1/4] Checking Docker Desktop...
docker ps >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    echo.
    pause
    exit /b 1
)
echo ✓ Docker Desktop is running
echo.

REM Start Minikube
echo [2/4] Starting Minikube...
minikube start --driver=docker
if errorlevel 1 (
    echo ERROR: Failed to start Minikube
    echo Try running: minikube delete
    echo Then run this script again
    echo.
    pause
    exit /b 1
)
echo ✓ Minikube started successfully
echo.

REM Check deployment status
echo [3/4] Checking deployment status...
kubectl get pods
echo.
kubectl get ingress
echo.

REM Check if pods are running
kubectl get pods | findstr "Running" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Pods are not running yet
    echo This might be the first time setup
    echo Please follow KUBERNETES.md for complete setup
    echo.
    pause
    exit /b 1
)

echo ✓ Pods are running
echo.

REM Start Minikube Tunnel
echo [4/4] Starting Minikube Tunnel...
echo.
echo ========================================
echo   IMPORTANT: Keep this window open!
echo ========================================
echo.
echo Your application is available at:
echo   http://todo.local
echo.
echo Press Ctrl+C to stop the tunnel
echo ========================================
echo.

minikube tunnel

REM This line only runs if tunnel is stopped
echo.
echo Tunnel stopped. Application is no longer accessible.
echo Run this script again to restart.
pause
