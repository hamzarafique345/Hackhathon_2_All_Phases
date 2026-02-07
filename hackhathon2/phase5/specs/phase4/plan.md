# Phase 4: Implementation Plan

## Executive Summary

This plan outlines the step-by-step implementation of containerization and Kubernetes deployment for the Todo Chatbot application. The implementation follows a bottom-up approach: Dockerfiles → Helm Chart → Documentation → Testing.

## Architecture Decisions

### 1. Container Strategy

**Decision**: Use multi-stage Docker builds for both frontend and backend.

**Rationale**:
- Reduces final image size by excluding build dependencies
- Separates build-time and runtime concerns
- Industry best practice for production deployments

**Frontend Build Strategy**:
- Stage 1 (deps): Install all dependencies
- Stage 2 (builder): Build Next.js production bundle
- Stage 3 (runner): Minimal runtime with only production dependencies

**Backend Build Strategy**:
- Single-stage build (Python apps are simpler)
- Copy entire backend directory structure (src/, ai_agent/)
- Set PYTHONPATH=/app for proper module resolution

### 2. Kubernetes Deployment Strategy

**Decision**: Use Helm charts instead of raw YAML manifests.

**Rationale**:
- Easier to manage related resources as a single unit
- Supports parameterization via values.yaml
- Simplifies upgrades and rollbacks
- Industry standard for Kubernetes package management

**Alternative Considered**: Raw kubectl apply with YAML files
**Why Rejected**: Less maintainable, harder to parameterize, no built-in versioning

### 3. Image Distribution Strategy

**Decision**: Build images locally and load into Minikube using `minikube image load`.

**Rationale**:
- No need for external container registry
- Faster iteration during development
- Suitable for hackathon/demo environment
- Minikube has built-in support for local images

**Alternative Considered**: Push to Docker Hub or GitHub Container Registry
**Why Rejected**: Adds complexity, requires authentication, slower for local development

### 4. Networking Strategy

**Decision**: Frontend exposed via NodePort, backend as ClusterIP.

**Rationale**:
- NodePort provides simple external access without Ingress controller
- Backend doesn't need external exposure (security best practice)
- Frontend communicates with backend via Kubernetes DNS

**Alternative Considered**: Ingress controller for both services
**Why Rejected**: Overkill for local development, adds complexity

### 5. Configuration Management

**Decision**: Split configuration into ConfigMap (non-sensitive) and Secret (sensitive).

**Rationale**:
- Follows Kubernetes security best practices
- Secrets are base64 encoded and can be encrypted at rest
- ConfigMaps are easier to inspect and debug
- Clear separation of concerns

### 6. Environment Variable Strategy

**Frontend Environment Variables**:
- Build-time: None (all runtime for flexibility)
- Runtime: Injected via Kubernetes ConfigMap/Secret
- Public variables: Prefixed with NEXT_PUBLIC_

**Backend Environment Variables**:
- All runtime variables
- Database URL and secrets from Kubernetes Secret
- Non-sensitive config from ConfigMap

## Implementation Phases

### Phase 1: Docker Images (Priority: HIGH)

**Objective**: Create production-ready Dockerfiles for frontend and backend.

#### Task 1.1: Frontend Dockerfile
**File**: `frontend/Dockerfile`

**Requirements**:
- Multi-stage build (deps → builder → runner)
- Base image: node:20-alpine
- Optimize layer caching (copy package files first)
- Run as non-root user (node)
- Expose port 3000
- Health check on root endpoint

**Key Considerations**:
- Next.js standalone output for smaller image
- Copy .next/standalone and public directories
- Set NODE_ENV=production

**Validation**:
```bash
docker build -t todo-frontend:latest ./frontend
docker run -p 3000:3000 todo-frontend:latest
```

#### Task 1.2: Backend Dockerfile
**File**: `backend/Dockerfile`

**Requirements**:
- Base image: python:3.11-slim
- Copy entire backend directory (multi-folder structure)
- Install dependencies from requirements.txt
- Set PYTHONPATH=/app
- Expose port 8000
- Run uvicorn with proper host binding

**Key Considerations**:
- Must preserve directory structure (src/, ai_agent/)
- PYTHONPATH critical for imports like `from src.database import...`
- Use --host 0.0.0.0 for container networking

**Validation**:
```bash
docker build -t todo-backend:latest ./backend
docker run -p 8000:8000 -e DATABASE_URL=... todo-backend:latest
```

### Phase 2: Helm Chart (Priority: HIGH)

