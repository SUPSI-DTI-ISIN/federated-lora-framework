from unittest.mock import MagicMock, patch

from schemas.celery import CeleryJobResultType


class TestFederatedLearningCelerySignals:
    def test_success_signal_publishes_to_redis(self):
        mock_redis = MagicMock()
        mock_sender = MagicMock()
        mock_sender.request.id = "task-success-1"

        with patch("services.celery.signals.federated_learning_job_celery_signals.get_redis_client_sync", return_value=mock_redis):
            from services.celery.signals.federated_learning_job_celery_signals import (
                federated_learning_celery_job_success_signal,
            )
            federated_learning_celery_job_success_signal(sender=mock_sender, result="output")

        mock_redis.publish.assert_called_once()
        channel, payload = mock_redis.publish.call_args[0]
        assert channel == "job_updates"
        assert "task-success-1" in payload
        assert CeleryJobResultType.SUCCESS.value in payload

    def test_failure_signal_publishes_to_redis(self):
        mock_redis = MagicMock()

        with patch("services.celery.signals.federated_learning_job_celery_signals.get_redis_client_sync", return_value=mock_redis):
            from services.celery.signals.federated_learning_job_celery_signals import (
                federated_learning_celery_job_failure_signal,
            )
            federated_learning_celery_job_failure_signal(
                sender=MagicMock(),
                task_id="task-fail-2",
                exception=RuntimeError("boom"),
                args=[], kwargs={}, traceback=None, einfo=None,
            )

        mock_redis.publish.assert_called_once()
        channel, payload = mock_redis.publish.call_args[0]
        assert channel == "job_updates"
        assert "task-fail-2" in payload
        assert CeleryJobResultType.FAILURE.value in payload

    def test_signals_init_exports(self):
        import services.celery.signals.federated_learning_job_celery_signals as m
        assert hasattr(m, "federated_learning_celery_job_success_signal")
        assert hasattr(m, "federated_learning_celery_job_failure_signal")
