from enum import Enum


class FederatedLearningJobStatus(Enum):
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILURE = "failure"