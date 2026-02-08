import requests
from pydantic import ValidationError

from clients.schemas import QueryRequestDTO, QueryResponseDTO
from .inference_service_client_interface import InferenceServiceClientInterface


class InferenceServiceClient(InferenceServiceClientInterface):
    __INSTANCE = None

    def __init__(self, inference_service_url: str):
        self.__inference_service_url = inference_service_url

    @classmethod
    def get_instance(cls, inference_service_url: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(inference_service_url=inference_service_url)
        return cls.__INSTANCE

    def inference_model(self, query_request_dto: QueryRequestDTO) -> QueryResponseDTO:
        inference_url = f"{self.__inference_service_url}/api_inference/inference"

        try:
            resp = requests.post(inference_url, headers={"Accept": "application/json", "Content-Type": "application/json",}, json=query_request_dto.model_dump())
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(err)

        data = resp.json()
        try:
            return QueryResponseDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")