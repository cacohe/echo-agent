"""Tests for core processing engine."""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from src.core.associator import Associator
from src.core.patterns import PatternAnalyzer
from src.core.processor import RecordProcessor
from src.models.schemas import Mood, Record, RecordCreate, RecordType


@pytest.fixture
def mock_sqlite_store():
    return MagicMock()


@pytest.fixture
def mock_vector_store():
    return MagicMock()


@pytest.fixture
def mock_llm_client():
    return MagicMock()


class TestRecordProcessor:
    def test_initialization(
        self, mock_sqlite_store, mock_vector_store, mock_llm_client
    ):
        processor = RecordProcessor(
            mock_sqlite_store, mock_vector_store, mock_llm_client
        )

        assert processor.sqlite_store is mock_sqlite_store
        assert processor.vector_store is mock_vector_store
        assert processor.llm_client is mock_llm_client

    def test_process_record(
        self, mock_sqlite_store, mock_vector_store, mock_llm_client
    ):
        processor = RecordProcessor(
            mock_sqlite_store, mock_vector_store, mock_llm_client
        )

        mock_llm_client.get_embedding.return_value = [0.1] * 1536
        mock_vector_store.search.return_value = []

        record_create = RecordCreate(
            content="Test content",
            type=RecordType.TEXT,
            mood=Mood.HAPPY,
        )

        record, insights = processor.process_record(record_create)

        assert record.content == "Test content"
        assert record.type == RecordType.TEXT
        assert record.mood == Mood.HAPPY
        assert record.embedding == [0.1] * 1536

        mock_sqlite_store.save_record.assert_called_once()
        mock_vector_store.add_record.assert_called_once()
        mock_llm_client.get_embedding.assert_called_once_with("Test content")

    def test_generate_weekly_report_empty(
        self, mock_sqlite_store, mock_vector_store, mock_llm_client
    ):
        processor = RecordProcessor(
            mock_sqlite_store, mock_vector_store, mock_llm_client
        )

        mock_sqlite_store.get_recent_records.return_value = []

        report = processor.generate_weekly_report("2024-01")

        assert report["total_records"] == 0
        assert report["mood_distribution"] == {}
        assert report["patterns"] == []
        assert report["highlight"] == "本周还没有记录。"

    def test_generate_weekly_report_with_records(
        self, mock_sqlite_store, mock_vector_store, mock_llm_client
    ):
        processor = RecordProcessor(
            mock_sqlite_store, mock_vector_store, mock_llm_client
        )

        mock_records = [
            Record(
                id=uuid4(),
                content="Record 1",
                type=RecordType.TEXT,
                mood=Mood.HAPPY,
                created_at=datetime(2024, 1, 15, 10, 0, 0),
            ),
            Record(
                id=uuid4(),
                content="Record 2",
                type=RecordType.TEXT,
                mood=Mood.HAPPY,
                created_at=datetime(2024, 1, 16, 14, 0, 0),
            ),
        ]

        mock_sqlite_store.get_recent_records.return_value = mock_records
        mock_llm_client.generate_weekly_summary.return_value = "本周表现不错！"

        report = processor.generate_weekly_report("2024-03")

        assert report["total_records"] == 2
        assert report["mood_distribution"]["happy"] == 2
        assert report["highlight"] == "本周表现不错！"


class TestAssociator:
    def test_initialization(
        self, mock_vector_store, mock_sqlite_store, mock_llm_client
    ):
        associator = Associator(mock_vector_store, mock_llm_client, mock_sqlite_store)

        assert associator.vector_store is mock_vector_store
        assert associator.llm_client is mock_llm_client
        assert associator.sqlite_store is mock_sqlite_store

    def test_find_related_no_embedding(
        self, mock_vector_store, mock_sqlite_store, mock_llm_client
    ):
        associator = Associator(mock_vector_store, mock_llm_client, mock_sqlite_store)

        record = Record(
            id=uuid4(),
            content="Test content",
            type=RecordType.TEXT,
            embedding=None,
        )

        related = associator.find_related(record)

        assert related == []
        mock_vector_store.search.assert_not_called()

    def test_find_related_with_embedding(
        self, mock_vector_store, mock_sqlite_store, mock_llm_client
    ):
        associator = Associator(mock_vector_store, mock_llm_client, mock_sqlite_store)

        record = Record(
            id=uuid4(),
            content="Test content",
            type=RecordType.TEXT,
            embedding=[0.1] * 1536,
        )

        mock_vector_store.search.return_value = [
            {
                "id": "2",
                "content": "Related content",
                "metadata": {"type": "text", "mood": "happy"},
            },
            {
                "id": "3",
                "content": "Another related",
                "metadata": {"type": "text", "mood": "neutral"},
            },
        ]

        with patch.object(associator, "_get_record_by_id", side_effect=["2", "3"]):
            related = associator.find_related(record, limit=5)

        mock_vector_store.search.assert_called_once()


class TestPatternAnalyzer:
    def test_initialization(self, mock_sqlite_store, mock_llm_client):
        analyzer = PatternAnalyzer(mock_sqlite_store, mock_llm_client)

        assert analyzer.sqlite_store is mock_sqlite_store
        assert analyzer.llm_client is mock_llm_client

    def test_analyze_patterns_empty_records(self, mock_sqlite_store, mock_llm_client):
        analyzer = PatternAnalyzer(mock_sqlite_store, mock_llm_client)

        patterns = analyzer.analyze_patterns([])

        assert patterns == []

    def test_analyze_patterns_insufficient_records(
        self, mock_sqlite_store, mock_llm_client
    ):
        analyzer = PatternAnalyzer(mock_sqlite_store, mock_llm_client)

        records = [
            Record(
                id=uuid4(),
                content="Record 1",
                type=RecordType.TEXT,
                mood=Mood.HAPPY,
            ),
            Record(
                id=uuid4(),
                content="Record 2",
                type=RecordType.TEXT,
                mood=Mood.HAPPY,
            ),
        ]

        patterns = analyzer.analyze_patterns(records)

        assert patterns == []

    def test_analyze_mood_pattern(self, mock_sqlite_store, mock_llm_client):
        analyzer = PatternAnalyzer(mock_sqlite_store, mock_llm_client)

        records = [
            Record(
                id=uuid4(),
                content="Record 1",
                type=RecordType.TEXT,
                mood=Mood.HAPPY,
                created_at=datetime(2024, 1, 15, 10, 0, 0),
            ),
            Record(
                id=uuid4(),
                content="Record 2",
                type=RecordType.TEXT,
                mood=Mood.HAPPY,
                created_at=datetime(2024, 1, 16, 14, 0, 0),
            ),
            Record(
                id=uuid4(),
                content="Record 3",
                type=RecordType.TEXT,
                mood=Mood.HAPPY,
                created_at=datetime(2024, 1, 17, 9, 0, 0),
            ),
        ]

        patterns = analyzer.analyze_patterns(records)

        mood_pattern = next((p for p in patterns if p.name == "mood_trend"), None)
        assert mood_pattern is not None
        assert mood_pattern.frequency == 3
