import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from clients.inference_service.inference_service_client import InferenceServiceClient
from clients.schemas import QueryRequestDTO
from schemas.chat import ConversationDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    InferenceServiceClient._InferenceServiceClient__INSTANCE = None
    yield
    InferenceServiceClient._InferenceServiceClient__INSTANCE = None


def _make_request():
    return QueryRequestDTO(
        user_id="u-1",
        chat_id=1,
        model_key="model-v1",
        adapter_version=1,
        prompt="Hello",
        conversation_history=[],
    )


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = InferenceServiceClient.get_instance(inference_service_url="http://inference:8095")
        i2 = InferenceServiceClient.get_instance(inference_service_url="http://inference:8095")
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = InferenceServiceClient.get_instance(inference_service_url="http://inference:8095")
        InferenceServiceClient._InferenceServiceClient__INSTANCE = None
        i2 = InferenceServiceClient.get_instance(inference_service_url="http://inference:8095")
        assert i1 is not i2


class TestInferenceModel:
    async def test_calls_post_and_raises_for_status(self):
        client = InferenceServiceClient(inference_service_url="http://inference:8095")
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()

        mock_http_client = AsyncMock()
        mock_http_client.post = AsyncMock(return_value=mock_resp)

        mock_ctx = AsyncMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)

        with patch("clients.inference_service.inference_service_client.httpx.AsyncClient", return_value=mock_ctx):
            await client.inference_model(query_request_dto=_make_request())

        mock_http_client.post.assert_awaited_once()
        call_kwargs = mock_http_client.post.call_args
        assert "api_inference/inference" in call_kwargs.args[0]
        mock_resp.raise_for_status.assert_called_once()

    async def test_raises_runtime_error_on_http_error(self):
        import requests
        client = InferenceServiceClient(inference_service_url="http://inference:8095")

        mock_http_client = AsyncMock()
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock(
            side_effect=requests.exceptions.HTTPError("404 Not Found")
        )
        mock_http_client.post = AsyncMock(return_value=mock_resp)

        mock_ctx = AsyncMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_http_client)
        mock_ctx.__aexit__ = AsyncMock(return_value=False)

        with patch("clients.inference_service.inference_service_client.httpx.AsyncClient", return_value=mock_ctx):
            with pytest.raises(RuntimeError):
                await client.inference_model(query_request_dto=_make_request())
