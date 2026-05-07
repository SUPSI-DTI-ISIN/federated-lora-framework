import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from database.database_connector import DatabaseConnector


@pytest.fixture(autouse=True)
def reset_connector():
    DatabaseConnector._engine = None
    DatabaseConnector._async_session_local = None
    yield
    DatabaseConnector._engine = None
    DatabaseConnector._async_session_local = None


class TestInitDatabaseConnection:
    def test_sets_engine_and_session(self):
        mock_engine = MagicMock()
        mock_session_maker = MagicMock()

        with patch("database.database_connector.create_async_engine", return_value=mock_engine), \
             patch("database.database_connector.async_sessionmaker", return_value=mock_session_maker):
            DatabaseConnector.init_database_connection()

        assert DatabaseConnector._engine is mock_engine
        assert DatabaseConnector._async_session_local is mock_session_maker


class TestTestConnection:
    async def test_raises_when_engine_is_none(self):
        with pytest.raises(RuntimeError, match="does not initialize"):
            await DatabaseConnector.test_connection()

    async def test_executes_select_1(self):
        mock_conn = AsyncMock()
        mock_begin_ctx = AsyncMock()
        mock_begin_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_begin_ctx.__aexit__ = AsyncMock(return_value=False)

        mock_engine = MagicMock()
        mock_engine.begin = MagicMock(return_value=mock_begin_ctx)
        DatabaseConnector._engine = mock_engine

        await DatabaseConnector.test_connection()

        mock_conn.execute.assert_awaited_once()

    async def test_propagates_exception(self):
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock(side_effect=Exception("DB down"))

        mock_begin_ctx = AsyncMock()
        mock_begin_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_begin_ctx.__aexit__ = AsyncMock(return_value=False)

        mock_engine = MagicMock()
        mock_engine.begin = MagicMock(return_value=mock_begin_ctx)
        DatabaseConnector._engine = mock_engine

        with pytest.raises(Exception, match="DB down"):
            await DatabaseConnector.test_connection()


class TestCloseConnection:
    async def test_disposes_engine_and_clears_state(self):
        mock_engine = AsyncMock()
        DatabaseConnector._engine = mock_engine
        DatabaseConnector._async_session_local = MagicMock()

        await DatabaseConnector.close_connection()

        mock_engine.dispose.assert_awaited_once()
        assert DatabaseConnector._engine is None
        assert DatabaseConnector._async_session_local is None

    async def test_does_not_raise_when_engine_is_none(self):
        await DatabaseConnector.close_connection()
        assert DatabaseConnector._engine is None


class TestGetDbSession:
    async def test_yields_session_and_closes_it(self):
        mock_session = AsyncMock()
        mock_session_ctx = AsyncMock()
        mock_session_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_ctx.__aexit__ = AsyncMock(return_value=False)

        DatabaseConnector._async_session_local = MagicMock(return_value=mock_session_ctx)

        sessions = [s async for s in DatabaseConnector.get_db_session()]

        assert sessions == [mock_session]
        mock_session.close.assert_awaited_once()


class TestDatabaseInit:
    def test_exports_database_connector(self):
        from database import DatabaseConnector as DC
        assert DC is DatabaseConnector

    def test_version(self):
        import database
        assert database.__version__ == "1.0.0"
