from abc import ABC, abstractmethod


class ManagementServiceInterface(ABC):
    @abstractmethod
    async def start_federated_learning(self):
        raise NotImplementedError