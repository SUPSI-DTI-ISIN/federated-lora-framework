from unittest.mock import patch

from clients.inference_service.inference_service_client import InferenceServiceClient
from clients.inference_service.dependencies import get_inference_service_client


class TestGetInferenceServiceClient:
    def test_returns_inference_service_client_instance(self):
        client = get_inference_service_client()
        assert isinstance(client, InferenceServiceClient)
