# Echo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the MVP of Echo - a personal reflection and decision-making AI assistant focused on workplace emotion and decision tracking.

**Architecture:** FastAPI backend with SQLite + ChromaDB for storage, OpenAI GPT-4o mini for LLM processing. Mobile-first API design with voice/text input and proactive insight delivery.

**Tech Stack:** Python 3.11+, FastAPI, SQLite, ChromaDB, OpenAI SDK, Pydantic, APScheduler

---

## File Structure

```
echo-agent/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration management
│   ├── logger.py               # Logger module (independent封装)
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── records.py          # Record CRUD endpoints
│   │   └── insights.py         # Insight generation endpoints
│   │
│   ├── core/                   # Core processing engine
│   │   ├── __init__.py
│   │   ├── processor.py        # Main record processor
│   │   ├── associator.py       # Implicit association engine
│   │   └── patterns.py          # Pattern recognition
│   │
│   ├── memory/                 # Storage layer
│   │   ├── __init__.py
│   │   ├── sqlite_store.py     # SQLite storage
│   │   └── vector_store.py     # ChromaDB vector storage
│   │
│   ├── llm/                    # LLM interfaces
│   │   ├── __init__.py
│   │   └── openai_client.py    # OpenAI client wrapper
│   │
│   └── models/                 # Data models
│       ├── __init__.py
│       └── schemas.py          # Pydantic models
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_processor.py
│   ├── test_associator.py
│   └── test_api.py
│
├── requirements.txt
└── README.md
```

---

## Task 1: Project Foundation

**Files:**
- Create: `src/__init__.py`
- Create: `src/logger.py`
- Create: `src/config.py`
- Create: `requirements.txt`

- [ ] **Step 1: Create requirements.txt**

```txt
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
openai==1.12.0
chromadb==0.4.22
sqlite-utils==3.35.2
apscheduler==3.10.4
python-multipart==0.0.6
httpx==0.26.0
pytest==7.4.4
pytest-asyncio==0.23.3
```

- [ ] **Step 2: Create src/__init__.py**

```python
"""Echo - Personal Reflection and Decision AI Assistant."""
__version__ = "0.1.0"
```

- [ ] **Step 3: Create src/logger.py**

```python
"""
Logger module - unified configuration, global usage.
All modules use `from src.logger import get_logger`.
Business code MUST NOT call logging.basicConfig().
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get logger instance by name.

    Args:
        name: logger name, recommend passing __name__
        level: log level, defaults to LOG_LEVEL env or INFO

    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level or logging.INFO)

    return logger
```

- [ ] **Step 4: Create src/config.py**

```python
"""
Configuration management - environment variables and app settings.
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""

    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    DB_PATH: Path = DATA_DIR / "echo.db"
    VECTOR_DIR: Path = DATA_DIR / "chromadb"

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    LOG_LEVEL: int = logging.INFO

    @classmethod
    def ensure_dirs(cls):
        """Ensure data directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.VECTOR_DIR.mkdir(exist_ok=True)


config = Config()
```

- [ ] **Step 5: Run test to verify imports work**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -c "from src.logger import get_logger; from src.config import config; print('OK')"
```

Expected: OK

- [ ] **Step 6: Commit**

```bash
git add requirements.txt src/__init__.py src/logger.py src/config.py
git commit -m "feat: add project foundation with logger and config"
```

---

## Task 2: Data Models

**Files:**
- Create: `src/models/__init__.py`
- Create: `src/models/schemas.py`
- Create: `tests/test_schemas.py`

- [ ] **Step 1: Create src/models/__init__.py**

```python
"""Data models for Echo."""
from src.models.schemas import (
    Record,
    RecordCreate,
    RecordResponse,
    Insight,
    InsightType,
    Reminder,
    ReminderCreate,
    WeeklyReport,
)

__all__ = [
    "Record",
    "RecordCreate",
    "RecordResponse",
    "Insight",
    "InsightType",
    "Reminder",
    "ReminderCreate",
    "WeeklyReport",
]
```

- [ ] **Step 2: Create src/models/schemas.py**

```python
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
    related_record_ids: list[UUID] = []
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
    frequency: int
    confidence: float


class WeeklyReport(BaseModel):
    """Weekly insight report."""
    period: str
    total_records: int
    mood_distribution: dict[str, int]
    patterns: list[PatternInfo]
    highlight: str
```

- [ ] **Step 3: Create tests/test_schemas.py**

```python
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
        content="Feeling good today",
        type=RecordType.VINE,
        mood=Mood.HAPPY
    )
    assert record.mood == Mood.HAPPY


def test_reminder_create():
    """Test ReminderCreate validation."""
    reminder = ReminderCreate(
        condition="下次我记录加班",
        action="问我还记得跳槽的纠结吗"
    )
    assert reminder.condition == "下次我记录加班"
```

- [ ] **Step 4: Run tests**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -m pytest tests/test_schemas.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add src/models/__init__.py src/models/schemas.py tests/test_schemas.py
git commit -m "feat: add data models"
```

---

## Task 3: Storage Layer (SQLite + ChromaDB)

**Files:**
- Create: `src/memory/__init__.py`
- Create: `src/memory/sqlite_store.py`
- Create: `src/memory/vector_store.py`
- Create: `tests/test_storage.py`

- [ ] **Step 1: Create src/memory/__init__.py**

```python
"""Storage layer for Echo."""
from src.memory.sqlite_store import SQLiteStore
from src.memory.vector_store import VectorStore

__all__ = ["SQLiteStore", "VectorStore"]
```

- [ ] **Step 2: Create src/memory/sqlite_store.py**

