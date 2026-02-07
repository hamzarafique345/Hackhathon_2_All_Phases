# Quickstart Guide: Authentication and Landing Page

**Feature**: 002-auth-landing
**Date**: 2026-01-08
**Purpose**: Setup instructions for local development environment

## Prerequisites

Before starting, ensure you have the following installed:

- **Node.js**: 18.x or higher (for Next.js 16)
- **Python**: 3.11 or higher
- **npm** or **yarn**: Latest version
- **pip**: Latest version
- **Git**: For version control
- **Neon Account**: Free tier account at https://neon.tech

## Project Structure

```
phase2/
├── frontend/          # Next.js 16 application
├── backend/           # FastAPI application
└── specs/             # Feature specifications
```

## Setup Instructions

### 1. Clone Repository and Checkout Branch

```bash
# Navigate to project root
cd "C:\Officialy Hamza\Test\Hackhathon 2\phase2"

# Ensure you're on the feature branch
git checkout 002-auth-landing
```

---

### 2. Backend Setup

#### 2.1 Create Backend Directory Structure

```bash
# Create backend directories
mkdir -p backend/src
cd backend
```

#### 2.2 Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 2.3 Install Backend Dependencies

Create `requirements.txt`:

```txt
fastapi==0.110.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
pyjwt==2.8.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
asyncpg==0.29.0
python-multipart==0.0.9
```

Install dependencies:

```bash
pip install -r requirements.txt
```

#### 2.4 Configure Backend Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.neon.tech/dbname?sslmode=require

# Authentication Configuration
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-long-change-this-in-production
JWT_ALGORITHM=HS256

# CORS Configuration
FRONTEND_URL=http://localhost:3000
```

**Important**: Replace `DATABASE_URL` with your actual Neon PostgreSQL connection string.

Create `.env.example` for documentation:

```env
DATABASE_URL=postgresql://username:password@host/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
FRONTEND_URL=http://localhost:3000
```

#### 2.5 Setup Neon Database

1. Go to https://neon.tech and sign in
2. Create a new project (or use existing)
3. Create a new database named `todo_app`
4. Copy the connection string from Neon dashboard
5. Update `DATABASE_URL` in `.env` file

**Connection String Format**:
```
postgresql://username:password@ep-xxx-xxx.neon.tech/todo_app?sslmode=require
```

#### 2.6 Verify Backend Setup

Create a simple test file `backend/test_connection.py`:

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    database_url = os.getenv("DATABASE_URL")
    # Convert postgres:// to postgresql+asyncpg://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(database_url, echo=True)

    async with engine.begin() as conn:
        result = await conn.execute("SELECT 1")
        print("Database connection successful!")
        print(f"Result: {result.scalar()}")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run the test:

```bash
python test_connection.py
```

Expected output: "Database connection successful!"

---

### 3. Frontend Setup

#### 3.1 Navigate to Frontend Directory

```bash
cd ../frontend
```

#### 3.2 Install Frontend Dependencies

```bash
# Install existing dependencies
npm install

# Install additional dependencies for this feature
npm install better-auth axios lucide-react

# Install shadcn/ui CLI (if not already installed)
npx shadcn-ui@latest init
```

When prompted by shadcn-ui init:
- Style: Default
- Base color: Slate
- CSS variables: Yes
- TypeScript: Yes
- Import alias: @/components

#### 3.3 Install shadcn/ui Components

```bash
# Install required UI components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add card
```

#### 3.4 Configure Frontend Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
# Better Auth Configuration
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars-long-change-this-in-production
BETTER_AUTH_URL=http://localhost:3000

# Backend API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Important**: Use the SAME `BETTER_AUTH_SECRET` as in backend `.env` file.

Create `.env.example` for documentation:

```env
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 3.5 Verify Frontend Setup

```bash
# Start development server
npm run dev
```

Expected output:
```
▲ Next.js 16.x.x
- Local:        http://localhost:3000
- Ready in X.Xs
```

Open browser to http://localhost:3000 to verify Next.js is running.

---

### 4. Generate Shared Secret

Both frontend and backend must use the SAME `BETTER_AUTH_SECRET`. Generate a secure secret:

**Option 1: Using Node.js**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**Option 2: Using Python**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Option 3: Using OpenSSL**
```bash
openssl rand -hex 32
```

