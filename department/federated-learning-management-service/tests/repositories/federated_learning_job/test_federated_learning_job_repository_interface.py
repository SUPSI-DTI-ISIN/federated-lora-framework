import pytest

from repositories.federated_learning_job.federated_learning_job_repository_interface import (
    FederatedLearningJobRepositoryInterface,
)


class TestFederatedLearningJobRepositoryInterface:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            FederatedLearningJobRepositoryInterface()

    def test_incomplete_subclass_cannot_be_instantiated(self):
        class Incomplete(FederatedLearningJobRepositoryInterface):
            pass

        with pytest.raises(TypeError):
            Incomplete()

    def test_complete_subclass_can_be_instantiated(self):
        class Concrete(FederatedLearningJobRepositoryInterface):
            async def save(self, federated_learning_job_model): ...
            async def get_all(self): ...
            async def get_by_status(self, status): ...
            async def get_by_celery_task_id(self, celery_task_id): ...

        assert isinstance(Concrete(), FederatedLearningJobRepositoryInterface)

    async def test_abstract_methods_raise_not_implemented(self):
        class CallerThrough(FederatedLearningJobRepositoryInterface):
            async def save(self, federated_learning_job_model):
                return await super().save(federated_learning_job_model)

            async def get_all(self):
                return await super().get_all()

            async def get_by_status(self, status):
                return await super().get_by_status(status)

            async def get_by_celery_task_id(self, celery_task_id):
                return await super().get_by_celery_task_id(celery_task_id)

        obj = CallerThrough()

        with pytest.raises(NotImplementedError):
            await obj.save(None)
        with pytest.raises(NotImplementedError):
            await obj.get_all()
        with pytest.raises(NotImplementedError):
            await obj.get_by_status(None)
        with pytest.raises(NotImplementedError):
            await obj.get_by_celery_task_id("t")
