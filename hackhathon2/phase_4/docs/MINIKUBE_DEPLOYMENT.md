# Minikube Deployment Guide

This guide covers deploying the Todo Chatbot application to Minikube using Helm.

## Prerequisites

Before starting, ensure you have completed:
1. ✅ Built Docker images (see [DOCKER_SETUP.md](./DOCKER_SETUP.md))
2. ✅ Loaded images into Minikube
3. ✅ Minikube is running
4. ✅ kubectl is configured to use Minikube context

### Required Information

You'll need the following credentials:
- **DATABASE_URL**: Your Neon PostgreSQL connection string
- **BETTER_AUTH_SECRET**: A secure 32+ character string (must match between frontend and backend)
- **OPENROUTER_API_KEY**: Your OpenRouter API key for AI chatbot functionality

## Deployment Overview

The deployment consists of:
- **Backend Deployment**: FastAPI application (1 replica)
- **Backend Service**: ClusterIP (internal only)
- **Frontend Deployment**: Next.js application (1 replica)
- **Frontend Service**: NodePort (external access on port 30000)
- **ConfigMap**: Non-sensitive configuration
- **Secret**: Sensitive credentials

## Step-by-Step Deployment

### Step 1: Verify Minikube Status

```bash
# Check Minikube status
minikube status
```

**Expected Output:**
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

If not running:
```bash
minikube start
```

### Step 2: Verify Images are Loaded

```bash
# List images in Minikube
minikube image ls | grep todo
```

**Expected Output:**
```
docker.io/library/todo-backend:latest
docker.io/library/todo-frontend:latest
```

If images are missing, load them:
```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Step 3: Create Kubernetes Secret

Create a secret with your actual credentials:

```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='postgresql://username:password@ep-xxx-xxx.neon.tech/dbname?sslmode=require' \
  --from-literal=BETTER_AUTH_SECRET='your-32-character-secret-here-change-this' \
  --from-literal=OPENROUTER_API_KEY='your-openrouter-api-key-here'
```

**Important Notes:**
- Replace the placeholder values with your actual credentials
- DATABASE_URL must be a valid Neon PostgreSQL connection string
- BETTER_AUTH_SECRET must be at least 32 characters
- Keep these credentials secure and never commit them to version control

**Verify secret creation:**
```bash
kubectl get secret todo-secrets
```

**Expected Output:**
```
NAME           TYPE     DATA   AGE
todo-secrets   Opaque   3      5s
```

**View secret details (without revealing values):**
```bash
kubectl describe secret todo-secrets
```

### Step 4: Deploy with Helm

Navigate to the project root directory:
```bash
cd C:\Officialy Hamza\Test\hackhathon2\phase_4
```

Install the Helm chart:
```bash
helm install todo-app ./todo-helm-chart
```

**Expected Output:**
```
NAME: todo-app
LAST DEPLOYED: Tue Jan 28 23:30:00 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

### Step 5: Verify Deployment

Check all resources were created:

```bash
# Check deployments
kubectl get deployments
```

**Expected Output:**
```
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
backend-deployment    1/1     1            1           30s
frontend-deployment   1/1     1            1           30s
```

```bash
# Check pods
kubectl get pods
```

**Expected Output:**
```
NAME                                   READY   STATUS    RESTARTS   AGE
backend-deployment-xxxxx-yyyyy         1/1     Running   0          45s
frontend-deployment-xxxxx-zzzzz        1/1     Running   0          45s
```

```bash
# Check services
kubectl get services
```

**Expected Output:**
```
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
backend-service    ClusterIP   10.96.xxx.xxx   <none>        8000/TCP         1m
frontend-service   NodePort    10.96.xxx.xxx   <none>        3000:30000/TCP   1m
kubernetes         ClusterIP   10.96.0.1       <none>        443/TCP          10m
```

```bash
# Check ConfigMap
kubectl get configmap todo-config
```

```bash
# Check Secret
kubectl get secret todo-secrets
```

### Step 6: Access the Application

Get the frontend URL:

```bash
minikube service frontend-service --url
```

**Expected Output:**
```
http://192.168.49.2:30000
```

