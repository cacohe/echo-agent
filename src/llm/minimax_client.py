"""
MiniMax API client wrapper for Echo.
Handles LLM interactions with MiniMax API.
"""

from typing import Optional

import httpx

from src.logger import get_logger
from src.config import config

logger = get_logger(__name__)


class MiniMaxClient:
    """MiniMax API client with chat completion support."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "M2-her",
        base_url: str = "https://api.minimaxi.com",
    ):
        self.api_key = api_key or config.MINIMAX_API_KEY
        self.model = model
        self.base_url = base_url
        if not self.api_key:
            logger.warning("MiniMax API key not set. LLM features will not work.")
        else:
            self.client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )

    def chat(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Generate chat completion using MiniMax API."""
        if not self.api_key:
            return "MiniMax API key not configured. Please set MINIMAX_API_KEY environment variable."

        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        try:
            response = self.client.post("/v1/text/chatcompletion_v2", json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("base_resp", {}).get("status_code") != 0:
                error_msg = data.get("base_resp", {}).get("status_msg", "Unknown error")
                logger.error(f"MiniMax API error: {error_msg}")
                return f"MiniMax API error: {error_msg}"

            choices = data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return ""
        except httpx.HTTPError as e:
            logger.error(f"MiniMax HTTP error: {e}")
            return f"MiniMax API error: {str(e)}"
        except Exception as e:
            logger.error(f"MiniMax unexpected error: {e}")
            return f"MiniMax API error: {str(e)}"

    def generate_insight(self, current_record: str, related_records: list[dict]) -> str:
        """Generate an insight based on current record and related history."""
        if not related_records:
            return ""

        if not self.api_key:
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


minimax_client = MiniMaxClient()
