"""
Utility functions for building prompts from structured data.

Handles the conversion from API-level data structures (like message lists)
into message dicts for the Ollama /api/chat endpoint.
"""

def build_messages_from_chat(messages) -> list[dict]:
    """Convert a list of Message objects to dicts for the Ollama /api/chat endpoint."""
    return [{"role": m.role, "content": m.content} for m in messages]

def build_messages_from_response(instructions: str | None, input_text: str) -> list[dict]:
    """Build a messages list from an optional system instruction and user input."""
    messages = []
    if instructions:
        messages.append({"role": "system", "content": instructions})
    messages.append({"role": "user", "content": input_text})
    return messages
