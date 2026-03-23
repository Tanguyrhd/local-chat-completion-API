"""
LLM orchestration layer.

LLMEngine sits between the API routes and the Ollama client.
It handles model resolution, response wrapping, and the agentic tool-calling
loop so that routes stay thin and the Ollama client stays focused on HTTP.
"""

import logging
import time

from core.config import settings
from services import tool_registry
from services.ollama_client import chat_with_ollama, stream_from_ollama
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

    def generate_response(
        self,
        model: str | None,
        messages: list[dict],
        temperature: float,
        use_tools: bool = False,
    ) -> Response:
        """
        Generate a response from the LLM, with an optional agentic tool-calling loop.

        When use_tools=True, registered tools are passed to Ollama. If the model
        decides to call one, the tool is executed locally and its result is fed
        back to the model. This repeats until the model returns a plain text reply.

        Args:
            model: The model name to use. Falls back to default_model if None.
            messages: Pre-built list of message dicts (built by prompt_builder).
            temperature: Sampling temperature between 0.0 and 1.0.
            use_tools: Whether to expose registered tools to the model.

        Returns:
            Response: A typed Pydantic object containing the model name and assistant reply.
        """
        model = model or self.default_model
        logger.info(
            "Generating response with model=%s temperature=%s use_tools=%s",
            model, temperature, use_tools,
        )
        start = time.time()

        tools = tool_registry.get_schemas() if use_tools else None
        messages = list(messages)  # avoid mutating the caller's list

        while True:
            message = chat_with_ollama(
                model=model, messages=messages, temperature=temperature, tools=tools
            )

            if not message.get("tool_calls"):
                logger.info("Response generated in %.2fs", time.time() - start)
                return Response(
                    model=model,
                    output=ResponseOutput(content=message.get("content", "")),
                )

            # Append assistant message with tool_calls, then execute each tool
            messages.append({
                "role": "assistant",
                "content": message.get("content", ""),
                "tool_calls": message["tool_calls"],
            })
            for tool_call in message["tool_calls"]:
                name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                result = tool_registry.execute(name, arguments)
                messages.append({"role": "tool", "content": result})

            logger.info("Tool calls executed, continuing generation loop")

    def stream_response(self, model: str | None, messages: list[dict], temperature: float):
        """
        Stream a response from the LLM token by token.

        Note: streaming is not supported when use_tools=True. The endpoint
        falls back to generate_response in that case.

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
