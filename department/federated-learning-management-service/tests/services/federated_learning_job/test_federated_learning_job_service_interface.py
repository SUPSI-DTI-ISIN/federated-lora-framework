import pytest

from services.federated_learning_job.federated_learning_job_service_interface import (
    FederatedLearningJobServiceInterface,
)


class TestFederatedLearningJobServiceInterface:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            FederatedLearningJobServiceInterface()

    def test_complete_subclass_can_be_instantiated(self):
        class Concrete(FederatedLearningJobServiceInterface):
            async def create_federated_learning_job(self, celery_task_id): ...
            async def get_all_federated_learning_jobs(self): ...
            async def ensure_no_job_in_progress(self): ...
            async def update_job_status_from_celery(self, celery_job_dto): ...

        assert isinstance(Concrete(), FederatedLearningJobServiceInterface)

    async def test_abstract_methods_raise_not_implemented(self):
        class CallerThrough(FederatedLearningJobServiceInterface):
            async def create_federated_learning_job(self, celery_task_id):
                return await super().create_federated_learning_job(celery_task_id)

            async def get_all_federated_learning_jobs(self):
                return await super().get_all_federated_learning_jobs()

            async def ensure_no_job_in_progress(self):
                return await super().ensure_no_job_in_progress()

            async def update_job_status_from_celery(self, celery_job_dto):
                return await super().update_job_status_from_celery(celery_job_dto)

        obj = CallerThrough()

        with pytest.raises(NotImplementedError):
            await obj.create_federated_learning_job("t")
        with pytest.raises(NotImplementedError):
            await obj.get_all_federated_learning_jobs()
        with pytest.raises(NotImplementedError):
            await obj.ensure_no_job_in_progress()
        with pytest.raises(NotImplementedError):
            await obj.update_job_status_from_celery(None)
