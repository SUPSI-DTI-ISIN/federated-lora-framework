from unittest.mock import AsyncMock

from repositories.federated_learning_job.dependencies import (
    get_federated_learning_job_repository,
    build_federated_learning_job_repository,
)
from repositories.federated_learning_job.federated_learning_job_repository_interface import (
    FederatedLearningJobRepositoryInterface,
)


class TestGetFederatedLearningJobRepository:
    def test_returns_repository_interface(self):
        assert isinstance(get_federated_learning_job_repository(db=AsyncMock()), FederatedLearningJobRepositoryInterface)

    def test_uses_provided_session(self):
        mock_session = AsyncMock()
        assert get_federated_learning_job_repository(db=mock_session)._db_session is mock_session

    def test_repository_init_exports(self):
        from repositories.federated_learning_job import (
            FederatedLearningJobRepositoryInterface,
            get_federated_learning_job_repository as fn,
        )
        assert FederatedLearningJobRepositoryInterface is not None
        assert fn is not None

    def test_repository_init_version(self):
        import repositories.federated_learning_job as r
        assert r.__version__ == "1.0.0"


class TestBuildFederatedLearningJobRepository:
    def test_returns_repository_interface(self):
        assert isinstance(build_federated_learning_job_repository(db=AsyncMock()), FederatedLearningJobRepositoryInterface)

    def test_uses_provided_session(self):
        mock_session = AsyncMock()
        assert build_federated_learning_job_repository(db=mock_session)._db_session is mock_session
