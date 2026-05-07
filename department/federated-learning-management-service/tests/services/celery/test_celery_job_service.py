import pytest
from unittest.mock import MagicMock, patch

from services.celery.celery_job_service import CeleryJobService


@pytest.fixture(autouse=True)
def reset_singleton():
    CeleryJobService._CeleryJobService__INSTANCE = None
    yield
    CeleryJobService._CeleryJobService__INSTANCE = None


@pytest.fixture()
def service():
    return CeleryJobService.get_instance(
        flwr_app_base_path="/tmp/flwr",
        federated_learning_deployment_environment="local-simulation",
        is_federated_learning_simulation_environment=False,
    )


@pytest.fixture()
def simulation_service():
    return CeleryJobService.get_instance(
        flwr_app_base_path="/tmp/flwr",
        federated_learning_deployment_environment="local-simulation",
        is_federated_learning_simulation_environment=True,
    )


class TestGetInstance:
    def test_returns_same_object_on_repeated_calls(self):
        a = CeleryJobService.get_instance(
            flwr_app_base_path="/tmp/flwr",
            federated_learning_deployment_environment="local",
            is_federated_learning_simulation_environment=False,
        )
        b = CeleryJobService.get_instance(
            flwr_app_base_path="/tmp/flwr",
            federated_learning_deployment_environment="local",
            is_federated_learning_simulation_environment=False,
        )
        assert a is b

    def test_returns_non_none_instance(self):
        assert CeleryJobService.get_instance(
            flwr_app_base_path="/tmp/flwr",
            federated_learning_deployment_environment="local",
            is_federated_learning_simulation_environment=False,
        ) is not None


class TestStartFederatedLearning:
    def test_returns_task_id_for_real_environment(self, service):
        mock_task = MagicMock()
        mock_task.id = "task-real-123"
        mock_real_task = MagicMock()
        mock_real_task.delay = MagicMock(return_value=mock_task)

        with patch("services.celery.celery_job_service.start_federated_learning_celery_task", mock_real_task):
            result = service.start_federated_learning()

        assert result == "task-real-123"

    def test_calls_real_task_with_correct_args(self, service):
        mock_task = MagicMock()
        mock_task.id = "t"
        mock_real_task = MagicMock()
        mock_real_task.delay = MagicMock(return_value=mock_task)

        with patch("services.celery.celery_job_service.start_federated_learning_celery_task", mock_real_task):
            service.start_federated_learning()

        mock_real_task.delay.assert_called_once_with("/tmp/flwr", "local-simulation")

    def test_returns_task_id_for_simulation_environment(self, simulation_service):
        mock_task = MagicMock()
        mock_task.id = "task-sim-456"
        mock_sim_task = MagicMock()
        mock_sim_task.delay = MagicMock(return_value=mock_task)

        with patch("services.celery.celery_job_service.start_federated_learning_simulation_celery_task", mock_sim_task):
            result = simulation_service.start_federated_learning()

        assert result == "task-sim-456"

    def test_calls_simulation_task_with_correct_args(self, simulation_service):
        mock_task = MagicMock()
        mock_task.id = "t"
        mock_sim_task = MagicMock()
        mock_sim_task.delay = MagicMock(return_value=mock_task)

        with patch("services.celery.celery_job_service.start_federated_learning_simulation_celery_task", mock_sim_task):
            simulation_service.start_federated_learning()

        mock_sim_task.delay.assert_called_once_with("/tmp/flwr")
