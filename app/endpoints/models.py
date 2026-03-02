"""
Route handler for the /v1/models endpoint.

Lists the models currently available on the local Ollama server.
"""

from fastapi import APIRouter, Depends
from core.security import verify_api_key
from services.ollama_client import get_ollama_models

router = APIRouter()


@router.get("/v1/models")
def list_models(_=Depends(verify_api_key)):
    """
    List all locally available Ollama models.

    Proxifies Ollama's /api/tags endpoint and returns a simplified list.

    Args:
        _: API key dependency — runs verify_api_key before this handler executes.

    Returns:
        dict: A dict with a "models" list, each entry having "id" and "size".
    """
    models = get_ollama_models()
    return {"models": [{"id": m["name"], "size": m.get("size")} for m in models]}
