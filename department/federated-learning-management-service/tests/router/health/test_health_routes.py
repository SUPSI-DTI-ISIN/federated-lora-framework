import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from router.health.routes import router


@pytest.fixture()
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestHealthRoutes:
    def test_get_health_with_trailing_slash(self, client):
        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json() == {"status": "Healthy"}

    def test_get_health_without_trailing_slash(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "Healthy"}

    def test_response_contains_status_field(self, client):
        assert "status" in client.get("/health/").json()

    def test_router_init_export(self):
        from router.health import router as r
        assert r is not None

    def test_router_version(self):
        import router.health as rh
        assert rh.__version__ == "1.0.0"
