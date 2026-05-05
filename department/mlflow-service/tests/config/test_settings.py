import pytest


class TestSettings:
    def _make_settings(self, **kwargs):
        from config.settings import Settings
        defaults = dict(model_key="m", keycloak_url="http://kc", realm_name="R")
        defaults.update(kwargs)
        return Settings(**defaults)

    def test_required_fields_are_set(self):
        s = self._make_settings(model_key="my-model", keycloak_url="http://kc", realm_name="Realm")
        assert s.model_key == "my-model"
        assert s.keycloak_url == "http://kc"
        assert s.realm_name == "Realm"

    def test_optional_fields_accept_explicit_values(self):
        s = self._make_settings(
            device_map="auto",
            model_base_path="./model",
            frontend_url="http://localhost:3001",
        )
        assert s.device_map == "auto"
        assert s.model_base_path == "./model"
        assert s.frontend_url == "http://localhost:3001"
        assert s.keycloak_global_hostname_url is None
        assert s.rank == 8
        assert s.lora_alpha == 16
        assert s.lora_dropout == 0.05

    def test_lora_config_property_reflects_settings(self):
        s = self._make_settings()
        lc = s.lora_config
        assert lc.r == 8
        assert lc.lora_alpha == 16
        assert lc.lora_dropout == 0.05
        assert lc.bias == "none"

    def test_lora_config_uses_custom_rank_and_alpha(self):
        s = self._make_settings(rank=16, lora_alpha=32, lora_dropout=0.1)
        lc = s.lora_config
        assert lc.r == 16
        assert lc.lora_alpha == 32
        assert lc.lora_dropout == 0.1

    def test_cors_origins_wraps_frontend_url(self):
        s = self._make_settings(frontend_url="http://myapp.com")
        assert s.cors_origins == ["http://myapp.com"]

    def test_cors_origins_default(self):
        s = self._make_settings(frontend_url="http://localhost:3001")
        assert s.cors_origins == ["http://localhost:3001"]

    def test_task_type_default(self):
        from peft import TaskType
        s = self._make_settings()
        assert s.task_type == TaskType.CAUSAL_LM

    def test_keycloak_global_hostname_url_can_be_set(self):
        s = self._make_settings(keycloak_global_hostname_url="http://global-kc")
        assert s.keycloak_global_hostname_url == "http://global-kc"


class TestConfigInit:
    def test_settings_singleton_is_exported(self):
        from config import settings
        assert settings is not None
        assert hasattr(settings, "model_key")

    def test_version(self):
        import config
        assert config.__version__ == "1.0.0"
