from entities.base_model import BaseModel
from entities.federated_learning_job_model import FederatedLearningJobModel
from entities.federated_learning_job_status_model import FederatedLearningJobStatus


class TestFederatedLearningJobModel:
    def test_tablename(self):
        assert FederatedLearningJobModel.__tablename__ == "federated_learning_jobs"

    def test_inherits_base_model(self):
        assert issubclass(FederatedLearningJobModel, BaseModel)

    def test_column_names(self):
        columns = {col.name for col in FederatedLearningJobModel.__table__.columns}
        assert columns == {"id", "celery_task_id", "status", "created_at"}

    def test_id_is_primary_key(self):
        assert FederatedLearningJobModel.__table__.c["id"].primary_key is True

    def test_celery_task_id_is_unique(self):
        assert FederatedLearningJobModel.__table__.c["celery_task_id"].unique is True

    def test_attribute_assignment(self):
        model = FederatedLearningJobModel()
        model.celery_task_id = "task-abc"
        model.status = FederatedLearningJobStatus.IN_PROGRESS

        assert model.celery_task_id == "task-abc"
        assert model.status == FederatedLearningJobStatus.IN_PROGRESS


class TestEntitiesInit:
    def test_exports_are_importable(self):
        from entities import BaseModel, FederatedLearningJobModel, FederatedLearningJobStatus
        assert BaseModel is not None
        assert FederatedLearningJobModel is not None
        assert FederatedLearningJobStatus is not None

    def test_version(self):
        import entities
        assert entities.__version__ == "1.0.0"

    def test_all_list(self):
        import entities
        assert set(entities.__all__) == {"BaseModel", "FederatedLearningJobModel", "FederatedLearningJobStatus"}
