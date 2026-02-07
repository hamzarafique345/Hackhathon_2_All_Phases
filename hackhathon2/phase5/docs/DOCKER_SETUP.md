# Docker Setup Guide

This guide covers building and testing Docker images for the Todo Chatbot application.

## Prerequisites

### Required Software
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
  - Version: 20.10 or higher
  - Download: https://www.docker.com/products/docker-desktop
- **Minikube** (for Kubernetes deployment)
  - Version: 1.30 or higher
  - Download: https://minikube.sigs.k8s.io/docs/start/
- **kubectl** (Kubernetes CLI)
  - Version: 1.27 or higher
  - Download: https://kubernetes.io/docs/tasks/tools/
- **Helm** (Kubernetes package manager)
  - Version: 3.12 or higher
  - Download: https://helm.sh/docs/intro/install/

### Verify Installation

```bash
# Check Docker
docker --version
docker ps

# Check Minikube
minikube version

# Check kubectl
kubectl version --client

# Check Helm
helm version
```

## Project Structure

```
phase_4/
├── frontend/
│   ├── Dockerfile          # Frontend container definition
│   ├── package.json
│   ├── next.config.ts      # Configured for standalone output
│   └── ...
├── backend/
│   ├── Dockerfile          # Backend container definition
│   ├── requirements.txt
│   ├── src/                # Main application code
│   ├── ai_agent/           # AI chatbot implementation
│   └── ...
└── todo-helm-chart/        # Kubernetes deployment manifests
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
```

## Building Docker Images

### Step 1: Build Backend Image

Navigate to the project root directory:

```bash
cd C:\Officialy Hamza\Test\hackhathon2\phase_4
```

Build the backend image:

```bash
docker build -t todo-backend:latest ./backend
```

**Expected Output:**
```
[+] Building 45.2s (12/12) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 1.23kB
 => [internal] load .dockerignore
 => [1/6] FROM docker.io/library/python:3.11-slim
 => [2/6] WORKDIR /app
 => [3/6] COPY requirements.txt .
 => [4/6] RUN pip install --no-cache-dir -r requirements.txt
 => [5/6] COPY . .
 => [6/6] ENV PYTHONPATH=/app
 => exporting to image
 => => naming to docker.io/library/todo-backend:latest
```

**Verify the image:**

```bash
docker images | grep todo-backend
```

Expected output:
```
todo-backend    latest    abc123def456    2 minutes ago    520MB
```

### Step 2: Build Frontend Image

Build the frontend image:

```bash
docker build -t todo-frontend:latest ./frontend
```

**Expected Output:**
```
[+] Building 120.5s (18/18) FINISHED
 => [internal] load build definition from Dockerfile
 => [deps 1/3] FROM docker.io/library/node:20-alpine
 => [deps 2/3] COPY package.json package-lock.json ./
 => [deps 3/3] RUN npm ci
 => [builder 1/3] COPY --from=deps /app/node_modules ./node_modules
 => [builder 2/3] COPY . .
 => [builder 3/3] RUN npm run build
 => [runner 1/5] COPY --from=builder /app/public ./public
 => [runner 2/5] COPY --from=builder /app/.next/standalone ./
 => [runner 3/5] COPY --from=builder /app/.next/static ./.next/static
 => exporting to image
 => => naming to docker.io/library/todo-frontend:latest
```

**Verify the image:**

```bash
docker images | grep todo-frontend
```

Expected output:
```
todo-frontend   latest    def456ghi789    3 minutes ago    180MB
```

## Testing Docker Images Locally

### Test Backend Container

Run the backend container with environment variables:

```bash
docker run -d \
  --name todo-backend-test \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://your-neon-url-here" \
  -e BETTER_AUTH_SECRET="your-secret-here-min-32-chars" \
  -e JWT_ALGORITHM="HS256" \
  -e FRONTEND_URL="http://localhost:3000" \
  -e OPENROUTER_API_KEY="your-api-key-here" \
  -e API_BASE_URL="http://localhost:8000" \
  todo-backend:latest
```

**Test the backend:**

```bash
# Check if container is running
docker ps | grep todo-backend-test

# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2026-01-28T...","version":"1.0.0","database":"connected"}

# View logs
docker logs todo-backend-test

# Stop and remove container
docker stop todo-backend-test
docker rm todo-backend-test
```

### Test Frontend Container

Run the frontend container:

```bash
docker run -d \
  --name todo-frontend-test \
  -p 3000:3000 \
  -e BETTER_AUTH_SECRET="your-secret-here-min-32-chars" \
  -e BETTER_AUTH_URL="http://localhost:3000" \
  -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
  todo-frontend:latest
```

