"""
Route handler for the /v1/chat/completions endpoint.

Implements an OpenAI-compatible chat completion endpoint that accepts
a conversation history and returns the model's reply.
"""

from fastapi import APIRouter, Depends
from models.chat import ChatCompletionRequest
from services.llm_engine import LLMEngine
from utils.prompt_builder import build_prompt_from_messages
from core.security import verify_api_key

router = APIRouter()

@router.post("/v1/chat/completions")
def create_chat_completion(request: ChatCompletionRequest, _=Depends(verify_api_key)):
    """
    Generate one or more chat completions from a conversation history.

    Converts the message list into a single prompt, then calls the LLM
    n times independently and returns all results in OpenAI-compatible format.

    Args:
        request: Validated request body containing model, messages, temperature, and n.
        _: API key dependency — runs verify_api_key before this handler executes.

    Returns:
        dict: OpenAI-compatible response with a "choices" list of n completions.
    """
    prompt = build_prompt_from_messages(request.messages)

    # Call the engine n times to generate multiple independent completions
    responses = [
        LLMEngine.generate_response(
            model=request.model,
            input_text=prompt,
            temperature=request.temperature
        )
        for _ in range(request.n)
    ]

    return {
        "model": responses[0].model,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": r.output.content
                }
            }
            for r in responses
        ]
    }
