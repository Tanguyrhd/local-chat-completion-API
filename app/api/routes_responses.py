"""
Route handler for the /v1/responses endpoint.

Provides a simpler alternative to /v1/chat/completions — accepts a single
input string and an optional system instruction instead of a message history.
"""

from fastapi import APIRouter, Depends
from models.response import ResponseRequest
from services.llm_engine import LLMEngine
from core.security import verify_api_key

router = APIRouter()

@router.post("/v1/responses")
def create_response(request: ResponseRequest, _=Depends(verify_api_key)):
    """
    Generate a response from a single input string.

    Passes the request directly to LLMEngine and returns the result as-is.
    FastAPI automatically serializes the returned Pydantic object to JSON.

    Args:
        request: Validated request body containing model, instructions, input, and temperature.
        _: API key dependency — runs verify_api_key before this handler executes.

    Returns:
        Response: A Pydantic object with the model name and the assistant's reply.
    """
    return LLMEngine.generate_response(
        model=request.model,
        instructions=request.instructions,
        input_text=request.input,
        temperature=request.temperature
    )
