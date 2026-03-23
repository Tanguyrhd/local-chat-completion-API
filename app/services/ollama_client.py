"""
HTTP client for the local Ollama inference server.

This module is the only place in the app that communicates directly with Ollama.
All other modules go through these functions to generate text.
"""

import json
import requests
from core.config import settings


def chat_with_ollama(
    model: str,
    messages: list[dict],
    temperature: float,
    tools: list[dict] | None = None,
) -> dict:
    """
    Send messages to Ollama and return the full assistant message dict.

    Unlike a simple text-only call, this returns the complete message object
    so that the caller can inspect tool_calls if the model wants to use a tool.

    Args:
        model: The name of the Ollama model to use (e.g. "llama3", "mistral").
        messages: List of message dicts with "role" and "content" keys.
        temperature: Sampling temperature between 0.0 and 1.0.
        tools: Optional list of OpenAI-compatible tool schemas to expose.

    Returns:
        dict: The full assistant message from Ollama
              (may contain "content" and/or "tool_calls").

    Raises:
        requests.HTTPError: If Ollama returns a 4xx or 5xx response.
        requests.ConnectionError: If the Ollama server is not running.
    """
    payload: dict = {
        "model": model,
        "messages": messages,
        "options": {"temperature": temperature},
        "stream": False,
    }
    if tools:
        payload["tools"] = tools

    response = requests.post(settings.OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["message"]


def stream_from_ollama(model: str, messages: list[dict], temperature: float):
    """
    Stream text chunks from the Ollama /api/chat endpoint.

    Yields one string per token as the model generates it, without waiting
    for the full response.

    Args:
        model: The name of the Ollama model to use.
        messages: List of message dicts with "role" and "content" keys.
        temperature: Sampling temperature between 0.0 and 1.0.

    Yields:
        str: Individual text chunks from the model output.

    Raises:
        requests.HTTPError: If Ollama returns a 4xx or 5xx response.
        requests.ConnectionError: If the Ollama server is not running.
    """
    response = requests.post(
        settings.OLLAMA_URL,
        json={
            "model": model,
            "messages": messages,
            "options": {"temperature": temperature},
            "stream": True,
        },
        stream=True,
    )
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            if not chunk.get("done"):
                yield chunk["message"]["content"]


def get_ollama_models() -> list[dict]:
    """
    Fetch the list of locally available models from Ollama.

    Returns:
        list[dict]: Raw model entries from Ollama's /api/tags response.

    Raises:
        requests.HTTPError: If Ollama returns a 4xx or 5xx response.
        requests.ConnectionError: If the Ollama server is not running.
    """
    base_url = settings.OLLAMA_URL.rsplit("/api/", 1)[0]
    response = requests.get(f"{base_url}/api/tags")
    response.raise_for_status()
    return response.json().get("models", [])
