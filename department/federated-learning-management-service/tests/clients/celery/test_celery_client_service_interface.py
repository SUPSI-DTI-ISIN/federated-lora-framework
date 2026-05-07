import pytest
from abc import ABC

from clients.celery.celery_client_service_interface import CeleryClientServiceInterface


class _ConcreteClient(CeleryClientServiceInterface):
    def get_celery_client(self):
        return super().get_celery_client()


class TestCeleryClientServiceInterface:
    def test_is_abstract(self):
        assert issubclass(CeleryClientServiceInterface, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            CeleryClientServiceInterface()

    def test_abstract_methods_defined(self):
        assert CeleryClientServiceInterface.__abstractmethods__ == {"get_celery_client"}

    def test_complete_subclass_can_be_instantiated(self):
        class Concrete(CeleryClientServiceInterface):
            def get_celery_client(self): ...

        assert isinstance(Concrete(), CeleryClientServiceInterface)

    def test_abstract_method_body_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            _ConcreteClient().get_celery_client()
