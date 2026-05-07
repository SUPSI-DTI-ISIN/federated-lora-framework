from abc import ABC, abstractmethod

from schemas.inference import QueryResponseDTO
from schemas.inference.query_request_dto import QueryRequestDTO


class InferenceServiceInterface(ABC):
    @abstractmethod
    async def inference_model(self, query_request_dto: QueryRequestDTO) -> QueryResponseDTO:
        raise NotImplementedError