```python
"""
SQLite storage for structured records and insights.
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.logger import get_logger
from src.models.schemas import Record, Insight, Reminder, InsightType, RecordType, Mood

logger = get_logger(__name__)


class SQLiteStore:
    """SQLite storage handler."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS records (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    type TEXT NOT NULL,
                    mood TEXT,
                    context TEXT,
                    created_at TEXT NOT NULL,
                    embedding BLOB
                );

                CREATE TABLE IF NOT EXISTS insights (
                    id TEXT PRIMARY KEY,
                    record_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    related_record_ids TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (record_id) REFERENCES records(id)
                );

                CREATE TABLE IF NOT EXISTS reminders (
                    id TEXT PRIMARY KEY,
                    condition TEXT NOT NULL,
                    action TEXT NOT NULL,
                    record_id TEXT,
                    is_active INTEGER DEFAULT 1,
                    next_trigger TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (record_id) REFERENCES records(id)
                );

                CREATE INDEX IF NOT EXISTS idx_records_created_at ON records(created_at);
                CREATE INDEX IF NOT EXISTS idx_insights_record_id ON insights(record_id);
                CREATE INDEX IF NOT EXISTS idx_reminders_active ON reminders(is_active);
            """)
            conn.commit()
        logger.info(f"Database initialized at {self.db_path}")

    @contextmanager
    def _get_conn(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def save_record(self, record: Record) -> Record:
        """Save a record to database."""
        import json
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO records (id, content, type, mood, context, created_at, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record.id),
                    record.content,
                    record.type.value,
                    record.mood.value if record.mood else None,
                    json.dumps(record.context) if record.context else None,
                    record.created_at.isoformat(),
                    None,
                )
            )
            conn.commit()
        logger.info(f"Record saved: {record.id}")
        return record

    def get_record(self, record_id: str) -> Optional[Record]:
        """Get a record by ID."""
        import json
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM records WHERE id = ?", (record_id,)
            ).fetchone()
            if not row:
                return None
            return Record(
                id=row["id"],
                content=row["content"],
                type=RecordType(row["type"]),
                mood=Mood(row["mood"]) if row["mood"] else None,
                context=json.loads(row["context"]) if row["context"] else None,
                created_at=datetime.fromisoformat(row["created_at"]),
            )

    def get_recent_records(self, limit: int = 50) -> list[Record]:
        """Get recent records ordered by creation time."""
        import json
        records = []
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM records ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
            for row in rows:
                records.append(Record(
                    id=row["id"],
                    content=row["content"],
                    type=RecordType(row["type"]),
                    mood=Mood(row["mood"]) if row["mood"] else None,
                    context=json.loads(row["context"]) if row["context"] else None,
                    created_at=datetime.fromisoformat(row["created_at"]),
                ))
        return records

    def save_insight(self, insight: Insight) -> Insight:
        """Save an insight to database."""
        import json
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO insights (id, record_id, type, content, confidence, related_record_ids, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(insight.id),
                    str(insight.record_id),
                    insight.type.value,
                    insight.content,
                    insight.confidence,
                    json.dumps([str(x) for x in insight.related_record_ids]),
                    insight.created_at.isoformat(),
                )
            )
            conn.commit()
        logger.info(f"Insight saved: {insight.id}")
        return insight

    def save_reminder(self, reminder: Reminder) -> Reminder:
        """Save a reminder to database."""
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO reminders (id, condition, action, record_id, is_active, next_trigger, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(reminder.id),
                    reminder.condition,
                    reminder.action,
                    str(reminder.record_id) if reminder.record_id else None,
                    1 if reminder.is_active else 0,
                    reminder.next_trigger.isoformat() if reminder.next_trigger else None,
                    reminder.created_at.isoformat(),
                )
            )
            conn.commit()
        logger.info(f"Reminder saved: {reminder.id}")
        return reminder

    def get_active_reminders(self) -> list[Reminder]:
        """Get all active reminders."""
        reminders = []
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM reminders WHERE is_active = 1 ORDER BY created_at DESC"
            ).fetchall()
            for row in rows:
                reminders.append(Reminder(
                    id=row["id"],
                    condition=row["condition"],
                    action=row["action"],
                    record_id=row["record_id"] if row["record_id"] else None,
                    is_active=bool(row["is_active"]),
                    next_trigger=datetime.fromisoformat(row["next_trigger"]) if row["next_trigger"] else None,
                    created_at=datetime.fromisoformat(row["created_at"]),
                ))
        return reminders
```

- [ ] **Step 3: Create src/memory/vector_store.py**

```python
"""
ChromaDB vector storage for semantic search and long-term memory.
"""

from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings

from src.logger import get_logger

logger = get_logger(__name__)


class VectorStore:
    """ChromaDB vector store handler."""

    def __init__(self, persist_dir: Path):
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="echo_records",
            metadata={"description": "Echo personal reflection records"}
        )
        logger.info(f"Vector store initialized at {persist_dir}")

    def add_record(self, record_id: str, content: str, embedding: list[float], metadata: Optional[dict] = None):
        """Add a record to vector store."""
        self.collection.add(
            ids=[record_id],
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata or {}]
        )
        logger.debug(f"Record added to vector store: {record_id}")

    def search(self, query_embedding: list[float], n_results: int = 5, where: Optional[dict] = None) -> list[dict]:
        """Search for similar records."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        return [
            {
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "distance": results["distances"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else None,
            }
            for i in range(len(results["ids"][0]))
        ]

    def delete_record(self, record_id: str):
        """Delete a record from vector store."""
        self.collection.delete(ids=[record_id])
        logger.debug(f"Record deleted from vector store: {record_id}")
```

