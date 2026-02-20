"""
Main entry point of the FastAPI application.

This module creates the FastAPI instance and registers all routers (route groups).
It also sets up logging before the app starts.

Run with:
     PYTHONPATH=app uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from api import routes_chat, routes_responses, routes_models
from core.config.logging_config import setup_logging

# Initialize the logging system before anything else (format, level, etc.)
setup_logging()

# Main FastAPI application instance
app = FastAPI(
    title="Local Chat Completion API",
    description="OpenAI-compatible API running locally via Ollama",
    version="2.0.0",
)

# Register routers
# Each router groups the routes of a functional domain
app.include_router(routes_chat.router)      # /v1/chat/completions
app.include_router(routes_responses.router) # /v1/responses
app.include_router(routes_models.router)    # /v1/models


@app.get("/")
def root():
    """Health check and API info."""
    return {
        "name": app.title,
        "descritpion": app.description,
        "version": app.version,
        "status": "running",
        "docs": "/docs",
        "endpoints": ["/v1/chat/completions", "/v1/responses", "/v1/models"],
    }
