from schemas.health import HealthCheck


class TestHealthCheck:
    def test_default_status(self):
        hc = HealthCheck()
        assert hc.status == "Healthy"

    def test_custom_status(self):
        hc = HealthCheck(status="OK")
        assert hc.status == "OK"


class TestHealthInit:
    def test_exports_health_check(self):
        from schemas.health import HealthCheck as HC
        assert HC is HealthCheck

    def test_version(self):
        import schemas.health as sh
        assert sh.__version__ == "1.0.0"
