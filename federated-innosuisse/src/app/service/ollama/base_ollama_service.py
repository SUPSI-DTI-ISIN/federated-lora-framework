from abc import ABC, abstractmethod


class BaseOllamaService(ABC):
    @abstractmethod
    def call_model(self, system_prompt: str, user_prompt: str) -> str:
        ...