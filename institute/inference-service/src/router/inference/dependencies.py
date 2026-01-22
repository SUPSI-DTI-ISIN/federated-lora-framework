from fastapi import Depends

from services.clients.model_service import ModelServiceClientInterface, ModelServiceClient
from services.inference import InferenceServiceInterface, InferenceService

from config import settings

def get_model_service_client(model_service_url: str = Depends(settings.model_service_url)) -> ModelServiceClientInterface:
    return ModelServiceClient.get_instance(model_service_url=model_service_url)

def get_inference_service(model_service_client: ModelServiceClientInterface = Depends(get_model_service_client)) -> InferenceServiceInterface:
    return InferenceService.get_instance(model_service_client=model_service_client)