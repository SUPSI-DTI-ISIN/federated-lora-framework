from abc import ABC, abstractmethod

from schemas.job import FederatedLearningJobStartResponseDTO

class JobServiceInterface(ABC):
    @abstractmethod
    def start_federated_learning(self) -> FederatedLearningJobStartResponseDTO:
        raise NotImplementedError