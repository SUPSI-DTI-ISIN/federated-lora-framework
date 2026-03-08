from abc import ABC, abstractmethod

class CeleryJobServiceInterface(ABC):
    @abstractmethod
    def start_federated_learning(self) -> str:
        raise NotImplementedError