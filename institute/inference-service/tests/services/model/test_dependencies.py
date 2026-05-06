import pytest
from unittest.mock import MagicMock
from services.model.model_service import ModelService
from services.model.dependencies import build_model_service


@pytest.fixture(autouse=True)
def reset_singleton():
    ModelService._ModelService__INSTANCE = None
    yield
    ModelService._ModelService__INSTANCE = None


class TestBuildModelService:
    def test_returns_model_service_instance(self):
        mock_client = MagicMock()
        svc = build_model_service(
            max_cached_adapters=3,
            device_map="cpu",
            model_service_client=mock_client,
        )
        assert isinstance(svc, ModelService)
