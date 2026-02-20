"""
Pydantic models for the /v1/responses endpoint.

Three models work together to represent the full request/response cycle:
  ResponseRequest  → validates the incoming request body
  ResponseOutput   → wraps the LLM's text reply
  Response         → the full object returned to the caller
"""

from pydantic import BaseModel
from typing import Optional


class ResponseRequest(BaseModel):
    """
    Request body for POST /v1/responses.

    Attributes:
        model: The LLM to use. Falls back to DEFAULT_MODEL from settings if not provided.
        instructions: the role to set to the model
        input: The prompt to send to the model.
        temperature: Sampling temperature between 0.0 and 1.0.
    """

    model: Optional[str] = None
    instructions: Optional[str] = None
    input: str
    temperature: Optional[float] = 0.7
    stream: bool = False


class ResponseOutput(BaseModel):
    """
    The LLM's reply, wrapped with a role identifier.

    Attributes:
        role: Always "assistant" — identifies who produced this output.
        content: The generated text from the model.
    """

    role: str = "assistant"
    content: str


class Response(BaseModel):
    """
    Full response object returned by the API.

    Built by LLMEngine and returned directly by the route handler.

    Attributes:
        model: Name of the model that generated the response.
        output: The assistant's reply wrapped in a ResponseOutput.
    """

    model: str
    output: ResponseOutput