- [ ] **Step 4: Create tests/test_storage.py**

```python
"""Tests for storage layer."""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from src.memory.sqlite_store import SQLiteStore
from src.memory.vector_store import VectorStore
from src.models.schemas import Record, RecordType, Mood, Insight, InsightType, Reminder


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    yield db_path
    db_path.unlink(missing_ok=True)


@pytest.fixture
def sqlite_store(temp_db):
    """Create SQLiteStore instance."""
    return SQLiteStore(temp_db)


@pytest.fixture
def temp_vector_dir():
    """Create a temporary directory for vector store."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_save_and_get_record(sqlite_store):
    """Test saving and retrieving a record."""
    record = Record(
        content="Test record content",
        type=RecordType.TEXT,
        mood=Mood.NEUTRAL,
    )
    saved = sqlite_store.save_record(record)
    
    retrieved = sqlite_store.get_record(str(saved.id))
    assert retrieved is not None
    assert retrieved.content == "Test record content"
    assert retrieved.mood == Mood.NEUTRAL


def test_get_recent_records(sqlite_store):
    """Test getting recent records."""
    for i in range(5):
        record = Record(content=f"Record {i}", type=RecordType.TEXT)
        sqlite_store.save_record(record)
    
    recent = sqlite_store.get_recent_records(limit=3)
    assert len(recent) == 3


def test_save_insight(sqlite_store):
    """Test saving an insight."""
    record = Record(content="Test", type=RecordType.TEXT)
    sqlite_store.save_record(record)
    
    insight = Insight(
        record_id=record.id,
        type=InsightType.ASSOCIATION,
        content="Test insight",
        confidence=0.85,
    )
    saved = sqlite_store.save_insight(insight)
    
    assert saved.id is not None


def test_save_and_get_reminder(sqlite_store):
    """Test saving and getting reminders."""
    reminder = Reminder(
        condition="下次加班",
        action="提醒我休息",
    )
    saved = sqlite_store.save_reminder(reminder)
    
    active = sqlite_store.get_active_reminders()
    assert len(active) == 1
    assert active[0].condition == "下次加班"


def test_vector_store_add_and_search(temp_vector_dir):
    """Test vector store add and search."""
    store = VectorStore(temp_vector_dir)
    
    store.add_record(
        record_id="test-1",
        content="I am feeling stressed about work",
        embedding=[0.1] * 1536,
        metadata={"mood": "stressed"}
    )
    
    results = store.search(
        query_embedding=[0.1] * 1536,
        n_results=1
    )
    
    assert len(results) == 1
    assert results[0]["id"] == "test-1"
```

- [ ] **Step 5: Run tests**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -m pytest tests/test_storage.py -v
```

Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add src/memory/__init__.py src/memory/sqlite_store.py src/memory/vector_store.py tests/test_storage.py
git commit -m "feat: add storage layer with SQLite and ChromaDB"
```

---

## Task 4: LLM Client

**Files:**
- Create: `src/llm/__init__.py`
- Create: `src/llm/openai_client.py`
- Create: `tests/test_llm.py`

- [ ] **Step 1: Create src/llm/__init__.py**

```python
"""LLM interfaces for Echo."""
from src.llm.openai_client import OpenAIClient, openai_client

__all__ = ["OpenAIClient", "openai_client"]
```

- [ ] **Step 2: Create src/llm/openai_client.py**

```python
"""
OpenAI client wrapper for Echo.
Handles all LLM interactions including embedding and chat.
"""

from typing import Optional

from openai import OpenAI

from src.logger import get_logger
from src.config import config

logger = get_logger(__name__)


class OpenAIClient:
    """OpenAI client wrapper with embedding and chat support."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model
        if not self.api_key:
            logger.warning("OpenAI API key not set. LLM features will not work.")
        else:
            self.client = OpenAI(api_key=self.api_key)

    def get_embedding(self, text: str) -> list[float]:
        """Get embedding for a text using text-embedding-3-small."""
        if not self.api_key:
            return [0.0] * 1536

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def chat(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Generate chat completion."""
        if not self.api_key:
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."

        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content

    def generate_insight(self, current_record: str, related_records: list[dict]) -> str:
        """Generate an insight based on current record and related history."""
        if not related_records:
            return ""

        related_context = "\n".join([
            f"- [{r.get('created_at', 'unknown')}] {r.get('content', '')}"
            for r in related_records[:5]
        ])

        prompt = f"""Based on the user's current record and their past entries, generate a meaningful insight.

Current record:
{current_record}

Related past entries:
{related_context}

Generate a brief, warm insight (2-3 sentences) that connects the current moment with their history.
Focus on patterns, growth, or反差 (contrast with past).
Keep it conversational and supportive, in Chinese.

Insight:"""

        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, temperature=0.8)

    def generate_weekly_summary(self, records: list[dict]) -> str:
        """Generate a weekly summary from records."""
        if not records:
            return "本周还没有记录。"

        records_text = "\n".join([
            f"- [{r.get('created_at', '')}] {r.get('content', '')}"
            for r in records
        ])

        prompt = f"""Analyze the following weekly records and generate a concise summary.

Records:
{records_text}

Generate a weekly summary in Chinese that includes:
1. Overall mood/emotional trend
2. Key patterns noticed
3. One highlight or notable moment

Keep it warm, personal, and不超过200字."""

        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, temperature=0.7)


openai_client = OpenAIClient()
```

- [ ] **Step 3: Create tests/test_llm.py**

