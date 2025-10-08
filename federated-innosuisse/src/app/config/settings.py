
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pdf_folder: str = "./pdf-innosuisse"

    llm_ollama_host: str = os.getenv("LLM_OLLAMA_HOST", "http://host.docker.internal:11434")
    llm_ollama_model: str = os.getenv("LLM_OLLAMA_MODEL", "llama3.2:3b")

    class Config:
        env_file = ".env"

settings = Settings()
