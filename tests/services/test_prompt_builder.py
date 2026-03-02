"""
Unit tests for prompt_builder utility functions.

These tests cover pure functions with no external dependencies.
"""

from services.prompt_builder import build_messages_from_response


def test_build_messages_from_response_without_instructions():
    result = build_messages_from_response(None, "Hello")
    assert result == [{"role": "user", "content": "Hello"}]


def test_build_messages_from_response_with_instructions():
    result = build_messages_from_response("You are a pirate.", "What is the weather?")
    assert result == [
        {"role": "system", "content": "You are a pirate."},
        {"role": "user", "content": "What is the weather?"},
    ]
