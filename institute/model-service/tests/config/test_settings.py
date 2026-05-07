class TestSettings:
    def _make(self, **kwargs):
        from config.settings import Settings
        defaults = dict(
            keycloak_url="http://kc.local",
            institute_name="TestInstitute",
            model_key="llama-3",
        )
        defaults.update(kwargs)
        return Settings(**defaults)

    def test_required_fields(self):
        s = self._make(keycloak_url="http://kc", institute_name="Inst", model_key="mistral")
        assert s.keycloak_url == "http://kc"
        assert s.institute_name == "Inst"
        assert s.model_key == "mistral"

    def test_default_model_base_path(self):
        s = self._make()
        assert s.model_base_path in ("./model", "/tmp/models")

    def test_default_frontend_url(self):
        s = self._make()
        assert s.frontend_url == "http://localhost:3000"

    def test_default_mlflow_url(self):
        s = self._make()
        assert "mlflow" in s.mlflow_department_service_url or "9010" in s.mlflow_department_service_url

    def test_keycloak_global_hostname_url_default(self):
        s = self._make()
        assert s.keycloak_global_hostname_url == ""

    def test_keycloak_global_hostname_url_explicit(self):
        s = self._make(keycloak_global_hostname_url="http://global.kc")
        assert s.keycloak_global_hostname_url == "http://global.kc"

    def test_cors_origins_wraps_frontend_url(self):
        s = self._make(frontend_url="http://myapp.com")
        assert s.cors_origins == ["http://myapp.com"]

    def test_optional_fields_accept_explicit_values(self):
        s = self._make(
            model_base_path="/data/models",
            frontend_url="http://app.example.com",
            mlflow_department_service_url="http://mlflow:9010/api_mlflow",
        )
        assert s.model_base_path == "/data/models"
        assert s.frontend_url == "http://app.example.com"
        assert s.mlflow_department_service_url == "http://mlflow:9010/api_mlflow"


class TestConfigInit:
    def test_settings_singleton_exported(self):
        from config import settings
        assert settings is not None
        assert hasattr(settings, "model_key")

    def test_version(self):
        import config
        assert config.__version__ == "1.0.0"
