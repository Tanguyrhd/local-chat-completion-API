"""
Unit tests for prompt_builder utility functions.

These tests cover pure functions with no external dependencies.
"""

from utils.prompt_builder import build_messages_from_chat, build_messages_from_response
from models.chat import Message


def test_build_messages_from_chat_single_user():
    messages = [Message(role="user", content="Hello")]
    result = build_messages_from_chat(messages)
    assert result == [{"role": "user", "content": "Hello"}]


def test_build_messages_from_chat_system_and_user():
    messages = [
        Message(role="system", content="You are helpful."),
        Message(role="user", content="Hi"),
    ]
    result = build_messages_from_chat(messages)
    assert result == [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hi"},
    ]


def test_build_messages_from_chat_multi_turn_order_preserved():
    messages = [
        Message(role="user", content="My name is Alice."),
        Message(role="assistant", content="Nice to meet you, Alice!"),
        Message(role="user", content="What is my name?"),
    ]
    result = build_messages_from_chat(messages)
    assert len(result) == 3
    assert result[0]["role"] == "user"
    assert result[1]["role"] == "assistant"
    assert result[2]["role"] == "user"


def test_build_messages_from_response_without_instructions():
    result = build_messages_from_response(None, "Hello")
    assert result == [{"role": "user", "content": "Hello"}]


def test_build_messages_from_response_with_instructions():
    result = build_messages_from_response("You are a pirate.", "What is the weather?")
    assert result == [
        {"role": "system", "content": "You are a pirate."},
        {"role": "user", "content": "What is the weather?"},
    ]
