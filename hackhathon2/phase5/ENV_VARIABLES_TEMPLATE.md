# Environment Variables Template for Production

## 🔐 Railway (Backend) Environment Variables

Copy these to Railway Dashboard → Variables:

```env
# Database Connection (Neon PostgreSQL)
DATABASE_URL=postgresql://neondb_owner:npg_YOJCdEGxT81D@ep-gentle-salad-a4zjmszl-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require

# Authentication Secret (IMPORTANT: Generate new for production)
BETTER_AUTH_SECRET=55ffea195578f78e86aed40a107690c23c7c8f08cc4504fea8d9dedd7bc56794

# JWT Algorithm
JWT_ALGORITHM=HS256

# Frontend URL (Update after Vercel deployment)
FRONTEND_URL=https://your-app.vercel.app

# OpenRouter API Key (for AI chatbot)
OPENROUTER_API_KEY=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
```

---

## ▲ Vercel (Frontend) Environment Variables

Copy these to Vercel Dashboard → Settings → Environment Variables:

```env
# Backend API URL (Update with your Railway URL)
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app

# Authentication Secret (Same as Railway)
BETTER_AUTH_SECRET=55ffea195578f78e86aed40a107690c23c7c8f08cc4504fea8d9dedd7bc56794

# Frontend URL (Will be your Vercel URL)
BETTER_AUTH_URL=https://your-app.vercel.app
```

---

## 🔒 Security Recommendations

### ⚠️ IMPORTANT: Generate New Secrets for Production

**Current secrets are for development only!**

Generate new production secrets:

```bash
# Generate new BETTER_AUTH_SECRET
openssl rand -hex 32

# Example output:
# a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2

# Use this new secret in BOTH Railway and Vercel
```

### What to Keep Secret:
- ✅ `BETTER_AUTH_SECRET` - Authentication key
- ✅ `DATABASE_URL` - Database connection string
- ✅ `OPENROUTER_API_KEY` - AI API key

### What Can Be Public:
- ✅ `NEXT_PUBLIC_API_URL` - Backend URL (public anyway)
- ✅ `FRONTEND_URL` - Frontend URL (public anyway)
- ✅ `JWT_ALGORITHM` - Algorithm name (HS256)

---

## 📝 Deployment Order

### Step 1: Deploy Backend First
1. Add all Railway environment variables
2. Deploy to Railway
3. Get Railway URL: `https://your-app.up.railway.app`

### Step 2: Deploy Frontend Second
1. Update `NEXT_PUBLIC_API_URL` with Railway URL
2. Add all Vercel environment variables
3. Deploy to Vercel
4. Get Vercel URL: `https://your-app.vercel.app`

### Step 3: Update Backend CORS
1. Go back to Railway
2. Update `FRONTEND_URL` with Vercel URL
3. Railway will auto-redeploy

---

## ✅ Verification Checklist

After setting environment variables:

### Railway:
- [ ] `DATABASE_URL` - Contains Neon connection string
- [ ] `BETTER_AUTH_SECRET` - 64 character hex string
- [ ] `JWT_ALGORITHM` - Set to "HS256"
- [ ] `FRONTEND_URL` - Points to Vercel URL
- [ ] `OPENROUTER_API_KEY` - Starts with "sk-or-v1-"

### Vercel:
- [ ] `NEXT_PUBLIC_API_URL` - Points to Railway URL
- [ ] `BETTER_AUTH_SECRET` - Same as Railway
- [ ] `BETTER_AUTH_URL` - Points to Vercel URL

---

## 🔄 Updating Environment Variables

### Railway:
1. Go to Railway Dashboard
2. Select your project
3. Click "Variables" tab
4. Edit or add variables
5. Railway auto-redeploys

### Vercel:
1. Go to Vercel Dashboard
2. Select your project
3. Settings → Environment Variables
4. Edit or add variables
5. Redeploy required (Vercel will prompt)

---

## 🧪 Testing Environment Variables

### Test Backend:
```bash
# Health check should show database connected
curl https://your-app.up.railway.app/health

# Should return:
{
  "status": "healthy",
  "database": "connected"
}
```

### Test Frontend:
1. Open browser console (F12)
2. Go to your Vercel URL
3. Check Network tab
4. API calls should go to Railway URL
5. No CORS errors should appear

---

## 🚨 Troubleshooting

### Issue: "Database connection failed"
**Check**: `DATABASE_URL` in Railway
- Must include `?sslmode=require`
- Must be the full connection string from Neon

### Issue: "CORS policy error"
**Check**: `FRONTEND_URL` in Railway
- Must match Vercel URL exactly
- No trailing slash
- Must include `https://`

### Issue: "Failed to fetch API"
**Check**: `NEXT_PUBLIC_API_URL` in Vercel
- Must point to Railway URL
- Must include `https://`
- Must be accessible from browser

### Issue: "Authentication failed"
**Check**: `BETTER_AUTH_SECRET` matches in both Railway and Vercel
- Must be identical in both places
- Case-sensitive
- No extra spaces

---

## 📋 Quick Copy-Paste Template

### For Railway:
```
DATABASE_URL=<your-neon-database-url>
BETTER_AUTH_SECRET=<generate-new-secret>
JWT_ALGORITHM=HS256
FRONTEND_URL=<your-vercel-url>
OPENROUTER_API_KEY=<your-openrouter-key>
```

### For Vercel:
```
NEXT_PUBLIC_API_URL=<your-railway-url>
BETTER_AUTH_SECRET=<same-as-railway>
BETTER_AUTH_URL=<your-vercel-url>
```

---

## 🎯 Final Checklist

Before going live:

- [ ] Generated new `BETTER_AUTH_SECRET` for production
- [ ] All environment variables set in Railway
- [ ] All environment variables set in Vercel
- [ ] `FRONTEND_URL` in Railway matches Vercel URL
- [ ] `NEXT_PUBLIC_API_URL` in Vercel matches Railway URL
- [ ] Tested health endpoint
- [ ] Tested authentication
- [ ] Tested AI chatbot
- [ ] No errors in browser console

---

**Ready to deploy!** 🚀
