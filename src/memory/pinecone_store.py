"""Pinecone vector store for production."""

from typing import Optional

from pinecone import Pinecone, ServerlessSpec


class PineconeStore:
    """Pinecone vector store for semantic search (production)."""

    def __init__(
        self,
        api_key: str,
        environment: str = "us-east-1",
        index_name: str = "echo-records",
    ) -> None:
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        self._ensure_index(environment)

    def _ensure_index(self, environment: str) -> None:
        existing = self.pc.list_indexes()
        if self.index_name not in existing:
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=environment),
            )
        self.index = self.pc.Index(self.index_name)

    def add_record(
        self,
        record_id: str,
        content: str,
        embedding: list[float],
        metadata: Optional[dict] = None,
    ) -> None:
        self.index.upsert(
            vectors=[
                {
                    "id": record_id,
                    "values": embedding,
                    "metadata": {
                        "content": content,
                        **(metadata or {}),
                    },
                }
            ]
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
        where: Optional[dict] = None,
    ) -> list[dict]:
        results = self.index.query(
            vector=query_embedding,
            top_k=n_results,
            include_metadata=True,
        )

        if not results.matches:
            return []

        return [
            {
                "id": match.id,
                "content": match.metadata.get("content", ""),
                "metadata": match.metadata,
                "distance": match.score,
            }
            for match in results.matches
        ]

    def delete_record(self, record_id: str) -> None:
        self.index.delete(ids=[record_id])
