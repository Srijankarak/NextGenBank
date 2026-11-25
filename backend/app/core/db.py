import asyncio
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.app.core.config import settings
from backend.app.core.logging import get_logger
from backend.app.core.model_registry import load_models

logger = get_logger()

# 1. Create the Async Database Engine with Connection Pooling
engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_pre_ping=True,   # Verify connection is alive before handing it to a request
    pool_size=5,          # Keep 5 permanent open connections ready
    max_overflow=10,      # Allow up to 10 extra connections during traffic spikes
    pool_timeout=30,      # Wait max 30s for a free connection before raising error
    pool_recycle=1800,    # Refresh connections every 30 mins to avoid stale TCP drops
)

# 2. Session Factory: Creates individual AsyncSession objects per HTTP request
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Prevent SQLAlchemy from wiping attributes after commit
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency Injection generator.
    Yields a database session per request, rolls back on errors, and always closes.
    """
    session = async_session()
    try:
        yield session
    except Exception as e:
        logger.error(f"Database session error: {e}")
        if session:
            try:
                await session.rollback()
                logger.info("Successfully rolled back session after error")
            except Exception as rollback_error:
                logger.error(f"Error during session rollback: {rollback_error}")
        raise
    finally:
        if session:
            try:
                await session.close()
                logger.debug("Database session closed successfully")
            except Exception as close_error:
                logger.error(f"Error closing database session: {close_error}")


async def init_db() -> None:
    """
    Loads all SQLModel models and verifies database connectivity on startup
    with exponential backoff retries.
    """
    try:
        load_models()
        logger.info("Models loaded successfully")

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                async with engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                logger.info("Database connection verified successfully")
                break
            except Exception:
                if attempt == max_retries - 1:
                    logger.error(
                        f"Failed to verify database connection after {max_retries} attempts"
                    )
                    raise
                logger.warning(f"Database connection attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(retry_delay * (attempt + 1))

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
