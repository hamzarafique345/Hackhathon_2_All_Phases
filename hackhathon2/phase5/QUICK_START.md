# Quick Start Guide - Todo Application

Get your Todo application running in 3 simple steps!

## 🚀 For First Time Setup

### Prerequisites Check

Before starting, make sure you have:
- ✅ Docker Desktop installed and running
- ✅ Minikube installed
- ✅ Helm installed

**Quick check:**
```bash
docker --version
minikube version
helm version
```

### Step 1: Start Everything

```bash
# Navigate to project folder
cd C:\Officialy Hamza\Test\hackhathon2\phase_4

# Start Minikube
minikube start --driver=docker

# Enable Ingress
minikube addons enable ingress
```

### Step 2: Build and Deploy

```bash
# Build images
cd backend
docker build -t todo-backend:latest .
cd ../frontend
docker build --build-arg NEXT_PUBLIC_API_URL=http://todo.local --build-arg BETTER_AUTH_URL=http://todo.local -t todo-frontend:v4 .
cd ..

# Load into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:v4

# Create secrets (REPLACE WITH YOUR CREDENTIALS!)
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='your-database-url' \
  --from-literal=BETTER_AUTH_SECRET='your-secret' \
  --from-literal=OPENROUTER_API_KEY='your-api-key' \
  --dry-run=client -o yaml | \
kubectl label --local -f - app.kubernetes.io/managed-by=Helm -o yaml | \
kubectl annotate --local -f - meta.helm.sh/release-name=todo-app meta.helm.sh/release-namespace=default -o yaml | \
kubectl apply -f -

# Deploy with Helm
helm install todo-app ./todo-helm-chart
```

### Step 3: Configure Access

```powershell
# Add to hosts file (PowerShell as Admin)
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "`n127.0.0.1 todo.local"

# Start tunnel (keep terminal open)
minikube tunnel
```

### Step 4: Access Application

Open browser: **http://todo.local**

---

## 🔄 Daily Usage (After Restart)

### Simple 3-Step Process

```bash
# 1. Start Minikube
minikube start

# 2. Start tunnel (keep terminal open)
minikube tunnel

# 3. Open browser
# http://todo.local
```

**That's it!** Your application is ready.

---

## 📋 Quick Reference

### Check Status

```bash
# Check if everything is running
kubectl get pods
kubectl get ingress

# Expected output:
# backend-deployment-xxxxx    1/1  Running
# frontend-deployment-xxxxx   1/1  Running
# todo-ingress               nginx  todo.local  192.168.49.2
```

### View Logs

```bash
# Frontend logs
kubectl logs deployment/frontend-deployment --tail=20

# Backend logs
kubectl logs deployment/backend-deployment --tail=20

# Follow logs in real-time
kubectl logs -f deployment/backend-deployment
```

### Restart Application

```bash
# Restart frontend
kubectl rollout restart deployment/frontend-deployment

# Restart backend
kubectl rollout restart deployment/backend-deployment

# Restart both
kubectl rollout restart deployment/frontend-deployment deployment/backend-deployment
```

### Stop Everything

```bash
# Stop tunnel (Ctrl+C in tunnel terminal)

# Stop Minikube (saves state)
minikube stop

# Or delete everything (fresh start next time)
minikube delete
```

---

## 🆘 Quick Troubleshooting

### Can't access http://todo.local?

```bash
# Check hosts file
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"

# Check tunnel is running
# Should see: "Tunnel successfully started"

# Restart browser
```

### Pods not running?

```bash
# Check status
kubectl get pods

# View details
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Restart
kubectl rollout restart deployment/frontend-deployment
```

### Backend errors?

```bash
# Check backend health
curl http://todo.local/health

# Should return: {"status":"healthy",...}

