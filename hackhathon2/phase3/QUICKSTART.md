# Quick Start Guide

Get the Todo App authentication system up and running in 5 minutes.

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Neon PostgreSQL account (free tier available at https://neon.tech)

## Step 1: Get Database URL

1. Sign up at https://neon.tech
2. Create a new project
3. Copy the connection string (starts with `postgresql://`)

## Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit backend/.env:**
```env
DATABASE_URL=your-neon-postgresql-url-here
BETTER_AUTH_SECRET=create-a-random-32-character-string-here
JWT_ALGORITHM=HS256
FRONTEND_URL=http://localhost:3000
```

**Start backend:**
```bash
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8001
```

✅ Backend running at http://localhost:8000

## Step 3: Frontend Setup

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
```

**Edit frontend/.env.local:**
```env
BETTER_AUTH_SECRET=same-secret-as-backend
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Start frontend:**
```bash
npm run dev
```

✅ Frontend running at http://localhost:3000

## Step 4: Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Get Started" to sign up
3. Fill in your email and password
4. You'll be redirected to the dashboard
5. Try logging out and signing in again

## Troubleshooting

### Backend won't start
- Check DATABASE_URL is correct
- Ensure virtual environment is activated
- Verify all dependencies installed: `pip list`

### Frontend won't start
- Delete `node_modules` and `.next` folders
- Run `npm install` again
- Check NEXT_PUBLIC_API_URL points to backend

### Can't connect to database
- Verify Neon PostgreSQL URL is correct
- Check your internet connection
- Ensure database is not paused (Neon free tier)

### CORS errors
- Verify FRONTEND_URL in backend/.env matches frontend URL
- Check both servers are running
- Clear browser cache

## Next Steps

- Explore the API documentation in README.md
- Check VALIDATION_REPORT.md for detailed feature list
- Review the code structure in the project folders

## Need Help?

- Check the main README.md for detailed documentation
- Review the API endpoints section
- Open an issue on GitHub

---

Happy coding! 🚀
