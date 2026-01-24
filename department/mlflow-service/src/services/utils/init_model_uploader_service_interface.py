from abc import ABC, abstractmethod


class InitModelUploaderServiceInterface(ABC):
    @abstractmethod
    def upload_model(self, model_key: str):
        raise NotImplementedError