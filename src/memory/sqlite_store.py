"""SQLite storage for structured data."""

import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID

import sqlite3

from src.models.schemas import Insight, InsightType, Record, RecordType, Reminder


class SQLiteStore:
    """SQLite storage for records, insights, and reminders."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    type TEXT NOT NULL,
                    mood TEXT,
                    context TEXT,
                    embedding TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_records_created_at ON records(created_at DESC)"
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS insights (
                    id TEXT PRIMARY KEY,
                    record_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    related_record_ids TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (record_id) REFERENCES records(id)
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reminders (
                    id TEXT PRIMARY KEY,
                    condition TEXT NOT NULL,
                    action TEXT NOT NULL,
                    record_id TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    next_trigger TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (record_id) REFERENCES records(id)
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_reminders_is_active ON reminders(is_active)"
            )

    @contextmanager
    def _get_conn(self):
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False, timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def save_record(self, record: Record) -> Record:
        with self._get_conn() as conn:
            embedding_str = json.dumps(record.embedding) if record.embedding else None
            conn.execute(
                """
                INSERT OR REPLACE INTO records (id, content, type, mood, context, embedding, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record.id),
                    record.content,
                    record.type.value,
                    record.mood.value if record.mood else None,
                    json.dumps(record.context) if record.context else None,
                    embedding_str,
                    record.created_at.isoformat(),
                ),
            )
            conn.commit()
        return record

    def get_record(self, record_id: str) -> Optional[Record]:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM records WHERE id = ?", (record_id,)
            ).fetchone()
            if not row:
                return None
            return self._row_to_record(row)

    def delete_record(self, record_id: str) -> None:
        with self._get_conn() as conn:
            conn.execute("DELETE FROM insights WHERE record_id = ?", (record_id,))
            conn.execute("DELETE FROM reminders WHERE record_id = ?", (record_id,))
            conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
            conn.commit()

    def get_recent_records(self, limit: int = 50) -> list[Record]:
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM records ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [self._row_to_record(row) for row in rows]

    def _row_to_record(self, row: sqlite3.Row) -> Record:
        return Record(
            id=row["id"],
            content=row["content"],
            type=RecordType(row["type"]),
            mood=row["mood"],
            context=json.loads(row["context"]) if row["context"] else None,
            embedding=json.loads(row["embedding"]) if row["embedding"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def save_insight(self, insight: Insight) -> Insight:
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO insights (id, record_id, type, content, confidence, related_record_ids, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(insight.id),
                    str(insight.record_id),
                    insight.type.value,
                    insight.content,
                    insight.confidence,
                    json.dumps([str(id) for id in insight.related_record_ids]),
                    insight.created_at.isoformat(),
                ),
            )
            conn.commit()
        return insight

    def get_insight(self, insight_id: str) -> Optional[Insight]:
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM insights WHERE id = ?", (insight_id,)
            ).fetchone()
            if not row:
                return None
            return self._row_to_insight(row)

    def _row_to_insight(self, row: sqlite3.Row) -> Insight:
        return Insight(
            id=row["id"],
            record_id=row["record_id"],
            type=InsightType(row["type"]),
            content=row["content"],
            confidence=row["confidence"],
            related_record_ids=[
                UUID(id) for id in json.loads(row["related_record_ids"])
            ],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def save_reminder(self, reminder: Reminder) -> Reminder:
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO reminders (id, condition, action, record_id, is_active, next_trigger, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(reminder.id),
                    reminder.condition,
                    reminder.action,
                    str(reminder.record_id) if reminder.record_id else None,
                    1 if reminder.is_active else 0,
                    reminder.next_trigger.isoformat()
                    if reminder.next_trigger
                    else None,
                    reminder.created_at.isoformat(),
                ),
            )
            conn.commit()
        return reminder

    def get_active_reminders(self) -> list[Reminder]:
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM reminders WHERE is_active = 1"
            ).fetchall()
            return [self._row_to_reminder(row) for row in rows]

    def _row_to_reminder(self, row: sqlite3.Row) -> Reminder:
        return Reminder(
            id=row["id"],
            condition=row["condition"],
            action=row["action"],
            record_id=row["record_id"],
            is_active=bool(row["is_active"]),
            next_trigger=datetime.fromisoformat(row["next_trigger"])
            if row["next_trigger"]
            else None,
            created_at=datetime.fromisoformat(row["created_at"]),
        )
