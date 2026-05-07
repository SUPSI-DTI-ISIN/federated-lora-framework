from .model_registry_service_interface import ModelRegistryServiceInterface
from .model_registry_service import ModelRegistryService

def get_model_registry_service() -> ModelRegistryServiceInterface:
    return ModelRegistryService.get_instance()