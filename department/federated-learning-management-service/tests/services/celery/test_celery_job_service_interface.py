import pytest
from abc import ABC

from services.celery.celery_job_service_interface import CeleryJobServiceInterface


class _ConcreteService(CeleryJobServiceInterface):
    def start_federated_learning(self) -> str:
        return super().start_federated_learning()


class TestCeleryJobServiceInterface:
    def test_is_abstract(self):
        assert issubclass(CeleryJobServiceInterface, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            CeleryJobServiceInterface()

    def test_abstract_methods_defined(self):
        assert CeleryJobServiceInterface.__abstractmethods__ == {"start_federated_learning"}

    def test_partial_subclass_raises_type_error(self):
        class Partial(CeleryJobServiceInterface):
            pass

        with pytest.raises(TypeError):
            Partial()

    def test_abstract_method_body_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            _ConcreteService().start_federated_learning()
