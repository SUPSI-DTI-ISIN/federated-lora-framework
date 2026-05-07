class TestSettings:
    def _make_settings(self, **kwargs):
        from config.settings import Settings
        defaults = dict(
            keycloak_url="http://kc.local",
            institute_name="TestInstitute",
        )
        defaults.update(kwargs)
        return Settings(**defaults)

    def test_required_fields_are_set(self):
        s = self._make_settings(
            keycloak_url="http://kc.example.com",
            institute_name="MyInstitute",
        )
        assert s.keycloak_url == "http://kc.example.com"
        assert s.institute_name == "MyInstitute"

    def test_optional_fields_accept_explicit_values(self):
        s = self._make_settings(
            frontend_url="http://app.example.com",
            database_url="mysql+aiomysql://user:pass@db:3306/docs",
        )
        assert s.frontend_url == "http://app.example.com"
        assert s.database_url == "mysql+aiomysql://user:pass@db:3306/docs"

    def test_default_database_url_uses_aiomysql(self):
        s = self._make_settings()
        assert "mysql+aiomysql" in s.database_url

    def test_default_frontend_url(self):
        s = self._make_settings()
        assert s.frontend_url == "http://localhost:3000"

    def test_keycloak_global_hostname_url_defaults_to_empty_string(self):
        s = self._make_settings()
        assert s.keycloak_global_hostname_url == ""

    def test_keycloak_global_hostname_url_can_be_set(self):
        s = self._make_settings(keycloak_global_hostname_url="http://global.kc.example.com")
        assert s.keycloak_global_hostname_url == "http://global.kc.example.com"

    def test_cors_origins_wraps_frontend_url(self):
        s = self._make_settings(frontend_url="http://myapp.com")
        assert s.cors_origins == ["http://myapp.com"]

    def test_cors_origins_default(self):
        s = self._make_settings()
        assert s.cors_origins == ["http://localhost:3000"]


class TestConfigInit:
    def test_settings_singleton_is_exported(self):
        from config import settings
        assert settings is not None
        assert hasattr(settings, "keycloak_url")

    def test_version(self):
        import config
        assert config.__version__ == "1.0.0"
