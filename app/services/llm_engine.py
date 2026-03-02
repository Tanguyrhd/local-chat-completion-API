"""
LLM orchestration layer.

LLMEngine sits between the API routes and the Ollama client.
It handles model resolution and response wrapping,
so that routes stay thin and the Ollama client stays focused on HTTP.
"""

import logging
import time

from core.config import settings
from services.ollama_client import generate_with_ollama, stream_from_ollama
from schemas.responses import Response, ResponseOutput

logger = logging.getLogger(__name__)


class LLMEngine:
    """
    Central orchestrator for LLM interactions.

    Acts as a facade between the API layer and the underlying model client.
    Injected into endpoints via FastAPI's Depends(LLMEngine) pattern.
    """

    def __init__(self):
        self.default_model = settings.DEFAULT_MODEL

    def generate_response(self, model: str | None, messages: list[dict], temperature: float):
        """
        Generate a single response from the LLM.

        Resolves the model to use, then delegates to the Ollama client for generation.

        Args:
            model: The model name to use. Falls back to default_model if None.
            messages: Pre-built list of message dicts (built by prompt_builder).
            temperature: Sampling temperature between 0.0 and 1.0.

        Returns:
            Response: A typed Pydantic object containing the model name and assistant reply.
        """
        model = model or self.default_model
        logger.info("Generating response with model=%s temperature=%s", model, temperature)
        start = time.time()

        output_text = generate_with_ollama(
            model=model, messages=messages, temperature=temperature
        )

        logger.info("Response generated in %.2fs", time.time() - start)
        return Response(model=model, output=ResponseOutput(content=output_text))

    def stream_response(self, model: str | None, messages: list[dict], temperature: float):
        """
        Stream a response from the LLM token by token.

        Resolves the model to use, then returns the model name and a generator
        that yields text chunks as they are produced by Ollama.

        Args:
            model: The model name to use. Falls back to default_model if None.
            messages: Pre-built list of message dicts (built by prompt_builder).
            temperature: Sampling temperature between 0.0 and 1.0.

        Returns:
            tuple[str, Generator]: The resolved model name and a chunk generator.
        """
        model = model or self.default_model
        logger.info("Streaming response with model=%s temperature=%s", model, temperature)
        return model, stream_from_ollama(model=model, messages=messages, temperature=temperature)
