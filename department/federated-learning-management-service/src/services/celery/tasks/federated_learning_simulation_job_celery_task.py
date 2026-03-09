import os
import subprocess

from pathlib import Path
from celery.utils.log import get_task_logger

from clients.celery import celery

logger = get_task_logger(__name__)

@celery.task(bind=True)
def start_federated_learning_simulation_celery_task(self, flwr_app_path: str):
    task_id = self.request.id
    logger.info("Starting FL simulation task %s", task_id)

    app_path = Path(flwr_app_path).resolve()

    if not app_path.exists():
        raise FileNotFoundError(f"FLWR_APP_PATH does not exist: {app_path}")

    scripts_path = app_path / "scripts"
    simulation_script = scripts_path / "run_simulation.sh"

    if not simulation_script.exists():
        raise FileNotFoundError(f"Simulation script not found: {simulation_script}")

    venv_python = app_path / ".venv" / "bin" / "python"
    if not venv_python.exists():
        raise FileNotFoundError(
            f"Virtual environment not found in FL app directory: {venv_python}. "
            "Run 'python -m venv .venv && .venv/bin/pip install -e .' inside the FL service."
        )

    fl_venv = str(app_path / ".venv")
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = fl_venv
    env["PATH"] = f"{fl_venv}/bin:{os.environ.get('PATH', '')}"

    env.pop("PYTHONHOME", None)

    logger.info("Using FL venv: %s", fl_venv)
    logger.info("Running simulation script: %s", simulation_script)

    result = subprocess.run(
        ["bash", str(simulation_script)],
        cwd=str(scripts_path),
        env=env,
        capture_output=True,
        text=True,
    )

    logger.info("Process finished with return code %s", result.returncode)

    if result.returncode != 0:
        logger.error("Simulation stderr: %s", result.stderr)
        raise RuntimeError(
            f"FL simulation failed (exit {result.returncode}):\n{result.stderr}"
        )

    logger.info("Simulation stdout: %s", result.stdout)
    return result.stdout