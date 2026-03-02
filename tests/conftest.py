"""
Shared pytest fixtures for the test suite.

Provides:
- client: TestClient with LLMEngine mocked via dependency_overrides
- client_with_auth: TestClient with API_KEY set to "test-key"
"""

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from main import app
from core.config import settings
from services.llm_engine import LLMEngine
from schemas.responses import Response, ResponseOutput

MOCK_CONTENT = "This is a mocked LLM response."


def make_fake_engine():
    """Build a fake LLMEngine that never calls Ollama."""
    fake = MagicMock(spec=LLMEngine)

    def fake_generate(model, **_):
        return Response(
            model=model or settings.DEFAULT_MODEL,
            output=ResponseOutput(content=MOCK_CONTENT),
        )

    fake.generate_response.side_effect = fake_generate
    return fake


@pytest.fixture
def client():
    """TestClient with LLMEngine mocked via dependency_overrides."""
    app.dependency_overrides[LLMEngine] = make_fake_engine
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_auth(monkeypatch):
    """TestClient with API_KEY enforced. Returns (client, api_key) tuple."""
    monkeypatch.setattr(settings, "API_KEY", "test-key")
    app.dependency_overrides[LLMEngine] = make_fake_engine
    yield TestClient(app), "test-key"
    app.dependency_overrides.clear()
