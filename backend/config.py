"""AETHER Configuration Module.

Loads environment variables with safe defaults and validates connection parameters.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings schema backed by pydantic-settings."""

    # Environment
    AETHER_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # API Host/Port
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    # PostgreSQL Database
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5433
    DB_USER: str = "aether_user"
    DB_PASSWORD: str = ""
    DB_NAME: str = "aether_db"
    DATABASE_URL: str = ""

    # Hardware-conscious connection pooling
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 5
    DB_POOL_TIMEOUT: int = 30

    # Local LLM Runtime
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton instance of application settings."""
    return Settings()
