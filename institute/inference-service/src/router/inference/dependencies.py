from fastapi import Depends

from clients.model_service import ModelServiceClientInterface, ModelServiceClient
from services.inference import InferenceServiceInterface, InferenceService

from config import settings
from services.model import ModelServiceInterface, ModelService


def get_model_service_client() -> ModelServiceClientInterface:
    return ModelServiceClient.get_instance(model_service_url=settings.model_service_url)

def get_model_service(max_cached_models: int = settings.max_cached_models, device_map: str = settings.device_map, model_service_client: ModelServiceClientInterface = Depends(get_model_service_client)) -> ModelServiceInterface:
    return ModelService.get_instance(model_service_client=model_service_client, max_cached_models=max_cached_models, device_map=device_map)

def get_inference_service() -> InferenceServiceInterface:
    return InferenceService.get_instance()