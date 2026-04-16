from .model_registry_service_interface import ModelRegistryServiceInterface
from .dependencies import get_model_registry_service

__all__ = [
    'ModelRegistryServiceInterface',
    'get_model_registry_service'
]

__version__ = "1.0.0"