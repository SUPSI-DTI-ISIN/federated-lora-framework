from unittest.mock import AsyncMock

from services.federated_learning_job.dependencies import get_federated_learning_job_service
from services.federated_learning_job.federated_learning_job_service_interface import (
    FederatedLearningJobServiceInterface,
)


class TestGetFederatedLearningJobService:
    def test_returns_service_interface(self):
        assert isinstance(
            get_federated_learning_job_service(federated_learning_job_repository=AsyncMock()),
            FederatedLearningJobServiceInterface,
        )

    def test_service_init_exports(self):
        from services.federated_learning_job import (
            FederatedLearningJobServiceInterface,
            get_federated_learning_job_service as fn,
        )
        assert FederatedLearningJobServiceInterface is not None
        assert fn is not None

    def test_service_init_version(self):
        import services.federated_learning_job as s
        assert s.__version__ == "1.0.0"
