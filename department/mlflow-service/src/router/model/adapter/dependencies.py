from services.adapter import AdapterRegistryServiceInterface, AdapterRegistryService

def get_adapter_registry_service() -> AdapterRegistryServiceInterface:
    return AdapterRegistryService.get_instance()