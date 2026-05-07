from enum import Enum

from entities.federated_learning_job_status_model import FederatedLearningJobStatus


class TestFederatedLearningJobStatus:
    def test_is_enum(self):
        assert issubclass(FederatedLearningJobStatus, Enum)

    def test_in_progress_value(self):
        assert FederatedLearningJobStatus.IN_PROGRESS.value == "in_progress"

    def test_success_value(self):
        assert FederatedLearningJobStatus.SUCCESS.value == "success"

    def test_failure_value(self):
        assert FederatedLearningJobStatus.FAILURE.value == "failure"

    def test_all_members(self):
        assert set(FederatedLearningJobStatus.__members__) == {"IN_PROGRESS", "SUCCESS", "FAILURE"}
