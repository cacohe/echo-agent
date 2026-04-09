"""FastAPI endpoints for insights and reminders."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.core.processor import RecordProcessor
from src.llm.openai_client import OpenAIClient
from src.memory.sqlite_store import SQLiteStore
from src.memory.vector_store import VectorStore
from src.models.schemas import Reminder, ReminderCreate
from src.config import config

router = APIRouter(prefix="/api/insights", tags=["insights"])

_processor: Optional[RecordProcessor] = None

_reminders: list[Reminder] = []


def get_processor() -> RecordProcessor:
    """Singleton factory for RecordProcessor."""
    global _processor
    if _processor is None:
        config.ensure_dirs()
        sqlite_store = SQLiteStore(config.DB_PATH)
        vector_store = VectorStore(config.VECTOR_DIR)
        llm_client = OpenAIClient()
        _processor = RecordProcessor(sqlite_store, vector_store, llm_client)
    return _processor


@router.get("/weekly")
async def get_weekly_report(period: Optional[str] = None) -> dict:
    """Get weekly insight report for the specified period."""
    processor = get_processor()
    report = processor.generate_weekly_report(period or "")
    return report


@router.get("/reminders", response_model=list[Reminder])
async def get_reminders() -> list[Reminder]:
    """Get all active reminders."""
    processor = get_processor()
    reminders = processor.sqlite_store.get_active_reminders()
    return reminders


@router.post(
    "/reminders",
    response_model=Reminder,
    status_code=status.HTTP_201_CREATED,
)
async def create_reminder(request: ReminderCreate) -> Reminder:
    """Create a new reminder."""
    processor = get_processor()

    reminder = Reminder(
        condition=request.condition,
        action=request.action,
        record_id=request.record_id,
    )

    processor.sqlite_store.save_reminder(reminder)
    return reminder
