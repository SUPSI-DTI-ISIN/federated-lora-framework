from .model_service import ModelService
from .model_service_interface import ModelServiceInterface
from clients.model_service import ModelServiceClientInterface, build_model_service_client
from config import settings

def build_model_service(max_cached_adapters: int = settings.max_cached_adapters, device_map: str = settings.device_map, model_service_client: ModelServiceClientInterface = build_model_service_client()) -> ModelServiceInterface:
    return ModelService.get_instance(model_service_client=model_service_client, max_cached_adapters=max_cached_adapters, device_map=device_map)