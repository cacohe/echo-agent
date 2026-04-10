"""Storage factory - returns appropriate store based on environment."""

from pathlib import Path
from typing import Union

from src.logger import get_logger

logger = get_logger(__name__)


def create_store() -> tuple:
    """
    Create appropriate storage instances based on environment.

    Returns (sqlite_store, vector_store) for local development
    or (postgres_store, pinecone_store) for production.
    """
    import os

    database_url = os.getenv("DATABASE_URL")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    if database_url and pinecone_api_key:
        logger.info("Using production storage (PostgreSQL + Pinecone)")
        from src.memory.postgres_store import PostgresStore
        from src.memory.pinecone_store import PineconeStore

        postgres_store = PostgresStore(database_url)
        pinecone_store = PineconeStore(
            api_key=pinecone_api_key,
            environment=os.getenv("PINECONE_ENVIRONMENT", "us-east-1"),
        )
        return postgres_store, pinecone_store
    else:
        logger.info("Using local storage (SQLite + ChromaDB)")
        from src.memory.sqlite_store import SQLiteStore
        from src.memory.vector_store import VectorStore
        from src.config import config

        config.ensure_dirs()
        sqlite_store = SQLiteStore(config.DB_PATH)
        vector_store = VectorStore(config.VECTOR_DIR)
        return sqlite_store, vector_store
