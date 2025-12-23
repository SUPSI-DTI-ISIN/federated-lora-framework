from config import settings
from schemas.inference import QueryResponseDTO, QueryRequestDTO
from services.inference_service_interface import InferenceServiceInterface

class InferenceService(InferenceServiceInterface):
    async def inference_model(self, query_request_dto: QueryRequestDTO) -> QueryResponseDTO:
        response: str = f"This is a mocked response from prompt {query_request_dto.prompt}"
        return QueryResponseDTO(query=query_request_dto.prompt, response=response, model_id=settings.model_id)