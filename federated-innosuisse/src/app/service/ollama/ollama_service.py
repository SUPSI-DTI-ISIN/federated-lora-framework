import json
from typing import List, override
import ollama

from app.config.settings import settings
from app.model.section import Section
from app.service.ollama.base_ollama_service import BaseOllamaService

def build_prompt(system_prompt: str, user_prompt: str) -> str:
    return (
        "SYSTEM PROMPT:\n"
        + system_prompt
        + "\n\n"
        + "USER PROMPT\n"
        + user_prompt
    )


class OllamaService(BaseOllamaService):
    def __init__(self):
        self._host = settings.llm_ollama_host
        self._model = settings.llm_ollama_model
        self.client = ollama.Client(host=self._host)
    
    @override
    def call_model(self, system_prompt: str, user_prompt: str) -> str:
        if not self._is_ollama_running():
            return []
    
        if not self._model_exists():
            return []

        print("\nCall ollama model")
        result = self.client.generate(model=self._model, prompt=build_prompt(system_prompt, user_prompt))
        raw = str(result.get('response', ''))
        print(raw)

        return raw
    
    def _is_ollama_running(self) -> bool:
        try:
            if self._host == None:
                return False

            _ = self.client.list()
            return True
        except Exception:
            print(f"Ollama is not running on host: {self._host}")
            return False
        
    def _model_exists(self) -> bool:
        try:
            if self._model == None:
                return False
            
            self.client.show(self._model)
            return True
        except Exception:
            print(f"Ollama has not the required model: {self._model}")
            return False
