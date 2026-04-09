"""Tests for API endpoints."""

from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.core.processor import RecordProcessor
from src.models.schemas import (
    Insight,
    InsightType,
    Mood,
    Record,
    RecordCreate,
    RecordResponse,
    RecordType,
    Reminder,
)
from src.api.records import RecordResponseData


@pytest.fixture
def mock_processor():
    processor = MagicMock(spec=RecordProcessor)
    return processor


@pytest.fixture
def mock_record():
    return Record(
        id=uuid4(),
        content="Test record content",
        type=RecordType.TEXT,
        mood=Mood.HAPPY,
        context={"source": "test"},
        created_at=datetime.utcnow(),
        embedding=[0.1] * 1536,
    )


@pytest.fixture
def mock_insight(mock_record):
    return Insight(
        id=uuid4(),
        record_id=mock_record.id,
        type=InsightType.ASSOCIATION,
        content="Test insight content",
        confidence=0.85,
        related_record_ids=[],
        created_at=datetime.utcnow(),
    )


class TestRecordsAPI:
    """Tests for records API endpoints."""

    def test_record_create_request_model(self):
        """Test RecordCreateRequest model validation."""
        request = RecordCreate(
            content="Test content",
            type=RecordType.TEXT,
            mood=Mood.HAPPY,
        )
        assert request.content == "Test content"
        assert request.type == RecordType.TEXT
        assert request.mood == Mood.HAPPY

    def test_record_response_model(self, mock_record):
        """Test RecordResponse model."""
        response = RecordResponse(
            id=mock_record.id,
            content=mock_record.content,
            type=mock_record.type,
            mood=mock_record.mood,
            context=mock_record.context,
            created_at=mock_record.created_at,
        )
        assert response.content == "Test record content"
        assert response.mood == Mood.HAPPY

    def test_record_response_data_model(self, mock_record, mock_insight):
        """Test RecordResponseData model with insights."""
        response = RecordResponseData(
            id=mock_record.id,
            content=mock_record.content,
            type=mock_record.type,
            mood=mock_record.mood,
            context=mock_record.context,
            created_at=mock_record.created_at,
            insights=[mock_insight],
        )
        assert len(response.insights) == 1
        assert response.insights[0].content == "Test insight content"

    def test_record_create_validation(self):
        """Test RecordCreate validation."""
        record = RecordCreate(content="Valid content")
        assert record.content == "Valid content"

        with pytest.raises(Exception):
            RecordCreate(content="")

    def test_record_type_enum(self):
        """Test RecordType enum values."""
        assert RecordType.VOICE.value == "voice"
        assert RecordType.TEXT.value == "text"

    def test_mood_enum(self):
        """Test Mood enum values."""
        assert Mood.HAPPY.value == "happy"
        assert Mood.NEUTRAL.value == "neutral"
        assert Mood.LOW.value == "low"
        assert Mood.ANGRY.value == "angry"


class TestInsightsAPI:
    """Tests for insights API endpoints."""

    def test_reminder_model(self):
        """Test Reminder model."""
        reminder = Reminder(
            condition="mood == 'low'",
            action="Send encouraging message",
        )
        assert reminder.condition == "mood == 'low'"
        assert reminder.action == "Send encouraging message"
        assert reminder.is_active is True

    def test_insight_model(self, mock_record):
        """Test Insight model."""
        insight = Insight(
            record_id=mock_record.id,
            type=InsightType.PATTERN,
            content="You tend to feel low on Mondays",
            confidence=0.75,
        )
        assert insight.type == InsightType.PATTERN
        assert insight.confidence == 0.75

    def test_insight_type_enum(self):
        """Test InsightType enum values."""
        assert InsightType.ASSOCIATION.value == "association"
        assert InsightType.PATTERN.value == "pattern"
        assert InsightType.COUNTERFACTUAL.value == "counterfactual"


class TestWeeklyReport:
    """Tests for weekly report generation."""

    def test_weekly_report_structure(self):
        """Test weekly report data structure."""
        report = {
            "period": "2024-01",
            "total_records": 5,
            "mood_distribution": {"happy": 3, "neutral": 2},
            "patterns": [
                {
                    "name": "mood_trend",
                    "description": "Improving mood",
                    "frequency": 3,
                    "confidence": 0.8,
                }
            ],
            "highlight": "Great week overall!",
        }

        assert report["period"] == "2024-01"
        assert report["total_records"] == 5
        assert "mood_distribution" in report
        assert "patterns" in report
        assert "highlight" in report

    def test_empty_weekly_report(self):
        """Test empty weekly report structure."""
        report = {
            "period": "2024-02",
            "total_records": 0,
            "mood_distribution": {},
            "patterns": [],
            "highlight": "本周还没有记录。",
        }

        assert report["total_records"] == 0
        assert report["mood_distribution"] == {}
        assert report["highlight"] == "本周还没有记录。"
