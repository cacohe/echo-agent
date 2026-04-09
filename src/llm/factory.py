"""
LLM client factory - returns the appropriate client based on config.
"""

from src.config import config
from src.llm.openai_client import OpenAIClient
from src.llm.minimax_client import MiniMaxClient


def get_llm_client():
    """
    Get LLM client based on LLM_PROVIDER config.

    Returns OpenAIClient if LLM_PROVIDER is "openai" or not set.
    Returns MiniMaxClient if LLM_PROVIDER is "minimax".
    """
    if config.LLM_PROVIDER == "minimax":
        return MiniMaxClient(
            api_key=config.MINIMAX_API_KEY,
            model=config.MINIMAX_MODEL,
            base_url=config.MINIMAX_BASE_URL,
        )
    else:
        return OpenAIClient(
            api_key=config.OPENAI_API_KEY,
            model=config.OPENAI_MODEL,
        )
