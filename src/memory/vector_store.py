"""Vector storage using ChromaDB."""

from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings


class VectorStore:
    """ChromaDB vector store for semantic search."""

    def __init__(self, persist_dir: Path) -> None:
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(name="records")

    def add_record(
        self,
        record_id: str,
        content: str,
        embedding: list[float],
        metadata: Optional[dict] = None,
    ) -> None:
        self.collection.add(
            ids=[record_id],
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata] if metadata else None,
        )

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 5,
        where: Optional[dict] = None,
    ) -> list[dict]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )
        if not results["ids"] or not results["ids"][0]:
            return []
        return [
            {
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
                if results["metadatas"]
                else None,
                "distance": results["distances"][0][i]
                if results.get("distances")
                else None,
            }
            for i in range(len(results["ids"][0]))
        ]

    def delete_record(self, record_id: str) -> None:
        self.collection.delete(ids=[record_id])
