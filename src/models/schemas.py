"""
Pydantic models for API request/response and internal data structures.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RecordType(str, Enum):
    """Type of record input."""

    VOICE = "voice"
    TEXT = "text"


class InsightType(str, Enum):
    """Type of insight generated."""

    ASSOCIATION = "association"
    PATTERN = "pattern"
    COUNTERFACTUAL = "counterfactual"


class Mood(str, Enum):
    """Emotional mood tags."""

    HAPPY = "happy"
    NEUTRAL = "neutral"
    LOW = "low"
    ANGRY = "angry"


class RecordCreate(BaseModel):
    """Request model for creating a record."""

    content: str = Field(..., min_length=1, max_length=5000)
    type: RecordType = RecordType.TEXT
    mood: Optional[Mood] = None
    context: Optional[dict] = None


class Record(BaseModel):
    """Internal record model."""

    id: UUID = Field(default_factory=uuid4)
    content: str
    type: RecordType
    mood: Optional[Mood] = None
    context: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    embedding: Optional[list[float]] = None


class RecordResponse(BaseModel):
    """Response model for a record."""

    id: UUID
    content: str
    type: RecordType
    mood: Optional[Mood] = None
    context: Optional[dict] = None
    created_at: datetime


class Insight(BaseModel):
    """Insight generated from a record."""

    id: UUID = Field(default_factory=uuid4)
    record_id: UUID
    type: InsightType
    content: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    related_record_ids: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReminderCreate(BaseModel):
    """Request model for creating a reminder."""

    condition: str = Field(..., min_length=1)
    action: str = Field(..., min_length=1)
    record_id: Optional[UUID] = None


class Reminder(BaseModel):
    """Reminder model."""

    id: UUID = Field(default_factory=uuid4)
    condition: str
    action: str
    record_id: Optional[UUID] = None
    is_active: bool = True
    next_trigger: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PatternInfo(BaseModel):
    """Pattern information."""

    name: str
    description: str
    frequency: int = Field(..., ge=0)
    confidence: float = Field(..., ge=0.0, le=1.0)


class WeeklyReport(BaseModel):
    """Weekly insight report."""

    period: str
    total_records: int
    mood_distribution: dict[str, int]
    patterns: list[PatternInfo]
    highlight: str
