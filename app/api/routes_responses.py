"""
Route handler for the /v1/responses endpoint.

Provides a simpler alternative to /v1/chat/completions — accepts a single
input string and an optional system instruction instead of a message history.
"""

import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from models.response import ResponseRequest
from services.llm_engine import LLMEngine
from core.security import verify_api_key
from utils.prompt_builder import build_messages_from_response

router = APIRouter()


def _sse_generator(chunks):
    """Wrap text chunks in Server-Sent Events format."""
    for chunk in chunks:
        yield f"data: {json.dumps({'content': chunk})}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/v1/responses")
def create_response(request: ResponseRequest, _=Depends(verify_api_key)):
    """
    Generate a response from a single input string.

    Builds a messages list from instructions and input via prompt_builder,
    then delegates to LLMEngine. Supports streaming via the `stream` field.

    Args:
        request: Validated request body containing model, instructions, input, temperature, and stream.
        _: API key dependency — runs verify_api_key before this handler executes.

    Returns:
        Response | StreamingResponse: Full response object, or SSE stream if stream=True.
    """
    messages = build_messages_from_response(request.instructions, request.input)

    if request.stream:
        _, chunks = LLMEngine.stream_response(
            model=request.model, messages=messages, temperature=request.temperature
        )
        return StreamingResponse(_sse_generator(chunks), media_type="text/event-stream")

    return LLMEngine.generate_response(
        model=request.model, messages=messages, temperature=request.temperature
    )
