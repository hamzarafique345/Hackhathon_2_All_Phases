# 🚀 Deployment Guide - Vercel & Railway

## 📋 Overview

This guide will help you deploy your Todo App with AI Chatbot to production:
- **Frontend (Next.js)** → Vercel
- **Backend (FastAPI)** → Railway
- **Database** → Neon PostgreSQL (already configured)

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Vercel        │
│   (Frontend)    │
│   Next.js       │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│   Railway       │
│   (Backend)     │
│   FastAPI       │
└────────┬────────┘
         │
         │ PostgreSQL
         │
┌────────▼────────┐
│   Neon          │
│   (Database)    │
│   PostgreSQL    │
└─────────────────┘
```

---

## 📦 Prerequisites

### 1. Accounts Needed
- ✅ **Vercel Account** - https://vercel.com/signup
- ✅ **Railway Account** - https://railway.app/
- ✅ **GitHub Account** - https://github.com/
- ✅ **Neon Database** - Already configured ✓

### 2. Install CLI Tools (Optional)
```bash
# Vercel CLI
npm install -g vercel

# Railway CLI
npm install -g @railway/cli
```

---

## 🎯 Deployment Strategy

### Phase 1: Deploy Backend to Railway
1. Backend must be deployed first
2. Get the Railway backend URL
3. Use this URL in frontend environment variables

### Phase 2: Deploy Frontend to Vercel
1. Configure frontend with Railway backend URL
2. Deploy to Vercel
3. Get Vercel frontend URL
4. Update backend CORS settings

---

## 🚂 Part 1: Deploy Backend to Railway

### Step 1: Prepare Backend for Deployment

#### 1.1 Create Railway Configuration Files

I've created these files for you:
- ✅ `backend/railway.toml` - Railway configuration
- ✅ `backend/Procfile` - Process file
- ✅ `backend/runtime.txt` - Python version

#### 1.2 Verify Requirements
Check `backend/requirements.txt` includes all dependencies:
```txt
fastapi==0.110.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
pyjwt==2.8.0
passlib==1.7.4
bcrypt==4.0.1
python-dotenv==1.0.0
asyncpg==0.30.0
python-multipart==0.0.9
email-validator==2.1.0
httpx>=0.24.0
```

### Step 2: Push Code to GitHub

#### 2.1 Initialize Git Repository (if not already done)
```bash
cd C:\Officialy Hamza\Test\hackhathon2\phase3

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Todo App with AI Chatbot"
```

#### 2.2 Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (e.g., "todo-app-ai-chatbot")
3. **Don't** initialize with README (you already have code)

#### 2.3 Push to GitHub
```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/todo-app-ai-chatbot.git

# Push code
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Railway

#### 3.1 Create New Project
1. Go to https://railway.app/
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your repository: `todo-app-ai-chatbot`

#### 3.2 Configure Root Directory
Railway needs to know where the backend code is:

1. In Railway dashboard, click on your service
2. Go to **Settings** tab
3. Find **"Root Directory"** setting
4. Set it to: `phase3/backend`
5. Click **Save**

#### 3.3 Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```env
# Database (already configured)
DATABASE_URL=postgresql://neondb_owner:npg_YOJCdEGxT81D@ep-gentle-salad-a4zjmszl-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require

# Authentication
BETTER_AUTH_SECRET=55ffea195578f78e86aed40a107690c23c7c8f08cc4504fea8d9dedd7bc56794
JWT_ALGORITHM=HS256

# Frontend URL (will update after Vercel deployment)
FRONTEND_URL=https://your-app.vercel.app

# API Base URL (Railway will provide this)
API_BASE_URL=${{RAILWAY_PUBLIC_DOMAIN}}

# OpenRouter API Key
OPENROUTER_API_KEY=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
```

**Important Notes:**
- `${{RAILWAY_PUBLIC_DOMAIN}}` is a Railway variable that auto-fills with your domain
- Update `FRONTEND_URL` after deploying to Vercel

#### 3.4 Deploy
1. Railway will automatically deploy
2. Wait for deployment to complete (2-5 minutes)
3. Check logs for any errors

#### 3.5 Get Your Backend URL
1. In Railway dashboard, click **"Settings"**
2. Under **"Domains"**, you'll see your Railway URL
3. It will look like: `https://your-app.up.railway.app`
4. **Save this URL** - you'll need it for Vercel!

