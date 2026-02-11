from abc import ABC, abstractmethod

from src.federated_learning_server.clients.schemas import FederatedDataDTO


class MlFlowServiceClientInterface(ABC):
    @abstractmethod
    def get_federated_data(self, model_key: str) -> FederatedDataDTO:
        raise NotImplementedError