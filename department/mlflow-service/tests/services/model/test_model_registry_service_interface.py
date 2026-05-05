import pytest
from abc import ABC
from services.model.model_registry_service_interface import ModelRegistryServiceInterface


class _ConcreteModel(ModelRegistryServiceInterface):
    def get_model_manifest(self, model_key):
        return super().get_model_manifest(model_key)

    def get_model_file(self, model_key, file_name):
        return super().get_model_file(model_key, file_name)


class TestModelRegistryServiceInterface:
    def test_is_abstract(self):
        assert issubclass(ModelRegistryServiceInterface, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            ModelRegistryServiceInterface()

    def test_abstract_methods_defined(self):
        assert ModelRegistryServiceInterface.__abstractmethods__ == {"get_model_manifest", "get_model_file"}

    def test_partial_subclass_raises_type_error(self):
        class Partial(ModelRegistryServiceInterface):
            def get_model_manifest(self, model_key):
                pass

        with pytest.raises(TypeError):
            Partial()

    @pytest.mark.parametrize("method,args", [
        ("get_model_manifest", ("m",)),
        ("get_model_file", ("m", "f.bin")),
    ])
    def test_abstract_method_bodies_raise_not_implemented(self, method, args):
        with pytest.raises(NotImplementedError):
            getattr(_ConcreteModel(), method)(*args)
