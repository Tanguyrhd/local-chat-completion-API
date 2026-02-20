"""
API tests for the POST /v1/chat/completions endpoint.

Ollama is mocked — no running Ollama instance required.
"""

from core.config.settings import settings


def test_basic_chat(client):
    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Hello"}]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    assert len(data["choices"]) == 1
    assert data["choices"][0]["message"]["role"] == "assistant"


def test_with_system_message(client):
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [
                {"role": "system", "content": "You are helpful."},
                {"role": "user", "content": "Hi"},
            ]
        },
    )
    assert response.status_code == 200


def test_multi_turn_conversation(client):
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [
                {"role": "user", "content": "My name is Alice."},
                {"role": "assistant", "content": "Nice to meet you!"},
                {"role": "user", "content": "What is my name?"},
            ]
        },
    )
    assert response.status_code == 200


def test_n_returns_multiple_choices(client):
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "n": 3,
        },
    )
    assert response.status_code == 200
    assert len(response.json()["choices"]) == 3


def test_missing_messages_returns_422(client):
    response = client.post("/v1/chat/completions", json={})
    assert response.status_code == 422


def test_default_model_used_when_not_specified(client):
    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Hello"}]},
    )
    assert response.status_code == 200
    assert response.json()["model"] == settings.DEFAULT_MODEL