**Alternative method:**
```bash
# Get Minikube IP
minikube ip

# Access at: http://<minikube-ip>:30000
# Example: http://192.168.49.2:30000
```

Open the URL in your browser. You should see the Todo Chatbot landing page.

### Step 7: Test the Application

1. **Sign Up**
   - Click "Get Started"
   - Enter email and password
   - Verify you're redirected to dashboard

2. **Create Tasks**
   - Add a new task
   - Mark task as complete
   - Delete a task

3. **Test AI Chatbot**
   - Open the chatbot interface
   - Send a message: "List my tasks"
   - Verify AI responds with your tasks
   - Try: "Create a task to buy groceries"
   - Verify task is created

4. **Sign Out and Sign In**
   - Sign out
   - Sign in with same credentials
   - Verify tasks persist

## Monitoring and Debugging

### View Logs

**Backend logs:**
```bash
# Get pod name
kubectl get pods | grep backend

# View logs
kubectl logs -f backend-deployment-xxxxx-yyyyy

# View last 50 lines
kubectl logs --tail=50 backend-deployment-xxxxx-yyyyy
```

**Frontend logs:**
```bash
# Get pod name
kubectl get pods | grep frontend

# View logs
kubectl logs -f frontend-deployment-xxxxx-zzzzz
```

### Check Pod Status

```bash
# Detailed pod information
kubectl describe pod backend-deployment-xxxxx-yyyyy

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Check Health Probes

```bash
# Backend health check
kubectl exec -it backend-deployment-xxxxx-yyyyy -- curl http://localhost:8000/health

# Frontend health check
kubectl exec -it frontend-deployment-xxxxx-zzzzz -- wget -qO- http://localhost:3000
```

### Resource Usage

```bash
# Check resource usage
kubectl top pods

# Check node resources
kubectl top nodes
```

### Access Pod Shell

```bash
# Backend shell
kubectl exec -it backend-deployment-xxxxx-yyyyy -- /bin/bash

# Frontend shell
kubectl exec -it frontend-deployment-xxxxx-zzzzz -- /bin/sh
```

## Updating the Deployment

### Update Configuration

Edit values.yaml and upgrade:

```bash
# Edit values.yaml
# Change replicas, resources, etc.

# Upgrade deployment
helm upgrade todo-app ./todo-helm-chart
```

### Update Images

After rebuilding images:

```bash
# Rebuild images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Load into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Restart deployments to use new images
kubectl rollout restart deployment/backend-deployment
kubectl rollout restart deployment/frontend-deployment

# Watch rollout status
kubectl rollout status deployment/backend-deployment
kubectl rollout status deployment/frontend-deployment
```

### Update Secrets

```bash
# Delete old secret
kubectl delete secret todo-secrets

# Create new secret with updated values
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='new-value' \
  --from-literal=BETTER_AUTH_SECRET='new-value' \
  --from-literal=OPENROUTER_API_KEY='new-value'

# Restart deployments to pick up new secret
kubectl rollout restart deployment/backend-deployment
kubectl rollout restart deployment/frontend-deployment
```

## Rollback

### View Helm History

```bash
helm history todo-app
```

**Expected Output:**
```
REVISION  UPDATED                   STATUS      CHART           APP VERSION  DESCRIPTION
1         Tue Jan 28 23:30:00 2026  deployed    todo-app-1.0.0  1.0.0        Install complete
2         Tue Jan 28 23:45:00 2026  deployed    todo-app-1.0.0  1.0.0        Upgrade complete
```

### Rollback to Previous Version

```bash
# Rollback to previous revision
helm rollback todo-app

# Rollback to specific revision
helm rollback todo-app 1
```

## Uninstalling

### Remove Helm Release

```bash
# Uninstall the application
helm uninstall todo-app
```

**Expected Output:**
```
release "todo-app" uninstalled
```

### Clean Up Resources

```bash
# Delete secret (if needed)
kubectl delete secret todo-secrets

# Delete ConfigMap (if needed)
kubectl delete configmap todo-config

# Verify all resources are removed
kubectl get all
```

### Stop Minikube

```bash
# Stop Minikube
minikube stop

