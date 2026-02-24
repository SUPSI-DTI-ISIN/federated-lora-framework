from schemas.job import FederatedLearningJobStartResponseDTO
from .job_service_interface import JobServiceInterface
from .tasks.federated_learning_job_celery_task import start_federated_learning_celery_task


class JobService(JobServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE


    def start_federated_learning(self) -> FederatedLearningJobStartResponseDTO:
        task = start_federated_learning_celery_task.delay()
        return FederatedLearningJobStartResponseDTO(
            job_id=task.id
        )