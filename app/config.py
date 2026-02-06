from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_HOST: str = "http://localhost:11434"
    API_PORT: int = 8000
    DEFAULT_MODEL: str = "llama3.2:3b"

    class Config:
        env_file = ".env"

settings = Settings()
