"""Tests for storage layer."""

import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from src.memory import SQLiteStore, VectorStore
from src.models.schemas import Insight, InsightType, Record, RecordType, Reminder


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sqlite_store(temp_dir):
    return SQLiteStore(temp_dir / "test.db")


@pytest.fixture
def vector_store(temp_dir):
    return VectorStore(temp_dir / "vectors")


class TestSQLiteStore:
    def test_save_and_get_record(self, sqlite_store):
        record = Record(
            id=uuid4(),
            content="Test record content",
            type=RecordType.TEXT,
            created_at=datetime.utcnow(),
        )
        saved = sqlite_store.save_record(record)
        assert saved.id == record.id

        retrieved = sqlite_store.get_record(str(record.id))
        assert retrieved is not None
        assert retrieved.id == record.id
        assert retrieved.content == "Test record content"

    def test_get_recent_records(self, sqlite_store):
        for i in range(5):
            record = Record(
                id=uuid4(),
                content=f"Record {i}",
                type=RecordType.TEXT,
                created_at=datetime.utcnow(),
            )
            sqlite_store.save_record(record)

        recent = sqlite_store.get_recent_records(limit=3)
        assert len(recent) == 3

    def test_save_insight(self, sqlite_store):
        record = Record(
            id=uuid4(),
            content="Test record",
            type=RecordType.TEXT,
            created_at=datetime.utcnow(),
        )
        sqlite_store.save_record(record)

        insight = Insight(
            id=uuid4(),
            record_id=record.id,
            type=InsightType.ASSOCIATION,
            content="Test insight",
            confidence=0.85,
            created_at=datetime.utcnow(),
        )
        saved = sqlite_store.save_insight(insight)
        assert saved.id == insight.id

    def test_save_and_get_reminder(self, sqlite_store):
        reminder = Reminder(
            id=uuid4(),
            condition="time > 9am",
            action="Start morning routine",
            created_at=datetime.utcnow(),
        )
        saved = sqlite_store.save_reminder(reminder)
        assert saved.id == reminder.id

        active = sqlite_store.get_active_reminders()
        assert len(active) == 1
        assert active[0].id == reminder.id


class TestVectorStore:
    def test_vector_store_add_and_search(self, vector_store):
        record_id = "test-record-1"
        content = "This is a test document about artificial intelligence"
        embedding = [0.1] * 768

        vector_store.add_record(record_id, content, embedding, {"source": "test"})

        query_embedding = [0.1] * 768
        results = vector_store.search(query_embedding, n_results=1)

        assert len(results) == 1
        assert results[0]["id"] == record_id
        assert results[0]["content"] == content

        vector_store.delete_record(record_id)
        results_after_delete = vector_store.search(query_embedding, n_results=1)
        assert len(results_after_delete) == 0
