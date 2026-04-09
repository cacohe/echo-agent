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
