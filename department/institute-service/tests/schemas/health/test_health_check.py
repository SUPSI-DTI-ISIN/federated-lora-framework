import pytest
from pydantic import BaseModel

from schemas.health.health_check import HealthCheck


class TestHealthCheck:
    def test_default_status_is_healthy(self):
        assert HealthCheck().status == "Healthy"

    def test_custom_status(self):
        assert HealthCheck(status="Degraded").status == "Degraded"

    def test_is_pydantic_model(self):
        assert issubclass(HealthCheck, BaseModel)

    def test_serialization(self):
        assert HealthCheck().model_dump() == {"status": "Healthy"}

    def test_deserialization(self):
        assert HealthCheck.model_validate({"status": "Unhealthy"}).status == "Unhealthy"


class TestHealthCheckInit:
    def test_exported_from_package(self):
        from schemas.health import HealthCheck as HC
        assert HC is HealthCheck

    def test_version(self):
        import schemas.health as h
        assert h.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.health as h
        assert "HealthCheck" in h.__all__
