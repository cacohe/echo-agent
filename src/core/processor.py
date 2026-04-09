"""Record processing engine."""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from src.core.patterns import PatternAnalyzer
from src.logger import get_logger
from src.models.schemas import Insight, InsightType, Record, RecordCreate

if TYPE_CHECKING:
    from src.llm.openai_client import OpenAIClient
    from src.memory.sqlite_store import SQLiteStore
    from src.memory.vector_store import VectorStore

logger = get_logger(__name__)


class RecordProcessor:
    """Processes records and generates insights."""

    def __init__(
        self,
        sqlite_store: "SQLiteStore",
        vector_store: "VectorStore",
        llm_client: "OpenAIClient",
    ) -> None:
        self.sqlite_store = sqlite_store
        self.vector_store = vector_store
        self.llm_client = llm_client
        self.pattern_analyzer = PatternAnalyzer(sqlite_store, llm_client)

    def process_record(
        self, record_create: RecordCreate
    ) -> tuple[Record, list[Insight]]:
        """Process a new record and generate insights."""
        embedding = self.llm_client.get_embedding(record_create.content)

        record = Record(
            content=record_create.content,
            type=record_create.type,
            mood=record_create.mood,
            context=record_create.context,
            embedding=embedding,
        )

        self.sqlite_store.save_record(record)

        self.vector_store.add_record(
            record_id=str(record.id),
            content=record.content,
            embedding=embedding,
            metadata={
                "type": record.type.value,
                "mood": record.mood.value if record.mood else None,
                "created_at": record.created_at.isoformat(),
            },
        )

        insights = self._generate_insights(record)

        for insight in insights:
            self.sqlite_store.save_insight(insight)

        return record, insights

    def _generate_insights(self, record: Record) -> list[Insight]:
        """Generate insights for a record based on related records."""
        insights = []

        if record.embedding:
            related = self.vector_store.search(
                query_embedding=record.embedding,
                n_results=5,
            )

            if related:
                related_records = [
                    {
                        "id": r["id"],
                        "content": r["content"],
                        "created_at": r["metadata"].get("created_at")
                        if r["metadata"]
                        else None,
                    }
                    for r in related
                    if r["id"] != str(record.id)
                ]

                if related_records:
                    insight_content = self.llm_client.generate_insight(
                        record.content, related_records
                    )

                    if insight_content:
                        insight = Insight(
                            record_id=record.id,
                            type=InsightType.ASSOCIATION,
                            content=insight_content,
                            confidence=0.8,
                            related_record_ids=[r["id"] for r in related_records[:3]],
                        )
                        insights.append(insight)

        return insights

    def generate_weekly_report(self, period: str) -> dict:
        """Generate a weekly report for the specified period."""
        try:
            week_start = datetime.strptime(period + "-1", "%Y-%W-%w")
            week_end = week_start + timedelta(days=6)
        except ValueError:
            week_start = datetime.utcnow() - timedelta(days=7)
            week_end = datetime.utcnow()

        records = self.sqlite_store.get_recent_records(limit=100)

        period_records = [r for r in records if week_start <= r.created_at <= week_end]

        if not period_records:
            return {
                "period": period,
                "total_records": 0,
                "mood_distribution": {},
                "patterns": [],
                "highlight": "本周还没有记录。",
            }

        mood_counts: dict[str, int] = {}
        for r in period_records:
            mood_key = r.mood.value if r.mood else "neutral"
            mood_counts[mood_key] = mood_counts.get(mood_key, 0) + 1

        records_data = [
            {
                "content": r.content,
                "mood": r.mood.value if r.mood else None,
                "created_at": r.created_at.isoformat(),
            }
            for r in period_records
        ]

        highlight = self.llm_client.generate_weekly_summary(records_data)

        patterns = self.pattern_analyzer.analyze_patterns(period_records)
        patterns_data = [
            {
                "name": p.name,
                "description": p.description,
                "frequency": p.frequency,
                "confidence": p.confidence,
            }
            for p in patterns
        ]

        return {
            "period": period,
            "total_records": len(period_records),
            "mood_distribution": mood_counts,
            "patterns": patterns_data,
            "highlight": highlight,
        }
