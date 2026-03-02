"""
Main entry point of the FastAPI application.

This module creates the FastAPI instance and registers all routers (route groups).
It also sets up logging before the app starts.

Run with:
     PYTHONPATH=app uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from endpoints import responses, models
from core.logging import setup_logging

# Initialize the logging system before anything else (format, level, etc.)
setup_logging()

# Main FastAPI application instance
app = FastAPI(
    title="Local Responses API",
    description="OpenAI-compatible API running locally via Ollama",
    version="2.0.0",
)

# Register routers
# Each router groups the routes of a functional domain
app.include_router(responses.router) # /v1/responses
app.include_router(models.router)    # /v1/models


@app.get("/")
def root():
    """Health check and API info."""
    return {
        "name": app.title,
        "descritpion": app.description,
        "version": app.version,
        "status": "running",
        "docs": "/docs",
        "endpoints": ["/v1/responses", "/v1/models"],
    }
