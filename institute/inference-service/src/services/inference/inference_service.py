from schemas.inference import QueryResponseDTO, QueryRequestDTO
from clients.model_service import ModelServiceClientInterface
from services.inference.inference_service_interface import InferenceServiceInterface

class InferenceService(InferenceServiceInterface):
    __INSTANCE = None

    def __init__(self, model_service_client: ModelServiceClientInterface):
        self.__model_service_client = model_service_client

    @classmethod
    def get_instance(cls, model_service_client: ModelServiceClientInterface):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(model_service_client=model_service_client)
        return cls.__INSTANCE


    async def inference_model(self, query_request_dto: QueryRequestDTO) -> QueryResponseDTO:
        model_path = self.__model_service_client.get_model_path_for_adapter(model_key=query_request_dto.model_key, adapter_version=query_request_dto.adapter_version)
        print(model_path.model_base_path)
        print(model_path.adapter_path)

        response: str = f"This is a mocked response from prompt {query_request_dto.prompt}"
        return QueryResponseDTO(prompt=query_request_dto.prompt, adapter_version=query_request_dto.adapter_version, response=response, model_key=query_request_dto.model_key)