Copy the generated secret and update BOTH:
- `backend/.env` → `BETTER_AUTH_SECRET`
- `frontend/.env.local` → `BETTER_AUTH_SECRET`

---

### 5. Update .gitignore

Ensure `.env` files are not committed to version control.

Add to `backend/.gitignore`:
```
.env
venv/
__pycache__/
*.pyc
```

Add to `frontend/.gitignore` (if not already present):
```
.env.local
.env*.local
```

---

## Running the Application

### Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already active)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Start Frontend Server

In a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Start Next.js development server
npm run dev
```

Expected output:
```
▲ Next.js 16.x.x
- Local:        http://localhost:3000
- Ready in X.Xs
```

---

## Verify Setup

### 1. Check Backend Health

Open browser or use curl:

```bash
curl http://localhost:8000/health
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

### 2. Check Frontend

Open browser to http://localhost:3000

You should see the Next.js default page (landing page will be implemented in tasks phase).

### 3. Check CORS Configuration

CORS should allow frontend (localhost:3000) to communicate with backend (localhost:8000).

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Ensure virtual environment is activated and dependencies are installed
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```

**Issue**: `Database connection failed`
- **Solution**: Verify `DATABASE_URL` in `.env` is correct
- Check Neon dashboard for connection string
- Ensure `?sslmode=require` is appended to connection string
- Test connection with `test_connection.py` script

**Issue**: `BETTER_AUTH_SECRET not found`
- **Solution**: Ensure `.env` file exists in `backend/` directory
- Verify `BETTER_AUTH_SECRET` is set in `.env`
- Restart backend server after updating `.env`

### Frontend Issues

**Issue**: `Module not found: Can't resolve 'better-auth'`
- **Solution**: Install better-auth
  ```bash
  npm install better-auth
  ```

**Issue**: `NEXT_PUBLIC_API_URL is undefined`
- **Solution**: Ensure `.env.local` file exists in `frontend/` directory
- Verify `NEXT_PUBLIC_API_URL` is set
- Restart Next.js dev server after updating `.env.local`

**Issue**: shadcn/ui components not found
- **Solution**: Run shadcn-ui init and add components
  ```bash
  npx shadcn-ui@latest init
  npx shadcn-ui@latest add button input label card
  ```

### CORS Issues

**Issue**: `CORS policy: No 'Access-Control-Allow-Origin' header`
- **Solution**: Verify backend CORS configuration in `main.py`
- Ensure `allow_origins` includes `http://localhost:3000`
- Ensure `allow_credentials=True` for cookie-based auth

---

## Development Workflow

### 1. Start Both Servers

Always run both backend and frontend servers during development:

**Terminal 1 (Backend)**:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```

### 2. Hot Reload

Both servers support hot reload:
- **Backend**: Changes to Python files automatically reload server
- **Frontend**: Changes to TypeScript/React files automatically refresh browser

### 3. Database Changes

When modifying database models:
1. Update models in `backend/src/models.py`
2. Create migration (future phase with Alembic)
3. Apply migration to database
4. Restart backend server

---

## Next Steps

After completing this setup:

1. ✅ Environment configured and verified
2. ⏭️ Run `/sp.tasks` to generate detailed task breakdown
3. ⏭️ Execute tasks via Claude Code to implement features
4. ⏭️ Test authentication flow end-to-end

---

## Quick Reference

### Backend Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn src.main:app --reload --port 8000

# Test database connection
python test_connection.py
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Add shadcn/ui component
npx shadcn-ui@latest add <component-name>

# Build for production
npm run build
```

### Environment Variables

**Backend** (`.env`):
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret (32+ chars)
- `JWT_ALGORITHM`: HS256
- `FRONTEND_URL`: http://localhost:3000

**Frontend** (`.env.local`):
- `BETTER_AUTH_SECRET`: Same as backend
- `BETTER_AUTH_URL`: http://localhost:3000
- `NEXT_PUBLIC_API_URL`: http://localhost:8000

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review constitution at `.specify/memory/constitution.md`
3. Review feature spec at `specs/002-auth-landing/spec.md`
4. Review implementation plan at `specs/002-auth-landing/plan.md`
