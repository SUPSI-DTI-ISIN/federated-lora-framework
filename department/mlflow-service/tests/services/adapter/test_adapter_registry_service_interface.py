import pytest
from abc import ABC
from services.adapter.adapter_registry_service_interface import AdapterRegistryServiceInterface


class _ConcreteAdapter(AdapterRegistryServiceInterface):
    def ensure_init_adapter(self, model_key):
        return super().ensure_init_adapter(model_key)

    def get_adapters_version(self, model_key):
        return super().get_adapters_version(model_key)

    def get_new_adapter_path(self, model_key):
        return super().get_new_adapter_path(model_key)

    def get_latest_adapter_path(self, model_key):
        return super().get_latest_adapter_path(model_key)

    def get_adapter_manifest(self, model_key, adapter_version):
        return super().get_adapter_manifest(model_key, adapter_version)

    def get_adapter_file(self, model_key, adapter_version, file_name):
        return super().get_adapter_file(model_key, adapter_version, file_name)

    def delete_adapter_version(self, model_key, adapter_version):
        return super().delete_adapter_version(model_key, adapter_version)


class TestAdapterRegistryServiceInterface:
    def test_is_abstract(self):
        assert issubclass(AdapterRegistryServiceInterface, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            AdapterRegistryServiceInterface()

    def test_abstract_methods_defined(self):
        assert AdapterRegistryServiceInterface.__abstractmethods__ == {
            "ensure_init_adapter",
            "get_adapters_version",
            "get_new_adapter_path",
            "get_latest_adapter_path",
            "get_adapter_manifest",
            "get_adapter_file",
            "delete_adapter_version",
        }

    def test_partial_subclass_raises_type_error(self):
        class Partial(AdapterRegistryServiceInterface):
            def ensure_init_adapter(self, model_key):
                pass

        with pytest.raises(TypeError):
            Partial()

    @pytest.mark.parametrize("method,args", [
        ("ensure_init_adapter", ("m",)),
        ("get_adapters_version", ("m",)),
        ("get_new_adapter_path", ("m",)),
        ("get_latest_adapter_path", ("m",)),
        ("get_adapter_manifest", ("m", 1)),
        ("get_adapter_file", ("m", 1, "f.bin")),
        ("delete_adapter_version", ("m", 1)),
    ])
    def test_abstract_method_bodies_raise_not_implemented(self, method, args):
        obj = _ConcreteAdapter()
        with pytest.raises(NotImplementedError):
            getattr(obj, method)(*args)
