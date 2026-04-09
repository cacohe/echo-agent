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
            model="text-embedding-3-small", input=text
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

        related_context = "\n".join(
            [
                f"- [{r.get('created_at', 'unknown')}] {r.get('content', '')}"
                for r in related_records[:5]
            ]
        )

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

        records_text = "\n".join(
            [f"- [{r.get('created_at', '')}] {r.get('content', '')}" for r in records]
        )

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
