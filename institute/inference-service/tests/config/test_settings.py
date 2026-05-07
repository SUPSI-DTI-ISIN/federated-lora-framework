class TestSettings:
    def _make(self, **kwargs):
        from config.settings import Settings
        defaults = dict(
            redis_url="redis://localhost:6379",
            institute_name="TestInstitute",
            keycloak_url="http://kc.local",
        )
        defaults.update(kwargs)
        return Settings(**defaults)

    def test_required_fields(self):
        s = self._make(redis_url="redis://r:6379", institute_name="Inst", keycloak_url="http://kc")
        assert s.redis_url == "redis://r:6379"
        assert s.institute_name == "Inst"
        assert s.keycloak_url == "http://kc"

    def test_default_max_cached_adapters(self):
        assert self._make().max_cached_adapters == 5

    def test_default_device_map(self):
        s = self._make()
        assert s.device_map in ("auto", "cpu")

    def test_default_frontend_url(self):
        assert self._make().frontend_url == "http://localhost:3000"

    def test_default_model_service_url(self):
        assert self._make().model_service_url == "http://localhost:8090"

    def test_keycloak_global_hostname_url_default(self):
        s = self._make()
        assert s.keycloak_global_hostname_url == ""

    def test_keycloak_global_hostname_url_explicit(self):
        s = self._make(keycloak_global_hostname_url="http://global.kc")
        assert s.keycloak_global_hostname_url == "http://global.kc"

    def test_cors_origins_wraps_frontend_url(self):
        s = self._make(frontend_url="http://myapp.com")
        assert s.cors_origins == ["http://myapp.com"]

    def test_system_prompt_with_adapter_is_non_empty(self):
        assert len(self._make().model_system_prompt_with_adapter_active) > 0

    def test_system_prompt_without_adapter_is_non_empty(self):
        assert len(self._make().model_system_prompt_without_adapter) > 0

    def test_optional_fields_accept_explicit_values(self):
        s = self._make(max_cached_adapters=10, device_map="cpu")
        assert s.max_cached_adapters == 10
        assert s.device_map == "cpu"


class TestConfigInit:
    def test_settings_singleton_exported(self):
        from config import settings
        assert settings is not None
        assert hasattr(settings, "redis_url")

    def test_version(self):
        import config
        assert config.__version__ == "1.0.0"
