import pytest
from unittest.mock import MagicMock, patch

from schemas.celery import CeleryJobResultType, CeleryJobDTO
from schemas.inference import QueryResponseDTO, QueryRequestDTO


class TestInferenceCeleryTaskSuccessSignal:
    def test_publishes_success_payload_to_redis(self):
        from services.inference.signals.inference_celery_signals import (
            inference_celery_task_success_signal,
        )

        response_dto = QueryResponseDTO(
            user_id="u-1", chat_id=1, prompt="Hello",
            response="Hi", model_key="llama-3", adapter_version=None,
        )
        result_json = response_dto.model_dump_json()

        mock_sender = MagicMock()
        mock_sender.request.id = "task-abc"

        mock_redis = MagicMock()

        with patch(
            "services.inference.signals.inference_celery_signals.get_redis_client_sync",
            return_value=mock_redis,
        ):
            inference_celery_task_success_signal(
                sender=mock_sender, result=result_json
            )

        mock_redis.publish.assert_called_once()
        channel, payload = mock_redis.publish.call_args[0]
        assert "u-1" in channel
        assert "inference:result" in channel

        published = CeleryJobDTO.model_validate_json(payload)
        assert published.result_type == CeleryJobResultType.SUCCESS
        assert published.job_id == "task-abc"
        assert published.chat_id == 1

    def test_publishes_to_correct_channel(self):
        from services.inference.signals.inference_celery_signals import (
            inference_celery_task_success_signal,
        )

        response_dto = QueryResponseDTO(
            user_id="user-xyz", chat_id=5, prompt="p",
            response="r", model_key="k", adapter_version=2,
        )

        mock_sender = MagicMock()
        mock_sender.request.id = "task-1"
        mock_redis = MagicMock()

        with patch(
            "services.inference.signals.inference_celery_signals.get_redis_client_sync",
            return_value=mock_redis,
        ):
            inference_celery_task_success_signal(
                sender=mock_sender, result=response_dto.model_dump_json()
            )

        channel = mock_redis.publish.call_args[0][0]
        assert "user-xyz" in channel


class TestInferenceCeleryTaskFailureSignal:
    def _make_request_json(self, **kwargs):
        defaults = dict(
            user_id="u-1", chat_id=1, model_key="llama-3",
            adapter_version=None, prompt="Hello", conversation_history=[],
        )
        defaults.update(kwargs)
        return QueryRequestDTO(**defaults).model_dump_json()

    def test_publishes_failure_payload_to_redis(self):
        from services.inference.signals.inference_celery_signals import (
            inference_celery_task_failure_signal,
        )

        mock_sender = MagicMock()
        mock_redis = MagicMock()

        with patch(
            "services.inference.signals.inference_celery_signals.get_redis_client_sync",
            return_value=mock_redis,
        ):
            inference_celery_task_failure_signal(
                sender=mock_sender,
                task_id="task-fail-1",
                exception=RuntimeError("model crashed"),
                args=[],
                kwargs={"query_request_dto": self._make_request_json()},
                traceback=None,
                einfo=None,
            )

        mock_redis.publish.assert_called_once()
        channel, payload = mock_redis.publish.call_args[0]
        assert "u-1" in channel

        published = CeleryJobDTO.model_validate_json(payload)
        assert published.result_type == CeleryJobResultType.FAILURE
        assert published.job_id == "task-fail-1"
        assert "model crashed" in published.error

    def test_publishes_to_correct_channel_on_failure(self):
        from services.inference.signals.inference_celery_signals import (
            inference_celery_task_failure_signal,
        )

        mock_sender = MagicMock()
        mock_redis = MagicMock()

        with patch(
            "services.inference.signals.inference_celery_signals.get_redis_client_sync",
            return_value=mock_redis,
        ):
            inference_celery_task_failure_signal(
                sender=mock_sender,
                task_id="task-2",
                exception=ValueError("bad input"),
                args=[],
                kwargs={"query_request_dto": self._make_request_json(user_id="user-abc", chat_id=7)},
                traceback=None,
                einfo=None,
            )

        channel = mock_redis.publish.call_args[0][0]
        assert "user-abc" in channel


class TestSignalsInit:
    def test_exports_success_signal(self):
        import services.inference.signals as sis
        assert "inference_celery_task_success_signal" in sis.__all__

    def test_exports_failure_signal(self):
        import services.inference.signals as sis
        assert "inference_celery_task_failure_signal" in sis.__all__

    def test_version(self):
        import services.inference.signals as sis
        assert sis.__version__ == "1.0.0"
