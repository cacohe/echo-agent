"""Association finding engine."""

from typing import TYPE_CHECKING, Optional

from src.logger import get_logger
from src.models.schemas import Record

if TYPE_CHECKING:
    from src.llm.openai_client import OpenAIClient
    from src.memory.sqlite_store import SQLiteStore
    from src.memory.vector_store import VectorStore

logger = get_logger(__name__)


class Associator:
    """Finds related records through vector similarity."""

    def __init__(
        self,
        vector_store: "VectorStore",
        llm_client: "OpenAIClient",
        sqlite_store: "SQLiteStore",
    ) -> None:
        self.vector_store = vector_store
        self.llm_client = llm_client
        self.sqlite_store = sqlite_store

    def find_related(self, record: Record, limit: int = 5) -> list[Record]:
        """Find records related to the given record."""
        if not record.embedding:
            return []

        results = self.vector_store.search(
            query_embedding=record.embedding,
            n_results=limit + 1,
        )

        related_records = []
        for r in results:
            if r["id"] != str(record.id):
                related_record = self._get_record_by_id(r["id"])
                if related_record:
                    related_records.append(related_record)

                if len(related_records) >= limit:
                    break

        return related_records

    def _get_record_by_id(self, record_id: str) -> Optional[Record]:
        """Get a record by its ID from SQLite store."""
        try:
            return self.sqlite_store.get_record(record_id)
        except Exception:
            return None
