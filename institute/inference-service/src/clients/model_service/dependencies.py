from .model_service_client_interface import ModelServiceClientInterface
from .model_service_client import ModelServiceClient
from config import settings

def build_model_service_client() -> ModelServiceClientInterface:
    return ModelServiceClient.get_instance(model_service_url=settings.model_service_url)