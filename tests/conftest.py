"""
Shared pytest fixtures for the test suite.

Provides:
- client: TestClient with Ollama mocked (no Ollama required)
- client_with_auth: TestClient with API_KEY set to "test-key"
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from main import app
from core.config.settings import settings

MOCK_RESPONSE = "This is a mocked LLM response."


@pytest.fixture
def client():
    """TestClient with Ollama mocked — no running Ollama instance required."""
    with patch("services.llm_engine.generate_with_ollama", return_value=MOCK_RESPONSE):
        yield TestClient(app)


@pytest.fixture
def client_with_auth(monkeypatch):
    """TestClient with API_KEY enforced. Returns (client, api_key) tuple."""
    monkeypatch.setattr(settings, "API_KEY", "test-key")
    with patch("services.llm_engine.generate_with_ollama", return_value=MOCK_RESPONSE):
        yield TestClient(app), "test-key"
