import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from clients.schemas import ModelPathDTO
from schemas.exceptions import ModelLoadingError
from schemas.model import LoadedModel
from services.model.model_service import ModelService


def _model_path(base="/models/llama", adapter=None):
    return ModelPathDTO(model_base_path=base, adapter_path=adapter)


@pytest.fixture(autouse=True)
def reset_singleton():
    ModelService._ModelService__INSTANCE = None
    yield
    ModelService._ModelService__INSTANCE = None


@pytest.fixture()
def mock_client():
    return MagicMock()


@pytest.fixture()
def service(mock_client):
    return ModelService(
        model_service_client=mock_client,
        max_cached_adapters=3,
        device_map="cpu",
    )


def _patch_model_loading():
    """Context manager that patches all heavy ML imports used in ModelService."""
    return patch.multiple(
        "services.model.model_service",
        AutoModelForCausalLM=MagicMock(
            from_pretrained=MagicMock(return_value=MagicMock(
                eval=MagicMock(),
                device="cpu",
                disable_adapters=MagicMock(),
                load_adapter=MagicMock(),
                set_adapter=MagicMock(),
                delete_adapter=MagicMock(),
            ))
        ),
        AutoTokenizer=MagicMock(from_pretrained=MagicMock(return_value=MagicMock())),
        QuantizationUtils=MagicMock(get_quantization_config=MagicMock(return_value=MagicMock())),
        TorchDtypeUtils=MagicMock(get_torch_dtype=MagicMock(return_value="float16")),
        remove_hook_from_module=MagicMock(),
        dispatch_model=MagicMock(side_effect=lambda model, device_map: model),
        infer_auto_device_map=MagicMock(return_value={}),
        get_balanced_memory=MagicMock(return_value={}),
    )


class TestGetInstance:
    def test_returns_same_instance(self, mock_client):
        i1 = ModelService.get_instance(
            model_service_client=mock_client, max_cached_adapters=3, device_map="cpu"
        )
        i2 = ModelService.get_instance(
            model_service_client=mock_client, max_cached_adapters=3, device_map="cpu"
        )
        assert i1 is i2

    def test_creates_new_instance_after_reset(self, mock_client):
        i1 = ModelService.get_instance(
            model_service_client=mock_client, max_cached_adapters=3, device_map="cpu"
        )
        ModelService._ModelService__INSTANCE = None
        i2 = ModelService.get_instance(
            model_service_client=mock_client, max_cached_adapters=3, device_map="cpu"
        )
        assert i1 is not i2


