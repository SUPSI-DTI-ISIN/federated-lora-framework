from services.model import ModelRegistryServiceInterface, ModelRegistryService

def get_model_registry_service() -> ModelRegistryServiceInterface:
    return ModelRegistryService.get_instance()