```python
"""Tests for LLM client."""

import pytest
from unittest.mock import patch, MagicMock

from src.llm.openai_client import OpenAIClient


def test_openai_client_init_without_key():
    """Test client initialization without API key."""
    client = OpenAIClient(api_key=None)
    assert client.api_key is None


def test_openai_client_init_with_key():
    """Test client initialization with API key."""
    with patch("src.llm.openai_client.OpenAI") as mock_openai:
        client = OpenAIClient(api_key="test-key")
        assert client.api_key == "test-key"


def test_get_embedding_without_key():
    """Test embedding generation without API key returns zero vector."""
    client = OpenAIClient(api_key=None)
    embedding = client.get_embedding("test text")
    assert len(embedding) == 1536
    assert all(e == 0.0 for e in embedding)


def test_chat_without_key():
    """Test chat without API key returns error message."""
    client = OpenAIClient(api_key=None)
    response = client.chat([{"role": "user", "content": "hello"}])
    assert "not configured" in response.lower()


@patch.object(OpenAIClient, "chat")
def test_generate_insight_with_no_related_records(mock_chat):
    """Test insight generation with no related records returns empty."""
    client = OpenAIClient(api_key="test")
    result = client.generate_insight("current record", [])
    assert result == ""


@patch.object(OpenAIClient, "chat")
def test_generate_insight_with_related_records(mock_chat):
    """Test insight generation with related records."""
    mock_chat.return_value = "这是一个洞察"

    client = OpenAIClient(api_key="test")
    related = [
        {"content": "past record 1", "created_at": "2024-01-01"},
        {"content": "past record 2", "created_at": "2024-01-02"},
    ]
    result = client.generate_insight("current record", related)

    assert result == "这是一个洞察"
    mock_chat.assert_called_once()


@patch.object(OpenAIClient, "chat")
def test_generate_weekly_summary(mock_chat):
    """Test weekly summary generation."""
    mock_chat.return_value = "本周总结"

    client = OpenAIClient(api_key="test")
    records = [
        {"content": "record 1", "created_at": "2024-01-01"},
        {"content": "record 2", "created_at": "2024-01-02"},
    ]
    result = client.generate_weekly_summary(records)

    assert result == "本周总结"
    mock_chat.assert_called_once()


def test_generate_weekly_summary_empty_records():
    """Test weekly summary with no records."""
    client = OpenAIClient(api_key="test")
    result = client.generate_weekly_summary([])
    assert "没有记录" in result
```

- [ ] **Step 4: Run tests**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -m pytest tests/test_llm.py -v
```

Expected: All tests pass

- [ ] **Step 5: Commit**

```bash
git add src/llm/__init__.py src/llm/openai_client.py tests/test_llm.py
git commit -m "feat: add OpenAI client wrapper"
```

---

## Task 5: Core Processing Engine

**Files:**
- Create: `src/core/__init__.py`
- Create: `src/core/processor.py`
- Create: `src/core/associator.py`
- Create: `src/core/patterns.py`
- Create: `tests/test_processor.py`

- [ ] **Step 1: Create src/core/__init__.py**

```python
"""Core processing engine for Echo."""
from src.core.processor import RecordProcessor
from src.core.associator import Associator
from src.core.patterns import PatternAnalyzer

__all__ = ["RecordProcessor", "Associator", "PatternAnalyzer"]
```

- [ ] **Step 2: Create src/core/processor.py**

```python
"""
Main record processor - orchestrates record processing pipeline.
"""

from datetime import datetime
from typing import Optional

from src.logger import get_logger
from src.models.schemas import Record, RecordCreate, Insight, InsightType
from src.memory.sqlite_store import SQLiteStore
from src.memory.vector_store import VectorStore
from src.llm.openai_client import OpenAIClient
from src.core.associator import Associator
from src.core.patterns import PatternAnalyzer

logger = get_logger(__name__)


class RecordProcessor:
    """Main processor for handling records and generating insights."""

    def __init__(
        self,
        sqlite_store: SQLiteStore,
        vector_store: VectorStore,
        llm_client: OpenAIClient,
    ):
        self.sqlite_store = sqlite_store
        self.vector_store = vector_store
        self.llm_client = llm_client
        self.associator = Associator(vector_store, llm_client)
        self.pattern_analyzer = PatternAnalyzer(sqlite_store, llm_client)

    def process_record(self, record_create: RecordCreate) -> tuple[Record, list[Insight]]:
        """
        Process a new record and generate insights.

        Returns:
            Tuple of (saved record, list of generated insights)
        """
        record = Record(
            content=record_create.content,
            type=record_create.type,
            mood=record_create.mood,
            context=record_create.context,
        )

        embedding = self.llm_client.get_embedding(record.content)
        record.embedding = embedding

        saved_record = self.sqlite_store.save_record(record)

        self.vector_store.add_record(
            record_id=str(saved_record.id),
            content=saved_record.content,
            embedding=embedding,
            metadata={
                "created_at": saved_record.created_at.isoformat(),
                "mood": saved_record.mood.value if saved_record.mood else None,
            }
        )

        insights = self._generate_insights(saved_record)

        for insight in insights:
            self.sqlite_store.save_insight(insight)

        logger.info(f"Processed record {saved_record.id} with {len(insights)} insights")
        return saved_record, insights

    def _generate_insights(self, record: Record) -> list[Insight]:
        """Generate insights for a record."""
        insights = []

        related = self.associator.find_related(record)
        if related:
            insight_content = self.llm_client.generate_insight(
                record.content,
                [{"content": r.content, "created_at": r.created_at.isoformat()} for r in related]
            )
            if insight_content:
                insight = Insight(
                    record_id=record.id,
                    type=InsightType.ASSOCIATION,
                    content=insight_content,
                    confidence=0.8,
                    related_record_ids=[r.id for r in related],
                )
                insights.append(insight)

        return insights

    def generate_weekly_report(self, period: Optional[str] = None) -> dict:
        """Generate weekly report."""
        recent_records = self.sqlite_store.get_recent_records(limit=100)

        records_data = [
            {
                "content": r.content,
                "created_at": r.created_at.isoformat(),
                "mood": r.mood.value if r.mood else None,
            }
            for r in recent_records
        ]

        summary = self.llm_client.generate_weekly_summary(records_data)
        patterns = self.pattern_analyzer.analyze_patterns(recent_records)

        mood_dist = {}
        for r in recent_records:
            mood = r.mood.value if r.mood else "neutral"
            mood_dist[mood] = mood_dist.get(mood, 0) + 1

        return {
            "period": period or datetime.utcnow().strftime("%Y-W%W"),
            "total_records": len(recent_records),
            "mood_distribution": mood_dist,
            "patterns": patterns,
            "highlight": summary,
        }
