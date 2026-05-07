import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestStartFederatedLearningCeleryTask:
    def test_raises_when_base_path_does_not_exist(self, tmp_path):
        from services.celery.tasks.federated_learning_job_celery_task import (
            start_federated_learning_celery_task,
        )
        fake_self = MagicMock()
        fake_self.request.id = "t"

        with pytest.raises(FileNotFoundError, match="does not exist"):
            start_federated_learning_celery_task(
                fake_self,
                flwr_app_base_path=str(tmp_path / "nonexistent"),
                federated_learning_deployment_environment="local",
            )

    def test_raises_when_no_subdirectory_found(self, tmp_path):
        from services.celery.tasks.federated_learning_job_celery_task import (
            start_federated_learning_celery_task,
        )
        fake_self = MagicMock()
        fake_self.request.id = "t"

        with pytest.raises(FileNotFoundError, match="No app directory"):
            start_federated_learning_celery_task(
                fake_self,
                flwr_app_base_path=str(tmp_path),
                federated_learning_deployment_environment="local",
            )

    def test_raises_when_multiple_subdirectories_found(self, tmp_path):
        from services.celery.tasks.federated_learning_job_celery_task import (
            start_federated_learning_celery_task,
        )
        (tmp_path / "app1").mkdir()
        (tmp_path / "app2").mkdir()
        fake_self = MagicMock()
        fake_self.request.id = "t"

        with pytest.raises(RuntimeError, match="Expected exactly one"):
            start_federated_learning_celery_task(
                fake_self,
                flwr_app_base_path=str(tmp_path),
                federated_learning_deployment_environment="local",
            )

    def test_raises_when_subprocess_returns_nonzero(self, tmp_path):
        from services.celery.tasks.federated_learning_job_celery_task import (
            start_federated_learning_celery_task,
        )
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()
        fake_self = MagicMock()
        fake_self.request.id = "t"

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "error output"

        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(RuntimeError, match="FL run failed"):
                start_federated_learning_celery_task(
                    fake_self,
                    flwr_app_base_path=str(tmp_path),
                    federated_learning_deployment_environment="local",
                )

    def test_returns_stdout_on_success(self, tmp_path):
        from services.celery.tasks.federated_learning_job_celery_task import (
            start_federated_learning_celery_task,
        )
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()
        fake_self = MagicMock()
        fake_self.request.id = "t"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "FL completed"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            result = start_federated_learning_celery_task(
                fake_self,
                flwr_app_base_path=str(tmp_path),
                federated_learning_deployment_environment="local",
            )

        assert result == "FL completed"


class TestStartFederatedLearningSimulationCeleryTask:
    def test_raises_when_app_path_does_not_exist(self, tmp_path):
        from services.celery.tasks.federated_learning_simulation_job_celery_task import (
            start_federated_learning_simulation_celery_task,
        )
        fake_self = MagicMock()
        fake_self.request.id = "t"

        with pytest.raises(FileNotFoundError, match="does not exist"):
            start_federated_learning_simulation_celery_task(
                fake_self, flwr_app_path=str(tmp_path / "nonexistent")
            )

    def test_raises_when_simulation_script_missing(self, tmp_path):
        from services.celery.tasks.federated_learning_simulation_job_celery_task import (
            start_federated_learning_simulation_celery_task,
        )
        (tmp_path / "scripts").mkdir()
        fake_self = MagicMock()
        fake_self.request.id = "t"

        with pytest.raises(FileNotFoundError, match="Simulation script not found"):
            start_federated_learning_simulation_celery_task(
                fake_self, flwr_app_path=str(tmp_path)
            )

    def test_raises_when_venv_missing(self, tmp_path):
        from services.celery.tasks.federated_learning_simulation_job_celery_task import (
            start_federated_learning_simulation_celery_task,
        )
        scripts = tmp_path / "scripts"
        scripts.mkdir()
        (scripts / "run_simulation.sh").write_text("#!/bin/bash")
        fake_self = MagicMock()
        fake_self.request.id = "t"

        with pytest.raises(FileNotFoundError, match="Virtual environment not found"):
            start_federated_learning_simulation_celery_task(
                fake_self, flwr_app_path=str(tmp_path)
            )

    def test_raises_when_subprocess_returns_nonzero(self, tmp_path):
        from services.celery.tasks.federated_learning_simulation_job_celery_task import (
            start_federated_learning_simulation_celery_task,
        )
        scripts = tmp_path / "scripts"
        scripts.mkdir()
        (scripts / "run_simulation.sh").write_text("#!/bin/bash")
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "python").write_text("")
        fake_self = MagicMock()
        fake_self.request.id = "t"

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "sim error"
        mock_result.stdout = ""

        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(RuntimeError, match="FL simulation failed"):
                start_federated_learning_simulation_celery_task(
                    fake_self, flwr_app_path=str(tmp_path)
                )

    def test_returns_stdout_on_success(self, tmp_path):
        from services.celery.tasks.federated_learning_simulation_job_celery_task import (
            start_federated_learning_simulation_celery_task,
        )
        scripts = tmp_path / "scripts"
        scripts.mkdir()
        (scripts / "run_simulation.sh").write_text("#!/bin/bash")
        venv_bin = tmp_path / ".venv" / "bin"
        venv_bin.mkdir(parents=True)
        (venv_bin / "python").write_text("")
        fake_self = MagicMock()
        fake_self.request.id = "t"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Simulation done"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            result = start_federated_learning_simulation_celery_task(
                fake_self, flwr_app_path=str(tmp_path)
            )

        assert result == "Simulation done"
