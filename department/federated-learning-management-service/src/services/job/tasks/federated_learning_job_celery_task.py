import subprocess
import sys

from pathlib import Path
from celery.utils.log import get_task_logger

from clients.celery import celery

logger = get_task_logger(__name__)

@celery.task(bind=True)
def start_federated_learning_celery_task(self, flwr_app_path: str, federated_learning_deployment_environment: str):
    print(sys.executable)

    task_id = self.request.id
    logger.info("Starting FL task %s", task_id)

    app_path = Path(flwr_app_path).resolve()

    if not app_path.exists():
        raise FileNotFoundError(f"FLWR_APP_PATH does not exist: {app_path}")

    logger.info("Detected Flower app directory: %s", app_path)

    cmd = [
        "flwr",
        "run",
        str(app_path),
        federated_learning_deployment_environment,
        "--stream"
    ]

    logger.info("Running command: %s", " ".join(cmd))

    result = subprocess.run(
        cmd,
        cwd=app_path,
        capture_output=True,
        text=True,
    )

    logger.info("Process finished with return code %s", result.returncode)

    if result.returncode != 0:
        logger.error("FLWR stderr: %s", result.stderr)
        raise RuntimeError(result.stderr)

    logger.info("FLWR stdout: %s", result.stdout)
    return result.stdout