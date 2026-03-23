"""
Tool registry for function calling.

Tools are registered with an OpenAI-compatible JSON schema and a Python handler.
The LLMEngine passes all registered schemas to Ollama and routes tool_call
responses back to the appropriate handler.

Usage:
    from services import tool_registry

    tool_registry.register(
        schema={
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name."}
                    },
                    "required": ["city"],
                },
            },
        },
        handler=lambda city: f"Weather in {city}: 22°C, sunny.",
    )
"""

import json
import logging
from typing import Callable

logger = logging.getLogger(__name__)

# name -> {"schema": dict, "handler": Callable}
_registry: dict[str, dict] = {}


def register(schema: dict, handler: Callable) -> None:
    """Register a tool with its schema and Python handler."""
    name = schema["function"]["name"]
    _registry[name] = {"schema": schema, "handler": handler}
    logger.info("Registered tool: %s", name)


def get_schemas() -> list[dict]:
    """Return all registered tool schemas (passed to Ollama as the tools param)."""
    return [v["schema"] for v in _registry.values()]


def execute(name: str, arguments: dict | str) -> str:
    """
    Execute a registered tool by name and return its result as a string.

    Args:
        name: The tool name from the model's tool_call.
        arguments: The arguments dict (or JSON string) from the model.

    Returns:
        str: The tool result, or an error message if execution fails.
    """
    if name not in _registry:
        return f"Error: unknown tool '{name}'"

    if isinstance(arguments, str):
        arguments = json.loads(arguments)

    logger.info("Executing tool '%s' with args %s", name, arguments)
    try:
        result = _registry[name]["handler"](**arguments)
        return str(result)
    except Exception as e:
        logger.error("Tool '%s' raised: %s", name, e)
        return f"Error: {e}"
