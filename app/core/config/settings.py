"""
Application configuration loaded from environment variables.

Uses pydantic-settings to automatically read values from the .env file
and validate their types. Any field can be overridden by setting the
corresponding environment variable.
"""

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Central configuration class for the application.

    Fields are loaded from environment variables (case-insensitive).
    If a variable is not set, the default value is used.
    """

    APP_NAME: str = "Mini OpenAI Clone"
    DEBUG: bool = True

    OLLAMA_URL: str = Field(
        default="http://localhost:11434/api/chat"
    )

    DEFAULT_MODEL: str = "llama3"

    API_KEY: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
