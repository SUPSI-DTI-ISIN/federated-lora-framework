from .adapter_registry_service_interface import AdapterRegistryServiceInterface
from .adapter_registry_service import AdapterRegistryService

def get_adapter_registry_service() -> AdapterRegistryServiceInterface:
    return AdapterRegistryService.get_instance()