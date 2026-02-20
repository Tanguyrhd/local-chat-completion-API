"""
Integration tests — require a running Ollama instance.

Run with: pytest -m integration
These tests are excluded from the default test run.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.integration
def test_responses_endpoint_real_ollama():
    response = client.post("/v1/responses", json={"input": "Say exactly: OK"})
    assert response.status_code == 200
    data = response.json()
    assert data["output"]["content"] != ""


@pytest.mark.integration
def test_responses_with_instructions_real_ollama():
    response = client.post(
        "/v1/responses",
        json={
            "instructions": "Always reply with exactly one word.",
            "input": "Are you ready?",
        },
    )
    assert response.status_code == 200
    assert response.json()["output"]["content"] != ""


@pytest.mark.integration
def test_chat_completions_real_ollama():
    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Say exactly: OK"}]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    assert len(data["choices"]) == 1
    assert data["choices"][0]["message"]["content"] != ""
