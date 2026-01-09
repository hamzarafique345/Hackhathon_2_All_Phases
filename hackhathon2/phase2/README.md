# Todo App - Full-Stack Authentication System

A modern, secure full-stack todo application with JWT authentication, built with Next.js 16, FastAPI, and PostgreSQL.

## 🚀 Features

- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Modern UI**: Responsive design with shadcn/ui components and Tailwind CSS
- **Type-Safe**: Full TypeScript support on frontend, Pydantic validation on backend
- **Fast & Reliable**: Built with Next.js 16 (App Router) and FastAPI async operations
- **Database**: PostgreSQL with SQLModel ORM and connection pooling

## 📋 Tech Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: PyJWT
- **Password Hashing**: Passlib (bcrypt)
- **Database Driver**: asyncpg

### Database
- **Database**: PostgreSQL (Neon serverless)
- **Connection**: Async with connection pooling

## 🛠️ Prerequisites

- **Node.js**: 18.x or higher
- **Python**: 3.11 or higher
- **PostgreSQL**: Neon account or local PostgreSQL instance
- **Git**: For version control

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd phase2
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Configure backend/.env:**
```env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key-min-32-characters
JWT_ALGORITHM=HS256
FRONTEND_URL=http://localhost:3000
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
```

**Configure frontend/.env.local:**
```env
BETTER_AUTH_SECRET=same-as-backend-secret
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:3000

## 📚 API Documentation

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-08T12:00:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

### Sign Up
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"  // optional
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-08T12:00:00Z"
  },
  "token": "jwt-token",
  "expiresAt": "2026-01-09T12:00:00Z"
}
```

### Sign In
```http
POST /auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "rememberMe": false  // optional, default: false
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-08T12:00:00Z"
  },
  "token": "jwt-token",
  "expiresAt": "2026-01-09T12:00:00Z"
}
```

### Verify Token
```http
GET /auth/verify
Authorization: Bearer <jwt-token>
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-01-08T12:00:00Z"
}
```

## 🎨 Application Routes

### Public Routes
- `/` - Landing page with features and call-to-action
- `/signup` - User registration form
- `/signin` - User authentication form

### Protected Routes
- `/dashboard` - User dashboard (requires authentication)

## 🔒 Security Features

- **Password Hashing**: Bcrypt with 12 rounds minimum
- **JWT Tokens**: Secure token generation and verification
- **Token Expiry**: 24 hours (default) or 7 days (remember me)
- **CORS Protection**: Restricted to frontend origin
- **SQL Injection Protection**: SQLModel/SQLAlchemy parameterized queries
- **Input Validation**: Pydantic models on backend, client-side validation on frontend
- **Authentication Guards**: Protected routes redirect to sign-in if not authenticated

## 📱 Responsive Design

The application is fully responsive with breakpoints at:
- **Mobile**: 375px
- **Tablet**: 768px
- **Desktop**: 1440px

## 🏗️ Project Structure

```
phase2/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application
│   │   ├── models.py        # Database models
│   │   ├── database.py      # Database configuration
│   │   └── auth.py          # JWT utilities
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── .gitignore
│
└── frontend/
    ├── app/
    │   ├── page.tsx         # Landing page
    │   ├── layout.tsx       # Root layout with AuthProvider
    │   ├── globals.css      # Global styles
    │   ├── signup/
    │   │   └── page.tsx     # Sign-up page
    │   ├── signin/
    │   │   └── page.tsx     # Sign-in page
    │   └── dashboard/
    │       └── page.tsx     # Protected dashboard
    ├── components/
    │   ├── ui/              # shadcn/ui components
    │   └── auth/
    │       └── AuthContext.tsx  # Auth state management
    ├── lib/
    │   ├── api-client.ts    # Axios instance with interceptors
    │   ├── auth.ts          # Auth utility functions
    │   └── utils.ts         # Utility functions
    ├── package.json
    ├── .env.example
    └── .gitignore
```

## 🧪 Testing

### Manual Testing Checklist

1. **Sign Up Flow**
   - [ ] Navigate to /signup
   - [ ] Fill in email, password, confirm password
   - [ ] Submit form
   - [ ] Verify redirect to dashboard
   - [ ] Check user data in database

2. **Sign In Flow**
   - [ ] Navigate to /signin
   - [ ] Enter registered credentials
   - [ ] Test "Remember me" checkbox
   - [ ] Submit form
   - [ ] Verify redirect to dashboard

3. **Protected Routes**
   - [ ] Access /dashboard without authentication
   - [ ] Verify redirect to /signin
   - [ ] Sign in and access /dashboard
   - [ ] Verify user information displayed

4. **Logout**
   - [ ] Click logout button on dashboard
   - [ ] Verify redirect to landing page
   - [ ] Try accessing /dashboard
   - [ ] Verify redirect to /signin

5. **Error Handling**
   - [ ] Try signing up with existing email
   - [ ] Try signing in with wrong password
   - [ ] Test form validation errors
   - [ ] Test network error handling

## 🚢 Deployment

### Backend Deployment (Recommended: Railway, Render, or Fly.io)

1. Set environment variables:
   - `DATABASE_URL`: Production PostgreSQL URL
   - `BETTER_AUTH_SECRET`: Secure random string (32+ characters)
   - `JWT_ALGORITHM`: HS256
   - `FRONTEND_URL`: Production frontend URL

2. Deploy command:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

### Frontend Deployment (Recommended: Vercel)

1. Set environment variables:
   - `BETTER_AUTH_SECRET`: Same as backend
   - `BETTER_AUTH_URL`: Production frontend URL
   - `NEXT_PUBLIC_API_URL`: Production backend URL

2. Build command: `npm run build`
3. Start command: `npm start`

## 📝 Environment Variables

### Backend (.env)
| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@host/db |
| BETTER_AUTH_SECRET | JWT secret key (32+ chars) | your-secret-key-here |
| JWT_ALGORITHM | JWT algorithm | HS256 |
| FRONTEND_URL | Frontend origin for CORS | http://localhost:3000 |

### Frontend (.env.local)
| Variable | Description | Example |
|----------|-------------|---------|
| BETTER_AUTH_SECRET | JWT secret (match backend) | your-secret-key-here |
| BETTER_AUTH_URL | Frontend URL | http://localhost:3000 |
| NEXT_PUBLIC_API_URL | Backend API URL | http://localhost:8000 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [shadcn/ui](https://ui.shadcn.com/) - UI component library
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [Neon](https://neon.tech/) - Serverless PostgreSQL

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ using Next.js, FastAPI, and PostgreSQL
