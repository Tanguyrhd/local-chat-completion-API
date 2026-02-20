"""
Route handler for the /v1/chat/completions endpoint.

Implements an OpenAI-compatible chat completion endpoint that accepts
a conversation history and returns the model's reply.
"""

import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from models.chat import ChatCompletionRequest
from services.llm_engine import LLMEngine
from utils.prompt_builder import build_messages_from_chat
from core.security import verify_api_key

router = APIRouter()


def _sse_generator(chunks):
    """Wrap text chunks in Server-Sent Events format."""
    for chunk in chunks:
        yield f"data: {json.dumps({'content': chunk})}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/v1/chat/completions")
def create_chat_completion(request: ChatCompletionRequest, _=Depends(verify_api_key)):
    """
    Generate one or more chat completions from a conversation history.

    Converts the message list to dicts via prompt_builder, then calls the LLM
    n times independently and returns all results in OpenAI-compatible format.
    Supports streaming via the `stream` field (n is ignored when streaming).

    Args:
        request: Validated request body containing model, messages, temperature, n, and stream.
        _: API key dependency — runs verify_api_key before this handler executes.

    Returns:
        dict | StreamingResponse: OpenAI-compatible response, or SSE stream if stream=True.
    """
    messages = build_messages_from_chat(request.messages)

    if request.stream:
        _, chunks = LLMEngine.stream_response(
            model=request.model, messages=messages, temperature=request.temperature
        )
        return StreamingResponse(_sse_generator(chunks), media_type="text/event-stream")

    # Call the engine n times to generate multiple independent completions
    responses = [
        LLMEngine.generate_response(
            model=request.model, messages=messages, temperature=request.temperature
        )
        for _ in range(request.n)
    ]

    return {
        "model": responses[0].model,
        "choices": [
            {"message": {"role": "assistant", "content": r.output.content}}
            for r in responses
        ],
    }
