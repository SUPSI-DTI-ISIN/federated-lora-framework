import pytest
from unittest.mock import patch, MagicMock

from src.federated_learning_client.clients.data_service.data_service_client import DataServiceClient
from src.federated_learning_client.clients.schemas import DocumentDTO, SectionDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    DataServiceClient._INSTANCE = None
    yield
    DataServiceClient._INSTANCE = None


def _doc_data():
    return [{"id": 1, "number": "DOC-001", "title": "My Project",
             "is_externally_approved": False,
             "sections": [{"id": 1, "title": "1. Intro", "content": "Content"}]}]


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = DataServiceClient.get_instance(data_service_url="http://data:8080")
        i2 = DataServiceClient.get_instance(data_service_url="http://data:8080")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = DataServiceClient.get_instance(data_service_url="http://data:8080")
        DataServiceClient._INSTANCE = None
        i2 = DataServiceClient.get_instance(data_service_url="http://data:8080")
        assert i1 is not i2


class TestGetDocuments:
    def _client(self):
        return DataServiceClient(data_service_url="http://data:8080")

    def test_returns_list_of_document_dtos(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = _doc_data()

        with patch("src.federated_learning_client.clients.data_service.data_service_client.requests.get",
                   return_value=mock_resp):
            result = self._client().get_documents()

        assert len(result) == 1
        assert isinstance(result[0], DocumentDTO)
        assert result[0].number == "DOC-001"

    def test_returns_empty_list(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = []

        with patch("src.federated_learning_client.clients.data_service.data_service_client.requests.get",
                   return_value=mock_resp):
            result = self._client().get_documents()

        assert result == []

    def test_raises_runtime_error_on_http_error(self):
        import requests as req
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = req.exceptions.HTTPError("404")

        with patch("src.federated_learning_client.clients.data_service.data_service_client.requests.get",
                   return_value=mock_resp):
            with pytest.raises(RuntimeError):
                self._client().get_documents()

    def test_raises_runtime_error_on_invalid_response(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = [{"bad": "shape"}]

        with patch("src.federated_learning_client.clients.data_service.data_service_client.requests.get",
                   return_value=mock_resp):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                self._client().get_documents()

    def test_url_contains_trainable_endpoint(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = []

        with patch("src.federated_learning_client.clients.data_service.data_service_client.requests.get",
                   return_value=mock_resp) as mock_get:
            self._client().get_documents()

        url = mock_get.call_args[0][0]
        assert "trainable" in url
        assert "api_data" in url