```

- [ ] **Step 3: Create src/core/associator.py**

```python
"""
Implicit association engine - finds semantic and temporal connections.
"""

from typing import Optional

from src.logger import get_logger
from src.models.schemas import Record
from src.memory.vector_store import VectorStore
from src.llm.openai_client import OpenAIClient

logger = get_logger(__name__)


class Associator:
    """Finds implicit associations between records."""

    def __init__(self, vector_store: VectorStore, llm_client: OpenAIClient):
        self.vector_store = vector_store
        self.llm_client = llm_client

    def find_related(self, record: Record, limit: int = 5) -> list[Record]:
        """
        Find records related to the given record.

        Uses vector similarity search to find semantically similar records.
        """
        if not record.embedding:
            return []

        try:
            results = self.vector_store.search(
                query_embedding=record.embedding,
                n_results=limit + 1,
                where=None
            )

            related_ids = [r["id"] for r in results if r["id"] != str(record.id)]
            related_records = []

            for rid in related_ids[:limit]:
                rec = self._get_record_by_id(rid)
                if rec:
                    related_records.append(rec)

            return related_records
        except Exception as e:
            logger.error(f"Error finding related records: {e}")
            return []

    def _get_record_by_id(self, record_id: str) -> Optional[Record]:
        """Get record by ID from SQLite store."""
        from src.memory.sqlite_store import SQLiteStore
        from src.config import config

        try:
            store = SQLiteStore(config.DB_PATH)
            return store.get_record(record_id)
        except Exception:
            return None
```

- [ ] **Step 4: Create src/core/patterns.py**

```python
"""
Pattern recognition engine - discovers temporal and behavioral patterns.
"""

from collections import defaultdict
from datetime import datetime, timedelta

from src.logger import get_logger
from src.models.schemas import Record, Mood, PatternInfo
from src.memory.sqlite_store import SQLiteStore
from src.llm.openai_client import OpenAIClient

logger = get_logger(__name__)


class PatternAnalyzer:
    """Analyzes records to discover patterns."""

    def __init__(self, sqlite_store: SQLiteStore, llm_client: OpenAIClient):
        self.sqlite_store = sqlite_store
        self.llm_client = llm_client

    def analyze_patterns(self, records: list[Record]) -> list[PatternInfo]:
        """Analyze records for patterns."""
        patterns = []

        mood_pattern = self._analyze_mood_pattern(records)
        if mood_pattern:
            patterns.append(mood_pattern)

        time_pattern = self._analyze_time_pattern(records)
        if time_pattern:
            patterns.append(time_pattern)

        keyword_pattern = self._analyze_keyword_pattern(records)
        if keyword_pattern:
            patterns.append(keyword_pattern)

        return patterns

    def _analyze_mood_pattern(self, records: list[Record]) -> Optional[PatternInfo]:
        """Analyze mood-related patterns."""
        mood_keywords = {
            Mood.HAPPY: ["开心", "高兴", "兴奋", "成就感", "顺利"],
            Mood.LOW: ["沮丧", "疲惫", "低落", "累", "压力"],
            Mood.ANGRY: ["生气", "愤怒", "烦躁", "恼火"],
        }

        mood_counts = defaultdict(int)
        for record in records:
            for mood, keywords in mood_keywords.items():
                if any(kw in record.content for kw in keywords):
                    mood_counts[mood] += 1

        if mood_counts:
            dominant = max(mood_counts, key=mood_counts.get)
            return PatternInfo(
                name="情绪主导模式",
                description=f"你近期最常见的情绪是{dominant.value}",
                frequency=mood_counts[dominant],
                confidence=0.7
            )
        return None

    def _analyze_time_pattern(self, records: list[Record]) -> Optional[PatternInfo]:
        """Analyze time-based patterns."""
        weekday_counts = defaultdict(int)
        for record in records:
            weekday = record.created_at.weekday()
            weekday_counts[weekday] += 1

        if weekday_counts:
            most_common_day = max(weekday_counts, key=weekday_counts.get)
            day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            return PatternInfo(
                name="记录时间模式",
                description=f"你更喜欢在{day_names[most_common_day]}记录",
                frequency=weekday_counts[most_common_day],
                confidence=0.6
            )
        return None

    def _analyze_keyword_pattern(self, records: list[Record]) -> Optional[PatternInfo]:
        """Analyze keyword/topic frequency patterns."""
        keywords = ["工作", "加班", "家人", "朋友", "健康", "睡眠", "运动"]
        keyword_counts = defaultdict(int)

        for record in records:
            content_lower = record.content.lower()
            for kw in keywords:
                if kw in content_lower:
                    keyword_counts[kw] += 1

        if keyword_counts:
            top_keyword = max(keyword_counts, key=keyword_counts.get)
            return PatternInfo(
                name="话题偏好",
                description=f"你最近谈论最多的是'{top_keyword}'",
                frequency=keyword_counts[top_keyword],
                confidence=0.65
            )
        return None