# Check logs
kubectl logs deployment/backend-deployment --tail=50
```

---

## 📱 Access Points

- **Frontend**: http://todo.local
- **Backend Health**: http://todo.local/health
- **Backend API**: http://todo.local/api/*
- **Auth Endpoints**: http://todo.local/auth/*

---

## 🎯 Common Tasks

### Update Frontend Code

```bash
# 1. Make changes to frontend code

# 2. Rebuild image
cd frontend
docker build --build-arg NEXT_PUBLIC_API_URL=http://todo.local --build-arg BETTER_AUTH_URL=http://todo.local -t todo-frontend:v4 .

# 3. Reload into Minikube
minikube image load todo-frontend:v4

# 4. Restart deployment
kubectl rollout restart deployment/frontend-deployment

# 5. Wait for new pod
kubectl get pods -w
```

### Update Backend Code

```bash
# 1. Make changes to backend code

# 2. Rebuild image
cd backend
docker build -t todo-backend:latest .

# 3. Reload into Minikube
minikube image load todo-backend:latest

# 4. Restart deployment
kubectl rollout restart deployment/backend-deployment

# 5. Wait for new pod
kubectl get pods -w
```

### Update Secrets

```bash
# 1. Delete old secret
kubectl delete secret todo-secrets

# 2. Create new secret
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='new-database-url' \
  --from-literal=BETTER_AUTH_SECRET='new-secret' \
  --from-literal=OPENROUTER_API_KEY='new-api-key' \
  --dry-run=client -o yaml | \
kubectl label --local -f - app.kubernetes.io/managed-by=Helm -o yaml | \
kubectl annotate --local -f - meta.helm.sh/release-name=todo-app meta.helm.sh/release-namespace=default -o yaml | \
kubectl apply -f -

# 3. Restart deployments
kubectl rollout restart deployment/frontend-deployment deployment/backend-deployment
```

### Clean Up Old Images

```bash
# Remove old Docker images
docker image prune -a

# Remove specific image
docker rmi todo-frontend:v3
```

---

## 📦 Sharing Your Project

### Create ZIP for Sharing

```bash
# Navigate to parent folder
cd C:\Officialy Hamza\Test\hackhathon2

# Create ZIP (exclude node_modules, venv, .next)
# Use Windows Explorer:
# 1. Right-click phase_4 folder
# 2. Send to → Compressed (zipped) folder
# 3. Name it: todo-app-kubernetes.zip
```

### What to Include in ZIP

**Include:**
- ✅ `backend/` folder (without `venv/`)
- ✅ `frontend/` folder (without `node_modules/`, `.next/`)
- ✅ `todo-helm-chart/` folder
- ✅ `README.md`
- ✅ `KUBERNETES.md`
- ✅ `QUICK_START.md`
- ✅ `.env.example` files

**Exclude:**
- ❌ `node_modules/`
- ❌ `venv/`
- ❌ `.next/`
- ❌ `.env` or `.env.local` (contains secrets!)
- ❌ `__pycache__/`
- ❌ `.git/` (if you want smaller ZIP)

### Clone Instructions for Others

```bash
# 1. Extract ZIP or clone repo
git clone <your-repo-url>
cd phase_4

# 2. Follow KUBERNETES.md "First Time Setup"

# 3. Create their own .env files with their credentials
```

---

## 🔗 Related Documentation

- **Full Setup Guide**: See `KUBERNETES.md`
- **Docker Desktop Guide**: See `DOCKER_DESKTOP_GUIDE.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Original README**: See `README.md`

---

## ⚡ Pro Tips

1. **Keep tunnel terminal open** - Don't close it while using the app
2. **Use `kubectl get pods -w`** - Watch pods in real-time
3. **Check logs first** - Most issues show up in logs
4. **Restart browser** - After editing hosts file
5. **Use Docker Desktop** - Visual way to see containers and images

---

**Need Help?** Check `TROUBLESHOOTING.md` or `KUBERNETES.md` for detailed guides.

**Last Updated**: January 29, 2026
