from commons import ModelResponseUtils
from schemas.inference import QueryResponseDTO, QueryRequestDTO
from schemas.model import LoadedModel
from services.inference.inference_service_interface import InferenceServiceInterface

class InferenceService(InferenceServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE


    async def inference_model(self, query_request_dto: QueryRequestDTO, loaded_model: LoadedModel) -> QueryResponseDTO:
        response = ModelResponseUtils.generate_model_response(loaded_model=loaded_model, prompt=query_request_dto.prompt)

        return QueryResponseDTO(
            prompt=query_request_dto.prompt,
            adapter_version=query_request_dto.adapter_version if loaded_model.has_adapter else None,
            response=response,
            model_key=query_request_dto.model_key
        )