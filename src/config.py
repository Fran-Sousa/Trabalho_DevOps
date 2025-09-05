"""Application settings."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


class Settings:
    """Development environment settings using .env files."""

    def __init__(self):
        """Config initialization."""
        self.database_url: str = os.getenv(
            "DATABASE_URL", "sqlite:///exemplo.db"
        )
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8001"))
        self.reload: bool = os.getenv("RELOAD", "false").lower() == "true"
        self.log_level: str = os.getenv("LOG_LEVEL", "info")

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return DOTENV_AVAILABLE and self.debug


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
