# Setup Verification Checklist

Use this checklist to verify your Todo application is set up correctly.

## ✅ Pre-Setup Verification

### Software Installation

- [ ] **Docker Desktop installed**
  ```bash
  docker --version
  # Should show: Docker version 20.x or higher
  ```

- [ ] **Docker Desktop is running**
  ```bash
  docker ps
  # Should work without errors
  ```

- [ ] **Minikube installed**
  ```bash
  minikube version
  # Should show: minikube version: v1.x or higher
  ```

- [ ] **kubectl installed**
  ```bash
  kubectl version --client
  # Should show client version
  ```

- [ ] **Helm installed**
  ```bash
  helm version
  # Should show: version.BuildInfo{Version:"v3.x"}
  ```

---

## ✅ Initial Setup Verification

### Step 1: Minikube

- [ ] **Minikube started successfully**
  ```bash
  minikube start --driver=docker
  # Should complete without errors
  ```

- [ ] **Minikube is running**
  ```bash
  minikube status
  # Should show all components Running
  ```

### Step 2: Ingress

- [ ] **Ingress addon enabled**
  ```bash
  minikube addons list | grep ingress
  # Should show: ingress: enabled
  ```

- [ ] **Ingress controller running**
  ```bash
  kubectl get pods -n ingress-nginx
  # Should show ingress-nginx-controller as Running
  ```

### Step 3: Docker Images

- [ ] **Backend image built**
  ```bash
  docker images | grep todo-backend
  # Should show: todo-backend:latest
  ```

- [ ] **Frontend image built**
  ```bash
  docker images | grep todo-frontend
  # Should show: todo-frontend:v4
  ```

- [ ] **Images loaded into Minikube**
  ```bash
  minikube image ls | grep todo
  # Should show both images
  ```

### Step 4: Kubernetes Secrets

- [ ] **Secret created**
  ```bash
  kubectl get secret todo-secrets
  # Should show: todo-secrets with AGE
  ```

- [ ] **Secret has correct keys**
  ```bash
  kubectl describe secret todo-secrets
  # Should show: DATABASE_URL, BETTER_AUTH_SECRET, OPENROUTER_API_KEY
  ```

- [ ] **Secret has Helm labels**
  ```bash
  kubectl get secret todo-secrets -o jsonpath='{.metadata.labels}'
  # Should show: app.kubernetes.io/managed-by: Helm
  ```

### Step 5: Helm Deployment

- [ ] **Helm chart deployed**
  ```bash
  helm list
  # Should show: todo-app with STATUS: deployed
  ```

- [ ] **Pods are running**
  ```bash
  kubectl get pods
  # Should show both pods with STATUS: Running and READY: 1/1
  ```

- [ ] **Services created**
  ```bash
  kubectl get svc
  # Should show: backend-service and frontend-service
  ```

- [ ] **Ingress created**
  ```bash
  kubectl get ingress
  # Should show: todo-ingress with HOST: todo.local
  ```

### Step 6: Hosts File

- [ ] **todo.local added to hosts file**
  ```powershell
  Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "todo.local"
  # Should show: 127.0.0.1 todo.local
  ```

### Step 7: Minikube Tunnel

- [ ] **Tunnel started**
  ```bash
  # In separate terminal:
  minikube tunnel
  # Should show: "Tunnel successfully started"
  ```

- [ ] **Ingress has address**
  ```bash
  kubectl get ingress todo-ingress
  # Should show ADDRESS: 192.168.49.2
  ```

---

## ✅ Application Verification

### Frontend Tests

- [ ] **Frontend is accessible**
  ```bash
  curl -I http://todo.local
  # Should return: HTTP/1.1 200 OK
  ```

- [ ] **Frontend loads in browser**
  - Open: http://todo.local
  - Should see: Todo application homepage

- [ ] **Sign up page loads**
  - Navigate to: http://todo.local/signup
  - Should see: Sign up form

- [ ] **Sign in page loads**
  - Navigate to: http://todo.local/signin
  - Should see: Sign in form

### Backend Tests

- [ ] **Backend health check works**
  ```bash
  curl http://todo.local/health
  # Should return: {"status":"healthy","database":"connected"}
  ```

- [ ] **Backend API responds**
  ```bash
  curl http://todo.local/api/users/1/tasks
  # Should return: {"detail":"Not authenticated"} (expected)
  ```

- [ ] **Auth endpoints work**
  ```bash
  curl -I http://todo.local/auth/verify
  # Should return: HTTP/1.1 401 Unauthorized (expected)
  ```

### Integration Tests

- [ ] **Can create account**
  - Go to: http://todo.local/signup
  - Fill in: email, password, name
  - Click: Sign Up
  - Should: Redirect to dashboard

