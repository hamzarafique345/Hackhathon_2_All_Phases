# Documentation Index - Todo Application

Complete documentation suite for the Kubernetes-deployed Todo application.

## 📚 Available Documentation

### 🚀 Getting Started

1. **[QUICK_START.md](QUICK_START.md)** - Start here!
   - 3-step quick start for first time
   - Daily usage after restart
   - Common tasks and commands
   - **Best for**: Getting up and running fast

2. **[KUBERNETES.md](KUBERNETES.md)** - Complete deployment guide
   - Detailed step-by-step setup
   - Architecture explanation
   - Production deployment guide
   - **Best for**: Understanding the full setup

### 🐳 Docker & Containers

3. **[DOCKER_DESKTOP_GUIDE.md](DOCKER_DESKTOP_GUIDE.md)** - Visual Docker guide
   - How to use Docker Desktop
   - Viewing containers and images
   - Monitoring resources
   - **Best for**: Understanding Docker Desktop

### 🔧 Troubleshooting

4. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving
   - Common issues and solutions
   - Diagnostic commands
   - Complete reset instructions
   - **Best for**: When something goes wrong

### 📖 Reference

5. **[README.md](README.md)** - Project overview
   - Original project documentation
   - Tech stack information
   - API documentation
   - **Best for**: Understanding the application

6. **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Verification checklist
   - Step-by-step verification
   - What to check at each stage
   - **Best for**: Ensuring everything works

7. **[FAQ.md](FAQ.md)** - Frequently asked questions
   - Common questions and answers
   - Tips and tricks
   - **Best for**: Quick answers

### 🤖 Automation

8. **[start-todo.bat](start-todo.bat)** - Windows startup script
   - Automated startup
   - Double-click to start
   - **Best for**: Quick daily startup

---

## 🎯 Which Document Should I Read?

### I'm Setting Up for the First Time
→ Start with **[QUICK_START.md](QUICK_START.md)**
→ Then read **[KUBERNETES.md](KUBERNETES.md)** for details

### I Restarted My Laptop
→ Read **[QUICK_START.md](QUICK_START.md)** - "Daily Usage" section
→ Or just run **[start-todo.bat](start-todo.bat)**

### Something Isn't Working
→ Check **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**
→ Use diagnostic commands to identify the issue

### I Want to Understand Docker Desktop
→ Read **[DOCKER_DESKTOP_GUIDE.md](DOCKER_DESKTOP_GUIDE.md)**
→ Visual guide with descriptions

### I'm Deploying to Production
→ Read **[KUBERNETES.md](KUBERNETES.md)** - "Production Deployment" section

### I Have a Quick Question
→ Check **[FAQ.md](FAQ.md)**
→ Or search in **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

---

## 📋 Quick Reference

### Essential Commands

```bash
# Start everything
minikube start
minikube tunnel  # Keep open

# Check status
kubectl get pods
kubectl get ingress

# View logs
kubectl logs deployment/frontend-deployment --tail=20
kubectl logs deployment/backend-deployment --tail=20

# Restart
kubectl rollout restart deployment/frontend-deployment

# Stop
minikube stop
```

### Access Points

- **Application**: http://todo.local
- **Backend Health**: http://todo.local/health
- **Backend API**: http://todo.local/api/*

---

**Last Updated**: January 29, 2026
**Version**: 1.0.0
