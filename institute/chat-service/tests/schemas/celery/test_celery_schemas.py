import pytest
from enum import Enum

from schemas.celery import CeleryJobResultType, CeleryJobDTO, QueryResponseDTO


class TestCeleryJobResultType:
    def test_is_enum(self):
        assert issubclass(CeleryJobResultType, Enum)

    def test_success_value(self):
        assert CeleryJobResultType.SUCCESS.value == "success"

    def test_failure_value(self):
        assert CeleryJobResultType.FAILURE.value == "failure"

    def test_all_members(self):
        assert set(CeleryJobResultType.__members__) == {"SUCCESS", "FAILURE"}


class TestQueryResponseDTO:
    def test_valid_dto(self):
        dto = QueryResponseDTO(
            user_id="u-1",
            chat_id=1,
            prompt="Hello",
            response="Hi",
            model_key="model-v1",
            adapter_version=2,
        )
        assert dto.user_id == "u-1"
        assert dto.chat_id == 1
        assert dto.response == "Hi"

    def test_adapter_version_can_be_none(self):
        dto = QueryResponseDTO(
            user_id="u-1",
            chat_id=1,
            prompt="Hello",
            response="Hi",
            model_key="model-v1",
            adapter_version=None,
        )
        assert dto.adapter_version is None


class TestCeleryJobDTO:
    def _make_dto(self, **kwargs):
        defaults = dict(
            job_id="job-1",
            result_type=CeleryJobResultType.SUCCESS,
            chat_id=1,
        )
        defaults.update(kwargs)
        return CeleryJobDTO(**defaults)

    def test_valid_success_dto(self):
        result = QueryResponseDTO(
            user_id="u-1", chat_id=1, prompt="p", response="r", model_key="k", adapter_version=None
        )
        dto = self._make_dto(result=result)
        assert dto.job_id == "job-1"
        assert dto.result_type == CeleryJobResultType.SUCCESS
        assert dto.result is result

    def test_valid_failure_dto(self):
        dto = self._make_dto(result_type=CeleryJobResultType.FAILURE, error="Something went wrong")
        assert dto.result_type == CeleryJobResultType.FAILURE
        assert dto.error == "Something went wrong"

    def test_result_defaults_to_none(self):
        dto = self._make_dto()
        assert dto.result is None

    def test_error_defaults_to_none(self):
        dto = self._make_dto()
        assert dto.error is None

    def test_missing_job_id_raises(self):
        with pytest.raises(Exception):
            CeleryJobDTO(result_type=CeleryJobResultType.SUCCESS, chat_id=1)

    def test_json_roundtrip(self):
        dto = self._make_dto(result_type=CeleryJobResultType.FAILURE, error="err")
        json_str = dto.model_dump_json()
        restored = CeleryJobDTO.model_validate_json(json_str)
        assert restored.job_id == dto.job_id
        assert restored.result_type == CeleryJobResultType.FAILURE
        assert restored.error == "err"


class TestSchemaCeleryInit:
    def test_exports_celery_job_result_type(self):
        from schemas.celery import CeleryJobResultType as T
        assert T is CeleryJobResultType

    def test_exports_celery_job_dto(self):
        from schemas.celery import CeleryJobDTO as D
        assert D is CeleryJobDTO

    def test_version(self):
        import schemas.celery as sc
        assert sc.__version__ == "1.0.0"
