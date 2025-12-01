import torch

from app.domain.llm_model import LlmModel
from app.training.core import load_peft_model


class ModelService:
    __INSTANCE = None

    def __init__(self, model_name: str):
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self._llm_model: LlmModel = load_peft_model(model_name)

        self._llm_model.model.to(self._device)
        self._llm_model.model.eval()

    @classmethod
    def get_model_service(cls, model_name: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(model_name)
        return cls.__INSTANCE

    @property
    def device(self) -> torch.device:
        return self._device

    @property
    def llm_model(self) -> LlmModel:
        return self._llm_model

    def load_model(self, model_name: str) -> bool:
        if self._llm_model is not None:
            return False

        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self._llm_model = load_peft_model(model_name)
        self._llm_model.model.to(self._device)
        self._llm_model.model.eval()
        return True

    def clear(self) -> bool:
        if self._llm_model is None:
            return False

        del self._llm_model

        self._device = None
        self._llm_model = None
        return True
