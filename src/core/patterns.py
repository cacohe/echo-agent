"""Pattern analysis engine."""

from collections import Counter
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from src.logger import get_logger
from src.models.schemas import Mood, PatternInfo, Record

if TYPE_CHECKING:
    from src.llm.openai_client import OpenAIClient
    from src.memory.sqlite_store import SQLiteStore

logger = get_logger(__name__)


class PatternAnalyzer:
    """Analyzes patterns in records."""

    def __init__(
        self,
        sqlite_store: "SQLiteStore",
        llm_client: "OpenAIClient",
    ) -> None:
        self.sqlite_store = sqlite_store
        self.llm_client = llm_client

    def analyze_patterns(self, records: list[Record]) -> list[PatternInfo]:
        """Analyze patterns across a list of records."""
        if len(records) < 3:
            return []

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
        """Analyze mood patterns in records."""
        moods = [r.mood for r in records if r.mood]

        if not moods:
            return None

        mood_counts = Counter(moods)
        most_common = mood_counts.most_common(1)[0]

        if most_common[1] >= 2 and most_common[1] / len(moods) > 0.5:
            return PatternInfo(
                name="mood_trend",
                description=f"最近倾向于{most_common[0].value}的情绪",
                frequency=most_common[1],
                confidence=0.7,
            )

        return None

    def _analyze_time_pattern(self, records: list[Record]) -> Optional[PatternInfo]:
        """Analyze temporal patterns in records."""
        if not records:
            return None

        hours = [r.created_at.hour for r in records]

        hour_counts = Counter(hours)
        most_common_hour, count = hour_counts.most_common(1)[0]

        if count >= 2 and count / len(records) > 0.4:
            time_label = (
                "凌晨"
                if 0 <= most_common_hour < 6
                else "上午"
                if 6 <= most_common_hour < 12
                else "下午"
                if 12 <= most_common_hour < 18
                else "晚上"
            )

            return PatternInfo(
                name="time_pattern",
                description=f"你倾向于在{time_label}记录",
                frequency=count,
                confidence=0.6,
            )

        return None

    def _analyze_keyword_pattern(self, records: list[Record]) -> Optional[PatternInfo]:
        """Analyze keyword/frequency patterns in records."""
        all_content = " ".join(r.content for r in records)

        common_words = ["工作", "生活", "朋友", "家", "学习", "休息", "开心", "烦恼"]
        found_keywords = [word for word in common_words if word in all_content]

        if found_keywords:
            keyword_counts = {word: all_content.count(word) for word in found_keywords}
            most_common_keyword = max(keyword_counts, key=keyword_counts.get)

            return PatternInfo(
                name="keyword_theme",
                description=f'最近的主题与"{most_common_keyword}"相关',
                frequency=keyword_counts[most_common_keyword],
                confidence=0.5,
            )

        return None
