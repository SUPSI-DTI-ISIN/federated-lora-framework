class TestSettings:
    def _make_settings(self, **kwargs):
        from config.settings import Settings
        defaults = dict(keycloak_url="http://kc.local", realm_name="TestRealm")
        defaults.update(kwargs)
        return Settings(**defaults)

    def test_required_fields_are_set(self):
        s = self._make_settings(keycloak_url="http://kc.example.com", realm_name="MyRealm")
        assert s.keycloak_url == "http://kc.example.com"
        assert s.realm_name == "MyRealm"

    def test_optional_fields_accept_explicit_values(self):
        s = self._make_settings(
            frontend_url="http://app.example.com",
            department_url="http://dept.example.com",
            database_url="mysql+aiomysql://user:pass@db:3306/mydb",
        )
        assert s.frontend_url == "http://app.example.com"
        assert s.department_url == "http://dept.example.com"
        assert s.database_url == "mysql+aiomysql://user:pass@db:3306/mydb"
        assert s.keycloak_global_hostname_url is None

    def test_default_database_url_uses_aiomysql(self):
        s = self._make_settings()
        assert "mysql+aiomysql" in s.database_url

    def test_default_frontend_url(self):
        s = self._make_settings()
        assert s.frontend_url == "http://localhost:3000"

    def test_default_department_url(self):
        s = self._make_settings()
        assert s.department_url == "http://localhost:81"

    def test_keycloak_global_hostname_url_defaults_to_none(self):
        s = self._make_settings()
        assert s.keycloak_global_hostname_url is None

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
