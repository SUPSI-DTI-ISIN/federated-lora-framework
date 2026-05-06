import pytest
from unittest.mock import MagicMock
from clients.mlflow.mlflow_service_client import MlFlowServiceClient
from services.utils.init_model_downloader_service import InitModelDownloaderService
from services.utils.dependencies import build_init_model_downloader_service


@pytest.fixture(autouse=True)
def reset_singletons():
    InitModelDownloaderService._INSTANCE = None
    MlFlowServiceClient._MlFlowServiceClient__INSTANCE = None
    yield
    InitModelDownloaderService._INSTANCE = None
    MlFlowServiceClient._MlFlowServiceClient__INSTANCE = None


class TestBuildInitModelDownloaderService:
    def test_returns_init_model_downloader_service_instance(self):
        mock_client = MagicMock()
        svc = build_init_model_downloader_service(mlflow_service_client=mock_client)
        assert isinstance(svc, InitModelDownloaderService)
