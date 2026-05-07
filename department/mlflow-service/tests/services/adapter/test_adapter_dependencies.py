import pytest
from services.adapter.dependencies import get_adapter_registry_service
from services.adapter.adapter_registry_service_interface import AdapterRegistryServiceInterface


@pytest.fixture(autouse=True)
def reset_singleton():
    from services.adapter.adapter_registry_service import AdapterRegistryService
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None
    yield
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None


class TestGetAdapterRegistryService:
    def test_returns_adapter_registry_service_interface(self):
        assert isinstance(get_adapter_registry_service(), AdapterRegistryServiceInterface)

    def test_returns_singleton(self):
        assert get_adapter_registry_service() is get_adapter_registry_service()

    def test_accepts_custom_device_map_and_lora_config(self):
        from peft import LoraConfig
        lc = LoraConfig(r=4, lora_alpha=8, lora_dropout=0.0, bias="none")
        assert isinstance(get_adapter_registry_service(device_map="cpu", lora_config=lc), AdapterRegistryServiceInterface)

    def test_adapter_init_exports(self):
        from services.adapter import AdapterRegistryServiceInterface, get_adapter_registry_service as fn
        assert AdapterRegistryServiceInterface is not None
        assert fn is not None

    def test_adapter_init_version(self):
        import services.adapter as sa
        assert sa.__version__ == "1.0.0"
