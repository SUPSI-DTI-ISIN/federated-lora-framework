import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from schemas.inference import QueryRequestDTO, QueryResponseDTO, ConversationDTO
from schemas.model import LoadedModel


def _make_request(**kwargs):
    defaults = dict(
        user_id="u-1", chat_id=1, model_key="llama-3",
        adapter_version=None, prompt="What is AI?", conversation_history=[],
    )
    defaults.update(kwargs)
    return QueryRequestDTO(**defaults)


def _make_loaded_model(has_adapter=False):
    return LoadedModel(
        model=MagicMock(),
        tokenizer=MagicMock(),
        has_adapter=has_adapter,
        loaded_at=datetime.now(timezone.utc),
    )


class TestInferenceCeleryTask:
    def test_returns_serialized_query_response(self):
        from services.inference.tasks.inference_celery_task import inference_celery_task

        request = _make_request()
        loaded_model = _make_loaded_model(has_adapter=False)

        mock_model_service = MagicMock()
        mock_model_service.get_or_load_model.return_value = loaded_model

        mock_self = MagicMock()
        mock_self.request.id = "task-123"

        with patch(
            "services.inference.tasks.inference_celery_task.build_model_service",
            return_value=mock_model_service,
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.build_chat_prompt_to_tokens_list",
            return_value=[1, 2, 3],
        ), patch(
            "services.inference.tasks.inference_celery_task.ModelResponseUtils.generate_model_response",
            return_value=[4, 5, 6],
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.response_ids_to_str",
            return_value="The answer is 42",
        ):
            result = inference_celery_task(mock_self, query_request_dto=request.model_dump_json())

        response = QueryResponseDTO.model_validate_json(result)
        assert response.user_id == "u-1"
        assert response.chat_id == 1
        assert response.prompt == "What is AI?"
        assert response.response == "The answer is 42"
        assert response.model_key == "llama-3"

    def test_uses_adapter_system_prompt_when_adapter_active(self):
        from services.inference.tasks.inference_celery_task import inference_celery_task

        request = _make_request(adapter_version=2)
        loaded_model = _make_loaded_model(has_adapter=True)

        mock_model_service = MagicMock()
        mock_model_service.get_or_load_model.return_value = loaded_model

        mock_self = MagicMock()
        mock_self.request.id = "task-456"

        with patch(
            "services.inference.tasks.inference_celery_task.build_model_service",
            return_value=mock_model_service,
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.build_chat_prompt_to_tokens_list",
            return_value=[1, 2],
        ) as mock_build_prompt, patch(
            "services.inference.tasks.inference_celery_task.ModelResponseUtils.generate_model_response",
            return_value=[3, 4],
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.response_ids_to_str",
            return_value="response",
        ):
            inference_celery_task(mock_self, query_request_dto=request.model_dump_json())

        call_kwargs = mock_build_prompt.call_args.kwargs
        from config import settings
        assert call_kwargs["system_prompt"] == settings.model_system_prompt_with_adapter_active

    def test_uses_no_adapter_system_prompt_when_no_adapter(self):
        from services.inference.tasks.inference_celery_task import inference_celery_task

        request = _make_request(adapter_version=None)
        loaded_model = _make_loaded_model(has_adapter=False)

        mock_model_service = MagicMock()
        mock_model_service.get_or_load_model.return_value = loaded_model

        mock_self = MagicMock()
        mock_self.request.id = "task-789"

        with patch(
            "services.inference.tasks.inference_celery_task.build_model_service",
            return_value=mock_model_service,
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.build_chat_prompt_to_tokens_list",
            return_value=[1],
        ) as mock_build_prompt, patch(
            "services.inference.tasks.inference_celery_task.ModelResponseUtils.generate_model_response",
            return_value=[2],
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.response_ids_to_str",
            return_value="response",
        ):
            inference_celery_task(mock_self, query_request_dto=request.model_dump_json())

        call_kwargs = mock_build_prompt.call_args.kwargs
        from config import settings
        assert call_kwargs["system_prompt"] == settings.model_system_prompt_without_adapter

    def test_adapter_version_is_none_in_response_when_no_adapter(self):
        from services.inference.tasks.inference_celery_task import inference_celery_task

        request = _make_request(adapter_version=None)
        loaded_model = _make_loaded_model(has_adapter=False)

        mock_model_service = MagicMock()
        mock_model_service.get_or_load_model.return_value = loaded_model

        mock_self = MagicMock()
        mock_self.request.id = "task-no-adapter"

        with patch(
            "services.inference.tasks.inference_celery_task.build_model_service",
            return_value=mock_model_service,
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.build_chat_prompt_to_tokens_list",
            return_value=[1],
        ), patch(
            "services.inference.tasks.inference_celery_task.ModelResponseUtils.generate_model_response",
            return_value=[2],
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.response_ids_to_str",
            return_value="response",
        ):
            result = inference_celery_task(mock_self, query_request_dto=request.model_dump_json())

        response = QueryResponseDTO.model_validate_json(result)
        assert response.adapter_version is None

    def test_adapter_version_preserved_in_response_when_adapter_active(self):
        from services.inference.tasks.inference_celery_task import inference_celery_task

        request = _make_request(adapter_version=5)
        loaded_model = _make_loaded_model(has_adapter=True)

        mock_model_service = MagicMock()
        mock_model_service.get_or_load_model.return_value = loaded_model

        mock_self = MagicMock()
        mock_self.request.id = "task-with-adapter"

        with patch(
            "services.inference.tasks.inference_celery_task.build_model_service",
            return_value=mock_model_service,
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.build_chat_prompt_to_tokens_list",
            return_value=[1],
        ), patch(
            "services.inference.tasks.inference_celery_task.ModelResponseUtils.generate_model_response",
            return_value=[2],
        ), patch(
            "services.inference.tasks.inference_celery_task.TokenizerUtils.response_ids_to_str",
            return_value="response",
        ):
            result = inference_celery_task(mock_self, query_request_dto=request.model_dump_json())

        response = QueryResponseDTO.model_validate_json(result)
        assert response.adapter_version == 5


class TestTasksInit:
    def test_exports_inference_celery_task(self):
        import services.inference.tasks as sit
        assert "inference_celery_task" in sit.__all__

    def test_version(self):
        import services.inference.tasks as sit
        assert sit.__version__ == "1.0.0"