class TestGetOrLoadModelNoAdapter:
    def test_returns_loaded_model_without_adapter(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path()

        with _patch_model_loading():
            result = service.get_or_load_model(model_key="llama-3", adapter_version=None)

        assert isinstance(result, LoadedModel)
        assert result.has_adapter is False

    def test_disables_adapters_when_loaded_adapters_exist(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path()

        with _patch_model_loading():
            # First load the model
            service.get_or_load_model(model_key="llama-3", adapter_version=None)
            # Simulate that adapters were loaded
            service._ModelService__loaded_adapters = {1: "v1"}
            # Now request without adapter — should call disable_adapters
            result = service.get_or_load_model(model_key="llama-3", adapter_version=None)

        service._ModelService__model.disable_adapters.assert_called()
        assert result.has_adapter is False

    def test_reuses_cached_model_for_same_key(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path()

        with _patch_model_loading():
            service.get_or_load_model(model_key="llama-3", adapter_version=None)
            call_count_after_first = mock_client.get_model_path_for_inference.call_count
            service.get_or_load_model(model_key="llama-3", adapter_version=None)
            call_count_after_second = mock_client.get_model_path_for_inference.call_count

        # Second call should not reload the base model
        assert call_count_after_second == call_count_after_first

    def test_reloads_model_for_different_key(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path()

        with _patch_model_loading():
            service.get_or_load_model(model_key="llama-3", adapter_version=None)
            service.get_or_load_model(model_key="mistral-7b", adapter_version=None)

        # Should have been called for both models
        assert mock_client.get_model_path_for_inference.call_count >= 2


class TestGetOrLoadModelWithAdapter:
    def test_returns_loaded_model_with_adapter(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path(
            adapter="/models/llama/adapters/v1"
        )

        with _patch_model_loading():
            result = service.get_or_load_model(model_key="llama-3", adapter_version=1)

        assert isinstance(result, LoadedModel)
        assert result.has_adapter is True

    def test_reuses_cached_adapter(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path(
            adapter="/models/llama/adapters/v1"
        )

        with _patch_model_loading():
            service.get_or_load_model(model_key="llama-3", adapter_version=1)
            call_count_after_first = mock_client.get_model_path_for_inference.call_count
            service.get_or_load_model(model_key="llama-3", adapter_version=1)
            call_count_after_second = mock_client.get_model_path_for_inference.call_count

        # Adapter already cached — no extra client call for adapter
        assert call_count_after_second == call_count_after_first

    def test_evicts_lru_adapter_when_cache_full(self, service, mock_client):
        """With max_cached_adapters=3, loading a 4th adapter should evict the LRU."""
        mock_client.get_model_path_for_inference.return_value = _model_path(
            adapter="/models/llama/adapters/vX"
        )

        with _patch_model_loading():
            # Load 3 adapters to fill the cache
            for v in [1, 2, 3]:
                service.get_or_load_model(model_key="llama-3", adapter_version=v)

            assert len(service._ModelService__loaded_adapters) == 3
            assert 1 in service._ModelService__loaded_adapters

            # Load a 4th — should evict adapter v1 (LRU)
            service.get_or_load_model(model_key="llama-3", adapter_version=4)

        assert len(service._ModelService__loaded_adapters) == 3
        assert 1 not in service._ModelService__loaded_adapters
        assert 4 in service._ModelService__loaded_adapters

    def test_lru_order_updated_on_access(self, service, mock_client):
        """Accessing adapter v1 after v2 should make v2 the LRU."""
        mock_client.get_model_path_for_inference.return_value = _model_path(
            adapter="/models/llama/adapters/vX"
        )

        with _patch_model_loading():
            service.get_or_load_model(model_key="llama-3", adapter_version=1)
            service.get_or_load_model(model_key="llama-3", adapter_version=2)
            service.get_or_load_model(model_key="llama-3", adapter_version=3)
            # Re-access v1 — makes v2 the LRU
            service.get_or_load_model(model_key="llama-3", adapter_version=1)
            # Load v4 — should evict v2 (now LRU)
            service.get_or_load_model(model_key="llama-3", adapter_version=4)

        assert 2 not in service._ModelService__loaded_adapters
        assert 1 in service._ModelService__loaded_adapters
        assert 4 in service._ModelService__loaded_adapters


class TestUnloadBaseModel:
    def test_unload_clears_model_state(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path()

        with _patch_model_loading():
            service.get_or_load_model(model_key="llama-3", adapter_version=None)

        assert service._ModelService__model is not None
        service._ModelService__unload_base_model()

        assert service._ModelService__model is None
        assert service._ModelService__tokenizer is None
        assert service._ModelService__model_key is None
        assert service._ModelService__loaded_adapters == {}
        assert service._ModelService__adapter_lru == []

    def test_unload_does_nothing_when_model_is_none(self, service):
        # Should not raise
        service._ModelService__unload_base_model()
        assert service._ModelService__model is None


class TestEvictLruAdapter:
    def test_evict_does_nothing_when_lru_empty(self, service):
        # Should not raise
        service._ModelService__evict_lru_adapter()

    def test_evict_removes_oldest_adapter(self, service, mock_client):
        mock_client.get_model_path_for_inference.return_value = _model_path(
            adapter="/models/llama/adapters/vX"
        )

        with _patch_model_loading():
            service.get_or_load_model(model_key="llama-3", adapter_version=1)
            service.get_or_load_model(model_key="llama-3", adapter_version=2)

        service._ModelService__evict_lru_adapter()

        assert 1 not in service._ModelService__loaded_adapters
        assert 2 in service._ModelService__loaded_adapters


class TestModelServiceInit:
    def test_exports(self):
        import services.model as sm
        assert "ModelServiceInterface" in sm.__all__
        assert "build_model_service" in sm.__all__

    def test_version(self):
        import services.model as sm
        assert sm.__version__ == "1.0.0"