```

- [ ] **Step 5: Create tests/test_processor.py**

```python
"""Tests for core processing engine."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.core.processor import RecordProcessor
from src.core.associator import Associator
from src.core.patterns import PatternAnalyzer
from src.models.schemas import Record, RecordCreate, RecordType, Mood


@pytest.fixture
def mock_sqlite_store():
    """Create a mock SQLite store."""
    store = MagicMock()
    store.save_record.return_value = Record(
        id="test-id",
        content="Test content",
        type=RecordType.TEXT,
        created_at=datetime.utcnow()
    )
    store.get_recent_records.return_value = []
    store.save_insight.return_value = None
    return store


@pytest.fixture
def mock_vector_store():
    """Create a mock vector store."""
    store = MagicMock()
    store.add_record.return_value = None
    store.search.return_value = []
    return store


@pytest.fixture
def mock_llm_client():
    """Create a mock LLM client."""
    client = MagicMock()
    client.get_embedding.return_value = [0.1] * 1536
    client.generate_insight.return_value = "Test insight"
    client.generate_weekly_summary.return_value = "Weekly summary"
    return client


def test_record_processor_init(mock_sqlite_store, mock_vector_store, mock_llm_client):
    """Test RecordProcessor initialization."""
    processor = RecordProcessor(
        sqlite_store=mock_sqlite_store,
        vector_store=mock_vector_store,
        llm_client=mock_llm_client
    )
    assert processor.sqlite_store == mock_sqlite_store
    assert processor.vector_store == mock_vector_store


def test_record_processor_process_record(mock_sqlite_store, mock_vector_store, mock_llm_client):
    """Test processing a new record."""
    processor = RecordProcessor(
        sqlite_store=mock_sqlite_store,
        vector_store=mock_vector_store,
        llm_client=mock_llm_client
    )

    record_create = RecordCreate(
        content="今天工作很累",
        type=RecordType.TEXT,
        mood=Mood.LOW
    )

    record, insights = processor.process_record(record_create)

    assert record.content == "今天工作累了"
    mock_sqlite_store.save_record.assert_called_once()
    mock_vector_store.add_record.assert_called_once()


def test_record_processor_generate_weekly_report(mock_sqlite_store, mock_vector_store, mock_llm_client):
    """Test generating weekly report."""
    processor = RecordProcessor(
        sqlite_store=mock_sqlite_store,
        vector_store=mock_vector_store,
        llm_client=mock_llm_client
    )

    report = processor.generate_weekly_report()

    assert "period" in report
    assert "total_records" in report
    assert "mood_distribution" in report


def test_associator_find_related_no_embedding():
    """Test associator with no embedding returns empty."""
    with patch("src.core.associator.VectorStore"):
        with patch("src.core.associator.OpenAIClient"):
            associator = Associator(MagicMock(), MagicMock())
            record = Record(content="test", type=RecordType.TEXT)
            record.embedding = None

            result = associator.find_related(record)
            assert result == []


def test_pattern_analyzer_analyze_patterns():
    """Test pattern analyzer with mock data."""
    mock_store = MagicMock()
    mock_client = MagicMock()

    analyzer = PatternAnalyzer(mock_store, mock_client)

    records = [
        Record(content="今天很开心", type=RecordType.TEXT, mood=Mood.HAPPY, created_at=datetime.utcnow()),
        Record(content="工作很累", type=RecordType.TEXT, mood=Mood.LOW, created_at=datetime.utcnow()),
    ]

    patterns = analyzer.analyze_patterns(records)
    assert isinstance(patterns, list)
```

- [ ] **Step 6: Run tests**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -m pytest tests/test_processor.py -v
```

Expected: All tests pass

- [ ] **Step 7: Commit**

```bash
git add src/core/__init__.py src/core/processor.py src/core/associator.py src/core/patterns.py tests/test_processor.py
git commit -m "feat: add core processing engine with associator and pattern analyzer"
```

---

## Task 6: API Endpoints

**Files:**
- Create: `src/api/__init__.py`
- Create: `src/api/records.py`
- Create: `src/api/insights.py`
- Create: `tests/test_api.py`

- [ ] **Step 1: Create src/api/__init__.py**

```python
"""API routes for Echo."""
from src.api.records import router as records_router
from src.api.insights import router as insights_router

__all__ = ["records_router", "insights_router"]
```

- [ ] **Step 2: Create src/api/records.py**

```python
"""
Records API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.logger import get_logger
from src.models.schemas import RecordCreate, RecordResponse, Insight
from src.memory.sqlite_store import SQLiteStore
from src.memory.vector_store import VectorStore
from src.llm.openai_client import OpenAIClient
from src.core.processor import RecordProcessor
from src.config import config

logger = get_logger(__name__)
router = APIRouter(prefix="/api/records", tags=["records"])

_processor: Optional[RecordProcessor] = None


def get_processor() -> RecordProcessor:
    """Get or create RecordProcessor singleton."""
    global _processor
    if _processor is None:
        config.ensure_dirs()
        sqlite_store = SQLiteStore(config.DB_PATH)
        vector_store = VectorStore(config.VECTOR_DIR)
        llm_client = OpenAIClient()
        _processor = RecordProcessor(sqlite_store, vector_store, llm_client)
    return _processor


