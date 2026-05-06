from enum import Enum

from schemas.sse import SseEvent


class TestSseEvent:
    def test_is_enum(self):
        assert issubclass(SseEvent, Enum)

    def test_inference_job_success_value(self):
        assert SseEvent.INFERENCE_JOB_SUCCESS.value == "inference_job_success"

    def test_inference_job_failure_value(self):
        assert SseEvent.INFERENCE_JOB_FAILURE.value == "inference_job_failure"

    def test_all_members(self):
        assert set(SseEvent.__members__) == {"INFERENCE_JOB_SUCCESS", "INFERENCE_JOB_FAILURE"}


class TestSseSchemasInit:
    def test_sse_event_is_exported(self):
        from schemas.sse import SseEvent as SE
        assert SE is SseEvent

    def test_version(self):
        import schemas.sse as ss
        assert ss.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.sse as ss
        assert "SseEvent" in ss.__all__
