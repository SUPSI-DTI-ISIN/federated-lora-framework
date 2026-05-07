import pytest
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError

from schemas.federated_learning_job.federated_learning_job_dto import FederatedLearningJobDTO


class TestFederatedLearningJobDTO:
    def _make_dto(self, **kwargs):
        defaults = dict(
            id=1,
            celery_task_id="task-abc",
            status="in_progress",
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        defaults.update(kwargs)
        return FederatedLearningJobDTO(**defaults)

    def test_fields_are_set_correctly(self):
        dto = self._make_dto()
        assert dto.id == 1
        assert dto.celery_task_id == "task-abc"
        assert dto.status == "in_progress"

    def test_is_pydantic_model(self):
        assert issubclass(FederatedLearningJobDTO, BaseModel)

    def test_serialization(self):
        dto = self._make_dto(id=5, celery_task_id="t-5", status="success")
        data = dto.model_dump()
        assert data["id"] == 5
        assert data["celery_task_id"] == "t-5"
        assert data["status"] == "success"

    def test_model_validate_from_orm_object(self):
        class FakeOrm:
            id = 7
            celery_task_id = "task-orm"
            status = "failure"
            created_at = datetime(2024, 6, 1, tzinfo=timezone.utc)

        dto = FederatedLearningJobDTO.model_validate(FakeOrm())
        assert dto.id == 7
        assert dto.celery_task_id == "task-orm"
        assert dto.status == "failure"

    @pytest.mark.parametrize("missing_field", ["id", "celery_task_id", "status", "created_at"])
    def test_missing_required_field_raises(self, missing_field):
        data = dict(
            id=1,
            celery_task_id="t",
            status="in_progress",
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        del data[missing_field]
        with pytest.raises(ValidationError):
            FederatedLearningJobDTO(**data)


class TestFederatedLearningJobDTOInit:
    def test_exported_from_package(self):
        from schemas.federated_learning_job import FederatedLearningJobDTO as D
        assert D is FederatedLearningJobDTO

    def test_version(self):
        import schemas.federated_learning_job as f
        assert f.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.federated_learning_job as f
        assert "FederatedLearningJobDTO" in f.__all__
