from abc import ABC, abstractmethod

from clients.schemas import QueryResponseDTO, QueryRequestDTO


class InferenceServiceClientInterface(ABC):
    @abstractmethod
    def inference_model(self, query_request_dto: QueryRequestDTO) -> QueryResponseDTO:
        raise NotImplementedError