#### 3.6 Test Backend
```bash
# Test health endpoint
curl https://your-app.up.railway.app/health

# Should return:
# {"status":"healthy","timestamp":"...","version":"1.0.0","database":"connected"}
```

---

## ▲ Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend for Deployment

#### 1.1 Update Environment Variables

Create `frontend/.env.production`:
```env
# Backend API URL (from Railway)
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app

# Auth Secret (same as backend)
BETTER_AUTH_SECRET=55ffea195578f78e86aed40a107690c23c7c8f08cc4504fea8d9dedd7bc56794

# Auth URL (will be your Vercel URL)
BETTER_AUTH_URL=https://your-app.vercel.app
```

#### 1.2 Verify vercel.json
Check `frontend/vercel.json` exists and is configured correctly.

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com/
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `phase3/frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Add Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
   BETTER_AUTH_SECRET=55ffea195578f78e86aed40a107690c23c7c8f08cc4504fea8d9dedd7bc56794
   BETTER_AUTH_URL=https://your-app.vercel.app
   ```

6. Click **"Deploy"**
7. Wait for deployment (2-5 minutes)

#### Option B: Deploy via Vercel CLI

```bash
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Follow prompts:
# - Link to existing project? No
# - Project name: todo-app-ai-chatbot
# - Directory: ./
# - Override settings? No
```

### Step 3: Get Your Frontend URL

After deployment:
1. Vercel will show your deployment URL
2. It will look like: `https://your-app.vercel.app`
3. **Save this URL**

### Step 4: Update Backend CORS Settings

Now that you have the Vercel URL, update Railway environment variables:

1. Go back to Railway dashboard
2. Go to **Variables** tab
3. Update `FRONTEND_URL`:
   ```
   FRONTEND_URL=https://your-app.vercel.app
   ```
4. Railway will automatically redeploy

---

## 🔧 Post-Deployment Configuration

### 1. Update CORS in Backend

The backend `src/main.py` already has CORS configured:
```python
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This will automatically use your Vercel URL from the environment variable.

### 2. Test Your Deployed App

#### 2.1 Test Backend
```bash
# Health check
curl https://your-app.up.railway.app/health

# API docs
open https://your-app.up.railway.app/docs
```

#### 2.2 Test Frontend
1. Open `https://your-app.vercel.app`
2. Sign up for a new account
3. Sign in
4. Create a task
5. Test the AI chatbot

### 3. Monitor Deployments

#### Railway Monitoring:
- **Logs**: Railway Dashboard → Deployments → View Logs
- **Metrics**: Railway Dashboard → Metrics
- **Health**: Check `/health` endpoint

#### Vercel Monitoring:
- **Logs**: Vercel Dashboard → Deployments → View Function Logs
- **Analytics**: Vercel Dashboard → Analytics
- **Performance**: Vercel Dashboard → Speed Insights

---

## 🔒 Security Checklist

### ✅ Before Going Live:

1. **Environment Variables**
   - ✅ Never commit `.env` files to Git
   - ✅ Use different secrets for production
   - ✅ Rotate `BETTER_AUTH_SECRET` for production

2. **Database**
   - ✅ Neon database is already secure (SSL required)
   - ✅ Connection pooling is configured
   - ✅ Database credentials are in environment variables

3. **API Security**
   - ✅ CORS is configured to only allow your frontend
   - ✅ JWT authentication is enabled
   - ✅ All endpoints require authentication

4. **Frontend Security**
   - ✅ API URL is environment-based
   - ✅ Tokens stored in localStorage (consider httpOnly cookies for production)
   - ✅ HTTPS enforced by Vercel

### 🔐 Recommended: Generate New Secrets for Production

```bash
# Generate new BETTER_AUTH_SECRET
openssl rand -hex 32

# Use this new secret in both Railway and Vercel
```

---

## 🐛 Troubleshooting

### Backend Issues

#### Issue: "Module not found" error
**Solution**: Check `requirements.txt` includes all dependencies
```bash
# In Railway logs, check for missing packages
# Add missing packages to requirements.txt
```

#### Issue: Database connection fails
**Solution**: Verify `DATABASE_URL` in Railway environment variables
```bash
# Test connection
curl https://your-app.up.railway.app/health
# Should show "database":"connected"
```

