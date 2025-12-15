import torch

from domain.llm_model import LlmModel
from training.core import load_peft_model


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