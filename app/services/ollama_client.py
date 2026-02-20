"""
HTTP client for the local Ollama inference server.

This module is the only place in the app that communicates directly with Ollama.
All other modules go through this function to generate text.
"""

import requests
from core.config.settings import settings


def generate_with_ollama(model: str, messages: list[dict], temperature: float):
    """
    Send a list of messages to the Ollama /api/chat endpoint and return the reply.

    Makes a synchronous POST request to the local Ollama server and waits
    for the full response before returning (no streaming).

    Args:
        model: The name of the Ollama model to use (e.g. "llama3", "mistral").
        messages: List of message dicts with "role" and "content" keys.
        temperature: Sampling temperature between 0.0 and 1.0.

    Returns:
        str: The raw generated text from the model.

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
            "stream": False,
        },
    )

    response.raise_for_status()

    return response.json()["message"]["content"]