# Delete Minikube cluster (removes all data)
minikube delete
```

## Troubleshooting

### Issue: Pods in CrashLoopBackOff

**Symptom:** Pods keep restarting

**Diagnosis:**
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Common Causes:**
1. **Invalid DATABASE_URL**
   - Check secret: `kubectl get secret todo-secrets -o yaml`
   - Verify Neon PostgreSQL URL format
   - Test connection from pod shell

2. **Missing Environment Variables**
   - Check deployment: `kubectl describe deployment backend-deployment`
   - Verify all required env vars are set

3. **Application Error**
   - Check logs for Python/Node.js errors
   - Verify PYTHONPATH is set correctly (backend)

**Solution:**
```bash
# Update secret with correct values
kubectl delete secret todo-secrets
kubectl create secret generic todo-secrets --from-literal=DATABASE_URL='correct-url' ...

# Restart deployment
kubectl rollout restart deployment/backend-deployment
```

### Issue: ImagePullBackOff

**Symptom:** Pods can't pull images

**Diagnosis:**
```bash
kubectl describe pod <pod-name>
```

**Solution:**
```bash
# Verify images are in Minikube
minikube image ls | grep todo

# If missing, load images
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Delete pod to force recreation
kubectl delete pod <pod-name>
```

### Issue: Frontend Can't Connect to Backend

**Symptom:** API calls fail with network errors

**Diagnosis:**
```bash
# Check if backend service exists
kubectl get service backend-service

# Test backend from frontend pod
kubectl exec -it frontend-deployment-xxxxx-zzzzz -- wget -qO- http://backend-service:8000/health
```

**Solution:**
1. Verify backend service is running:
   ```bash
   kubectl get pods | grep backend
   kubectl logs backend-deployment-xxxxx-yyyyy
   ```

2. Check NEXT_PUBLIC_API_URL in frontend:
   ```bash
   kubectl describe deployment frontend-deployment | grep NEXT_PUBLIC_API_URL
   ```

3. Should be: `http://backend-service:8000`

### Issue: Can't Access Frontend via Browser

**Symptom:** Browser can't connect to frontend URL

**Diagnosis:**
```bash
# Check Minikube status
minikube status

# Check service
kubectl get service frontend-service

# Get URL
minikube service frontend-service --url
```

**Solution:**
1. Ensure Minikube is running:
   ```bash
   minikube start
   ```

2. Check NodePort is correct (30000):
   ```bash
   kubectl get service frontend-service -o yaml | grep nodePort
   ```

3. Try accessing via Minikube IP:
   ```bash
   curl http://$(minikube ip):30000
   ```

4. Check firewall settings (Windows):
   - Allow port 30000 in Windows Firewall

### Issue: Database Connection Failed

**Symptom:** Backend logs show "could not connect to database"

**Diagnosis:**
```bash
# Check backend logs
kubectl logs backend-deployment-xxxxx-yyyyy | grep -i database

# Check secret
kubectl get secret todo-secrets -o jsonpath='{.data.DATABASE_URL}' | base64 -d
```

**Solution:**
1. Verify DATABASE_URL format:
   ```
   postgresql://username:password@host.neon.tech/dbname?sslmode=require
   ```

2. Test connection from pod:
   ```bash
   kubectl exec -it backend-deployment-xxxxx-yyyyy -- python -c "
   import os
   from sqlalchemy import create_engine
   engine = create_engine(os.getenv('DATABASE_URL'))
   conn = engine.connect()
   print('Connection successful!')
   "
   ```

3. Check Neon PostgreSQL:
   - Ensure database is not paused
   - Verify connection string is correct
   - Check IP allowlist (if configured)

### Issue: Health Checks Failing

**Symptom:** Pods show "Unhealthy" in readiness/liveness probes

**Diagnosis:**
```bash
kubectl describe pod <pod-name> | grep -A 10 "Liveness\|Readiness"
```

**Solution:**
1. Check if application is actually running:
   ```bash
   kubectl logs <pod-name>
   ```

2. Test health endpoint manually:
   ```bash
   # Backend
   kubectl exec -it backend-deployment-xxxxx-yyyyy -- curl http://localhost:8000/health

   # Frontend
   kubectl exec -it frontend-deployment-xxxxx-zzzzz -- wget -qO- http://localhost:3000
   ```

3. Increase initialDelaySeconds if app needs more startup time

