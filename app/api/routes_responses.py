"""
Route handler for the /v1/responses endpoint.

Provides a simpler alternative to /v1/chat/completions — accepts a single
input string and an optional system instruction instead of a message history.
"""

from fastapi import APIRouter, Depends
from models.response import ResponseRequest
from services.llm_engine import LLMEngine
from core.security import verify_api_key
from utils.prompt_builder import build_messages_from_response

router = APIRouter()

@router.post("/v1/responses")
def create_response(request: ResponseRequest, _=Depends(verify_api_key)):
    """
    Generate a response from a single input string.

    Builds a messages list from instructions and input via prompt_builder,
    then delegates to LLMEngine and returns the result as-is.

    Args:
        request: Validated request body containing model, instructions, input, and temperature.
        _: API key dependency — runs verify_api_key before this handler executes.

    Returns:
        Response: A Pydantic object with the model name and the assistant's reply.
    """
    messages = build_messages_from_response(request.instructions, request.input)

    return LLMEngine.generate_response(
        model=request.model,
        messages=messages,
        temperature=request.temperature
        )
