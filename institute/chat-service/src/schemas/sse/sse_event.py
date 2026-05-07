from enum import Enum


class SseEvent(Enum):
    INFERENCE_JOB_SUCCESS = "inference_job_success"
    INFERENCE_JOB_FAILURE = "inference_job_failure"