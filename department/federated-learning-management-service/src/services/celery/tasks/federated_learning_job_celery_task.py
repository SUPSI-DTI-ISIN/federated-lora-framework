import subprocess

from pathlib import Path
from celery.utils.log import get_task_logger

from clients.celery import celery

logger = get_task_logger(__name__)

@celery.task(bind=True)
def start_federated_learning_celery_task(self, flwr_app_base_path: str, federated_learning_deployment_environment: str):
    task_id = self.request.id
    logger.info("Starting FL task %s", task_id)

    base_path = Path(flwr_app_base_path).resolve()

    if not base_path.exists():
        raise FileNotFoundError(f"FLWR_APP_BASE_PATH does not exist: {base_path}")

    subdirs = [p for p in base_path.iterdir() if p.is_dir()]

    if len(subdirs) == 0:
        raise FileNotFoundError(f"No app directory found inside: {base_path}")

    if len(subdirs) > 1:
        raise RuntimeError(
            f"Expected exactly one app directory inside {base_path}, "
            f"found {len(subdirs)}: {[str(s) for s in subdirs]}"
        )

    app_path = subdirs[0]
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
        cwd=str(app_path),
        capture_output=True,
        text=True,
    )

    logger.info("Return code: %s", result.returncode)
    logger.info("STDOUT: %r", result.stdout)
    logger.info("STDERR: %r", result.stderr)

    logger.info("Process finished with return code %s", result.returncode)

    if result.returncode != 0 or result.stderr.strip():
        logger.error("FLWR stderr: %s", result.stderr)
        raise RuntimeError(
            f"FL run failed (exit {result.returncode}):\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    logger.info("FLWR stdout: %s", result.stdout)
    return result.stdout