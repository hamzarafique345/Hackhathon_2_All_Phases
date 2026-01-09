# Deployment Guide

Complete guide for deploying the Todo App authentication system to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup (Neon PostgreSQL)](#database-setup)
3. [Backend Deployment (Railway)](#backend-deployment)
4. [Frontend Deployment (Vercel)](#frontend-deployment)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- GitHub account
- Neon account (https://neon.tech)
- Railway account (https://railway.app) or alternative (Render, Fly.io)
- Vercel account (https://vercel.com)
- Git installed locally

---

## Database Setup (Neon PostgreSQL)

### Step 1: Create Neon Project

1. Go to https://neon.tech and sign in
2. Click "Create Project"
3. Choose a project name (e.g., "todo-app-prod")
4. Select a region closest to your users
5. Click "Create Project"

### Step 2: Get Connection String

1. In your Neon dashboard, click on your project
2. Go to "Connection Details"
3. Copy the connection string (starts with `postgresql://`)
4. **Important**: Save this securely - you'll need it for backend deployment

**Connection String Format:**
```
postgresql://username:password@host/database?sslmode=require
```

### Step 3: Configure Database

The database tables will be created automatically when the backend starts (via SQLModel's `create_all()`).

---

## Backend Deployment (Railway)

### Step 1: Prepare Repository

1. Ensure your code is pushed to GitHub
2. Make sure `backend/` directory contains:
   - `src/` folder with all Python files
   - `requirements.txt`
   - `.gitignore` (excludes `.env` and `venv/`)

### Step 2: Deploy to Railway

1. Go to https://railway.app and sign in with GitHub
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect Python and install dependencies

### Step 3: Configure Environment Variables

In Railway dashboard, go to your service → Variables:

```env
DATABASE_URL=your-neon-postgresql-connection-string
BETTER_AUTH_SECRET=generate-secure-random-32-char-string
JWT_ALGORITHM=HS256
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

**Generate secure secret:**
```bash
# On macOS/Linux:
openssl rand -base64 32

# On Windows (PowerShell):
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

### Step 4: Configure Start Command

In Railway dashboard → Settings → Deploy:

**Root Directory:** `backend`

**Start Command:**
```bash
uvicorn src.main:app --port $PORT
```

### Step 5: Deploy

1. Click "Deploy"
2. Wait for deployment to complete
3. Railway will provide a public URL (e.g., `https://your-app.railway.app`)
4. **Save this URL** - you'll need it for frontend configuration

### Step 6: Verify Backend

Test the health endpoint:
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-08T12:00:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

---

## Frontend Deployment (Vercel)

### Step 1: Prepare Repository

Ensure `frontend/` directory contains:
- `app/` folder with all pages
- `components/` folder
- `lib/` folder
- `package.json`
- `.gitignore` (excludes `.env.local` and `node_modules/`)

### Step 2: Deploy to Vercel

1. Go to https://vercel.com and sign in with GitHub
2. Click "Add New Project"
3. Import your GitHub repository
4. Vercel will auto-detect Next.js

### Step 3: Configure Project Settings

**Root Directory:** `frontend`

**Framework Preset:** Next.js

**Build Command:** `npm run build` (default)

**Output Directory:** `.next` (default)

### Step 4: Configure Environment Variables

In Vercel dashboard → Settings → Environment Variables:

```env
BETTER_AUTH_SECRET=same-secret-as-backend
BETTER_AUTH_URL=https://your-frontend-domain.vercel.app
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

**Important:**
- `BETTER_AUTH_SECRET` must match backend
- `BETTER_AUTH_URL` will be your Vercel domain
- `NEXT_PUBLIC_API_URL` is your Railway backend URL

### Step 5: Deploy

1. Click "Deploy"
2. Wait for deployment to complete
3. Vercel will provide a public URL (e.g., `https://your-app.vercel.app`)

### Step 6: Update Backend CORS

Go back to Railway → Your Backend Service → Variables:

Update `FRONTEND_URL` to your Vercel domain:
```env
FRONTEND_URL=https://your-app.vercel.app
```

Redeploy backend for changes to take effect.

---

## Environment Variables

### Backend Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DATABASE_URL | Yes | PostgreSQL connection string | postgresql://user:pass@host/db |
| BETTER_AUTH_SECRET | Yes | JWT secret key (32+ chars) | abc123...xyz789 |
| JWT_ALGORITHM | Yes | JWT signing algorithm | HS256 |
| FRONTEND_URL | Yes | Frontend origin for CORS | https://app.vercel.app |

### Frontend Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| BETTER_AUTH_SECRET | Yes | JWT secret (match backend) | abc123...xyz789 |
| BETTER_AUTH_URL | Yes | Frontend URL | https://app.vercel.app |
| NEXT_PUBLIC_API_URL | Yes | Backend API URL | https://api.railway.app |

---

## Post-Deployment Verification

### 1. Test Backend Health

```bash
curl https://your-backend.railway.app/health
```

### 2. Test Frontend

1. Open `https://your-app.vercel.app` in browser
2. Verify landing page loads
3. Check browser console for errors

### 3. Test Authentication Flow

1. Click "Get Started" → Sign Up
2. Create a new account
3. Verify redirect to dashboard
4. Check user information displays correctly
5. Test logout functionality
6. Test sign in with created account

### 4. Test API Integration

```bash
# Sign up
curl -X POST https://your-backend.railway.app/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Sign in
curl -X POST https://your-backend.railway.app/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Verify token (replace TOKEN with actual token from sign in response)
curl https://your-backend.railway.app/auth/verify \
  -H "Authorization: Bearer TOKEN"
```

---

## Troubleshooting

### Backend Issues

#### Database Connection Failed
- Verify DATABASE_URL is correct
- Check Neon database is not paused (free tier auto-pauses)
- Ensure connection string includes `?sslmode=require`

#### CORS Errors
- Verify FRONTEND_URL matches your Vercel domain exactly
- Check for trailing slashes (should not have one)
- Redeploy backend after changing FRONTEND_URL

#### 500 Internal Server Error
- Check Railway logs: Dashboard → Your Service → Logs
- Verify all environment variables are set
- Check BETTER_AUTH_SECRET is set and valid

### Frontend Issues

#### API Requests Failing
- Verify NEXT_PUBLIC_API_URL is correct
- Check backend is running and accessible
- Open browser DevTools → Network tab to see actual errors

#### Authentication Not Working
- Verify BETTER_AUTH_SECRET matches backend
- Check localStorage in browser DevTools
- Clear browser cache and cookies

#### Build Failures
- Check Vercel build logs
- Verify all dependencies in package.json
- Ensure TypeScript has no errors locally

### Database Issues

#### Tables Not Created
- Backend creates tables automatically on startup
- Check Railway logs for database connection errors
- Verify DATABASE_URL format is correct

#### Connection Pool Exhausted
- Neon free tier has connection limits
- Check for connection leaks in code
- Consider upgrading Neon plan

---

## Alternative Deployment Options

### Backend Alternatives

**Render:**
- Similar to Railway
- Free tier available
- Auto-detects Python
- Set environment variables in dashboard

**Fly.io:**
- Requires Dockerfile
- More configuration needed
- Good for global deployment

**Heroku:**
- Classic PaaS option
- Requires Procfile
- Free tier discontinued (paid plans only)

### Frontend Alternatives

**Netlify:**
- Similar to Vercel
- Auto-detects Next.js
- Set environment variables in dashboard

**Cloudflare Pages:**
- Fast global CDN
- Free tier generous
- Good for static sites

---

## Security Checklist

Before going to production:

- [ ] Generate strong BETTER_AUTH_SECRET (32+ characters)
- [ ] Use HTTPS for all connections
- [ ] Set secure CORS policy (specific origin, not *)
- [ ] Enable database SSL (Neon does this by default)
- [ ] Don't commit .env files to Git
- [ ] Use environment variables for all secrets
- [ ] Enable rate limiting (consider adding middleware)
- [ ] Set up monitoring and alerts
- [ ] Regular security updates for dependencies

---

## Monitoring & Maintenance

### Railway Monitoring
- Check logs regularly: Dashboard → Service → Logs
- Set up alerts for errors
- Monitor resource usage

### Vercel Monitoring
- Check Analytics: Dashboard → Analytics
- Monitor build times
- Check for failed deployments

### Database Monitoring
- Neon dashboard shows connection count
- Monitor query performance
- Set up alerts for high usage

---

## Scaling Considerations

### When to Scale

- Response times > 1 second
- Database connection pool exhausted
- High CPU/memory usage
- Increased user traffic

### Scaling Options

**Backend:**
- Upgrade Railway plan for more resources
- Add Redis for session caching
- Implement database read replicas
- Add load balancer for multiple instances

**Frontend:**
- Vercel scales automatically
- Consider CDN for static assets
- Implement client-side caching

**Database:**
- Upgrade Neon plan for more connections
- Add connection pooling (already implemented)
- Consider read replicas for heavy read workloads

---

## Rollback Procedure

### Backend Rollback (Railway)
1. Go to Dashboard → Service → Deployments
2. Find previous working deployment
3. Click "Redeploy"

### Frontend Rollback (Vercel)
1. Go to Dashboard → Deployments
2. Find previous working deployment
3. Click "Promote to Production"

### Database Rollback
- Neon provides point-in-time recovery
- Go to Dashboard → Backups
- Restore to previous state

---

## Support & Resources

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Neon Docs**: https://neon.tech/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs

---

## Conclusion

Your Todo App authentication system is now deployed and ready for production use!

**Next Steps:**
1. Set up custom domain (optional)
2. Configure monitoring and alerts
3. Implement additional features (todo CRUD operations)
4. Set up CI/CD pipeline
5. Add automated testing

For questions or issues, refer to the main README.md or open an issue on GitHub.

---

**Deployment Checklist:**
- [ ] Neon database created and connection string saved
- [ ] Backend deployed to Railway with all environment variables
- [ ] Backend health check passing
- [ ] Frontend deployed to Vercel with all environment variables
- [ ] CORS configured correctly (FRONTEND_URL updated)
- [ ] Authentication flow tested end-to-end
- [ ] All environment variables secured
- [ ] Monitoring set up
- [ ] Documentation reviewed

🎉 Congratulations on your deployment!