### Issue: Out of Resources

**Symptom:** Pods pending with "Insufficient cpu" or "Insufficient memory"

**Diagnosis:**
```bash
kubectl describe pod <pod-name> | grep -A 5 "Events"
kubectl top nodes
```

**Solution:**
1. Reduce resource requests in values.yaml:
   ```yaml
   resources:
     requests:
       cpu: 250m      # Reduced from 500m
       memory: 256Mi  # Reduced from 512Mi
   ```

2. Upgrade deployment:
   ```bash
   helm upgrade todo-app ./todo-helm-chart
   ```

3. Or increase Minikube resources:
   ```bash
   minikube stop
   minikube start --cpus=4 --memory=8192
   ```

## Advanced Configuration

### Custom Values

Create a custom values file:

```yaml
# custom-values.yaml
frontend:
  replicas: 2
  resources:
    requests:
      cpu: 250m
      memory: 256Mi

backend:
  replicas: 2
  resources:
    requests:
      cpu: 250m
      memory: 256Mi
```

Deploy with custom values:
```bash
helm install todo-app ./todo-helm-chart -f custom-values.yaml
```

### Enable Minikube Addons

```bash
# Enable metrics server
minikube addons enable metrics-server

# Enable dashboard
minikube addons enable dashboard

# Access dashboard
minikube dashboard
```

### Port Forwarding (Alternative Access)

Instead of NodePort, use port forwarding:

```bash
# Forward frontend port
kubectl port-forward service/frontend-service 3000:3000

# Access at: http://localhost:3000
```

## Production Considerations

This deployment is optimized for local development and demonstration. For production:

1. **Use Ingress Controller** instead of NodePort
2. **Enable TLS/SSL** with cert-manager
3. **Implement Network Policies** for security
4. **Use External Secrets Operator** for secret management
5. **Enable Horizontal Pod Autoscaling (HPA)**
6. **Configure Persistent Volumes** if needed
7. **Set up monitoring** with Prometheus/Grafana
8. **Implement logging** with ELK stack or similar
9. **Use managed Kubernetes** (EKS, GKE, AKS)
10. **Configure backup and disaster recovery**

## Quick Reference

### Deployment Commands
```bash
# Deploy
helm install todo-app ./todo-helm-chart

# Upgrade
helm upgrade todo-app ./todo-helm-chart

# Rollback
helm rollback todo-app

# Uninstall
helm uninstall todo-app
```

### Monitoring Commands
```bash
# Get all resources
kubectl get all

# Watch pods
kubectl get pods -w

# View logs
kubectl logs -f <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Resource usage
kubectl top pods
kubectl top nodes
```

### Access Commands
```bash
# Get frontend URL
minikube service frontend-service --url

# Port forward
kubectl port-forward service/frontend-service 3000:3000

# Access pod shell
kubectl exec -it <pod-name> -- /bin/bash
```

### Cleanup Commands
```bash
# Uninstall app
helm uninstall todo-app

# Delete secret
kubectl delete secret todo-secrets

# Stop Minikube
minikube stop

# Delete Minikube
minikube delete
```

## Success Checklist

Deployment is successful when:

- ✅ All pods are in "Running" state
- ✅ Health checks are passing (Ready 1/1)
- ✅ Frontend is accessible via browser
- ✅ User can sign up and sign in
- ✅ Tasks can be created, updated, and deleted
- ✅ AI chatbot responds to messages
- ✅ No errors in pod logs
- ✅ Backend can connect to Neon PostgreSQL
- ✅ Frontend can communicate with backend

## Next Steps

After successful deployment:

1. Test all application features thoroughly
2. Monitor logs for any errors
3. Document any issues encountered
4. Consider implementing production enhancements
5. Share deployment URL with stakeholders

## Support

If you encounter issues not covered in this guide:

1. Check pod logs: `kubectl logs <pod-name>`
2. Check events: `kubectl get events`
3. Review [DOCKER_SETUP.md](./DOCKER_SETUP.md) for image issues
4. Verify all prerequisites are met
5. Ensure credentials are correct

---

**Congratulations!** You've successfully deployed the Todo Chatbot application to Kubernetes using Minikube and Helm! 🎉
