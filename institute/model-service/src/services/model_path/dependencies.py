from .model_path_service_interface import ModelPathServiceInterface
from .model_path_service import ModelPathService

def get_model_path_service() -> ModelPathServiceInterface:
    return ModelPathService.get_instance()