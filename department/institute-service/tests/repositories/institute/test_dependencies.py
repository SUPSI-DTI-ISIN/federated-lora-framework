from unittest.mock import AsyncMock

from repositories.institute.dependencies import get_institute_repository, build_institute_repository
from repositories.institute.institute_repository_interface import InstituteRepositoryInterface


class TestGetInstituteRepository:
    def test_returns_institute_repository_interface(self):
        assert isinstance(get_institute_repository(db=AsyncMock()), InstituteRepositoryInterface)

    def test_uses_provided_session(self):
        mock_session = AsyncMock()
        assert get_institute_repository(db=mock_session)._db_session is mock_session

    def test_repository_init_exports(self):
        from repositories.institute import InstituteRepositoryInterface, get_institute_repository as fn
        assert InstituteRepositoryInterface is not None
        assert fn is not None

    def test_repository_init_version(self):
        import repositories.institute as ri
        assert ri.__version__ == "1.0.0"


class TestBuildInstituteRepository:
    def test_returns_institute_repository_interface(self):
        assert isinstance(build_institute_repository(db=AsyncMock()), InstituteRepositoryInterface)

    def test_uses_provided_session(self):
        mock_session = AsyncMock()
        assert build_institute_repository(db=mock_session)._db_session is mock_session
