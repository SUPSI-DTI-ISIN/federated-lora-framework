from schemas.job import FederatedLearningJobStartResponseDTO
from .job_service_interface import JobServiceInterface
from .tasks import start_federated_learning_celery_task, start_federated_learning_simulation_celery_task


class JobService(JobServiceInterface):
    __INSTANCE = None

    def __init__(self, flwr_app_base_path: str, federated_learning_deployment_environment: str, is_federated_learning_simulation_environment: bool):
        self.__flwr_app_base_path = flwr_app_base_path
        self.__federated_learning_deployment_environment = federated_learning_deployment_environment
        self.__is_federated_learning_simulation_environment = is_federated_learning_simulation_environment

    @classmethod
    def get_instance(cls, flwr_app_base_path: str, federated_learning_deployment_environment: str, is_federated_learning_simulation_environment: bool):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(flwr_app_base_path=flwr_app_base_path, federated_learning_deployment_environment=federated_learning_deployment_environment, is_federated_learning_simulation_environment=is_federated_learning_simulation_environment)
        return cls.__INSTANCE


    def start_federated_learning(self) -> FederatedLearningJobStartResponseDTO:
        if self.__is_federated_learning_simulation_environment:
            task = start_federated_learning_simulation_celery_task.delay(
                self.__flwr_app_base_path
            )
        else:
            task = start_federated_learning_celery_task.delay(
                self.__flwr_app_base_path,
                self.__federated_learning_deployment_environment
            )

        return FederatedLearningJobStartResponseDTO(
            job_id=task.id
        )