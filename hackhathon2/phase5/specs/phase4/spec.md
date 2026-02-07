# Phase 4: Containerization and Kubernetes Deployment Specification

## Overview

This specification defines the containerization and Kubernetes deployment strategy for the Todo Chatbot application. The goal is to deploy the application to Minikube for local development and demonstration purposes.

## System Architecture

### Components

1. **Frontend Service**
   - Technology: Next.js 16.1.1 (React 19.2.3)
   - Port: 3000
   - Exposure: NodePort (accessible from host machine)
   - Build: Multi-stage Docker build for optimized production image

2. **Backend Service**
   - Technology: FastAPI (Python 3.11+)
   - Port: 8000
   - Exposure: ClusterIP (internal only, accessed by frontend)
   - Structure: Multi-folder Python application (src/, ai_agent/)
   - PYTHONPATH: Must be configured to resolve internal imports

3. **Database**
   - Technology: Neon PostgreSQL (hosted externally)
   - Connection: Via DATABASE_URL environment variable
   - **NOT containerized** - uses external hosted service

## Container Specifications

### Frontend Container

**Base Image**: node:20-alpine (multi-stage build)

**Build Stages**:
1. Dependencies stage: Install npm packages
2. Build stage: Run `next build` to generate production bundle
3. Runtime stage: Minimal image with only production dependencies and built assets

**Runtime Command**: `npm start` (serves production build)

