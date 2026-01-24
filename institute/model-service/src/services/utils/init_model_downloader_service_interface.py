from abc import ABC, abstractmethod


class InitModelDownloaderServiceInterface(ABC):
    @abstractmethod
    def download_base_model(self, model_key: str) -> None:
        raise NotImplementedError