**Objective**: Create complete Helm chart with all Kubernetes resources.

#### Task 2.1: Chart Structure
**Directory**: `todo-helm-chart/`

**Files to Create**:
1. `Chart.yaml` - Chart metadata
2. `values.yaml` - Default configuration values
3. `templates/frontend-deployment.yaml` - Frontend Deployment
4. `templates/frontend-service.yaml` - Frontend Service (NodePort)
5. `templates/backend-deployment.yaml` - Backend Deployment
6. `templates/backend-service.yaml` - Backend Service (ClusterIP)
7. `templates/configmap.yaml` - Non-sensitive configuration
8. `templates/secret.yaml` - Sensitive data template

#### Task 2.2: Frontend Kubernetes Resources

**Deployment Specification**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
        env:
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: BETTER_AUTH_SECRET
        - name: BETTER_AUTH_URL
          value: "http://localhost:30000"
        - name: NEXT_PUBLIC_API_URL
          value: "http://backend-service:8000"
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
```

**Service Specification**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30000
```

#### Task 2.3: Backend Kubernetes Resources

**Deployment Specification**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: DATABASE_URL
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: BETTER_AUTH_SECRET
        - name: OPENROUTER_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: OPENROUTER_API_KEY
        - name: JWT_ALGORITHM
          valueFrom:
            configMapKeyRef:
              name: todo-config
              key: JWT_ALGORITHM
        - name: FRONTEND_URL
          valueFrom:
            configMapKeyRef:
              name: todo-config
              key: FRONTEND_URL
        - name: API_BASE_URL
          valueFrom:
            configMapKeyRef:
              name: todo-config
              key: API_BASE_URL
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 3
          periodSeconds: 10
```

**Service Specification**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
```

#### Task 2.4: ConfigMap and Secret

**ConfigMap**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
data:
  JWT_ALGORITHM: "HS256"
  FRONTEND_URL: "http://localhost:30000"
  API_BASE_URL: "http://backend-service:8000"
```

**Secret Template** (users must provide actual values):
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
type: Opaque
data:
  DATABASE_URL: <base64-encoded-value>
  BETTER_AUTH_SECRET: <base64-encoded-value>
  OPENROUTER_API_KEY: <base64-encoded-value>
```

#### Task 2.5: values.yaml

**Configuration**:
```yaml
frontend:
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  replicas: 1
  service:
    type: NodePort
    port: 3000
    nodePort: 30000
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

backend:
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  replicas: 1
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

config:
  jwtAlgorithm: "HS256"
  frontendUrl: "http://localhost:30000"
  apiBaseUrl: "http://backend-service:8000"
```

### Phase 3: Documentation (Priority: MEDIUM)

**Objective**: Create comprehensive deployment documentation.

#### Task 3.1: Docker Setup Documentation
**File**: `docs/DOCKER_SETUP.md`

**Contents**:
1. Prerequisites (Docker, Minikube, kubectl, Helm)
2. Building Docker images
3. Testing images locally
4. Loading images into Minikube
5. Troubleshooting common Docker issues

#### Task 3.2: Minikube Deployment Documentation
**File**: `docs/MINIKUBE_DEPLOYMENT.md`

**Contents**:
1. Minikube setup and configuration
2. Creating Kubernetes secrets
3. Deploying with Helm
4. Accessing the application
5. Monitoring and logs
6. Updating and rolling back
7. Troubleshooting deployment issues

### Phase 4: Testing and Validation (Priority: HIGH)

**Objective**: Ensure deployment works end-to-end.

#### Task 4.1: Local Docker Testing
**Steps**:
1. Build both images
2. Run containers with docker-compose (optional)
3. Verify frontend accessible on localhost:3000
4. Verify backend accessible on localhost:8000
5. Test API endpoints with curl

#### Task 4.2: Minikube Deployment Testing
**Steps**:
1. Start Minikube
2. Load images into Minikube
3. Create secrets
4. Deploy with Helm
5. Verify all pods are running
6. Access frontend via NodePort
7. Test complete user flow:
   - Sign up
   - Sign in
   - Create tasks
   - Use AI chatbot
   - Delete tasks
   - Sign out

#### Task 4.3: Health Check Validation
**Steps**:
1. Verify liveness probes are passing
2. Verify readiness probes are passing
3. Test pod restart behavior
4. Verify logs are accessible

## Implementation Order

### Critical Path
1. Backend Dockerfile (blocks backend deployment)
2. Frontend Dockerfile (blocks frontend deployment)
3. Helm chart templates (blocks deployment)
4. Documentation (blocks user adoption)

