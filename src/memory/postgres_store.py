"""PostgreSQL storage for structured data (production)."""

import json
from contextlib import contextmanager
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.models.schemas import Insight, InsightType, Record, RecordType, Reminder


class PostgresStore:
    """PostgreSQL storage for records, insights, and reminders."""

    def __init__(self, database_url: str) -> None:
        self.engine: Engine = create_engine(database_url)
        self._SessionLocal = sessionmaker(bind=self.engine)
        self._init_db()

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    type TEXT NOT NULL,
                    mood TEXT,
                    context TEXT,
                    embedding TEXT,
                    created_at TIMESTAMP NOT NULL
                )
                """)
            )
            conn.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS idx_records_created_at ON records(created_at DESC)"
                )
            )

            conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS insights (
                    id TEXT PRIMARY KEY,
                    record_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    related_record_ids TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (record_id) REFERENCES records(id)
                )
                """)
            )

            conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id TEXT PRIMARY KEY,
                    condition TEXT NOT NULL,
                    action TEXT NOT NULL,
                    record_id TEXT,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    next_trigger TIMESTAMP,
                    created_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (record_id) REFERENCES records(id)
                )
                """)
            )
            conn.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS idx_reminders_is_active ON reminders(is_active)"
                )
            )

    @contextmanager
    def _get_conn(self):
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def save_record(self, record: Record) -> Record:
        with self.engine.begin() as conn:
            embedding_str = json.dumps(record.embedding) if record.embedding else None
            conn.execute(
                text("""
                INSERT INTO records (id, content, type, mood, context, embedding, created_at)
                VALUES (:id, :content, :type, :mood, :context, :embedding, :created_at)
                ON CONFLICT (id) DO UPDATE SET
                    content = EXCLUDED.content,
                    mood = EXCLUDED.mood,
                    context = EXCLUDED.context
                """),
                {
                    "id": str(record.id),
                    "content": record.content,
                    "type": record.type.value,
                    "mood": record.mood.value if record.mood else None,
                    "context": json.dumps(record.context) if record.context else None,
                    "embedding": embedding_str,
                    "created_at": record.created_at,
                },
            )
        return record

    def get_record(self, record_id: str) -> Optional[Record]:
        with self.engine.begin() as conn:
            row = conn.execute(
                text("SELECT * FROM records WHERE id = :id"), {"id": record_id}
            ).fetchone()
            if not row:
                return None
            return self._row_to_record(row)

    def delete_record(self, record_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text("DELETE FROM insights WHERE record_id = :id"), {"id": record_id}
            )
            conn.execute(
                text("DELETE FROM reminders WHERE record_id = :id"), {"id": record_id}
            )
            conn.execute(text("DELETE FROM records WHERE id = :id"), {"id": record_id})

    def get_recent_records(self, limit: int = 50) -> list[Record]:
        with self.engine.begin() as conn:
            rows = conn.execute(
                text("SELECT * FROM records ORDER BY created_at DESC LIMIT :limit"),
                {"limit": limit},
            ).fetchall()
            return [self._row_to_record(row) for row in rows]

    def _row_to_record(self, row) -> Record:
        return Record(
            id=row.id,
            content=row.content,
            type=RecordType(row.type),
            mood=row.mood,
            context=json.loads(row.context) if row.context else None,
            embedding=json.loads(row.embedding) if row.embedding else None,
            created_at=row.created_at,
        )

    def save_insight(self, insight: Insight) -> Insight:
        with self.engine.begin() as conn:
            conn.execute(
                text("""
                INSERT INTO insights (id, record_id, type, content, confidence, related_record_ids, created_at)
                VALUES (:id, :record_id, :type, :content, :confidence, :related_record_ids, :created_at)
                ON CONFLICT (id) DO UPDATE SET
                    content = EXCLUDED.content,
                    confidence = EXCLUDED.confidence
                """),
                {
                    "id": str(insight.id),
                    "record_id": str(insight.record_id),
                    "type": insight.type.value,
                    "content": insight.content,
                    "confidence": insight.confidence,
                    "related_record_ids": json.dumps(
                        [str(id) for id in insight.related_record_ids]
                    ),
                    "created_at": insight.created_at,
                },
            )
        return insight

    def get_insight(self, insight_id: str) -> Optional[Insight]:
        with self.engine.begin() as conn:
            row = conn.execute(
                text("SELECT * FROM insights WHERE id = :id"), {"id": insight_id}
            ).fetchone()
            if not row:
                return None
            return self._row_to_insight(row)

    def _row_to_insight(self, row) -> Insight:
        return Insight(
            id=row.id,
            record_id=row.record_id,
            type=InsightType(row.type),
            content=row.content,
            confidence=row.confidence,
            related_record_ids=[UUID(id) for id in json.loads(row.related_record_ids)],
            created_at=row.created_at,
        )

    def save_reminder(self, reminder: Reminder) -> Reminder:
        with self.engine.begin() as conn:
            conn.execute(
                text("""
                INSERT INTO reminders (id, condition, action, record_id, is_active, next_trigger, created_at)
                VALUES (:id, :condition, :action, :record_id, :is_active, :next_trigger, :created_at)
                ON CONFLICT (id) DO UPDATE SET
                    condition = EXCLUDED.condition,
                    action = EXCLUDED.action,
                    is_active = EXCLUDED.is_active
                """),
                {
                    "id": str(reminder.id),
                    "condition": reminder.condition,
                    "action": reminder.action,
                    "record_id": str(reminder.record_id)
                    if reminder.record_id
                    else None,
                    "is_active": reminder.is_active,
                    "next_trigger": reminder.next_trigger,
                    "created_at": reminder.created_at,
                },
            )
        return reminder

    def get_active_reminders(self) -> list[Reminder]:
        with self.engine.begin() as conn:
            rows = conn.execute(
                text("SELECT * FROM reminders WHERE is_active = TRUE")
            ).fetchall()
            return [self._row_to_reminder(row) for row in rows]

    def _row_to_reminder(self, row) -> Reminder:
        return Reminder(
            id=row.id,
            condition=row.condition,
            action=row.action,
            record_id=row.record_id,
            is_active=row.is_active,
            next_trigger=row.next_trigger,
            created_at=row.created_at,
        )