**Environment Variables**:
- `BETTER_AUTH_SECRET` - Authentication secret (from Secret)
- `BETTER_AUTH_URL` - Frontend URL (http://localhost:30000 for Minikube NodePort)
- `NEXT_PUBLIC_API_URL` - Backend service URL (http://backend-service:8000)

**Health Check**: HTTP GET on `/` endpoint

**Resource Limits**:
- CPU: 500m (request), 1000m (limit)
- Memory: 512Mi (request), 1Gi (limit)

### Backend Container

**Base Image**: python:3.11-slim

**Build Process**:
1. Copy requirements.txt and install dependencies
2. Copy entire backend directory (src/, ai_agent/, tests/)
3. Set PYTHONPATH=/app to enable imports like `from src.database import...`

**Runtime Command**: `uvicorn src.main:app --host 0.0.0.0 --port 8000`

**Working Directory**: /app

**Environment Variables**:
- `DATABASE_URL` - Neon PostgreSQL connection string (from Secret)
- `BETTER_AUTH_SECRET` - Authentication secret (from Secret)
- `JWT_ALGORITHM` - JWT algorithm (from ConfigMap)
- `FRONTEND_URL` - Frontend service URL (from ConfigMap)
- `OPENROUTER_API_KEY` - AI API key (from Secret)
- `API_BASE_URL` - Backend URL (from ConfigMap)

**Health Check**: HTTP GET on `/health` endpoint

**Resource Limits**:
- CPU: 500m (request), 1000m (limit)
- Memory: 512Mi (request), 1Gi (limit)

## Kubernetes Resources

### Namespace
- Name: `default` (use default namespace for simplicity)

### Deployments

#### Frontend Deployment
- Name: `frontend-deployment`
- Replicas: 1 (single instance for demo)
- Selector: `app: frontend`
- Container: frontend
- Image: `todo-frontend:latest`
- ImagePullPolicy: `IfNotPresent` (for local Minikube images)

#### Backend Deployment
- Name: `backend-deployment`
- Replicas: 1 (single instance for demo)
- Selector: `app: backend`
- Container: backend
- Image: `todo-backend:latest`
- ImagePullPolicy: `IfNotPresent` (for local Minikube images)

### Services

#### Frontend Service
- Name: `frontend-service`
- Type: `NodePort`
- Port: 3000 (internal)
- TargetPort: 3000 (container)
- NodePort: 30000 (external access)
- Selector: `app: frontend`

#### Backend Service
- Name: `backend-service`
- Type: `ClusterIP` (internal only)
- Port: 8000 (internal)
- TargetPort: 8000 (container)
- Selector: `app: backend`

### ConfigMap

**Name**: `todo-config`

**Data**:
```yaml
JWT_ALGORITHM: "HS256"
FRONTEND_URL: "http://localhost:30000"
API_BASE_URL: "http://backend-service:8000"
```

### Secret

**Name**: `todo-secrets`

**Type**: Opaque

**Data** (base64 encoded):
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Authentication secret (32+ characters)
- `OPENROUTER_API_KEY` - AI API key

**Note**: Users must create this secret manually with their actual credentials.

## Networking Architecture

### Internal Communication
- Frontend → Backend: Uses Kubernetes DNS (`http://backend-service:8000`)
- Backend → Database: Direct connection via DATABASE_URL (external)

### External Access
- User → Frontend: Via Minikube NodePort on port 30000
- Access URL: `http://$(minikube ip):30000`

### CORS Configuration
- Backend allows requests from `FRONTEND_URL` (configured in ConfigMap)
- Must match the actual frontend access URL

## Helm Chart Structure

```
todo-helm-chart/
├── Chart.yaml                 # Chart metadata
├── values.yaml                # Default configuration values
└── templates/
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── configmap.yaml
    └── secret.yaml            # Template only - users provide values
```

### Values Configuration

**values.yaml** provides:
- Image names and tags
- Replica counts
- Resource limits
- Service ports
- NodePort configuration

Users can override values during installation:
```bash
helm install todo-app ./todo-helm-chart --set backend.image.tag=v1.0.0
```

## Deployment Strategy

### Prerequisites
1. Minikube installed and running
2. kubectl configured to use Minikube context
3. Helm 3.x installed
4. Docker images built and loaded into Minikube

### Deployment Steps

1. **Build Docker Images**
   ```bash
   docker build -t todo-frontend:latest ./frontend
   docker build -t todo-backend:latest ./backend
   ```

2. **Load Images into Minikube**
   ```bash
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   ```

3. **Create Secrets**
   ```bash
   kubectl create secret generic todo-secrets \
     --from-literal=DATABASE_URL='postgresql://...' \
     --from-literal=BETTER_AUTH_SECRET='your-secret-here' \
     --from-literal=OPENROUTER_API_KEY='your-api-key-here'
   ```

4. **Deploy with Helm**
   ```bash
   helm install todo-app ./todo-helm-chart
   ```

5. **Access Application**
   ```bash
   minikube service frontend-service --url
   ```

### Rollback Strategy
```bash
helm rollback todo-app [REVISION]
```

### Update Strategy
```bash
helm upgrade todo-app ./todo-helm-chart
```

## Health Checks and Readiness

### Frontend
- **Liveness Probe**: HTTP GET `/` every 30s
- **Readiness Probe**: HTTP GET `/` every 10s
- **Initial Delay**: 10s (allow Next.js to start)

### Backend
- **Liveness Probe**: HTTP GET `/health` every 30s
- **Readiness Probe**: HTTP GET `/health` every 10s
- **Initial Delay**: 5s (FastAPI starts quickly)

## Security Considerations

1. **Secrets Management**
   - All sensitive data stored in Kubernetes Secrets
   - Never commit secrets to version control
   - Use `.env.example` files as templates

2. **Network Policies**
   - Backend only accessible from within cluster
   - Frontend exposed via controlled NodePort

3. **Image Security**
   - Use official base images (node:20-alpine, python:3.11-slim)
   - Multi-stage builds to minimize attack surface
   - No root user in containers (future enhancement)

## Monitoring and Logging

### Logs Access
```bash
# Frontend logs
kubectl logs -f deployment/frontend-deployment

# Backend logs
kubectl logs -f deployment/backend-deployment
```

### Resource Monitoring
```bash
kubectl top pods
kubectl top nodes
```

## Troubleshooting

### Common Issues

1. **ImagePullBackOff**
   - Ensure images are loaded into Minikube: `minikube image ls`
   - Check ImagePullPolicy is `IfNotPresent`

2. **CrashLoopBackOff**
   - Check logs: `kubectl logs <pod-name>`
   - Verify environment variables are set correctly
   - Ensure database connection string is valid

3. **Service Not Accessible**
   - Verify Minikube is running: `minikube status`
   - Check service URL: `minikube service frontend-service --url`
   - Ensure NodePort is not blocked by firewall

4. **Backend Connection Failed**
   - Verify backend service is running: `kubectl get pods`
   - Check backend logs for errors
   - Ensure NEXT_PUBLIC_API_URL points to backend service

## Success Criteria

Phase 4 is complete when:

1. ✅ Docker images build successfully for frontend and backend
2. ✅ Images load into Minikube without errors
3. ✅ Helm chart deploys all resources successfully
4. ✅ Frontend is accessible via NodePort (http://$(minikube ip):30000)
5. ✅ Frontend can communicate with backend
6. ✅ Backend can connect to Neon PostgreSQL database
7. ✅ User can sign up, sign in, and manage tasks
8. ✅ AI chatbot functionality works in deployed environment
9. ✅ Health checks pass for both services
10. ✅ Documentation is complete and accurate

## Future Enhancements

- Ingress controller for production-like routing
- Horizontal Pod Autoscaling (HPA)
- Persistent volumes for local development
- CI/CD pipeline integration
- Production-ready secrets management (Sealed Secrets, Vault)
- Non-root container users
- Network policies for enhanced security
