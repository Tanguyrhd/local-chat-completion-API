"""
Route handler for the /v1/responses endpoint.

Accepts a single input string and an optional system instruction.
"""

import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from schemas.responses import ResponseRequest
from services.llm_engine import LLMEngine
from core.security import verify_api_key
from services.prompt_builder import build_messages_from_response

router = APIRouter()


def _sse_generator(model, chunks, temperature, stream):
    """Wrap text chunks in Server-Sent Events format."""
    yield f"data: {json.dumps({'model': model, 'temperature': temperature, 'stream': stream})}\n\n"
    for chunk in chunks:
        yield f"data: {json.dumps({'content': chunk})}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/v1/responses")
def create_response(
    request: ResponseRequest,
    _=Depends(verify_api_key),
    engine: LLMEngine = Depends(LLMEngine),
):
    """
    Generate a response from a single input string.

    Builds a messages list from instructions and input via prompt_builder,
    then delegates to LLMEngine. Supports streaming via the `stream` field.

    Args:
        request: Validated request body containing model, instructions, input, temperature, and stream.
        _: API key dependency — runs verify_api_key before this handler executes.
        engine: LLMEngine instance injected by FastAPI.

    Returns:
        Response | StreamingResponse: Full response object, or SSE stream if stream=True.
    """
    messages = build_messages_from_response(request.instructions, request.input)

    if request.stream and not request.tools:
        model, chunks = engine.stream_response(
            model=request.model, messages=messages, temperature=request.temperature
        )
        return StreamingResponse(_sse_generator(model, chunks, request.temperature, request.stream), media_type="text/event-stream")

    return engine.generate_response(
        model=request.model,
        messages=messages,
        temperature=request.temperature,
        use_tools=request.tools,
    )
