"""
Database configuration and connection management for Neon PostgreSQL.
"""
import os
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Convert postgres:// to postgresql+asyncpg:// for async support
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove sslmode and channel_binding from URL (asyncpg doesn't support them in URL)
# We'll configure SSL via connect_args instead
if "?" in DATABASE_URL:
    base_url, query_string = DATABASE_URL.split("?", 1)
    # Remove sslmode and channel_binding parameters
    params = [p for p in query_string.split("&") if not p.startswith("sslmode=") and not p.startswith("channel_binding=")]
    DATABASE_URL = base_url + ("?" + "&".join(params) if params else "")

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Additional connections when pool exhausted
    pool_pre_ping=True,  # Verify connections before use
    connect_args={
        "ssl": "require",  # Enable SSL for Neon
    }
)

# Create async session factory
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_db_and_tables():
    """Create database tables from SQLModel metadata."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """Dependency for getting async database session."""
    async with async_session_maker() as session:
        yield session
