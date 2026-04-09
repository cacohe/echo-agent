"""Association finding engine."""

from typing import TYPE_CHECKING, Optional

from src.logger import get_logger
from src.models.schemas import Record

if TYPE_CHECKING:
    from src.llm.openai_client import OpenAIClient
    from src.memory.vector_store import VectorStore

logger = get_logger(__name__)


class Associator:
    """Finds related records through vector similarity."""

    def __init__(
        self,
        vector_store: "VectorStore",
        llm_client: "OpenAIClient",
    ) -> None:
        self.vector_store = vector_store
        self.llm_client = llm_client

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
        """Get a record by its ID from vector store metadata."""
        results = self.vector_store.search(
            query_embedding=[0.0] * 1536,
            n_results=1,
            where={"record_id": record_id},
        )

        if results and results[0]["id"] == record_id:
            return Record(
                id=record_id,
                content=results[0]["content"],
                type=results[0]["metadata"].get("type", "text")
                if results[0]["metadata"]
                else "text",
                mood=results[0]["metadata"].get("mood")
                if results[0]["metadata"]
                else None,
            )

        return None
