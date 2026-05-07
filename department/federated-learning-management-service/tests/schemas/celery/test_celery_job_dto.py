import pytest
from pydantic import BaseModel, ValidationError

from schemas.celery.celery_job_dto import CeleryJobDTO
from schemas.celery.celery_job_result_type import CeleryJobResultType


class TestCeleryJobDTO:
    def test_fields_are_set_correctly(self):
        dto = CeleryJobDTO(job_id="task-1", result_type=CeleryJobResultType.SUCCESS)
        assert dto.job_id == "task-1"
        assert dto.result_type == CeleryJobResultType.SUCCESS
        assert dto.result is None
        assert dto.error is None

    def test_result_field_is_optional(self):
        dto = CeleryJobDTO(job_id="t", result_type=CeleryJobResultType.SUCCESS, result="output")
        assert dto.result == "output"

    def test_error_field_is_optional(self):
        dto = CeleryJobDTO(job_id="t", result_type=CeleryJobResultType.FAILURE, error="boom")
        assert dto.error == "boom"

    def test_is_pydantic_model(self):
        assert issubclass(CeleryJobDTO, BaseModel)

    def test_serialization(self):
        dto = CeleryJobDTO(job_id="t", result_type=CeleryJobResultType.SUCCESS)
        data = dto.model_dump()
        assert data["job_id"] == "t"
        assert data["result"] is None
        assert data["error"] is None

    def test_json_round_trip(self):
        dto = CeleryJobDTO(job_id="t", result_type=CeleryJobResultType.FAILURE, error="err")
        restored = CeleryJobDTO.model_validate_json(dto.model_dump_json())
        assert restored.job_id == "t"
        assert restored.result_type == CeleryJobResultType.FAILURE
        assert restored.error == "err"

    @pytest.mark.parametrize("missing_field", ["job_id", "result_type"])
    def test_missing_required_field_raises(self, missing_field):
        data = {"job_id": "t", "result_type": CeleryJobResultType.SUCCESS}
        del data[missing_field]
        with pytest.raises(ValidationError):
            CeleryJobDTO(**data)


class TestCelerySchemaInit:
    def test_exports_are_importable(self):
        from schemas.celery import CeleryJobDTO as D, CeleryJobResultType as R
        assert D is not None
        assert R is not None

    def test_version(self):
        import schemas.celery as c
        assert c.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.celery as c
        assert set(c.__all__) == {"CeleryJobResultType", "CeleryJobDTO"}