### Recommended Sequence
1. ✅ Create specification (completed)
2. ✅ Create implementation plan (this document)
3. → Create backend Dockerfile
4. → Create frontend Dockerfile
5. → Test Docker images locally
6. → Create Helm chart structure
7. → Create Helm templates (ConfigMap, Secret)
8. → Create Helm templates (Backend Deployment, Service)
9. → Create Helm templates (Frontend Deployment, Service)
10. → Create values.yaml
11. → Create Chart.yaml
12. → Create DOCKER_SETUP.md
13. → Create MINIKUBE_DEPLOYMENT.md
14. → Test complete deployment flow
15. → Document any issues and solutions

## Risk Analysis

### Risk 1: PYTHONPATH Configuration
**Impact**: HIGH
**Probability**: MEDIUM
**Mitigation**:
- Explicitly set PYTHONPATH=/app in Dockerfile
- Test imports before building final image
- Document the requirement clearly

### Risk 2: Next.js Environment Variables
**Impact**: MEDIUM
**Probability**: MEDIUM
**Mitigation**:
- Use NEXT_PUBLIC_ prefix for client-side variables
- Test that API URL is accessible from browser
- Document environment variable requirements

### Risk 3: Minikube Image Loading
**Impact**: MEDIUM
**Probability**: LOW
**Mitigation**:
- Use `minikube image load` instead of docker push
- Set imagePullPolicy: IfNotPresent
- Document the image loading process

### Risk 4: Database Connectivity
**Impact**: HIGH
**Probability**: LOW
**Mitigation**:
- Test DATABASE_URL from within Minikube
- Ensure Neon PostgreSQL allows external connections
- Provide clear error messages in logs

### Risk 5: CORS Issues
**Impact**: MEDIUM
**Probability**: MEDIUM
**Mitigation**:
- Configure FRONTEND_URL correctly in backend
- Test cross-origin requests
- Document CORS configuration

## Success Metrics

1. **Build Success**: Both Docker images build without errors
2. **Image Size**: Frontend < 200MB, Backend < 500MB
3. **Startup Time**: Frontend < 10s, Backend < 5s
4. **Health Checks**: 100% passing after initial delay
5. **Deployment Success**: Helm install completes without errors
6. **Functional Testing**: All user flows work in deployed environment
7. **Documentation Quality**: Users can deploy without assistance

## Rollback Plan

If deployment fails:
1. Check pod status: `kubectl get pods`
2. Check logs: `kubectl logs <pod-name>`
3. Rollback Helm release: `helm rollback todo-app`
4. Delete and recreate secrets if needed
5. Rebuild images if Dockerfile changes required

## Post-Implementation Tasks

1. Create Prompt History Record (PHR) for Phase 4
2. Update main README.md with Phase 4 information
3. Tag git commit for Phase 4 completion
4. Test deployment on fresh Minikube instance
5. Gather feedback and document lessons learned

## Dependencies

### External Dependencies
- Minikube (latest version)
- kubectl (compatible with Minikube)
- Helm 3.x
- Docker Desktop or Docker Engine
- Neon PostgreSQL (already provisioned)

### Internal Dependencies
- Phase 3 completion (AI chatbot working)
- Valid DATABASE_URL
- Valid OPENROUTER_API_KEY
- BETTER_AUTH_SECRET (32+ characters)

## Timeline Estimate

**Note**: Following project guidelines, no time estimates provided. Tasks are ordered by priority and dependencies.

## Acceptance Criteria

Phase 4 implementation is complete when:

1. ✅ Backend Dockerfile builds successfully
2. ✅ Frontend Dockerfile builds successfully
3. ✅ Helm chart structure is complete
4. ✅ All Kubernetes resources are defined
5. ✅ Documentation is comprehensive and accurate
6. ✅ Images load into Minikube successfully
7. ✅ Helm deployment succeeds
8. ✅ Frontend is accessible via NodePort
9. ✅ Backend health check passes
10. ✅ Frontend can communicate with backend
11. ✅ Backend can connect to database
12. ✅ All user flows work (signup, signin, tasks, chatbot)
13. ✅ Logs are accessible and informative
14. ✅ Documentation tested by following step-by-step

## Next Steps

Proceed to implementation phase:
1. Start with backend Dockerfile (critical path)
2. Follow with frontend Dockerfile
3. Create Helm chart
4. Write documentation
5. Test end-to-end deployment
