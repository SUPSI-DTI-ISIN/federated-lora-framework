import json
from typing import List
import ollama

from app.config.settings import settings
from app.model.section import Section

def build_prompt(system_prompt: str, user_prompt: str) -> str:
    return (
        "role: System\n"
        + "content: " + "\"" + system_prompt + "\""
        + "\n\n"
        + "role: User\n"
        + "content: " + "\"" + user_prompt + "\""
    )


class OllamaService:
    def __init__(self):
        self._host = settings.llm_ollama_host
        self._model = settings.llm_ollama_model
        self.client = ollama.Client(host=self._host)
    
    def generate_document_sections(self, system_prompt: str, user_prompt: str) -> str:
        if not self._is_ollama_running():
            return []
    
        if not self._model_exists():
            return []

        print("\nCall ollama model")
        result = self.client.generate(model=self._model, prompt=build_prompt(system_prompt, user_prompt))
        raw = str(result.get('response', ''))
        print(json.dumps(raw, indent=4))

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
