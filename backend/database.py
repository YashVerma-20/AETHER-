"""AETHER Database Session and Engine Management.

Implements lightweight connection pooling and session generators.
"""

import logging
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Engine configuration with conservative connection pool
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_pre_ping=True,  # Discards stale or severed connections safely
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency that yields an active database session and guarantees cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection() -> dict:
    """Verifies live PostgreSQL connectivity by executing a lightweight ping query.
    
    Returns:
        dict: Status dictionary with latency and server version info.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 AS is_alive, version();")).mappings().first()
            return {
                "status": "healthy",
                "connected": True,
                "version": result["version"],
                "database": settings.DB_NAME,
                "port": settings.DB_PORT,
            }
    except Exception as exc:
        logger.error("Database connection check failed: %s", exc)
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(exc),
            "database": settings.DB_NAME,
            "port": settings.DB_PORT,
        }
