from peft import LoraConfig

from .adapter_registry_service_interface import AdapterRegistryServiceInterface
from .adapter_registry_service import AdapterRegistryService
from config import settings

def get_adapter_registry_service(device_map: str = settings.device_map, lora_config: LoraConfig = settings.lora_config) -> AdapterRegistryServiceInterface:
    return AdapterRegistryService.get_instance(device_map=device_map, lora_config=lora_config)