#### Issue: CORS errors
**Solution**: Update `FRONTEND_URL` in Railway to match Vercel URL
```env
FRONTEND_URL=https://your-app.vercel.app
```

### Frontend Issues

#### Issue: "Failed to fetch" errors
**Solution**: Check `NEXT_PUBLIC_API_URL` points to Railway backend
```env
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
```

#### Issue: Build fails on Vercel
**Solution**: Check build logs, ensure all dependencies are in `package.json`

#### Issue: Environment variables not working
**Solution**: Vercel requires `NEXT_PUBLIC_` prefix for client-side variables
```env
# ✅ Correct (accessible in browser)
NEXT_PUBLIC_API_URL=https://...

# ❌ Wrong (only available server-side)
API_URL=https://...
```

---

## 📊 Deployment Checklist

### Pre-Deployment:
- [ ] Code pushed to GitHub
- [ ] All environment variables documented
- [ ] Database is accessible (Neon)
- [ ] All tests passing locally

### Backend (Railway):
- [ ] Repository connected
- [ ] Root directory set to `phase3/backend`
- [ ] Environment variables configured
- [ ] Deployment successful
- [ ] Health endpoint responding
- [ ] Backend URL saved

### Frontend (Vercel):
- [ ] Repository connected
- [ ] Root directory set to `phase3/frontend`
- [ ] Environment variables configured
- [ ] `NEXT_PUBLIC_API_URL` points to Railway
- [ ] Deployment successful
- [ ] Frontend URL saved

### Post-Deployment:
- [ ] Backend `FRONTEND_URL` updated with Vercel URL
- [ ] CORS working (no errors in browser console)
- [ ] Authentication working
- [ ] Tasks can be created/updated/deleted
- [ ] AI chatbot working
- [ ] All 6 chatbot commands tested

---

## 🎯 Quick Deployment Commands

### Deploy Backend to Railway:
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to production"
git push origin main

# 2. Railway will auto-deploy
# 3. Check logs in Railway dashboard
```

### Deploy Frontend to Vercel:
```bash
# Option 1: Via Dashboard
# - Go to vercel.com
# - Import GitHub repo
# - Configure and deploy

# Option 2: Via CLI
cd frontend
vercel --prod
```

### Update After Changes:
```bash
# Commit and push
git add .
git commit -m "Update: description of changes"
git push origin main

# Both Railway and Vercel will auto-deploy
```

---

## 📈 Performance Optimization

### Backend (Railway):
- Railway provides automatic scaling
- Database connection pooling is configured
- Health checks ensure uptime

### Frontend (Vercel):
- Vercel provides CDN and edge caching
- Next.js optimizations are automatic
- Static assets are cached

### Database (Neon):
- Connection pooling enabled
- SSL required for security
- Located in us-east-1 (consider region for users)

---

## 💰 Cost Estimation

### Free Tier Limits:

**Railway:**
- $5 free credit per month
- ~500 hours of runtime
- Suitable for development/testing

**Vercel:**
- 100 GB bandwidth per month
- Unlimited deployments
- Suitable for small to medium traffic

**Neon:**
- 0.5 GB storage
- 1 compute unit
- Suitable for development/testing

### Upgrade When:
- Traffic exceeds free tier limits
- Need more database storage
- Require better performance

---

## 🔄 CI/CD Pipeline

Both Railway and Vercel provide automatic deployments:

```
GitHub Push → Automatic Deployment
     ↓
   main branch
     ↓
  ┌──────────────┐
  │   Railway    │ ← Backend auto-deploys
  │   Vercel     │ ← Frontend auto-deploys
  └──────────────┘
```

### Branch Strategy:
- `main` → Production (auto-deploy)
- `dev` → Development (manual deploy)
- Feature branches → Preview deployments (Vercel)

---

## 📞 Support Resources

### Railway:
- Docs: https://docs.railway.app/
- Discord: https://discord.gg/railway
- Status: https://status.railway.app/

### Vercel:
- Docs: https://vercel.com/docs
- Discord: https://vercel.com/discord
- Status: https://www.vercel-status.com/

### Neon:
- Docs: https://neon.tech/docs
- Discord: https://discord.gg/neon
- Status: https://neonstatus.com/

---

## 🎉 Success!

Once deployed, your app will be live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.up.railway.app`
- **API Docs**: `https://your-app.up.railway.app/docs`

Share your app with the world! 🚀
