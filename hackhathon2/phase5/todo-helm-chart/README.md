# Todo App Helm Chart

A Helm chart for deploying the Todo Chatbot application to Kubernetes.

## Overview

This Helm chart deploys a complete Todo Chatbot application consisting of:
- **Frontend**: Next.js application with authentication and AI chatbot interface
- **Backend**: FastAPI application with MCP tools and AI agent
- **Database**: External Neon PostgreSQL (not containerized)

## Prerequisites

- Kubernetes 1.27+
- Helm 3.12+
- Docker images built and loaded into cluster
- Valid Neon PostgreSQL database

## Installation

### 1. Create Secret

Before installing the chart, create a Kubernetes secret with your credentials:

```bash
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL='postgresql://username:password@host.neon.tech/dbname?sslmode=require' \
  --from-literal=BETTER_AUTH_SECRET='your-32-character-secret-here' \
  --from-literal=OPENROUTER_API_KEY='your-openrouter-api-key-here'
```

### 2. Install Chart

```bash
helm install todo-app ./todo-helm-chart
```

### 3. Access Application

For Minikube:
```bash
minikube service frontend-service --url
```

For other Kubernetes clusters:
```bash
kubectl get service frontend-service
# Access via NodePort: http://<node-ip>:30000
```

## Configuration

The following table lists the configurable parameters and their default values.

### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `frontend.replicas` | Number of frontend replicas | `1` |
| `frontend.service.type` | Service type | `NodePort` |
| `frontend.service.port` | Service port | `3000` |
| `frontend.service.nodePort` | NodePort for external access | `30000` |
| `frontend.resources.requests.cpu` | CPU request | `500m` |
| `frontend.resources.requests.memory` | Memory request | `512Mi` |
| `frontend.resources.limits.cpu` | CPU limit | `1000m` |
| `frontend.resources.limits.memory` | Memory limit | `1Gi` |
| `frontend.env.betterAuthUrl` | Frontend URL for auth | `http://localhost:30000` |
| `frontend.env.nextPublicApiUrl` | Backend API URL | `http://backend-service:8000` |

### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `backend.replicas` | Number of backend replicas | `1` |
| `backend.service.type` | Service type | `ClusterIP` |
| `backend.service.port` | Service port | `8000` |
| `backend.resources.requests.cpu` | CPU request | `500m` |
| `backend.resources.requests.memory` | Memory request | `512Mi` |
| `backend.resources.limits.cpu` | CPU limit | `1000m` |
| `backend.resources.limits.memory` | Memory limit | `1Gi` |

### Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `config.jwtAlgorithm` | JWT algorithm | `HS256` |
| `config.frontendUrl` | Frontend URL for CORS | `http://localhost:30000` |
| `config.apiBaseUrl` | Backend API base URL | `http://backend-service:8000` |

## Customizing Values

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

Install with custom values:

```bash
helm install todo-app ./todo-helm-chart -f custom-values.yaml
```

Or override specific values:

```bash
helm install todo-app ./todo-helm-chart \
  --set frontend.replicas=2 \
  --set backend.replicas=2
```

## Upgrading

```bash
helm upgrade todo-app ./todo-helm-chart
```

With custom values:

```bash
helm upgrade todo-app ./todo-helm-chart -f custom-values.yaml
```

## Rollback

View release history:

```bash
helm history todo-app
```

Rollback to previous version:

```bash
helm rollback todo-app
```

Rollback to specific revision:

```bash
helm rollback todo-app 1
```

## Uninstalling

```bash
helm uninstall todo-app
```

This removes all Kubernetes resources associated with the chart, except for the Secret (which must be deleted manually if needed).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Kubernetes Cluster                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Frontend (NodePort 30000)                         │    │
│  │  - Next.js Application                             │    │
│  │  - Port: 3000                                      │    │
│  │  - Replicas: 1                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          │ HTTP                              │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Backend (ClusterIP)                               │    │
│  │  - FastAPI Application                             │    │
│  │  - Port: 8000                                      │    │
│  │  - Replicas: 1                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │
                           │ PostgreSQL
                           ▼
                  ┌─────────────────┐
                  │  Neon Database  │
                  │  (External)     │
                  └─────────────────┘
```

## Health Checks

### Frontend
- **Liveness Probe**: HTTP GET `/` every 30s (initial delay: 10s)
- **Readiness Probe**: HTTP GET `/` every 10s (initial delay: 5s)

### Backend
- **Liveness Probe**: HTTP GET `/health` every 30s (initial delay: 5s)
- **Readiness Probe**: HTTP GET `/health` every 10s (initial delay: 3s)

## Security

### Secrets Management
- All sensitive data stored in Kubernetes Secret (`todo-secrets`)
- Secret must be created before chart installation
- Never commit secrets to version control

### Network Security
- Backend exposed only within cluster (ClusterIP)
- Frontend exposed via NodePort for external access
- CORS configured to allow only frontend URL

### Image Security
- Uses official base images (node:20-alpine, python:3.11-slim)
- Multi-stage builds minimize attack surface
- Frontend runs as non-root user (nextjs:nodejs)

## Monitoring

### View Logs

```bash
# Frontend logs
kubectl logs -f deployment/frontend-deployment

# Backend logs
kubectl logs -f deployment/backend-deployment
```

### Check Status

```bash
# All resources
kubectl get all

# Pods
kubectl get pods

# Services
kubectl get services

# Deployments
kubectl get deployments
```

### Resource Usage

```bash
# Pod resources
kubectl top pods

# Node resources
kubectl top nodes
```

## Troubleshooting

### Pods Not Starting

Check pod status and events:
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

Common issues:
- ImagePullBackOff: Images not loaded into cluster
- CrashLoopBackOff: Application error or invalid configuration
- Pending: Insufficient resources

### Can't Access Frontend

Check service and get URL:
```bash
kubectl get service frontend-service
minikube service frontend-service --url  # For Minikube
```

### Backend Connection Issues

Test backend from frontend pod:
```bash
kubectl exec -it <frontend-pod> -- wget -qO- http://backend-service:8000/health
```

### Database Connection Failed

Check secret and backend logs:
```bash
kubectl get secret todo-secrets -o yaml
kubectl logs <backend-pod> | grep -i database
```

## Development

### Local Testing

Test the chart without installing:

```bash
# Dry run
helm install todo-app ./todo-helm-chart --dry-run --debug

# Template rendering
helm template todo-app ./todo-helm-chart

# Lint chart
helm lint ./todo-helm-chart
```

### Chart Structure

```
todo-helm-chart/
├── Chart.yaml                      # Chart metadata
├── values.yaml                     # Default configuration
├── README.md                       # This file
└── templates/
    ├── backend-deployment.yaml     # Backend Deployment
    ├── backend-service.yaml        # Backend Service
    ├── frontend-deployment.yaml    # Frontend Deployment
    ├── frontend-service.yaml       # Frontend Service
    ├── configmap.yaml              # ConfigMap for non-sensitive config
    └── secret.yaml                 # Secret template (documentation only)
```

## Requirements

- Kubernetes 1.27+
- Helm 3.12+
- Images: `todo-frontend:latest`, `todo-backend:latest`
- Secret: `todo-secrets` with DATABASE_URL, BETTER_AUTH_SECRET, OPENROUTER_API_KEY

## Support

For issues and questions:
1. Check pod logs: `kubectl logs <pod-name>`
2. Check events: `kubectl get events`
3. Review documentation in `docs/` directory
4. Verify all prerequisites are met

## License

This chart is part of the Todo Chatbot application.
