from schemas.health import HealthCheck


class TestHealthCheck:
    def test_default_status(self):
        assert HealthCheck().status == "Healthy"

    def test_custom_status(self):
        assert HealthCheck(status="OK").status == "OK"


class TestHealthInit:
    def test_exports_health_check(self):
        from schemas.health import HealthCheck as HC
        assert HC is HealthCheck

    def test_version(self):
        import schemas.health as sh
        assert sh.__version__ == "1.0.0"
