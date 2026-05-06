import pytest
from unittest.mock import MagicMock, patch

from schemas.inference import QueryRequestDTO, ConversationDTO
from services.inference.inference_service import InferenceService


@pytest.fixture(autouse=True)
def reset_singleton():
    InferenceService._InferenceService__INSTANCE = None
    yield
    InferenceService._InferenceService__INSTANCE = None


def _make_request(**kwargs):
    defaults = dict(
        user_id="u-1", chat_id=1, model_key="llama-3",
        adapter_version=None, prompt="Hello", conversation_history=[],
    )
    defaults.update(kwargs)
    return QueryRequestDTO(**defaults)


class TestGetInstance:
    def test_returns_same_instance(self):
        i1 = InferenceService.get_instance()
        i2 = InferenceService.get_instance()
        assert i1 is i2

    def test_creates_new_instance_after_reset(self):
        i1 = InferenceService.get_instance()
        InferenceService._InferenceService__INSTANCE = None
        i2 = InferenceService.get_instance()
        assert i1 is not i2


class TestInferenceModel:
    async def test_returns_task_id(self):
        service = InferenceService()
        mock_task = MagicMock()
        mock_task.id = "task-abc-123"

        mock_celery_task = MagicMock()
        mock_celery_task.delay.return_value = mock_task

        with patch(
            "services.inference.inference_service.inference_celery_task",
            mock_celery_task,
        ):
            result = await service.inference_model(query_request_dto=_make_request())

        assert result == "task-abc-123"

    async def test_calls_delay_with_serialized_dto(self):
        service = InferenceService()
        mock_task = MagicMock()
        mock_task.id = "task-xyz"
        request = _make_request(prompt="What is ML?")

        mock_celery_task = MagicMock()
        mock_celery_task.delay.return_value = mock_task

        with patch(
            "services.inference.inference_service.inference_celery_task",
            mock_celery_task,
        ):
            await service.inference_model(query_request_dto=request)

        mock_celery_task.delay.assert_called_once()
        call_kwargs = mock_celery_task.delay.call_args.kwargs
        assert "query_request_dto" in call_kwargs
        assert "What is ML?" in call_kwargs["query_request_dto"]

    async def test_passes_adapter_version_in_serialized_dto(self):
        service = InferenceService()
        mock_task = MagicMock()
        mock_task.id = "task-1"
        request = _make_request(adapter_version=3)

        mock_celery_task = MagicMock()
        mock_celery_task.delay.return_value = mock_task

        with patch(
            "services.inference.inference_service.inference_celery_task",
            mock_celery_task,
        ):
            await service.inference_model(query_request_dto=request)

        serialized = mock_celery_task.delay.call_args.kwargs["query_request_dto"]
        assert "3" in serialized


class TestInferenceServiceInit:
    def test_exports(self):
        import services.inference as si
        assert "InferenceServiceInterface" in si.__all__
        assert "get_inference_service" in si.__all__

    def test_version(self):
        import services.inference as si
        assert si.__version__ == "1.0.0"
