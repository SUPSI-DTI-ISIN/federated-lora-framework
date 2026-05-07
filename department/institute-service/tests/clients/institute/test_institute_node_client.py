import pytest
import requests as req
from unittest.mock import patch, MagicMock

from clients.institute.institute_node_client import InstituteNodeClient
from schemas.exceptions.institute_errors import InstituteUnreachableError


@pytest.fixture(autouse=True)
def reset_singleton():
    InstituteNodeClient._InstituteNodeClient__INSTANCE = None
    yield
    InstituteNodeClient._InstituteNodeClient__INSTANCE = None


class TestInstituteNodeClientSingleton:
    def test_get_instance_returns_same_object(self):
        a = InstituteNodeClient.get_instance()
        b = InstituteNodeClient.get_instance()
        assert a is b

    def test_get_instance_returns_institute_node_client(self):
        assert isinstance(InstituteNodeClient.get_instance(), InstituteNodeClient)


class TestGetInstituteTrainingParticipation:
    async def test_success_returns_dto(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "institute_name": "Alpha",
            "trainable_samples_number": 42,
        }
        mock_response.raise_for_status = MagicMock()

        with patch("clients.institute.institute_node_client.requests.get", return_value=mock_response):
            result = await InstituteNodeClient().get_institute_training_participation("http://alpha.local")

        assert result.institute_name == "Alpha"
        assert result.trainable_samples_number == 42

    async def test_http_error_raises_unreachable(self):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock(side_effect=req.exceptions.HTTPError("404"))

        with patch("clients.institute.institute_node_client.requests.get", return_value=mock_response):
            with pytest.raises(InstituteUnreachableError):
                await InstituteNodeClient().get_institute_training_participation("http://dead.local")

    async def test_request_exception_raises_unreachable(self):
        with patch(
            "clients.institute.institute_node_client.requests.get",
            side_effect=req.RequestException("timeout"),
        ):
            with pytest.raises(InstituteUnreachableError):
                await InstituteNodeClient().get_institute_training_participation("http://timeout.local")

    async def test_invalid_response_shape_raises_runtime_error(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {"unexpected_key": "value"}
        mock_response.raise_for_status = MagicMock()

        with patch("clients.institute.institute_node_client.requests.get", return_value=mock_response):
            with pytest.raises(RuntimeError, match="Invalid response shape"):
                await InstituteNodeClient().get_institute_training_participation("http://bad-shape.local")

    async def test_url_is_constructed_correctly(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "institute_name": "Beta",
            "trainable_samples_number": 10,
        }
        mock_response.raise_for_status = MagicMock()

        with patch("clients.institute.institute_node_client.requests.get", return_value=mock_response) as mock_get:
            await InstituteNodeClient().get_institute_training_participation("http://beta.local")

        assert mock_get.call_args[0][0] == "http://beta.local/api_data/documents/training-samples"
