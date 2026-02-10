from abc import ABC, abstractmethod
from typing import List

from federated_learning_client.clients.schemas import DocumentDTO


class DataServiceClientInterface(ABC):
    @abstractmethod
    def get_documents(self) -> List[DocumentDTO]:
        raise NotImplementedError