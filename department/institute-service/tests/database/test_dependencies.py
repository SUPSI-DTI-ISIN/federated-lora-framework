from unittest.mock import AsyncMock, patch

from database.dependencies import get_db_session


class TestGetDbSession:
    def test_database_init_exports(self):
        from database import DatabaseConnector, get_db_session as fn
        assert DatabaseConnector is not None
        assert fn is not None

    def test_database_init_version(self):
        import database
        assert database.__version__ == "1.0.0"

    async def test_delegates_to_connector(self):
        mock_session = AsyncMock()

        async def _fake_get_db_session():
            yield mock_session

        with patch("database.dependencies.DatabaseConnector.get_db_session", return_value=_fake_get_db_session()):
            sessions = [s async for s in get_db_session()]

        assert sessions == [mock_session]

    async def test_yields_exactly_one_session(self):
        mock_session = AsyncMock()

        async def _fake_get_db_session():
            yield mock_session

        with patch("database.dependencies.DatabaseConnector.get_db_session", return_value=_fake_get_db_session()):
            sessions = [s async for s in get_db_session()]

        assert len(sessions) == 1
