# Frequently Asked Questions (FAQ)

Common questions and answers about the Todo application Kubernetes deployment.

## 📋 Table of Contents

- [General Questions](#general-questions)
- [Setup Questions](#setup-questions)
- [Daily Usage Questions](#daily-usage-questions)
- [Troubleshooting Questions](#troubleshooting-questions)
- [Docker Desktop Questions](#docker-desktop-questions)
- [Production Questions](#production-questions)

---

## 🎯 General Questions

### Q: What is this project?

**A:** A full-stack Todo application with AI chatbot features, deployed on Kubernetes using Helm and Ingress. It includes:
- Next.js 16 frontend
- FastAPI Python backend
- PostgreSQL database (Neon)
- Kubernetes deployment with Ingress
- Local development with Minikube

### Q: Why use Kubernetes for a Todo app?

**A:** This setup demonstrates production-ready deployment practices:
- ✅ Scalable architecture
- ✅ Easy to deploy to cloud (AWS/GCP/Azure)
- ✅ Industry-standard practices
- ✅ Learning opportunity for Kubernetes
- ✅ Single domain routing with Ingress

### Q: Can I use this in production?

**A:** Yes! The Ingress setup is production-ready. You just need to:
- Replace `todo.local` with your real domain
- Add SSL/TLS certificates
- Use cloud Kubernetes (EKS/GKE/AKS)
- Use managed database
- See KUBERNETES.md "Production Deployment" section

---

## 🚀 Setup Questions

### Q: Do I need to install Kubernetes separately?

**A:** No! Minikube includes Kubernetes. You only need:
- Docker Desktop
- Minikube
- kubectl (comes with Docker Desktop)
- Helm

### Q: How long does initial setup take?

**A:** Approximately 30-45 minutes for first-time setup:
- Installing prerequisites: 10-15 min
- Building Docker images: 15-20 min
- Deploying to Kubernetes: 5-10 min

### Q: Can I skip the Ingress setup?

**A:** Not recommended. Ingress provides:
- Single domain for frontend and backend
- No CORS issues
- Production-ready architecture
- Proper routing

Without Ingress, you'd need NodePort services which aren't production-ready.

### Q: What are the minimum system requirements?

**A:**
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 8GB minimum (16GB recommended)
- **CPU**: 4 cores recommended
- **Disk**: 20GB free space

### Q: Can I use this on Mac or Linux?

**A:** Yes! The setup is similar:
- Mac: Use Homebrew to install tools
- Linux: Use package manager (apt/yum)
- Commands are mostly the same
- Hosts file location differs:
  - Mac/Linux: `/etc/hosts`
  - Windows: `C:\Windows\System32\drivers\etc\hosts`

---

## 🔄 Daily Usage Questions

### Q: Do I need to rebuild images every time I restart?

**A:** No! Once images are loaded into Minikube, they persist. You only need to:
1. Start Minikube: `minikube start`
2. Start tunnel: `minikube tunnel`
3. Access: `http://todo.local`

### Q: Why do I need to keep the tunnel terminal open?

**A:** The Minikube tunnel creates a network route from your localhost to the Kubernetes cluster. Without it, your browser can't reach the Ingress controller.

Think of it like a VPN connection - it needs to stay active.

### Q: Can I close Docker Desktop while the app is running?

**A:** No. Docker Desktop runs the Minikube container, which runs your Kubernetes cluster. Closing Docker Desktop stops everything.

### Q: How do I stop the application?

**A:**
```bash
# Stop tunnel (Ctrl+C in tunnel terminal)

# Stop Minikube (saves state)
minikube stop

# Or delete everything (fresh start next time)
minikube delete
```

### Q: Does stopping Minikube delete my data?

**A:** No. `minikube stop` saves the state. Your deployments, pods, and data persist.

`minikube delete` removes everything - use only for fresh start.

---

## 🔍 Troubleshooting Questions

### Q: Why can't I access http://todo.local?

**A:** Check these in order:
1. **Hosts file**: `Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"`
2. **Tunnel running**: Look for terminal with "Tunnel successfully started"
3. **Pods running**: `kubectl get pods` - both should be 1/1 Running
4. **Ingress exists**: `kubectl get ingress` - should show todo-ingress
5. **Restart browser**: Close all windows and reopen

### Q: Pods are in CrashLoopBackOff - what do I do?

**A:**
```bash
# Check logs for error
kubectl logs <pod-name>

# Common causes:
# 1. Wrong DATABASE_URL - recreate secret
# 2. Missing environment variables - check secret exists
# 3. Image not loaded - reload image into Minikube
```

See TROUBLESHOOTING.md for detailed solutions.

### Q: Frontend shows "An error occurred" - how to fix?

**A:**
```bash
# 1. Check backend is accessible
curl http://todo.local/health

# 2. Check frontend logs
kubectl logs deployment/frontend-deployment --tail=50

# 3. Check backend logs
kubectl logs deployment/backend-deployment --tail=50

# 4. Verify Ingress routing
kubectl describe ingress todo-ingress
```

### Q: How do I see what's wrong with my pod?

**A:**
```bash
# Get pod name
kubectl get pods

# Describe pod (shows events and errors)
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# View previous logs (if pod crashed)
kubectl logs <pod-name> --previous
```

---

## 🐳 Docker Desktop Questions

### Q: Where are my application containers in Docker Desktop?

**A:** Your application pods run INSIDE the `minikube` container. You won't see them as separate containers in Docker Desktop.

To see your pods: `kubectl get pods`

### Q: Why is Docker Desktop using so much memory?

**A:** Minikube runs a full Kubernetes cluster, which needs resources. You can adjust:
- Docker Desktop → Settings → Resources
- Reduce CPUs to 2-4
- Reduce Memory to 4-8GB

### Q: Can I see my application logs in Docker Desktop?

**A:** Docker Desktop shows Kubernetes system logs, not your application logs.

For application logs, use:
```bash
kubectl logs deployment/frontend-deployment
kubectl logs deployment/backend-deployment
```

### Q: How do I clean up old Docker images?

**A:**
```bash
# Remove all unused images
docker image prune -a

# Remove specific image
docker rmi todo-frontend:v3

# Check remaining images
docker images
```

---

## 🚀 Production Questions

### Q: How do I deploy this to AWS/GCP/Azure?

**A:** See KUBERNETES.md "Production Deployment" section. Summary:
1. Push images to container registry (ECR/GCR/ACR)
2. Update Helm values with registry URLs
3. Update Ingress with real domain
4. Add SSL/TLS certificates
5. Deploy to cloud Kubernetes cluster
6. Update DNS to point to load balancer

### Q: Do I need to change the code for production?

**A:** Minimal changes needed:
1. **Frontend**: Rebuild with production domain
   ```bash
   docker build --build-arg NEXT_PUBLIC_API_URL=https://yourdomain.com -t frontend:v1 .
   ```
2. **Backend**: No code changes needed
3. **Secrets**: Use production credentials
4. **Ingress**: Update with real domain and SSL

### Q: How do I add SSL/TLS certificates?

**A:** Use cert-manager:
```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Update Ingress with TLS section (see KUBERNETES.md)
```

### Q: Can I use a different database?

**A:** Yes! Just update the DATABASE_URL secret:
```bash
kubectl delete secret todo-secrets
# Recreate with new DATABASE_URL
```

The backend works with any PostgreSQL database.

### Q: How do I scale the application?

**A:**
```bash
# Scale frontend to 3 replicas
kubectl scale deployment/frontend-deployment --replicas=3

# Scale backend to 2 replicas
kubectl scale deployment/backend-deployment --replicas=2

# Or update Helm values and upgrade
```

---

## 💡 Tips & Tricks

### Q: How can I make startup faster?

**A:** Create a startup script (already provided: `start-todo.bat`):
- Double-click to start everything
- Keeps tunnel terminal open automatically

### Q: How do I update my code changes?

**A:**
```bash
# 1. Make code changes
# 2. Rebuild image
docker build -t todo-frontend:v5 .

# 3. Load into Minikube
minikube image load todo-frontend:v5

# 4. Update Helm values (change tag to v5)
# 5. Upgrade deployment
helm upgrade todo-app ./todo-helm-chart
```

### Q: Can I use a different port instead of 80?

**A:** Yes, but you'd need to:
1. Update Ingress to use different port
2. Update hosts file: `127.0.0.1:8080 todo.local`
3. Access: `http://todo.local:8080`

Not recommended - port 80 is standard for HTTP.

### Q: How do I backup my deployment?

**A:**
```bash
# Export all resources
kubectl get all -o yaml > backup.yaml

# Export secrets (be careful - contains sensitive data)
kubectl get secret todo-secrets -o yaml > secrets-backup.yaml

# Export Ingress
kubectl get ingress todo-ingress -o yaml > ingress-backup.yaml
```

### Q: Can I run multiple Todo apps on the same Minikube?

**A:** Yes! Use different namespaces:
```bash
# Create namespace
kubectl create namespace todo-app-2

# Deploy to namespace
helm install todo-app-2 ./todo-helm-chart --namespace todo-app-2

# Update Ingress with different host (todo2.local)
```

---

## 🔗 Related Documentation

- **Setup Guide**: KUBERNETES.md
- **Quick Start**: QUICK_START.md
- **Troubleshooting**: TROUBLESHOOTING.md
- **Docker Guide**: DOCKER_DESKTOP_GUIDE.md

---

## ❓ Still Have Questions?

1. **Check other documentation files** - Most questions are answered there
2. **Search in TROUBLESHOOTING.md** - Common issues and solutions
3. **Run diagnostic commands** - Often reveals the issue
4. **Check logs** - `kubectl logs` shows what's happening

---

**Last Updated**: January 29, 2026
**Version**: 1.0.0
