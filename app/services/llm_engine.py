"""
LLM orchestration layer.

LLMEngine sits between the API routes and the Ollama client.
It handles model resolution, prompt construction, and response wrapping,
so that routes stay thin and the Ollama client stays focused on HTTP.
"""

from core.config.settings import settings
from services.ollama_client import generate_with_ollama
from models.response import Response, ResponseOutput
from models.chat import Message
from utils.prompt_builder import build_prompt_from_messages

class LLMEngine:
    """
    Central orchestrator for LLM interactions.

    Acts as a facade between the API layer and the underlying model client.
    Handles model resolution and prompt preparation before delegating
    the actual generation to the Ollama client.

    keeping it as a class for future implementation like :
        Add multiple related methods (generate_response, stream_response, count_tokens...)
        Make it instantiable so it holds state (e.g. a connection pool, a cache)
        Support dependency injection via FastAPI's Depends(LLMEngine) pattern
    """

    @staticmethod
    def generate_response(model: str | None, instructions: str | None, input_text: str, temperature: float):
        """
        Generate a single response from the LLM.

        Resolves the model to use, optionally prepends a system instruction
        to the prompt, then delegates to the Ollama client for generation.

        Args:
            model: The model name to use. Falls back to DEFAULT_MODEL if None.
            instructions: Optional system-level instruction prepended to the prompt.
                          E.g. "You are a comedian, just make jokes."
            input_text: The user's input or the pre-built prompt string.
            temperature: Sampling temperature between 0.0 and 1.0.

        Returns:
            Response: A typed Pydantic object containing the model name and assistant reply.
        """
        model = model or settings.DEFAULT_MODEL

        # If a system instruction is provided, prepend it to the prompt
        if instructions:
            messages = [
                Message(role="system", content=instructions),
                Message(role="user", content=input_text),
            ]
            input_text = build_prompt_from_messages(messages)

        output_text = generate_with_ollama(
            model=model,
            prompt=input_text,
            temperature=temperature
        )

        return Response(
            model=model,
            output=ResponseOutput(content=output_text)
        )
