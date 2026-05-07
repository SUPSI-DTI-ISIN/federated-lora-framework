import pytest
from unittest.mock import AsyncMock, MagicMock

from database.database_connector import DatabaseConnector


@pytest.fixture(autouse=True)
def reset_connector():
    DatabaseConnector._engine = None
    DatabaseConnector._async_session_local = None
    yield
    DatabaseConnector._engine = None
    DatabaseConnector._async_session_local = None


class TestGetDbSessionDependency:
    async def test_yields_session(self):
        mock_session = AsyncMock()
        mock_session_ctx = AsyncMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=False)
        DatabaseConnector._async_session_local = MagicMock(return_value=mock_session_ctx)

        from database.dependencies import get_db_session
        sessions = [s async for s in get_db_session()]

        assert sessions == [mock_session]
