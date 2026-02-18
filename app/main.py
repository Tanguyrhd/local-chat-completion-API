from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
from typing import List, Optional

app = FastAPI(
    title="Local Chat Completion API",
    description="API locale compatible OpenAI utilisant Ollama",
    version="1.0.0"
)
## separer pour etre juste faire un truc

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "llama3.2:3b"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    id: str
    model: str
    choices: List[dict]
    usage: dict


## end point peut avoir son propre file / dossier

@app.get("/")
async def root():
    return {
        "message": "Local Chat Completion API",
        "status": "running"
    }

@app.get("/v1/models")
async def list_models():
    """Liste les modèles disponibles (compatible OpenAI)"""
    try:
        models = ollama.list()
        return {
            "object": "list",
            "data": [
                {
                    "id": model['name'],
                    "object": "model",
                    "owned_by": "local"
                }
                for model in models.get('models', [])
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
async def chat_completion(request: ChatRequest):
    """Endpoint principal compatible OpenAI"""
    try:
        # Convertit les messages Pydantic en dict
        messages = [msg.dict() for msg in request.messages]

        # Appelle Ollama
        response = ollama.chat(
            model=request.model,
            messages=messages,
            options={
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            }
        )

        # Formate la réponse façon OpenAI
        return {
            "id": "chatcmpl-local",
            "object": "chat.completion",
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response['message']['content']
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Ollama: {str(e)}")

@app.get("/health")
async def health_check():
    """Vérifie si Ollama est accessible"""
    try:
        ollama.list()
        return {"status": "healthy", "ollama": "connected"}
    except:
        return {"status": "unhealthy", "ollama": "disconnected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
