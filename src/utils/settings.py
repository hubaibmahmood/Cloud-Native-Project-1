"""Application settings management using pydantic-settings."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    All settings can be overridden via environment variables or .env file.
    """

    # Database configuration
    DATABASE_URL: str = "postgresql+asyncpg://localhost/taskdb"

    @field_validator("DATABASE_URL")
    @classmethod
    def clean_database_url(cls, v: str) -> str:
        """Clean database URL for asyncpg compatibility.

        Neon PostgreSQL and other providers may use parameters not supported by asyncpg:
        - sslmode=require → ssl=require (asyncpg uses 'ssl' not 'sslmode')
        - channel_binding=require → removed (asyncpg doesn't support this)
        """
        # Replace sslmode with ssl for asyncpg
        if "sslmode=" in v:
            v = v.replace("sslmode=", "ssl=")

        # Remove channel_binding parameter (not supported by asyncpg)
        if "channel_binding=require" in v:
            # Remove &channel_binding=require or ?channel_binding=require
            v = v.replace("&channel_binding=require", "")
            v = v.replace("?channel_binding=require", "")
            # Clean up if we removed the first param (leaving orphaned &)
            v = v.replace("?&", "?")

        return v

    # Logging configuration
    LOG_LEVEL: str = "INFO"

    # API configuration
    API_PREFIX: str = "/tasks"

    # Database configuration
    ENVIRONMENT: str = "development"  # development, staging, production

    # Model configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields from .env
    )


# Global settings instance
settings = Settings()
