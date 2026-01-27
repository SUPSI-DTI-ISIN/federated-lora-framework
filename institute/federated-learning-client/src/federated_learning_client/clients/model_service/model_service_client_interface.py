from abc import ABC, abstractmethod

from federated_learning_client.clients.schemas import ModelPathDTO


class ModelServiceClientInterface(ABC):
    @abstractmethod
    def get_model_path(self, model_key: str) -> ModelPathDTO:
        raise NotImplementedError