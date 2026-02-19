"""
Utility functions for building prompts from structured data.

Handles the conversion from API-level data structures (like message lists)
into raw strings that the LLM can consume.
"""

def build_prompt_from_messages(messages):
    """
    Convert a list of chat messages into a single formatted prompt string.

    Each message is formatted as "[ROLE]: content" on its own line.
    A trailing "[ASSISTANT]:" cue is appended at the end to prompt
    the model to generate the next reply.

    Args:
        messages: Ordered list of messages representing the conversation history.

    Returns:
        str: A formatted prompt string ready to be sent to the LLM.

    Example:
        Input:
            [Message(role="system", content="You are helpful."),
             Message(role="user", content="What is Python?")]

        Output:
            "[SYSTEM]: You are helpful.\\n[USER]: What is Python?\\n[ASSISTANT]:"
    """
    prompt = ""

    for msg in messages:
        prompt += f"[{msg.role.upper()}]: {msg.content}\n"

    prompt += "[ASSISTANT]:"

    return prompt
