"""
LLM orchestration layer.

LLMEngine sits between the API routes and the Ollama client.
It handles model resolution and response wrapping,
so that routes stay thin and the Ollama client stays focused on HTTP.
"""

from core.config.settings import settings
from services.ollama_client import generate_with_ollama
from models.response import Response, ResponseOutput


class LLMEngine:
    """
    Central orchestrator for LLM interactions.

    Acts as a facade between the API layer and the underlying model client.
    Handles model resolution before delegating the actual generation to the Ollama client.

    keeping it as a class for future implementation like :
        Add multiple related methods (generate_response, stream_response, count_tokens...)
        Make it instantiable so it holds state (e.g. a connection pool, a cache)
        Support dependency injection via FastAPI's Depends(LLMEngine) pattern
    """

    @staticmethod
    def generate_response(model: str | None, messages: list[dict], temperature: float):
        """
        Generate a single response from the LLM.

        Resolves the model to use, then delegates to the Ollama client for generation.

        Args:
            model: The model name to use. Falls back to DEFAULT_MODEL if None.
            messages: Pre-built list of message dicts (built by prompt_builder).
            temperature: Sampling temperature between 0.0 and 1.0.

        Returns:
            Response: A typed Pydantic object containing the model name and assistant reply.
        """
        model = model or settings.DEFAULT_MODEL

        output_text = generate_with_ollama(
            model=model, messages=messages, temperature=temperature
        )

        return Response(model=model, output=ResponseOutput(content=output_text))
