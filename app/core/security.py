"""
API key authentication for the application.

Provides a FastAPI dependency that validates the x-api-key request header.
If no API_KEY is configured in settings, authentication is skipped entirely.
"""

from fastapi import Header, HTTPException
from core.config.settings import settings


def verify_api_key(x_api_key: str = Header(default=None)):

    if settings.API_KEY is None:
        return

    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
