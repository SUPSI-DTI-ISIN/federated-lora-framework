from unittest.mock import AsyncMock

from services.inference.dependencies import get_inference_service
from services.inference.inference_service import InferenceService


class TestGetInferenceService:
    def test_returns_inference_service_instance(self):
        mock_client = AsyncMock()
        service = get_inference_service(inference_service_client=mock_client)
        assert isinstance(service, InferenceService)
