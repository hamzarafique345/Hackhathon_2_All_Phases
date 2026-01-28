# Docker Desktop Guide - Todo Application

Visual guide to understanding and managing your Todo application in Docker Desktop.

## 📋 Table of Contents

- [Opening Docker Desktop](#opening-docker-desktop)
- [Viewing Containers](#viewing-containers)
- [Viewing Images](#viewing-images)
- [Viewing Logs](#viewing-logs)
- [Monitoring Resources](#monitoring-resources)
- [Managing Images and Containers](#managing-images-and-containers)
- [Troubleshooting with Docker Desktop](#troubleshooting-with-docker-desktop)

---

## 🐳 Opening Docker Desktop

### Step 1: Launch Docker Desktop

1. **Windows**: Click Start Menu → Search "Docker Desktop"
2. **Or**: Click Docker whale icon in system tray
3. **Wait**: For Docker to fully start (whale icon becomes normal)

### Step 2: Verify Docker is Running

**In Docker Desktop:**
- Bottom left should show: "Engine running"
- Green indicator light

**In Terminal:**
```bash
docker ps
# Should work without errors
```

---

## 📦 Viewing Containers

### Navigate to Containers

1. **Click "Containers" in left sidebar**
2. **You'll see:**
   - `minikube` - Your Kubernetes cluster (always running)
   - Status indicators (green = running)

### Understanding the Minikube Container

**What is it?**
- Minikube runs as a Docker container
- Inside this container, Kubernetes runs your application pods
- Think of it as a "container within a container"

**Container Details:**
```
Name: minikube
Image: gcr.io/k8s-minikube/kicbase
Status: Running
Ports: Multiple (for Kubernetes API)
```

### Viewing Container Details

1. **Click on `minikube` container**
2. **Tabs available:**
   - **Logs**: Kubernetes system logs
   - **Inspect**: Container configuration
   - **Stats**: CPU, Memory, Network usage
   - **Files**: Container filesystem

### What You WON'T See

❌ You won't see individual pods (frontend/backend) as separate containers
✅ They run INSIDE the minikube container
✅ Use `kubectl get pods` to see your application pods

---

## 🖼️ Viewing Images

### Navigate to Images

1. **Click "Images" in left sidebar**
2. **You'll see all Docker images**

### Your Application Images

**Look for these images:**

```
todo-frontend:v4
- Size: ~395MB
- Created: [timestamp]
- Used by: Kubernetes frontend pod

todo-backend:latest
- Size: ~700MB
- Created: [timestamp]
- Used by: Kubernetes backend pod
```

### System Images

You'll also see Kubernetes system images:
- `gcr.io/k8s-minikube/kicbase` - Minikube base
- `registry.k8s.io/ingress-nginx/controller` - Ingress controller
- `registry.k8s.io/pause` - Kubernetes pause containers
- `docker.io/library/node` - Node.js base image
- `docker.io/library/python` - Python base image

### Image Actions

**Right-click on an image to:**
- **Run**: Create a container from image
- **Push**: Push to Docker registry
- **Remove**: Delete the image
- **Inspect**: View image details

---

## 📊 Viewing Logs

### Method 1: Docker Desktop (System Logs)

1. **Click "Containers"**
2. **Click on `minikube`**
3. **Click "Logs" tab**
4. **You'll see:** Kubernetes system logs

**What you'll see:**
- Kubernetes API server logs
- kubelet logs
- Container runtime logs

**Limitations:**
- These are system logs, not your application logs
- Not very useful for debugging your app

### Method 2: kubectl (Application Logs) ✅ RECOMMENDED

**Frontend Logs:**
```bash
# Last 50 lines
kubectl logs deployment/frontend-deployment --tail=50

# Follow logs in real-time
kubectl logs -f deployment/frontend-deployment

# All logs
kubectl logs deployment/frontend-deployment
```

**Backend Logs:**
```bash
# Last 50 lines
kubectl logs deployment/backend-deployment --tail=50

# Follow logs in real-time
kubectl logs -f deployment/backend-deployment

# All logs
kubectl logs deployment/backend-deployment
```

**Specific Pod Logs:**
```bash
# Get pod name
kubectl get pods

# View logs
kubectl logs <pod-name>

# Example:
kubectl logs backend-deployment-55bbbd6568-n5485
```

### Understanding Log Output

**Frontend Logs (Next.js):**
```
▲ Next.js 16.1.1
- Local:         http://localhost:3000
- Network:       http://0.0.0.0:3000

✓ Starting...
✓ Ready in 2.3s
```

**Backend Logs (FastAPI):**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     10.244.0.1:47250 - "GET /health HTTP/1.1" 200 OK
```

---

## 📈 Monitoring Resources

### Docker Desktop Resource Monitor

1. **Click "Containers"**
2. **See resource usage:**
   - CPU %
   - Memory usage
   - Network I/O
   - Disk I/O

### Minikube Container Resources

**Typical usage:**
- **CPU**: 10-30% (idle), 50-80% (active)
- **Memory**: 2-4GB
- **Network**: Varies with traffic

### Adjusting Resources

**If performance is slow:**

1. **Settings → Resources**
2. **Adjust:**
   - **CPUs**: 4 recommended (minimum 2)
   - **Memory**: 8GB recommended (minimum 4GB)
   - **Disk**: 20GB minimum
3. **Click "Apply & Restart"**

### Monitoring with kubectl

```bash
# Pod resource usage (requires metrics-server)
kubectl top pods

# Node resource usage
kubectl top nodes

# Describe pod for resource limits
kubectl describe pod <pod-name>
```

---

## 🛠️ Managing Images and Containers

### Removing Old Images

**Why?**
- Free up disk space
- Clean up old versions
- Improve performance

**Method 1: Docker Desktop**
1. Click "Images"
2. Find old image (e.g., `todo-frontend:v3`)
3. Click trash icon
4. Confirm deletion

**Method 2: Command Line**
```bash
# Remove specific image
docker rmi todo-frontend:v3

# Remove all unused images
docker image prune -a

# Remove all unused images (force)
docker image prune -a -f
```

### Managing Containers

**Pause Container:**
```bash
# Pause minikube (saves state)
minikube stop
```

**Resume Container:**
```bash
# Resume minikube
minikube start
```

**Delete Container:**
```bash
# Delete minikube (removes everything)
minikube delete
```

### Cleaning Up

**Remove everything and start fresh:**
```bash
# 1. Delete Minikube
minikube delete

# 2. Remove images
docker rmi todo-frontend:v4 todo-backend:latest

# 3. Clean up unused images
docker image prune -a

# 4. Start fresh
minikube start
# Then follow setup steps again
```

---

## 🔍 Troubleshooting with Docker Desktop

### Issue 1: Docker Desktop Won't Start

**Symptoms:**
- Whale icon stays gray
- "Docker Desktop starting..." forever

**Solutions:**

1. **Restart Docker Desktop:**
   - Right-click whale icon → Quit Docker Desktop
   - Wait 10 seconds
   - Start Docker Desktop again

2. **Restart Computer:**
   - Sometimes Windows needs a restart

3. **Check WSL 2:**
   - Settings → General → Use WSL 2 based engine (should be checked)

4. **Reinstall Docker Desktop:**
   - Uninstall Docker Desktop
   - Download latest version
   - Install again

### Issue 2: Minikube Container Not Running

**Symptoms:**
- No `minikube` container in Docker Desktop
- `kubectl` commands fail

**Solutions:**

```bash
# Check Minikube status
minikube status

# If not running, start it
minikube start

# If fails, delete and recreate
minikube delete
minikube start --driver=docker
```

### Issue 3: High Resource Usage

**Symptoms:**
- Computer is slow
- Docker using too much CPU/Memory

**Solutions:**

1. **Adjust Resources:**
   - Settings → Resources
   - Reduce CPUs to 2
   - Reduce Memory to 4GB

2. **Stop Unused Containers:**
   ```bash
   minikube stop
   ```

3. **Clean Up:**
   ```bash
   docker system prune -a
   ```

### Issue 4: Can't See Application Logs

**Symptoms:**
- Logs tab shows system logs only
- Can't find application logs

**Solution:**

✅ **Use kubectl instead of Docker Desktop:**
```bash
kubectl logs deployment/frontend-deployment --tail=50
kubectl logs deployment/backend-deployment --tail=50
```

### Issue 5: Images Not Showing

**Symptoms:**
- Built images don't appear in Docker Desktop

**Solutions:**

```bash
# List images
docker images

# If missing, rebuild
cd frontend
docker build -t todo-frontend:v4 .

cd ../backend
docker build -t todo-backend:latest .
```

---

## 📊 Docker Desktop Dashboard

### Understanding the Dashboard

**Containers Tab:**
- Shows all running containers
- Minikube container = your Kubernetes cluster
- Click for logs, stats, files

**Images Tab:**
- Shows all Docker images
- Your app images + system images
- Click to run, remove, or inspect

**Volumes Tab:**
- Shows Docker volumes
- Minikube uses volumes for persistent storage

**Dev Environments Tab:**
- Not used for this project

### Useful Dashboard Features

**Search:**
- Search for specific containers/images
- Filter by status (running, stopped)

**Bulk Actions:**
- Select multiple images
- Delete all at once

**Settings:**
- Configure Docker resources
- Enable/disable features
- View diagnostics

---

## 🎯 Best Practices

### 1. Monitor Resource Usage

- Check CPU/Memory regularly
- Adjust resources if needed
- Stop Minikube when not in use

### 2. Clean Up Regularly

```bash
# Weekly cleanup
docker image prune -a
docker system prune
```

### 3. Use kubectl for Logs

- Docker Desktop logs = system logs
- kubectl logs = application logs
- Always use kubectl for debugging

### 4. Keep Docker Desktop Updated

- Check for updates regularly
- Settings → Software Updates
- Update when available

### 5. Backup Important Data

- Export images before major changes
- Keep Helm charts in version control
- Document your configuration

---

## 📝 Quick Reference

### Essential Docker Desktop Shortcuts

- **Ctrl+K**: Quick search
- **Ctrl+,**: Settings
- **Ctrl+R**: Restart Docker Desktop

### Essential Commands

```bash
# Check Docker status
docker ps

# List images
docker images

# View logs
kubectl logs deployment/frontend-deployment

# Check resources
kubectl top pods

# Restart Minikube
minikube stop && minikube start
```

---

## 🔗 Related Documentation

- **Full Setup**: See `KUBERNETES.md`
- **Quick Start**: See `QUICK_START.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`

---

**Last Updated**: January 29, 2026
**Version**: 1.0.0
