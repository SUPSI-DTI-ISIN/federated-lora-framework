from enum import Enum

from schemas.celery.celery_job_result_type import CeleryJobResultType


class TestCeleryJobResultType:
    def test_is_enum(self):
        assert issubclass(CeleryJobResultType, Enum)

    def test_success_value(self):
        assert CeleryJobResultType.SUCCESS.value == "success"

    def test_failure_value(self):
        assert CeleryJobResultType.FAILURE.value == "failure"

    def test_all_members(self):
        assert set(CeleryJobResultType.__members__) == {"SUCCESS", "FAILURE"}
