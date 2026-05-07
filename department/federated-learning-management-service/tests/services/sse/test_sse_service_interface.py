import pytest
from abc import ABC

from services.sse.sse_service_interface import SseServiceInterface


class TestSseServiceInterface:
    def test_is_abstract(self):
        assert issubclass(SseServiceInterface, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            SseServiceInterface()

    def test_abstract_methods_defined(self):
        assert SseServiceInterface.__abstractmethods__ == {"generate_sse_events"}

    def test_complete_subclass_can_be_instantiated(self):
        class Concrete(SseServiceInterface):
            async def generate_sse_events(self, request): ...

        assert isinstance(Concrete(), SseServiceInterface)

    async def test_abstract_method_body_raises_not_implemented(self):
        class CallerThrough(SseServiceInterface):
            async def generate_sse_events(self, request):
                return await super().generate_sse_events(request)

        with pytest.raises(NotImplementedError):
            await CallerThrough().generate_sse_events(None)
