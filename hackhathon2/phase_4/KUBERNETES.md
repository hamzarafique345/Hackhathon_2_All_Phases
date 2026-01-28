# Kubernetes Deployment Guide - Todo Application

Complete guide for deploying the Todo application on Kubernetes with Ingress.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [First Time Setup](#first-time-setup)
- [Daily Usage](#daily-usage)
- [Docker Desktop Guide](#docker-desktop-guide)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## 🎯 Overview

This guide covers deploying the Todo application using:
- **Kubernetes** (via Minikube)
- **Helm** (package manager)
- **Ingress** (single domain routing)
- **Docker Desktop** (container runtime)

### Architecture

```
Browser → http://todo.local
    ↓
Ingress Controller (nginx)
    ├─ /api/*   → Backend Service → Backend Pod (FastAPI)
    ├─ /auth/*  → Backend Service → Backend Pod (FastAPI)
    ├─ /health  → Backend Service → Backend Pod (FastAPI)
    └─ /*       → Frontend Service → Frontend Pod (Next.js)
```

---

## 📦 Prerequisites

### Required Software

1. **Docker Desktop** (Latest)
   - Download: https://www.docker.com/products/docker-desktop
   - Enable Kubernetes in Settings

2. **Minikube** (Latest)
   - Download: https://minikube.sigs.k8s.io/docs/start/
   - Windows: `choco install minikube` or download installer

3. **kubectl** (Comes with Docker Desktop)
   - Verify: `kubectl version --client`

4. **Helm** (v3.x)
   - Download: https://helm.sh/docs/intro/install/
   - Windows: `choco install kubernetes-helm`

### System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 20GB free space
- **CPU**: 4 cores recommended

---

## 🚀 First Time Setup

### Step 1: Start Docker Desktop

1. Open Docker Desktop
2. Wait for Docker to start (whale icon in system tray)
3. Verify: `docker ps` (should work without errors)

### Step 2: Start Minikube

```bash
# Start Minikube with Docker driver
minikube start --driver=docker

# Verify status
minikube status
```

**Expected output:**
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

### Step 3: Enable Ingress

```bash
# Enable Ingress addon
minikube addons enable ingress

# Wait for Ingress controller (takes 1-2 minutes)
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s
```

### Step 4: Build Docker Images

```bash
# Navigate to project root
cd C:\Officialy Hamza\Test\hackhathon2\phase_4

# Build backend
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend with correct URL
cd frontend
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://todo.local \
  --build-arg BETTER_AUTH_URL=http://todo.local \
  -t todo-frontend:v4 .
cd ..
```

### Step 5: Load Images into Minikube

```bash
# Load backend
minikube image load todo-backend:latest

# Load frontend
minikube image load todo-frontend:v4

# Verify
minikube image ls | grep todo
```

**Expected output:**
```
docker.io/library/todo-backend:latest
docker.io/library/todo-frontend:v4
```

### Step 6: Create Kubernetes Secrets

**⚠️ IMPORTANT:** Replace placeholder values with your actual credentials!

```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='postgresql://username:password@host/database?sslmode=require' \
  --from-literal=BETTER_AUTH_SECRET='your-32-character-secret-here' \
  --from-literal=OPENROUTER_API_KEY='your-openrouter-api-key' \
  --dry-run=client -o yaml | \
kubectl label --local -f - app.kubernetes.io/managed-by=Helm -o yaml | \
kubectl annotate --local -f - \
  meta.helm.sh/release-name=todo-app \
  meta.helm.sh/release-namespace=default \
  -o yaml | \
kubectl apply -f -
```

**How to get your credentials:**

1. **DATABASE_URL**:
   - Sign up at https://neon.tech
   - Create a database
   - Copy connection string

2. **BETTER_AUTH_SECRET**:
   - Generate: `openssl rand -hex 32`
   - Or use: https://generate-secret.vercel.app/32

3. **OPENROUTER_API_KEY**:
   - Sign up at https://openrouter.ai
   - Get API key from dashboard

### Step 7: Deploy with Helm

```bash
# Deploy application
helm install todo-app ./todo-helm-chart

# Verify deployment
kubectl get pods
kubectl get svc
kubectl get ingress
```

**Wait for pods to be Running (1-2 minutes):**
```bash
kubectl get pods -w
```

Press `Ctrl+C` when both pods show `1/1 Running`.

### Step 8: Add todo.local to Hosts File

**Open PowerShell as Administrator:**

```powershell
# Add entry
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "`n127.0.0.1 todo.local"

# Verify
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"
```

**Expected output:**
```
127.0.0.1 todo.local
```

### Step 9: Start Minikube Tunnel

**Open a NEW terminal and keep it open:**

```bash
minikube tunnel
```

**Expected output:**
```
✓ Tunnel successfully started

NOTE: Please do not close this terminal as this process must stay alive...
```

**⚠️ IMPORTANT:** Keep this terminal open while using the application!

### Step 10: Access Application

**Open your browser:**

```
http://todo.local
```

You should see the Todo application! 🎉

---

## 🔄 Daily Usage (After Restart)

### Quick Start (3 Steps)

When you restart your laptop, follow these steps:

#### 1. Start Docker Desktop

- Open Docker Desktop
- Wait for it to fully start

#### 2. Start Minikube

```bash
minikube start
```

#### 3. Start Minikube Tunnel

**Open terminal and keep it open:**

```bash
minikube tunnel
```

#### 4. Access Application

```
http://todo.local
```

### Quick Start Script

Create `start-todo.bat` in project root:

```batch
@echo off
echo ========================================
echo   Todo Application - Quick Start
echo ========================================
echo.

echo [1/3] Starting Minikube...
minikube start
if errorlevel 1 (
    echo ERROR: Failed to start Minikube
    pause
    exit /b 1
)

echo.
echo [2/3] Checking deployment status...
kubectl get pods
kubectl get ingress

echo.
echo [3/3] Starting Minikube Tunnel...
echo.
echo ========================================
echo   IMPORTANT: Keep this window open!
echo ========================================
echo.
echo Application will be available at:
echo   http://todo.local
echo.
echo Press Ctrl+C to stop the tunnel
echo ========================================
echo.

minikube tunnel
```

**Usage:** Double-click `start-todo.bat`

---

## 🐳 Docker Desktop Guide

### Viewing Containers

1. **Open Docker Desktop**
2. **Click "Containers" tab**
3. **You'll see:**
   - `minikube` - Main Kubernetes cluster container
   - Inside minikube, your pods run

### Viewing Images

1. **Click "Images" tab**
2. **You'll see:**
   - `todo-frontend:v4` - Your frontend image (395MB)
   - `todo-backend:latest` - Your backend image (700MB)
   - System images (nginx, kubernetes, etc.)

### Viewing Logs

**Method 1: Docker Desktop**
1. Click "Containers"
2. Click on `minikube`
3. Click "Logs" tab
4. See Kubernetes system logs

**Method 2: kubectl (Better for app logs)**
```bash
# Frontend logs
kubectl logs deployment/frontend-deployment --tail=50

# Backend logs
kubectl logs deployment/backend-deployment --tail=50

# Follow logs in real-time
kubectl logs -f deployment/backend-deployment
```

### Resource Usage

**In Docker Desktop:**
1. Click "Containers"
2. See CPU and Memory usage
3. Monitor performance

**Via kubectl:**
```bash
# Get resource usage (if metrics-server enabled)
kubectl top pods

# Describe pod for detailed info
kubectl describe pod <pod-name>
```

### Managing Resources

**Adjust Docker Desktop Resources:**
1. Settings → Resources
2. Adjust:
   - CPUs: 4 recommended
   - Memory: 8GB recommended
   - Disk: 20GB minimum

**Clean Up Old Images:**
```bash
# Remove unused images
docker image prune -a

# Remove specific image
docker rmi todo-frontend:v3
```

---

## 🔍 Troubleshooting

### Issue 1: Can't Access http://todo.local

**Symptoms:**
- Browser shows "Can't reach this site"
- ERR_NAME_NOT_RESOLVED

**Solutions:**

```bash
# 1. Check hosts file
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"
# Should show: 127.0.0.1 todo.local

# 2. Check minikube tunnel is running
# You should have a terminal showing "Tunnel successfully started"

# 3. Check Ingress
kubectl get ingress todo-ingress
# Should show ADDRESS: 192.168.49.2

# 4. Restart browser
# Close all browser windows and reopen
```

### Issue 2: Pods Not Running

**Symptoms:**
- `kubectl get pods` shows CrashLoopBackOff or Error

**Solutions:**

```bash
# Check pod status
kubectl get pods

# Describe pod for details
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Common fixes:
# - Recreate secrets (Step 6)
# - Rebuild images (Step 4-5)
# - Restart deployment:
kubectl rollout restart deployment/frontend-deployment
kubectl rollout restart deployment/backend-deployment
```

### Issue 3: Ingress Not Working

**Symptoms:**
- Pods running but can't access via todo.local
- 503 Service Unavailable

**Solutions:**

```bash
# Check Ingress controller
kubectl get pods -n ingress-nginx

# Should show ingress-nginx-controller as Running

# If not running, restart Ingress:
minikube addons disable ingress
minikube addons enable ingress

# Wait 2 minutes, then check:
kubectl get pods -n ingress-nginx
```

### Issue 4: Frontend Shows Errors

**Symptoms:**
- "An error occurred. Please try again later."
- Console shows network errors

**Solutions:**

```bash
# 1. Check backend is accessible
curl http://todo.local/health
# Should return: {"status":"healthy",...}

# 2. Check frontend logs
kubectl logs deployment/frontend-deployment --tail=50

# 3. Check backend logs
kubectl logs deployment/backend-deployment --tail=50

# 4. Verify Ingress routing
kubectl describe ingress todo-ingress
```

### Issue 5: Database Connection Error

**Symptoms:**
- Backend logs show "database connection failed"
- Health check returns error

**Solutions:**

```bash
# 1. Check secret exists
kubectl get secret todo-secrets

# 2. Verify DATABASE_URL is correct
kubectl get secret todo-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 -d

# 3. Recreate secret with correct URL
kubectl delete secret todo-secrets
# Then run Step 6 again with correct DATABASE_URL
```

### Issue 6: Minikube Won't Start

**Symptoms:**
- `minikube start` fails
- Docker errors

**Solutions:**

```bash
# 1. Check Docker is running
docker ps

# 2. Delete and recreate Minikube
minikube delete
minikube start --driver=docker

# 3. If still fails, check Docker Desktop:
# - Restart Docker Desktop
# - Check Settings → Resources
# - Ensure WSL 2 is enabled (Windows)
```

### Issue 7: Images Not Loading

**Symptoms:**
- Pods show ImagePullBackOff
- Can't find image

**Solutions:**

```bash
# 1. Check images in Minikube
minikube image ls | grep todo

# 2. If missing, reload images
minikube image load todo-backend:latest
minikube image load todo-frontend:v4

# 3. Restart deployment
kubectl rollout restart deployment/frontend-deployment
kubectl rollout restart deployment/backend-deployment
```

---

## 📝 Useful Commands

### Kubernetes Commands

```bash
# View all resources
kubectl get all

# View pods with details
kubectl get pods -o wide

# View services
kubectl get svc

# View ingress
kubectl get ingress

# Describe resource (detailed info)
kubectl describe pod <pod-name>
kubectl describe ingress todo-ingress

# View logs
kubectl logs <pod-name>
kubectl logs deployment/frontend-deployment --tail=50
kubectl logs -f deployment/backend-deployment  # Follow logs

# Execute command in pod
kubectl exec -it <pod-name> -- sh
kubectl exec deployment/backend-deployment -- env

# Delete pod (auto-recreates)
kubectl delete pod <pod-name>

# Restart deployment
kubectl rollout restart deployment/frontend-deployment

# Check deployment status
kubectl rollout status deployment/frontend-deployment
```

### Helm Commands

```bash
# List releases
helm list

# Get release info
helm status todo-app

# Get values
helm get values todo-app

# Upgrade release
helm upgrade todo-app ./todo-helm-chart

# Rollback to previous version
helm rollback todo-app

# Uninstall release
helm uninstall todo-app

# View history
helm history todo-app
```

### Minikube Commands

```bash
# Start Minikube
minikube start

# Stop Minikube (saves state)
minikube stop

# Delete Minikube (removes everything)
minikube delete

# Get Minikube IP
minikube ip

# SSH into Minikube
minikube ssh

# View dashboard
minikube dashboard

# List addons
minikube addons list

# Enable addon
minikube addons enable <addon-name>

# Check status
minikube status

# View logs
minikube logs
```

### Docker Commands

```bash
# List images
docker images

# List containers
docker ps
docker ps -a  # Include stopped

# Build image
docker build -t <name>:<tag> .

# Remove image
docker rmi <image-name>:<tag>

# Remove all unused images
docker image prune -a

# View image details
docker inspect <image-name>

# Check Docker version
docker version
```

---

## 🚀 Production Deployment

### Deploying to Cloud (AWS EKS / GCP GKE / Azure AKS)

#### Step 1: Prepare Images

```bash
# Tag images for registry
docker tag todo-frontend:v4 your-registry/todo-frontend:v1
docker tag todo-backend:latest your-registry/todo-backend:v1

# Push to registry
docker push your-registry/todo-frontend:v1
docker push your-registry/todo-backend:v1
```

#### Step 2: Update Helm Values

Edit `todo-helm-chart/values.yaml`:

```yaml
frontend:
  image:
    repository: your-registry/todo-frontend
    tag: v1
    pullPolicy: Always

backend:
  image:
    repository: your-registry/todo-backend
    tag: v1
    pullPolicy: Always
```

#### Step 3: Update Ingress for Production

Edit `todo-helm-chart/templates/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - todo.yourdomain.com
    secretName: todo-tls
  rules:
  - host: todo.yourdomain.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
      - path: /auth
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
      - path: /health
        pathType: Exact
        backend:
          service:
            name: backend-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 3000
```

#### Step 4: Install cert-manager (for SSL)

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

#### Step 5: Deploy to Production

```bash
# Set kubectl context to production
kubectl config use-context production-cluster

# Create namespace
kubectl create namespace todo-app

# Create secrets in production
kubectl create secret generic todo-secrets \
  --namespace todo-app \
  --from-literal=DATABASE_URL='production-db-url' \
  --from-literal=BETTER_AUTH_SECRET='production-secret' \
  --from-literal=OPENROUTER_API_KEY='production-api-key'

# Deploy with Helm
helm install todo-app ./todo-helm-chart --namespace todo-app

# Verify
kubectl get pods -n todo-app
kubectl get ingress -n todo-app
```

#### Step 6: Configure DNS

```bash
# Get load balancer IP
kubectl get ingress todo-ingress -n todo-app

# Add A record in your DNS provider:
# todo.yourdomain.com → <LOAD_BALANCER_IP>
```

---

## 📚 Additional Resources

- **Kubernetes Docs**: https://kubernetes.io/docs/
- **Helm Docs**: https://helm.sh/docs/
- **Minikube Docs**: https://minikube.sigs.k8s.io/docs/
- **Ingress Nginx**: https://kubernetes.github.io/ingress-nginx/

---

**Last Updated**: January 29, 2026
**Version**: 1.0.0
