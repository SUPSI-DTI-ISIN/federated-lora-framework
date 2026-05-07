import pytest
from src.federated_learning_server.clients.schemas import FederatedDataDTO


class TestFederatedDataDTO:
    def test_valid(self):
        dto = FederatedDataDTO(
            new_adapter_path="/adapters/new",
            latest_adapter_path="/adapters/latest"
        )
        assert dto.new_adapter_path == "/adapters/new"
        assert dto.latest_adapter_path == "/adapters/latest"

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            FederatedDataDTO(new_adapter_path="/adapters/new")


class TestServerSchemasInit:
    def test_exports(self):
        from src.federated_learning_server.clients.schemas import __all__
        assert "FederatedDataDTO" in __all__

    def test_version(self):
        from src.federated_learning_server.clients.schemas import __version__
        assert __version__ == "1.0.0"
