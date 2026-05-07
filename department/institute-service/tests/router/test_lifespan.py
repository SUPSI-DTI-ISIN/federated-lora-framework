import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from schemas.exceptions.institute_errors import InstituteNameNotFoundError
from schemas.institute import InstituteDTO


def _make_lifespan_patches(mock_service, realm_name="Department", department_url="http://dept.local"):
    async def _fake_session():
        yield AsyncMock()

    return (
        patch("router.lifespan.DatabaseConnector.init_database_connection"),
        patch("router.lifespan.DatabaseConnector.test_connection", new_callable=AsyncMock),
        patch("router.lifespan.DatabaseConnector.get_db_session", return_value=_fake_session()),
        patch("router.lifespan.DatabaseConnector.close_connection", new_callable=AsyncMock),
        patch("router.lifespan.build_institute_repository", return_value=AsyncMock()),
        patch("router.lifespan.build_institute_service", return_value=mock_service),
        patch("router.lifespan.settings", **{"realm_name": realm_name, "department_url": department_url}),
    )


class TestLifespan:
    def test_lifespan_is_callable(self):
        from router.lifespan import lifespan
        assert callable(lifespan)

    def test_creates_default_institute_on_startup_when_not_found(self):
        mock_service = MagicMock()
        mock_service.get_by_name = AsyncMock(
            side_effect=InstituteNameNotFoundError(institute_name="Department")
        )
        mock_service.create_new_institute = AsyncMock()

        patches = _make_lifespan_patches(mock_service)
        with patches[0], patches[1] as mock_test, patches[2], patches[3] as mock_close, \
             patches[4], patches[5], patches[6]:
            from router.lifespan import lifespan
            with TestClient(FastAPI(lifespan=lifespan)):
                pass

        mock_service.create_new_institute.assert_called_once()
        mock_test.assert_awaited_once()
        mock_close.assert_awaited_once()

    def test_skips_creation_when_institute_already_exists(self):
        existing_dto = InstituteDTO(
            id=1, name="Department", url="http://dept.local", deletable=False, updatable=False
        )
        mock_service = MagicMock()
        mock_service.get_by_name = AsyncMock(return_value=existing_dto)
        mock_service.create_new_institute = AsyncMock()

        patches = _make_lifespan_patches(mock_service)
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6]:
            from router.lifespan import lifespan
            with TestClient(FastAPI(lifespan=lifespan)):
                pass

        mock_service.create_new_institute.assert_not_called()

    def test_app_is_reachable_during_lifespan(self):
        existing_dto = InstituteDTO(
            id=1, name="Department", url="http://dept.local", deletable=False, updatable=False
        )
        mock_service = MagicMock()
        mock_service.get_by_name = AsyncMock(return_value=existing_dto)

        patches = _make_lifespan_patches(mock_service)
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6]:
            from router.lifespan import lifespan
            from router.health.routes import router as health_router

            app = FastAPI(lifespan=lifespan)
            app.include_router(health_router)

            with TestClient(app) as client:
                assert client.get("/health/").status_code == 200
