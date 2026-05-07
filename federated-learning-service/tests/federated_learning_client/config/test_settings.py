class TestClientSettings:
    def _make(self, **kwargs):
        from src.federated_learning_client.config.settings import Settings
        return Settings(**kwargs)

    def test_defaults(self):
        s = self._make()
        assert s.data_service_url == "http://localhost:8080"
        assert s.model_service_url == "http://localhost:8090"
        assert s.model_key == "llama-2-7b"
        assert s.dataset_output_folder == "/tmp/fl_output"
        assert s.is_simulation_running_environment is False

    def test_device_map_default(self):
        s = self._make()
        assert s.device_map in ("auto", "cpu")

    def test_explicit_values(self):
        s = self._make(
            data_service_url="http://data:8080",
            model_service_url="http://model:8090",
            model_key="mistral-7b",
            dataset_output_folder="/data/output",
            is_simulation_running_environment=True,
        )
        assert s.data_service_url == "http://data:8080"
        assert s.model_key == "mistral-7b"
        assert s.is_simulation_running_environment is True


class TestClientConfigInit:
    def test_settings_exported(self):
        from src.federated_learning_client.config import settings
        assert settings is not None
        assert hasattr(settings, "model_key")

    def test_version(self):
        from src.federated_learning_client.config import __version__
        assert __version__ == "1.0.0"
