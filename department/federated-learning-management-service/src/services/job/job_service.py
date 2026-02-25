from schemas.job import FederatedLearningJobStartResponseDTO
from .job_service_interface import JobServiceInterface
from .tasks.federated_learning_job_celery_task import start_federated_learning_celery_task


class JobService(JobServiceInterface):
    __INSTANCE = None

    def __init__(self, flwr_app_path: str, federated_learning_deployment_environment: str):
        self.__flwr_app_path = flwr_app_path
        self.__federated_learning_deployment_environment = federated_learning_deployment_environment

    @classmethod
    def get_instance(cls, flwr_app_path: str, federated_learning_deployment_environment: str):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(flwr_app_path=flwr_app_path, federated_learning_deployment_environment=federated_learning_deployment_environment)
        return cls.__INSTANCE


    def start_federated_learning(self) -> FederatedLearningJobStartResponseDTO:
        task = start_federated_learning_celery_task.delay(
            self.__flwr_app_path,
            self.__federated_learning_deployment_environment
        )
        return FederatedLearningJobStartResponseDTO(
            job_id=task.id
        )