- [ ] **Can sign in**
  - Go to: http://todo.local/signin
  - Enter: credentials
  - Click: Sign In
  - Should: Redirect to dashboard

- [ ] **Can create task**
  - Sign in
  - Create a new task
  - Should: Task appears in list

- [ ] **Can use AI chatbot**
  - Sign in
  - Open chatbot
  - Send message
  - Should: Receive AI response

---

## ✅ Logs Verification

### Frontend Logs

- [ ] **Frontend is serving requests**
  ```bash
  kubectl logs deployment/frontend-deployment --tail=10
  # Should show: "Ready in X.Xs"
  ```

### Backend Logs

- [ ] **Backend is running**
  ```bash
  kubectl logs deployment/backend-deployment --tail=10
  # Should show: "Uvicorn running on http://0.0.0.0:8000"
  ```

- [ ] **Backend health checks passing**
  ```bash
  kubectl logs deployment/backend-deployment --tail=20 | grep health
  # Should show: "GET /health HTTP/1.1" 200 OK
  ```

- [ ] **No error messages**
  ```bash
  kubectl logs deployment/backend-deployment --tail=50 | grep -i error
  # Should show: No critical errors
  ```

---

## ✅ Resource Verification

### Pod Resources

- [ ] **Pods have sufficient resources**
  ```bash
  kubectl describe pod <pod-name> | grep -A 5 "Limits"
  # Should show: CPU and Memory limits
  ```

### Docker Desktop Resources

- [ ] **Docker has sufficient resources**
  - Open: Docker Desktop → Settings → Resources
  - Check: CPUs ≥ 4, Memory ≥ 8GB

---

## ✅ Security Verification

### Secrets

- [ ] **Secrets are not exposed**
  ```bash
  kubectl get secret todo-secrets -o yaml
  # Values should be base64 encoded, not plain text
  ```

- [ ] **Environment variables set correctly**
  ```bash
  kubectl exec deployment/frontend-deployment -- env | grep NEXT_PUBLIC
  # Should show: NEXT_PUBLIC_API_URL=http://todo.local
  ```

### Network

- [ ] **Services are ClusterIP (not exposed externally)**
  ```bash
  kubectl get svc
  # backend-service and frontend-service should be TYPE: ClusterIP
  ```

- [ ] **Only Ingress is exposed**
  ```bash
  kubectl get ingress
  # Only todo-ingress should exist
  ```

---

## ✅ Performance Verification

### Response Times

- [ ] **Frontend loads quickly**
  - Open: http://todo.local
  - Should load: < 3 seconds

- [ ] **Backend responds quickly**
  ```bash
  time curl http://todo.local/health
  # Should complete: < 1 second
  ```

### Resource Usage

- [ ] **Pods are not using excessive resources**
  ```bash
  kubectl top pods
  # CPU should be < 50%, Memory < 500Mi (idle)
  ```

---

## ✅ Daily Usage Verification

### After Restart

- [ ] **Minikube starts successfully**
  ```bash
  minikube start
  # Should complete without errors
  ```

- [ ] **Pods auto-start**
  ```bash
  kubectl get pods
  # Should show both pods Running
  ```

- [ ] **Tunnel works**
  ```bash
  minikube tunnel
  # Should show: "Tunnel successfully started"
  ```

- [ ] **Application accessible**
  - Open: http://todo.local
  - Should work immediately

---

## ✅ Troubleshooting Verification

### If Issues Occur

- [ ] **Can view pod logs**
  ```bash
  kubectl logs deployment/frontend-deployment
  # Should show logs without errors
  ```

- [ ] **Can describe pods**
  ```bash
  kubectl describe pod <pod-name>
  # Should show detailed information
  ```

- [ ] **Can restart deployments**
  ```bash
  kubectl rollout restart deployment/frontend-deployment
  # Should complete successfully
  ```

---

## 📊 Verification Summary

### All Green? ✅

If all checkboxes are checked:
- ✅ Your setup is complete and working correctly
- ✅ You can start using the application
- ✅ Refer to QUICK_START.md for daily usage

### Some Red? ❌

If some checkboxes are not checked:
- ❌ Review the failed step
- ❌ Check TROUBLESHOOTING.md for solutions
- ❌ Verify prerequisites are met
- ❌ Try the step again

---

## 🔄 Re-verification

### When to Re-verify

- After making changes to configuration
- After updating Docker images
- After system restart
- When troubleshooting issues
- Before deploying to production

### Quick Re-verification

```bash
# Run these commands for quick check
kubectl get pods
kubectl get ingress
curl http://todo.local/health
```

All should return successful results.

---

## 📝 Notes

- Keep this checklist handy for reference
- Use it after each major change
- Share with team members
- Update as needed for your environment

---

**Last Updated**: January 29, 2026
**Version**: 1.0.0
