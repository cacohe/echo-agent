"""
Configuration management - environment variables and app settings.
Loads environment variables from .env file in project root.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


PROJECT_ROOT: Path = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class Config:
    """Application configuration."""

    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    DB_PATH: Path = DATA_DIR / "echo.db"
    VECTOR_DIR: Path = DATA_DIR / "chromadb"

    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    MINIMAX_API_KEY: Optional[str] = os.getenv("MINIMAX_API_KEY")
    MINIMAX_MODEL: str = os.getenv("MINIMAX_MODEL", "M2-her")
    MINIMAX_BASE_URL: str = os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.com")

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT") or "8000")

    LOG_LEVEL: int = int(os.getenv("LOG_LEVEL", logging.INFO))

    @classmethod
    def ensure_dirs(cls):
        """Ensure data directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.VECTOR_DIR.mkdir(exist_ok=True)


config = Config()
