"""FastAPI endpoints for record management."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.core.processor import RecordProcessor
from src.llm.openai_client import OpenAIClient
from src.memory.sqlite_store import SQLiteStore
from src.memory.vector_store import VectorStore
from src.models.schemas import (
    Insight,
    Mood,
    Record,
    RecordCreate,
    RecordResponse,
    RecordType,
)
from src.config import config

router = APIRouter(prefix="/api/records", tags=["records"])

_processor: Optional[RecordProcessor] = None


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


class RecordResponseData(RecordResponse):
    """Response model for record (insights not fetched for single record)."""

    insights: list[Insight] = []


@router.post(
    "",
    response_model=RecordResponseData,
    status_code=status.HTTP_201_CREATED,
)
async def create_record(request: RecordCreate) -> RecordResponseData:
    """Create a new record and generate insights."""
    processor = get_processor()

    record, insights = processor.process_record(request)

    return RecordResponseData(
        id=record.id,
        content=record.content,
        type=record.type,
        mood=record.mood,
        context=record.context,
        created_at=record.created_at,
        insights=insights,
    )


@router.get("", response_model=list[RecordResponse])
async def list_records(
    limit: int = 50,
    offset: int = 0,
    mood: Optional[Mood] = None,
) -> list[RecordResponse]:
    """List all records with optional filtering."""
    processor = get_processor()
    records = processor.sqlite_store.get_recent_records(limit=limit + offset)

    if mood:
        records = [r for r in records if r.mood == mood]

    records = records[offset : offset + limit]

    return [
        RecordResponse(
            id=r.id,
            content=r.content,
            type=r.type,
            mood=r.mood,
            context=r.context,
            created_at=r.created_at,
        )
        for r in records
    ]


@router.get("/{record_id}", response_model=RecordResponse)
async def get_record(record_id: UUID) -> RecordResponse:
    """Get a single record by ID."""
    processor = get_processor()
    record = processor.sqlite_store.get_record(str(record_id))

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record {record_id} not found",
        )

    return RecordResponse(
        id=record.id,
        content=record.content,
        type=record.type,
        mood=record.mood,
        context=record.context,
        created_at=record.created_at,
    )
