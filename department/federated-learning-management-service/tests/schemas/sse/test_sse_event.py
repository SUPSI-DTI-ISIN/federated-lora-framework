from enum import Enum

from schemas.sse.sse_event import SseEvent


class TestSseEvent:
    def test_is_enum(self):
        assert issubclass(SseEvent, Enum)

    def test_federated_learning_job_update_value(self):
        assert SseEvent.FEDERATED_LEARNING_JOB_UPDATE.value == "federated_learning_job_update"

    def test_all_members(self):
        assert set(SseEvent.__members__) == {"FEDERATED_LEARNING_JOB_UPDATE"}


class TestSseSchemaInit:
    def test_exported_from_package(self):
        from schemas.sse import SseEvent as E
        assert E is SseEvent

    def test_version(self):
        import schemas.sse as s
        assert s.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.sse as s
        assert "SseEvent" in s.__all__