class RecordCreateRequest(BaseModel):
    content: str
    type: str = "text"
    mood: Optional[str] = None
    context: Optional[dict] = None


class RecordResponseData(BaseModel):
    id: str
    content: str
    type: str
    mood: Optional[str] = None
    created_at: str
    insights: list[dict] = []


@router.post("", response_model=RecordResponseData)
async def create_record(
    request: RecordCreateRequest,
    processor: RecordProcessor = Depends(get_processor)
):
    """
    Create a new record and generate insights.

    This is the main endpoint for adding new voice/text records.
    The AI will automatically find related past records and generate insights.
    """
    from src.models.schemas import RecordCreate as ModelRecordCreate, RecordType, Mood

    try:
        record_create = ModelRecordCreate(
            content=request.content,
            type=RecordType(request.type),
            mood=Mood(request.mood) if request.mood else None,
            context=request.context,
        )

        record, insights = processor.process_record(record_create)

        return RecordResponseData(
            id=str(record.id),
            content=record.content,
            type=record.type.value,
            mood=record.mood.value if record.mood else None,
            created_at=record.created_at.isoformat(),
            insights=[
                {
                    "id": str(i.id),
                    "type": i.type.value,
                    "content": i.content,
                    "confidence": i.confidence,
                }
                for i in insights
            ]
        )
    except Exception as e:
        logger.error(f"Error creating record: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[RecordResponseData])
async def get_records(
    limit: int = 20,
    offset: int = 0,
    search: Optional[str] = None,
    processor: RecordProcessor = Depends(get_processor)
):
    """
    Get recent records with optional search.

    - **limit**: Maximum number of records to return (default 20)
    - **offset**: Number of records to skip (for pagination)
    - **search**: Optional text search in record content
    """
    try:
        store = processor.sqlite_store
        records = store.get_recent_records(limit=limit + offset)

        if search:
            records = [r for r in records if search.lower() in r.content.lower()]

        records = records[offset:offset + limit]

        return [
            RecordResponseData(
                id=str(r.id),
                content=r.content,
                type=r.type.value,
                mood=r.mood.value if r.mood else None,
                created_at=r.created_at.isoformat(),
                insights=[]
            )
            for r in records
        ]
    except Exception as e:
        logger.error(f"Error getting records: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{record_id}", response_model=RecordResponseData)
async def get_record(
    record_id: str,
    processor: RecordProcessor = Depends(get_processor)
):
    """Get a specific record by ID."""
    try:
        record = processor.sqlite_store.get_record(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        return RecordResponseData(
            id=str(record.id),
            content=record.content,
            type=record.type.value,
            mood=record.mood.value if record.mood else None,
            created_at=record.created_at.isoformat(),
            insights=[]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting record: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 3: Create src/api/insights.py**

```python
"""
Insights API endpoints.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.logger import get_logger
from src.models.schemas import WeeklyReport, PatternInfo, Insight, InsightType
from src.memory.sqlite_store import SQLiteStore
from src.memory.vector_store import VectorStore
from src.llm.openai_client import OpenAIClient
from src.core.processor import RecordProcessor
from src.config import config

logger = get_logger(__name__)
router = APIRouter(prefix="/api/insights", tags=["insights"])

_processor: Optional[RecordProcessor] = None


def get_processor() -> RecordProcessor:
    """Get or create RecordProcessor singleton."""
    global _processor
    if _processor is None:
        config.ensure_dirs()
        sqlite_store = SQLiteStore(config.DB_PATH)
        vector_store = VectorStore(config.VECTOR_DIR)
        llm_client = OpenAIClient()
        _processor = RecordProcessor(sqlite_store, vector_store, llm_client)
    return _processor


@router.get("/weekly", response_model=WeeklyReport)
async def get_weekly_report(
    period: Optional[str] = None,
    processor: RecordProcessor = Depends(get_processor)
):
    """
    Get weekly insight report.

    Includes mood distribution, detected patterns, and a highlight summary.
    """
    try:
        report_data = processor.generate_weekly_report(period)

        return WeeklyReport(
            period=report_data["period"],
            total_records=report_data["total_records"],
            mood_distribution=report_data["mood_distribution"],
            patterns=[PatternInfo(**p) for p in report_data["patterns"]],
            highlight=report_data["highlight"]
        )
    except Exception as e:
        logger.error(f"Error generating weekly report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reminders")
async def get_reminders(
    processor: RecordProcessor = Depends(get_processor)
):
    """Get all active future reminders."""
    try:
        reminders = processor.sqlite_store.get_active_reminders()
        return [
            {
                "id": str(r.id),
                "condition": r.condition,
                "action": r.action,
                "record_id": str(r.record_id) if r.record_id else None,
                "is_active": r.is_active,
                "created_at": r.created_at.isoformat(),
            }
            for r in reminders
        ]
    except Exception as e:
        logger.error(f"Error getting reminders: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 4: Create tests/test_api.py**

```python
"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_processor():
    """Create a mock RecordProcessor."""
    with patch("src.api.records.get_processor") as mock:
        processor = MagicMock()
        mock.return_value = processor
        yield processor


def test_create_record_endpoint(client, mock_processor):
    """Test POST /api/records endpoint."""
    from src.models.schemas import Record, Insight

    mock_processor.process_record.return_value = (
        Record(
            id="test-id",
            content="Test record",
            type="text",
            created_at=datetime.utcnow()
        ),
        []
    )

    response = client.post(
        "/api/records",
        json={"content": "Test record", "type": "text"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test record"
    assert "id" in data


def test_get_records_endpoint(client, mock_processor):
    """Test GET /api/records endpoint."""
    from src.models.schemas import Record, RecordType

    mock_processor.sqlite_store.get_recent_records.return_value = [
        Record(id="1", content="Record 1", type=RecordType.TEXT, created_at=datetime.utcnow()),
        Record(id="2", content="Record 2", type=RecordType.TEXT, created_at=datetime.utcnow()),
    ]

    response = client.get("/api/records")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_weekly_report_endpoint(client, mock_processor):
    """Test GET /api/insights/weekly endpoint."""
    mock_processor.generate_weekly_report.return_value = {
        "period": "2024-W15",
        "total_records": 10,
        "mood_distribution": {"happy": 5, "low": 5},
        "patterns": [
            {"name": "情绪模式", "description": "你近期情绪波动", "frequency": 3, "confidence": 0.8}
        ],
        "highlight": "这是本周的亮点"
    }

    response = client.get("/api/insights/weekly")

    assert response.status_code == 200
    data = response.json()
    assert data["period"] == "2024-W15"
    assert "patterns" in data


def test_get_reminders_endpoint(client, mock_processor):
    """Test GET /api/insights/reminders endpoint."""
    from src.models.schemas import Reminder

    mock_processor.sqlite_store.get_active_reminders.return_value = [
        Reminder(
            condition="下次加班",
            action="提醒休息",
            created_at=datetime.utcnow()
        )
    ]

    response = client.get("/api/insights/reminders")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["condition"] == "下次加班"
```

- [ ] **Step 5: Run tests**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -m pytest tests/test_api.py -v
```

Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add src/api/__init__.py src/api/records.py src/api/insights.py tests/test_api.py
git commit -m "feat: add REST API endpoints for records and insights"
```

---

## Task 7: Main Application Entry Point

**Files:**
- Create: `src/main.py`
- Create: `tests/test_main.py`

- [ ] **Step 1: Create src/main.py**

```python
"""
Echo - Personal Reflection and Decision AI Assistant
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.logger import get_logger
from src.config import config
from src.api import records_router, insights_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    config.ensure_dirs()
    logger.info("Echo starting up...")
    yield
    logger.info("Echo shutting down...")


app = FastAPI(
    title="Echo",
    description="Personal Reflection and Decision AI Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records_router)
app.include_router(insights_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Echo",
        "version": "0.1.0",
        "description": "Personal Reflection and Decision AI Assistant"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
```

- [ ] **Step 2: Create tests/test_main.py**

```python
"""Tests for main application."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test GET / endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Echo"
    assert "version" in data


def test_health_check(client):
    """Test GET /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

- [ ] **Step 3: Run tests**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -m pytest tests/test_main.py -v
```

Expected: All tests pass

- [ ] **Step 4: Commit**

```bash
git add src/main.py tests/test_main.py
git commit -m "feat: add FastAPI main application entry point"
```

---

## Task 8: Run All Tests and Verify

- [ ] **Step 1: Install dependencies**

```bash
cd /home/hehe/codespace/agent/echo-agent && uv venv && uv add fastapi uvicorn pydantic openai chromadb sqlite-utils apscheduler python-multipart httpx pytest pytest-asyncio
```

- [ ] **Step 2: Run all tests**

```bash
cd /home/hehe/codespace/agent/echo-agent && python -m pytest tests/ -v
```

Expected: All tests pass

- [ ] **Step 3: Start server and test health**

```bash
cd /home/hehe/codespace/agent/echo-agent && timeout 5 python -c "from src.main import app; from fastapi.testclient import TestClient; client = TestClient(app); print(client.get('/health').json())"
```

Expected: {"status": "healthy"}

---

## Task 9: Documentation

- [ ] **Step 1: Create README.md**

```markdown
# Echo - Personal Reflection and Decision AI

Echo is an AI assistant that captures your daily碎片化 thoughts, emotions, and decisions through low-friction voice/text input, then provides insights, pattern recognition, and decision support across months and years.

## Features

- **Low-friction input**: Voice or text recording with minimal friction
- **Implicit association**: AI automatically finds connections between current and past records
- **Pattern recognition**: Discover emotional and behavioral patterns you weren't aware of
- **Decision support**: Get objective snapshots from your history when facing decisions
- **Proactive reminders**: AI proactively reminds you based on your past entries

## Quick Start

### Backend

```bash
# Install dependencies
uv venv
uv add fastapi uvicorn pydantic openai chromadb sqlite-utils apscheduler python-multipart httpx pytest pytest-asyncio

# Set API key
export OPENAI_API_KEY="your-api-key"

# Run server
python -m src.main
```

### API Endpoints

- `POST /api/records` - Create a new record
- `GET /api/records` - Get recent records
- `GET /api/insights/weekly` - Get weekly insight report
- `GET /api/insights/reminders` - Get active reminders

### Frontend (Coming Soon)

A mobile app is planned for easier voice input and push notifications.

## Architecture

```
src/
├── api/           # REST API endpoints
├── core/          # Core processing engine
├── memory/        # SQLite + ChromaDB storage
├── llm/           # OpenAI client wrapper
└── models/        # Pydantic data models
```

## License

MIT
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with quick start guide"
```

---

## Plan Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Project Foundation | logger.py, config.py, requirements.txt |
| 2 | Data Models | schemas.py |
| 3 | Storage Layer | sqlite_store.py, vector_store.py |
| 4 | LLM Client | openai_client.py |
| 5 | Core Processing | processor.py, associator.py, patterns.py |
| 6 | API Endpoints | records.py, insights.py |
| 7 | Main App | main.py |
| 8 | Test All | - |
| 9 | Documentation | README.md |

---

## Execution Options

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**