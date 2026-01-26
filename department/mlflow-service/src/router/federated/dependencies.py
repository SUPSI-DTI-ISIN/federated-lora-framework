from services.adapter import AdapterRegistryServiceInterface, AdapterRegistryService
from services.model import ModelRegistryServiceInterface, ModelRegistryService

def get_model_registry_service() -> ModelRegistryServiceInterface:
    return ModelRegistryService.get_instance()

def get_adapter_registry_service() -> AdapterRegistryServiceInterface:
    return AdapterRegistryService.get_instance()