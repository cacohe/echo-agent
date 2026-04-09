"""Tests for data models."""

import pytest
from src.models.schemas import (
    RecordCreate,
    RecordType,
    Mood,
    InsightType,
    ReminderCreate,
)


def test_record_create_validation():
    """Test RecordCreate validation."""
    record = RecordCreate(content="Test record", type=RecordType.TEXT)
    assert record.content == "Test record"
    assert record.type == RecordType.TEXT


def test_record_create_with_mood():
    """Test RecordCreate with mood."""
    record = RecordCreate(
        content="Feeling good today", type=RecordType.TEXT, mood=Mood.HAPPY
    )
    assert record.mood == Mood.HAPPY


def test_reminder_create():
    """Test ReminderCreate validation."""
    reminder = ReminderCreate(
        condition="下次我记录加班", action="问我还记得跳槽的纠结吗"
    )
    assert reminder.condition == "下次我记录加班"
