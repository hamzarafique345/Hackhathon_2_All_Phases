# Phase 4: Quick Command Reference

This document provides all commands needed to deploy the Todo Chatbot application to Minikube.

## Prerequisites Check

```bash
# Verify all tools are installed
docker --version
minikube version
kubectl version --client
helm version
```

## Complete Deployment Flow

### Step 1: Build Docker Images

```bash
# Navigate to project root
cd C:\Officialy Hamza\Test\hackhathon2\phase_4

# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image
docker build -t todo-frontend:latest ./frontend

# Verify images
docker images | grep todo
```

### Step 2: Start Minikube

```bash
# Start Minikube
minikube start

# Verify status
minikube status
```

### Step 3: Load Images into Minikube

```bash
# Load backend image
minikube image load todo-backend:latest

# Load frontend image
minikube image load todo-frontend:latest

# Verify images in Minikube
minikube image ls | grep todo
```

### Step 4: Create Kubernetes Secret

```bash
# Create secret with your actual credentials
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='postgresql://neondb_owner:npg_YOJCdEGxT81D@ep-gentle-salad-a4zjmszl-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require' \
  --from-literal=BETTER_AUTH_SECRET='55ffea195578f78e86aed40a107690c23c7c8f08cc4504fea8d9dedd7bc56794' \
  --from-literal=OPENROUTER_API_KEY='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'

# Verify secret
kubectl get secret todo-secrets
```

### Step 5: Deploy with Helm

```bash
# Install Helm chart
helm install todo-app ./todo-helm-chart

# Verify deployment
kubectl get all
```

### Step 6: Access Application

```bash
# Get frontend URL
minikube service frontend-service --url

# Open in browser
# Navigate to: http://<minikube-ip>:30000
```

## Monitoring Commands

```bash
# Check pod status
kubectl get pods

# View backend logs
kubectl logs -f deployment/backend-deployment

# View frontend logs
kubectl logs -f deployment/frontend-deployment

# Check all resources
kubectl get all

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Resource usage
kubectl top pods
kubectl top nodes
```

## Update Commands

```bash
# Rebuild and reload images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Restart deployments
kubectl rollout restart deployment/backend-deployment
kubectl rollout restart deployment/frontend-deployment

# Watch rollout status
kubectl rollout status deployment/backend-deployment
kubectl rollout status deployment/frontend-deployment
```

## Helm Management

```bash
# Upgrade deployment
helm upgrade todo-app ./todo-helm-chart

# View history
helm history todo-app

# Rollback
helm rollback todo-app

# Uninstall
helm uninstall todo-app
```

## Cleanup Commands

```bash
# Uninstall application
helm uninstall todo-app

# Delete secret
kubectl delete secret todo-secrets

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Troubleshooting Commands

```bash
# Describe pod (shows events and errors)
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>

# Get previous pod logs (if crashed)
kubectl logs <pod-name> --previous

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Test backend health from frontend pod
kubectl exec -it <frontend-pod> -- wget -qO- http://backend-service:8000/health

# Check secret values (base64 encoded)
kubectl get secret todo-secrets -o yaml

# Port forward (alternative access)
kubectl port-forward service/frontend-service 3000:3000
```

## Quick Test Flow

```bash
# 1. Build images
docker build -t todo-backend:latest ./backend && docker build -t todo-frontend:latest ./frontend

# 2. Start Minikube and load images
minikube start && minikube image load todo-backend:latest && minikube image load todo-frontend:latest

# 3. Create secret (replace with your values)
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='your-db-url' \
  --from-literal=BETTER_AUTH_SECRET='your-secret' \
  --from-literal=OPENROUTER_API_KEY='your-api-key'

# 4. Deploy
helm install todo-app ./todo-helm-chart

# 5. Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=60s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=60s

# 6. Get URL and open in browser
minikube service frontend-service --url
```

## Environment Variables Reference

### Backend Environment Variables
- `DATABASE_URL` - Neon PostgreSQL connection string (Secret)
- `BETTER_AUTH_SECRET` - Authentication secret (Secret)
- `OPENROUTER_API_KEY` - AI API key (Secret)
- `JWT_ALGORITHM` - JWT algorithm (ConfigMap)
- `FRONTEND_URL` - Frontend URL for CORS (ConfigMap)
- `API_BASE_URL` - Backend URL (ConfigMap)

### Frontend Environment Variables
- `BETTER_AUTH_SECRET` - Authentication secret (Secret)
- `BETTER_AUTH_URL` - Frontend URL (values.yaml)
- `NEXT_PUBLIC_API_URL` - Backend API URL (values.yaml)

## Common Issues and Solutions

### Issue: ImagePullBackOff
```bash
# Solution: Load images into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
kubectl delete pod <pod-name>  # Force recreation
```

### Issue: CrashLoopBackOff
```bash
# Solution: Check logs and fix configuration
kubectl logs <pod-name>
kubectl describe pod <pod-name>
# Update secret if needed, then restart
kubectl rollout restart deployment/<deployment-name>
```

### Issue: Can't access frontend
```bash
# Solution: Get correct URL
minikube service frontend-service --url
# Or use port forwarding
kubectl port-forward service/frontend-service 3000:3000
```

### Issue: Backend connection failed
```bash
# Solution: Verify backend is running and accessible
kubectl get pods | grep backend
kubectl logs deployment/backend-deployment
kubectl exec -it <frontend-pod> -- wget -qO- http://backend-service:8000/health
```

## Success Verification

Run these commands to verify successful deployment:

```bash
# 1. All pods running
kubectl get pods
# Expected: All pods in "Running" state with "1/1" ready

# 2. Services created
kubectl get services
# Expected: frontend-service (NodePort) and backend-service (ClusterIP)

# 3. Backend health check
kubectl exec -it deployment/backend-deployment -- curl http://localhost:8000/health
# Expected: {"status":"healthy",...}

# 4. Frontend accessible
curl http://$(minikube ip):30000
# Expected: HTML response

# 5. No errors in logs
kubectl logs deployment/backend-deployment --tail=20
kubectl logs deployment/frontend-deployment --tail=20
# Expected: No error messages
```

## Complete Teardown

```bash
# Remove everything
helm uninstall todo-app
kubectl delete secret todo-secrets
kubectl delete configmap todo-config
minikube stop
minikube delete

# Remove Docker images (optional)
docker rmi todo-backend:latest todo-frontend:latest
```

---

For detailed documentation, see:
- [DOCKER_SETUP.md](./DOCKER_SETUP.md) - Docker image building and testing
- [MINIKUBE_DEPLOYMENT.md](./MINIKUBE_DEPLOYMENT.md) - Complete deployment guide
- [todo-helm-chart/README.md](../todo-helm-chart/README.md) - Helm chart documentation
