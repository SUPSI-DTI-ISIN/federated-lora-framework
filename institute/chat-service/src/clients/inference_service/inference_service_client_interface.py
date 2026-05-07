from abc import ABC, abstractmethod

from clients.schemas import QueryResponseDTO, QueryRequestDTO


class InferenceServiceClientInterface(ABC):
    @abstractmethod
    async def inference_model(self, query_request_dto: QueryRequestDTO) -> None:
        raise NotImplementedError