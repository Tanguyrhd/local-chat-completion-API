"""
Pydantic models for the /v1/chat/completions endpoint.

These models define and validate the shape of incoming request data,
following the OpenAI Chat Completion API format.
"""

from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    """
    A single message in a conversation.

    Attributes:
        role: The author of the message. One of "system", "user", or "assistant".
        content: The text content of the message.
    """

    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    """
    Request body for POST /v1/chat/completions.

    Attributes:
        model: The LLM to use. Falls back to DEFAULT_MODEL from settings if not provided.
        messages: The full conversation history, ordered from oldest to newest.
        n: Number of independent completions to generate for the same prompt.
           Defaults to 1. All n responses are returned in the "choices" list.
        temperature: Sampling temperature between 0.0 and 1.0.
                     Lower = more focused/deterministic, higher = more creative/random.
    """

    model: Optional[str] = None
    messages: List[Message]
    n: int = 1
    temperature: Optional[float] = 0.7
