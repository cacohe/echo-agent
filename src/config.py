"""
Configuration management - environment variables and app settings.
"""

import os
import logging
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""

    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    DB_PATH: Path = DATA_DIR / "echo.db"
    VECTOR_DIR: Path = DATA_DIR / "chromadb"

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    LOG_LEVEL: int = logging.INFO

    @classmethod
    def ensure_dirs(cls):
        """Ensure data directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.VECTOR_DIR.mkdir(exist_ok=True)


config = Config()
