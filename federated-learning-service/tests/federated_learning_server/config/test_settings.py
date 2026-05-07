class TestServerSettings:
    def _make(self, **kwargs):
        from src.federated_learning_server.config.settings import Settings
        return Settings(**kwargs)

    def test_defaults(self):
        s = self._make()
        assert s.mlflow_service_url == "http://localhost:9010"
        assert s.model_key == "llama-2-7b"

    def test_device_map_default(self):
        s = self._make()
        assert s.device_map in ("auto", "cpu")

    def test_explicit_values(self):
        s = self._make(
            mlflow_service_url="http://mlflow:9010",
            model_key="mistral-7b",
            device_map="cpu",
        )
        assert s.mlflow_service_url == "http://mlflow:9010"
        assert s.model_key == "mistral-7b"
        assert s.device_map == "cpu"


class TestServerConfigInit:
    def test_settings_exported(self):
        from src.federated_learning_server.config import settings
        assert settings is not None
        assert hasattr(settings, "model_key")

    def test_version(self):
        from src.federated_learning_server.config import __version__
        assert __version__ == "1.0.0"
