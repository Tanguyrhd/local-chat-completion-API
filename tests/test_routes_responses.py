"""
API tests for the POST /v1/responses endpoint.

Ollama is mocked — no running Ollama instance required.
"""


def test_basic_response(client):
    response = client.post("/v1/responses", json={"input": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert "model" in data
    assert "output" in data
    assert "content" in data["output"]


def test_explicit_model(client):
    response = client.post("/v1/responses", json={"model": "tinyllama", "input": "Hi"})
    assert response.status_code == 200
    assert response.json()["model"] == "tinyllama"


def test_with_instructions(client):
    response = client.post(
        "/v1/responses",
        json={
            "instructions": "You are a pirate.",
            "input": "What is the weather?",
        },
    )
    assert response.status_code == 200
    assert response.json()["output"]["content"] != ""


def test_with_temperature(client):
    response = client.post("/v1/responses", json={"input": "Hello", "temperature": 0.1})
    assert response.status_code == 200


def test_missing_input_returns_422(client):
    response = client.post("/v1/responses", json={})
    assert response.status_code == 422
