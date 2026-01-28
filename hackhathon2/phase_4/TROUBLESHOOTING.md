# Troubleshooting Guide - Todo Application

Complete troubleshooting guide for common issues with the Kubernetes deployment.

## 📋 Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Connection Issues](#connection-issues)
- [Pod Issues](#pod-issues)
- [Ingress Issues](#ingress-issues)
- [Database Issues](#database-issues)
- [Image Issues](#image-issues)
- [Minikube Issues](#minikube-issues)
- [Docker Desktop Issues](#docker-desktop-issues)
- [Performance Issues](#performance-issues)
- [Complete Reset](#complete-reset)

---

## 🔍 Quick Diagnostics

### Run These Commands First

```bash
# 1. Check Minikube status
minikube status

# 2. Check pods
kubectl get pods

# 3. Check services
kubectl get svc

# 4. Check ingress
kubectl get ingress

# 5. Check if tunnel is running
# Look for terminal with "Tunnel successfully started"
```

### Expected Healthy Output

```
# minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running

# kubectl get pods
NAME                                   READY   STATUS    RESTARTS   AGE
backend-deployment-xxxxx               1/1     Running   0          10m
frontend-deployment-xxxxx              1/1     Running   0          10m

# kubectl get ingress
NAME           CLASS   HOSTS        ADDRESS        PORTS   AGE
todo-ingress   nginx   todo.local   192.168.49.2   80      10m
```

---

## 🌐 Connection Issues

### Issue: Can't Access http://todo.local

**Symptoms:**
- Browser shows "This site can't be reached"
- ERR_NAME_NOT_RESOLVED error
- Page doesn't load

**Diagnostic Steps:**

```bash
# 1. Check hosts file
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"

# 2. Check Ingress
kubectl get ingress todo-ingress

# 3. Check tunnel
# Should have terminal showing "Tunnel successfully started"

# 4. Test with curl
curl -I http://todo.local
```

**Solutions:**

**Solution 1: Fix Hosts File**
```powershell
# Open PowerShell as Administrator
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "`n127.0.0.1 todo.local"

# Verify
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"

# Restart browser
```

**Solution 2: Start Minikube Tunnel**
```bash
# Open new terminal
minikube tunnel

# Keep this terminal open!
```

**Solution 3: Restart Browser**
- Close ALL browser windows
- Clear browser cache (Ctrl+Shift+Delete)
- Reopen browser
- Try http://todo.local again

**Solution 4: Check Firewall**
```bash
# Temporarily disable Windows Firewall
# Control Panel → Windows Defender Firewall → Turn off

# Try accessing again
# If works, add exception for Docker/Minikube
```

### Issue: 503 Service Unavailable

**Symptoms:**
- Browser shows "503 Service Unavailable"
- nginx error page

**Diagnostic Steps:**

```bash
# 1. Check pods are running
kubectl get pods

# 2. Check Ingress backend
kubectl describe ingress todo-ingress

# 3. Check service endpoints
kubectl get endpoints
```

**Solutions:**

**Solution 1: Wait for Pods**
```bash
# Pods might still be starting
kubectl get pods -w

# Wait until both show 1/1 Running
# Press Ctrl+C when ready
```

**Solution 2: Restart Ingress Controller**
```bash
# Restart Ingress
kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx

# Wait 1-2 minutes
kubectl get pods -n ingress-nginx
```

**Solution 3: Recreate Ingress**
```bash
# Delete Ingress
kubectl delete ingress todo-ingress

# Redeploy
helm upgrade todo-app ./todo-helm-chart
```

### Issue: Connection Timeout

**Symptoms:**
- Page loads forever
- Eventually times out
- No error message

**Solutions:**

```bash
# 1. Check if services are accessible internally
kubectl exec deployment/frontend-deployment -- wget -qO- http://backend-service:8000/health

# 2. Check Ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller --tail=50

# 3. Restart everything
kubectl rollout restart deployment/frontend-deployment deployment/backend-deployment
```

---

## 🐳 Pod Issues

### Issue: Pods in CrashLoopBackOff

**Symptoms:**
- `kubectl get pods` shows CrashLoopBackOff
- Pods keep restarting

**Diagnostic Steps:**

```bash
# 1. Check pod status
kubectl get pods

# 2. Describe pod
kubectl describe pod <pod-name>

# 3. Check logs
kubectl logs <pod-name>

# 4. Check previous logs (from crashed container)
kubectl logs <pod-name> --previous
```

**Common Causes & Solutions:**

**Cause 1: Database Connection Failed**
```bash
# Check backend logs
kubectl logs deployment/backend-deployment --tail=50

# Look for: "database connection failed" or similar

# Solution: Fix DATABASE_URL in secret
kubectl delete secret todo-secrets
# Recreate with correct DATABASE_URL (see KUBERNETES.md Step 6)
```

**Cause 2: Missing Environment Variables**
```bash
# Check if secret exists
kubectl get secret todo-secrets

# If missing, create it (see KUBERNETES.md Step 6)
```

**Cause 3: Image Pull Error**
```bash
# Check if images are loaded
minikube image ls | grep todo

# If missing, load images
minikube image load todo-backend:latest
minikube image load todo-frontend:v4
```

**Cause 4: Application Error**
```bash
# Check logs for error details
kubectl logs <pod-name> --previous

# Fix the error in code
# Rebuild image
# Reload into Minikube
# Restart deployment
```

### Issue: Pods Stuck in Pending

**Symptoms:**
- Pods show STATUS: Pending
- Never transition to Running

**Diagnostic Steps:**

```bash
# Describe pod to see why
kubectl describe pod <pod-name>

# Look for "Events" section at bottom
```

**Solutions:**

**Solution 1: Insufficient Resources**
```bash
# Check Minikube resources
minikube status

# Increase resources in Docker Desktop
# Settings → Resources → Increase CPU/Memory

# Restart Minikube
minikube stop
minikube start
```

**Solution 2: Image Pull Issues**
```bash
# Check if image exists
minikube image ls | grep todo

# If missing, load it
minikube image load todo-frontend:v4
```

### Issue: Pods in ImagePullBackOff

**Symptoms:**
- Pods show STATUS: ImagePullBackOff
- Can't pull image

**Solutions:**

```bash
# 1. Check image exists locally
docker images | grep todo

# 2. Load image into Minikube
minikube image load todo-frontend:v4
minikube image load todo-backend:latest

# 3. Update Helm values to use correct tag
# Edit todo-helm-chart/values.yaml
# Ensure tag matches loaded image

# 4. Upgrade deployment
helm upgrade todo-app ./todo-helm-chart

# 5. Delete old pods
kubectl delete pod -l app=frontend
kubectl delete pod -l app=backend
```

---

## 🔀 Ingress Issues

### Issue: Ingress Not Created

**Symptoms:**
- `kubectl get ingress` shows nothing
- Or shows no ADDRESS

**Solutions:**

```bash
# 1. Check if Ingress addon is enabled
minikube addons list | grep ingress

# 2. Enable if disabled
minikube addons enable ingress

# 3. Wait for Ingress controller
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s

# 4. Redeploy
helm upgrade todo-app ./todo-helm-chart
```

### Issue: Ingress Shows No Address

**Symptoms:**
- `kubectl get ingress` shows ADDRESS as empty or pending

**Solutions:**

```bash
# 1. Start Minikube tunnel
minikube tunnel

# 2. Wait 30 seconds

# 3. Check again
kubectl get ingress todo-ingress

# Should show ADDRESS: 192.168.49.2
```

### Issue: Ingress Routes Not Working

**Symptoms:**
- Can access frontend but not backend
- Or vice versa
- 404 errors on some routes

**Diagnostic Steps:**

```bash
# 1. Check Ingress configuration
kubectl describe ingress todo-ingress

# 2. Test each route
curl http://todo.local/
curl http://todo.local/health
curl http://todo.local/api/users/1/tasks

# 3. Check Ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller --tail=50
```

**Solutions:**

```bash
# 1. Verify Ingress rules
kubectl get ingress todo-ingress -o yaml

# 2. Check services exist
kubectl get svc

# 3. Recreate Ingress
kubectl delete ingress todo-ingress
helm upgrade todo-app ./todo-helm-chart
```

---

## 💾 Database Issues

### Issue: Database Connection Failed

**Symptoms:**
- Backend logs show "database connection failed"
- Health check returns error
- Can't sign up/sign in

**Diagnostic Steps:**

```bash
# 1. Check backend logs
kubectl logs deployment/backend-deployment --tail=50

# 2. Check secret exists
kubectl get secret todo-secrets

# 3. Verify DATABASE_URL
kubectl get secret todo-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 -d
```

**Solutions:**

**Solution 1: Fix DATABASE_URL**
```bash
# 1. Delete old secret
kubectl delete secret todo-secrets

# 2. Create new secret with correct URL
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='postgresql://user:pass@host/db?sslmode=require' \
  --from-literal=BETTER_AUTH_SECRET='your-secret' \
  --from-literal=OPENROUTER_API_KEY='your-key' \
  --dry-run=client -o yaml | \
kubectl label --local -f - app.kubernetes.io/managed-by=Helm -o yaml | \
kubectl annotate --local -f - meta.helm.sh/release-name=todo-app meta.helm.sh/release-namespace=default -o yaml | \
kubectl apply -f -

# 3. Restart backend
kubectl rollout restart deployment/backend-deployment
```

**Solution 2: Check Database is Accessible**
```bash
# Test connection from pod
kubectl exec deployment/backend-deployment -- python -c "
import psycopg2
import os
conn = psycopg2.connect(os.environ['DATABASE_URL'])
print('Connected!')
conn.close()
"
```

### Issue: Database SSL Error

**Symptoms:**
- Error: "SSL connection required"
- Connection refused

**Solution:**

```bash
# Ensure DATABASE_URL has sslmode=require
# Example:
# postgresql://user:pass@host/db?sslmode=require

# Update secret with correct URL
kubectl delete secret todo-secrets
# Recreate with sslmode=require in URL
```

---

## 🖼️ Image Issues

### Issue: Image Not Found

**Symptoms:**
- ImagePullBackOff error
- "image not found" in pod description

**Solutions:**

```bash
# 1. Check if image exists locally
docker images | grep todo

# 2. If missing, rebuild
cd frontend
docker build --build-arg NEXT_PUBLIC_API_URL=http://todo.local -t todo-frontend:v4 .

cd ../backend
docker build -t todo-backend:latest .

# 3. Load into Minikube
minikube image load todo-frontend:v4
minikube image load todo-backend:latest

# 4. Verify
minikube image ls | grep todo
```

### Issue: Wrong Image Version

**Symptoms:**
- Old code is running
- Changes not reflected

**Solutions:**

```bash
# 1. Build new image with new tag
docker build -t todo-frontend:v5 .

# 2. Load into Minikube
minikube image load todo-frontend:v5

# 3. Update Helm values
# Edit todo-helm-chart/values.yaml
# Change tag: v4 to tag: v5

# 4. Upgrade deployment
helm upgrade todo-app ./todo-helm-chart

# 5. Verify new pod is running
kubectl get pods
```

### Issue: Image Too Large

**Symptoms:**
- Build takes forever
- Image is several GB

**Solutions:**

```bash
# 1. Check .dockerignore exists
ls frontend/.dockerignore

# 2. If missing, create it
cat > frontend/.dockerignore << EOF
node_modules
.next
.git
.env.local
npm-debug.log*
EOF

# 3. Rebuild image
docker build -t todo-frontend:v4 .

# 4. Check size
docker images | grep todo-frontend
# Should be ~400MB, not GB
```

---

## 🚀 Minikube Issues

### Issue: Minikube Won't Start

**Symptoms:**
- `minikube start` fails
- Error messages about Docker

**Solutions:**

**Solution 1: Check Docker is Running**
```bash
# Verify Docker
docker ps

# If fails, start Docker Desktop
# Wait for it to fully start
```

**Solution 2: Delete and Recreate**
```bash
# Delete Minikube
minikube delete

# Start fresh
minikube start --driver=docker

# Redo setup steps (KUBERNETES.md Steps 4-8)
```

**Solution 3: Check Resources**
```bash
# Increase Docker Desktop resources
# Settings → Resources
# CPUs: 4
# Memory: 8GB

# Restart Docker Desktop
# Try minikube start again
```

### Issue: Minikube Tunnel Fails

**Symptoms:**
- `minikube tunnel` shows errors
- Can't access Ingress

**Solutions:**

```bash
# 1. Stop existing tunnel (Ctrl+C)

# 2. Check Minikube is running
minikube status

# 3. Restart tunnel
minikube tunnel

# 4. If asks for password, enter it
# (Windows may require admin privileges)
```

### Issue: Minikube is Slow

**Symptoms:**
- Commands take forever
- Pods slow to start

**Solutions:**

```bash
# 1. Increase resources
# Docker Desktop → Settings → Resources
# CPUs: 4+
# Memory: 8GB+

# 2. Restart Minikube
minikube stop
minikube start

# 3. Clean up old resources
minikube ssh
docker system prune -a
exit
```

---

## 🐋 Docker Desktop Issues

### Issue: Docker Desktop Won't Start

**Solutions:**

1. **Restart Docker Desktop**
   - Right-click whale icon → Quit
   - Wait 10 seconds
   - Start Docker Desktop

2. **Restart Computer**
   - Sometimes Windows needs a restart

3. **Check WSL 2**
   - Settings → General
   - Ensure "Use WSL 2 based engine" is checked

4. **Reinstall Docker Desktop**
   - Uninstall completely
   - Download latest version
   - Install fresh

### Issue: Docker Using Too Much Resources

**Solutions:**

```bash
# 1. Adjust resource limits
# Settings → Resources
# Reduce CPUs and Memory

# 2. Stop Minikube when not in use
minikube stop

# 3. Clean up
docker system prune -a
```

---

## ⚡ Performance Issues

### Issue: Application is Slow

**Diagnostic Steps:**

```bash
# 1. Check resource usage
kubectl top pods

# 2. Check pod resources
kubectl describe pod <pod-name>

# 3. Check Docker Desktop resources
# Dashboard → Containers → See CPU/Memory
```

**Solutions:**

**Solution 1: Increase Resources**
```bash
# Docker Desktop → Settings → Resources
# CPUs: 4+
# Memory: 8GB+
# Apply & Restart
```

**Solution 2: Optimize Images**
```bash
# Use multi-stage builds (already done)
# Minimize dependencies
# Use .dockerignore
```

**Solution 3: Check Database**
```bash
# Slow queries?
# Check database performance
# Add indexes if needed
```

---

## 🔄 Complete Reset

### When All Else Fails

**Complete cleanup and fresh start:**

```bash
# 1. Delete Minikube
minikube delete

# 2. Remove Docker images
docker rmi todo-frontend:v4 todo-backend:latest

# 3. Clean up Docker
docker system prune -a

# 4. Restart Docker Desktop

# 5. Start fresh
minikube start --driver=docker

# 6. Follow KUBERNETES.md from Step 3
```

---

## 📞 Getting Help

### Collect Diagnostic Information

Before asking for help, collect this info:

```bash
# 1. Minikube status
minikube status > diagnostics.txt

# 2. Pod status
kubectl get pods >> diagnostics.txt

# 3. Pod descriptions
kubectl describe pods >> diagnostics.txt

# 4. Logs
kubectl logs deployment/frontend-deployment --tail=100 >> diagnostics.txt
kubectl logs deployment/backend-deployment --tail=100 >> diagnostics.txt

# 5. Ingress info
kubectl describe ingress todo-ingress >> diagnostics.txt

# 6. Docker info
docker version >> diagnostics.txt
docker ps >> diagnostics.txt
```

Share `diagnostics.txt` when asking for help.

---

## 🔗 Related Documentation

- **Setup Guide**: `KUBERNETES.md`
- **Quick Start**: `QUICK_START.md`
- **Docker Guide**: `DOCKER_DESKTOP_GUIDE.md`

---

**Last Updated**: January 29, 2026
**Version**: 1.0.0