**Test the frontend:**

```bash
# Check if container is running
docker ps | grep todo-frontend-test

# Open in browser
# Navigate to: http://localhost:3000

# View logs
docker logs todo-frontend-test

# Stop and remove container
docker stop todo-frontend-test
docker rm todo-frontend-test
```

## Loading Images into Minikube

Before deploying to Kubernetes, load the images into Minikube's Docker daemon:

### Step 1: Start Minikube

```bash
minikube start
```

**Expected Output:**
```
😄  minikube v1.32.0 on Windows 11
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster
```

### Step 2: Load Backend Image

```bash
minikube image load todo-backend:latest
```

**Expected Output:**
```
Loading image todo-backend:latest into minikube...
```

**Verify:**

```bash
minikube image ls | grep todo-backend
```

### Step 3: Load Frontend Image

```bash
minikube image load todo-frontend:latest
```

**Expected Output:**
```
Loading image todo-frontend:latest into minikube...
```

**Verify:**

```bash
minikube image ls | grep todo-frontend
```

## Troubleshooting

### Issue: Docker Build Fails

**Symptom:** Build fails with "COPY failed" or "no such file or directory"

**Solution:**
1. Ensure you're in the correct directory (phase_4/)
2. Check that Dockerfile exists in the target directory
3. Verify all required files are present (package.json, requirements.txt)

```bash
# Check current directory
pwd

# List files
ls -la frontend/
ls -la backend/
```

### Issue: Backend Container Crashes

**Symptom:** Container exits immediately after starting

**Solution:**
1. Check logs for error messages:
   ```bash
   docker logs todo-backend-test
   ```

2. Common issues:
   - Invalid DATABASE_URL format
   - Missing environment variables
   - Database connection refused

3. Test database connection:
   ```bash
   # Enter container shell
   docker exec -it todo-backend-test /bin/bash

   # Test Python imports
   python -c "from src.database import create_db_and_tables"
   ```

### Issue: Frontend Build Fails

**Symptom:** "npm run build" fails during Docker build

**Solution:**
1. Check if next.config.ts has `output: 'standalone'`
2. Ensure all dependencies are in package.json
3. Try building locally first:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

### Issue: Image Too Large

**Symptom:** Docker image size exceeds 1GB

**Solution:**
1. Backend should be ~500MB, frontend ~180MB
2. Check for unnecessary files being copied
3. Add .dockerignore file to exclude:
   ```
   node_modules
   .next
   .git
   venv
   __pycache__
   *.pyc
   .env
   .env.local
   ```

### Issue: Minikube Image Load Fails

**Symptom:** "Error loading image into minikube"

**Solution:**
1. Ensure Minikube is running:
   ```bash
   minikube status
   ```

2. Restart Minikube if needed:
   ```bash
   minikube stop
   minikube start
   ```

3. Check Docker daemon:
   ```bash
   docker ps
   ```

### Issue: Port Already in Use

**Symptom:** "bind: address already in use"

**Solution:**
1. Check what's using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000

   # Linux/Mac
   lsof -i :8000
   lsof -i :3000
   ```

2. Stop conflicting containers:
   ```bash
   docker ps
   docker stop <container-id>
   ```

## Best Practices

### 1. Image Tagging
Always tag images with version numbers for production:
```bash
docker build -t todo-backend:1.0.0 ./backend
docker build -t todo-backend:latest ./backend
```

### 2. Layer Caching
Order Dockerfile commands from least to most frequently changed:
- Install system dependencies first
- Copy package files and install dependencies
- Copy application code last

### 3. Security
- Never include secrets in Dockerfiles
- Use environment variables for configuration
- Run containers as non-root users (frontend already does this)

### 4. Image Cleanup
Remove unused images to save disk space:
```bash
# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Remove specific image
docker rmi todo-backend:latest
```

## Next Steps

After successfully building and testing Docker images:

1. ✅ Images built successfully
2. ✅ Images loaded into Minikube
3. → Proceed to [MINIKUBE_DEPLOYMENT.md](./MINIKUBE_DEPLOYMENT.md) for Kubernetes deployment

## Quick Reference

### Build Commands
```bash
# Build both images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Load into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### Verification Commands
```bash
# List local images
docker images | grep todo

# List Minikube images
minikube image ls | grep todo

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

### Cleanup Commands
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove images
docker rmi todo-backend:latest todo-frontend:latest
```
