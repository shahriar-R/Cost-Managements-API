import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database

# Environment variables (default values for dev)
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "expenses")

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Base class for SQLAlchemy models
Base = declarative_base()

# Async engine for SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=False, future=True)


async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Databases package instance
database = Database(DATABASE_URL)


# Dependency for FastAPI routes/services
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
