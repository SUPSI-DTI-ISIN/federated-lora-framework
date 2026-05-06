import pytest
from services.inference.inference_service import InferenceService
from services.inference.dependencies import get_inference_service


@pytest.fixture(autouse=True)
def reset_singleton():
    InferenceService._InferenceService__INSTANCE = None
    yield
    InferenceService._InferenceService__INSTANCE = None


class TestGetInferenceService:
    def test_returns_inference_service_instance(self):
        svc = get_inference_service()
        assert isinstance(svc, InferenceService)
