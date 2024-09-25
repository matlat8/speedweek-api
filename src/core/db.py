
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncio
from sqlalchemy.exc import InterfaceError
from loguru import logger

# Import Models
# from core.models.auth import User
from src.config import settings

import src.log_config


Base = declarative_base()

# Database Configuration
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:"
    f"{settings.db_pass}@{settings.db_host}:"
    f"{settings.db_port}/{settings.db_name}"
)

# Engine Creation
engine = create_async_engine(
    DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=300, pool_pre_ping=True, echo=True
)

# Session Factory
AsyncSessionFactory = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# Dependency for Sessions
async def get_db_session() -> AsyncSession:
    retry_count = 3
    wait = 1
    attempt = 0
    while attempt < retry_count:
        session = None
        try:
            session = AsyncSessionFactory()
            async with session:
                yield session
            return  # If session creation is successful, exit the function
        except InterfaceError as e:
            if "connection is closed" in str(e) and session:
                logger.warning("Retrying database connection")
                await session.close()
            if attempt + 1 < retry_count:
                attempt += 1
                await asyncio.sleep(wait)
                logger.warning(f"Retrying database connection. Attempt {attempt}")
                wait *= 2  # Exponential backoff
            else:
                logger.error("Failed to connect to the database")
                raise  # Reraise if it's the last attempt or an unexpected error
        except Exception:
            if session:
                await session.close()
            raise
        finally:
            if session:
                await session.close()


# Utility Functions 
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
