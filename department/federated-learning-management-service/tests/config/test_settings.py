class TestSettings:
    def _make_settings(self, **kwargs):
        from config.settings import Settings
        defaults = dict(
            keycloak_url="http://kc.local",
            realm_name="TestRealm",
            redis_url="redis://localhost:6379",
            flwr_app_base_path="/tmp/flwr",
        )
        defaults.update(kwargs)
        return Settings(**defaults)

    def test_required_fields_are_set(self):
        s = self._make_settings(
            keycloak_url="http://kc.example.com",
            realm_name="MyRealm",
            redis_url="redis://redis:6379",
            flwr_app_base_path="/apps/flwr",
        )
        assert s.keycloak_url == "http://kc.example.com"
        assert s.realm_name == "MyRealm"
        assert s.redis_url == "redis://redis:6379"
        assert s.flwr_app_base_path == "/apps/flwr"

    def test_optional_fields_accept_explicit_values(self):
        s = self._make_settings(
            frontend_url="http://app.example.com",
            database_url="mysql+aiomysql://user:pass@db:3306/mydb",
            is_federated_learning_simulation_environment=True,
            federated_learning_deployment_environment="production",
        )
        assert s.frontend_url == "http://app.example.com"
        assert s.database_url == "mysql+aiomysql://user:pass@db:3306/mydb"
        assert s.is_federated_learning_simulation_environment is True
        assert s.federated_learning_deployment_environment == "production"
        assert s.keycloak_global_hostname_url is None

    def test_default_database_url_uses_aiomysql(self):
        s = self._make_settings()
        assert "mysql+aiomysql" in s.database_url

    def test_default_frontend_url(self):
        s = self._make_settings()
        assert s.frontend_url == "http://localhost:3000"

    def test_default_deployment_environment(self):
        s = self._make_settings()
        assert s.federated_learning_deployment_environment == "local-simulation"

    def test_default_simulation_flag_is_false(self):
        s = self._make_settings()
        assert s.is_federated_learning_simulation_environment is False

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
