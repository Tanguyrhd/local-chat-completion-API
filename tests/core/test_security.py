"""
Tests for API key authentication.

Covers: auth disabled (no API_KEY set), valid key, invalid key, missing key.
"""


def test_no_api_key_configured_auth_disabled(client):
    """When API_KEY is None, all requests pass through without a key."""
    response = client.post("/v1/responses", json={"input": "Hello"})
    assert response.status_code == 200


def test_valid_api_key_accepted(client_with_auth):
    client, api_key = client_with_auth
    response = client.post(
        "/v1/responses",
        json={"input": "Hello"},
        headers={"x-api-key": api_key},
    )
    assert response.status_code == 200


def test_invalid_api_key_rejected(client_with_auth):
    client, _ = client_with_auth
    response = client.post(
        "/v1/responses",
        json={"input": "Hello"},
        headers={"x-api-key": "wrong-key"},
    )
    assert response.status_code == 401


def test_missing_api_key_rejected(client_with_auth):
    client, _ = client_with_auth
    response = client.post("/v1/responses", json={"input": "Hello"})
    assert response.status_code == 401
