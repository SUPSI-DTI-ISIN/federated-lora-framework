import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from schemas.model import ModelAdaptersVersionDTO, ManifestDTO


@pytest.fixture(autouse=True)
def reset_singleton():
    from services.adapter.adapter_registry_service import AdapterRegistryService
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None
    yield
    AdapterRegistryService._AdapterRegistryService__INSTANCE = None


@pytest.fixture()
def service():
    from services.adapter.adapter_registry_service import AdapterRegistryService
    from peft import LoraConfig
    lc = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none")
    return AdapterRegistryService.get_instance(device_map="cpu", lora_config=lc)


class TestGetInstance:
    def test_returns_same_object_on_repeated_calls(self):
        from services.adapter.adapter_registry_service import AdapterRegistryService
        from peft import LoraConfig
        lc = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none")
        a = AdapterRegistryService.get_instance(device_map="cpu", lora_config=lc)
        b = AdapterRegistryService.get_instance(device_map="cpu", lora_config=lc)
        assert a is b

    def test_ignores_different_args_after_first_call(self):
        from services.adapter.adapter_registry_service import AdapterRegistryService
        from peft import LoraConfig
        lc = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, bias="none")
        first = AdapterRegistryService.get_instance(device_map="cpu", lora_config=lc)
        second = AdapterRegistryService.get_instance(device_map="cuda", lora_config=lc)
        assert first is second


class TestEnsureInitAdapter:
    def test_skips_model_loading_when_adapter_already_valid(self, service, tmp_path):
        adapter_dir = tmp_path / "init"
        adapter_dir.mkdir()
        (adapter_dir / "adapter_config.json").write_text("{}")
        (adapter_dir / "adapter_model.safetensors").write_bytes(b"x")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_init_adapter_path",
                   return_value=str(adapter_dir)), \
             patch("services.adapter.adapter_registry_service.ModelUtils.load_model") as mock_load:
            service.ensure_init_adapter(model_key="m")

        mock_load.assert_not_called()

    def test_creates_adapter_when_not_valid(self, service, tmp_path):
        init_path = tmp_path / "init"
        base_path = str(tmp_path / "base")
        fake_base_model = MagicMock()
        fake_peft_model = MagicMock()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_init_adapter_path",
                   return_value=str(init_path)), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_base_path",
                   return_value=base_path), \
             patch("services.adapter.adapter_registry_service.ModelUtils.load_model",
                   return_value=fake_base_model) as mock_load, \
             patch("services.adapter.adapter_registry_service.ModelUtils.get_peft_model",
                   return_value=fake_peft_model) as mock_peft, \
             patch("services.adapter.adapter_registry_service.remove_hook_from_module") as mock_remove, \
             patch("gc.collect") as mock_gc, \
             patch("torch.cuda.empty_cache") as mock_empty, \
             patch("torch.cuda.synchronize") as mock_sync:
            service.ensure_init_adapter(model_key="m")

        mock_load.assert_called_once_with(model_path=base_path, device_map="cpu")
        mock_peft.assert_called_once()
        fake_peft_model.save_pretrained.assert_called_once_with(str(init_path))
        mock_remove.assert_called_once_with(fake_peft_model, recurse=True)
        fake_peft_model.cpu.assert_called_once()
        fake_base_model.cpu.assert_called_once()
        mock_gc.assert_called_once()
        mock_empty.assert_called_once()
        mock_sync.assert_called_once()


class TestGetAdaptersVersion:
    def test_returns_none_versions_when_path_does_not_exist(self, service, tmp_path):
        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(tmp_path / "nonexistent")):
            result = service.get_adapters_version(model_key="m")

        assert isinstance(result, ModelAdaptersVersionDTO)
        assert result.adapters_version is None

    def test_returns_none_versions_when_directory_is_empty(self, service, tmp_path):
        adapters_dir = tmp_path / "adapters"
        adapters_dir.mkdir()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_dir)):
            result = service.get_adapters_version(model_key="m")

        assert result.adapters_version is None

    def test_returns_none_versions_when_only_non_digit_dirs_exist(self, service, tmp_path):
        adapters_dir = tmp_path / "adapters"
        adapters_dir.mkdir()
        (adapters_dir / "init").mkdir()
        (adapters_dir / "init" / "file.bin").write_bytes(b"x")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_dir)):
            result = service.get_adapters_version(model_key="m")

        assert result.adapters_version is None

    def test_returns_none_versions_when_digit_dirs_are_empty(self, service, tmp_path):
        adapters_dir = tmp_path / "adapters"
        adapters_dir.mkdir()
        (adapters_dir / "1").mkdir()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_dir)):
            result = service.get_adapters_version(model_key="m")

        assert result.adapters_version is None

    def test_returns_sorted_version_list(self, service, tmp_path):
        adapters_dir = tmp_path / "adapters"
        adapters_dir.mkdir()
        for v in [3, 1, 2]:
            d = adapters_dir / str(v)
            d.mkdir()
            (d / "file.bin").write_bytes(b"x")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_dir)):
            result = service.get_adapters_version(model_key="m")

        assert result.adapters_version == [1, 2, 3]

    def test_preserves_model_key(self, service, tmp_path):
        adapters_dir = tmp_path / "adapters"
        adapters_dir.mkdir()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_dir)):
            result = service.get_adapters_version(model_key="special-key")

        assert result.model_key == "special-key"


class TestGetNewAdapterPath:
    def test_returns_version_1_when_adapters_dir_does_not_exist(self, service, tmp_path):
        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(tmp_path / "nonexistent")), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path / "adapters" / "1")) as mock_v:
            result = service.get_new_adapter_path(model_key="m")

        mock_v.assert_called_once_with(model_key="m", version=1)
        assert result.endswith("1")

    def test_returns_version_1_when_no_versions_exist(self, service, tmp_path):
        adapters_dir = tmp_path / "adapters"
        adapters_dir.mkdir()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_dir)), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapters_dir / "1")) as mock_v:
            service.get_new_adapter_path(model_key="m")

        mock_v.assert_called_once_with(model_key="m", version=1)

    def test_increments_max_existing_version(self, service, tmp_path):
        adapters_dir = tmp_path / "adapters"
        adapters_dir.mkdir()
        for v in [1, 2]:
            d = adapters_dir / str(v)
            d.mkdir()
            (d / "f.bin").write_bytes(b"x")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapters_path",
                   return_value=str(adapters_dir)), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapters_dir / "3")) as mock_v:
            service.get_new_adapter_path(model_key="m")

        mock_v.assert_called_once_with(model_key="m", version=3)


class TestGetLatestAdapterPath:
    def test_returns_init_path_when_no_versions_exist(self, service, tmp_path):
        init_path = str(tmp_path / "init")

        with patch.object(service, "get_adapters_version",
                          return_value=ModelAdaptersVersionDTO(model_key="m")), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_init_adapter_path",
                   return_value=init_path):
            result = service.get_latest_adapter_path(model_key="m")

        assert result == str(Path(init_path).resolve())

    def test_returns_path_for_max_version(self, service, tmp_path):
        v3_path = str(tmp_path / "adapters" / "3")

        with patch.object(service, "get_adapters_version",
                          return_value=ModelAdaptersVersionDTO(model_key="m", adapters_version=[1, 2, 3])), \
             patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=v3_path) as mock_v:
            service.get_latest_adapter_path(model_key="m")

        mock_v.assert_called_once_with(model_key="m", version=3)


class TestGetAdapterManifest:
    def test_raises_when_adapter_path_does_not_exist(self, service, tmp_path):
        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path / "nonexistent")):
            with pytest.raises(FileNotFoundError) as exc_info:
                service.get_adapter_manifest(model_key="m", adapter_version=1)

        assert "m" in str(exc_info.value)
        assert "1" in str(exc_info.value)

    def test_returns_manifest_when_path_exists(self, service, tmp_path):
        adapter_dir = tmp_path / "1"
        adapter_dir.mkdir()
        (adapter_dir / "weights.bin").write_bytes(b"w")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapter_dir)):
            result = service.get_adapter_manifest(model_key="m", adapter_version=1)

        assert isinstance(result, ManifestDTO)
        assert result.model_key == "m"


class TestGetAdapterFile:
    def test_raises_when_adapter_dir_does_not_exist(self, service, tmp_path):
        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path / "nonexistent")):
            with pytest.raises(FileNotFoundError):
                service.get_adapter_file(model_key="m", adapter_version=1, file_name="f.bin")

    def test_returns_path_when_file_exists(self, service, tmp_path):
        adapter_dir = tmp_path / "1"
        adapter_dir.mkdir()
        f = adapter_dir / "weights.bin"
        f.write_bytes(b"w")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapter_dir)):
            assert service.get_adapter_file(model_key="m", adapter_version=1, file_name="weights.bin") == f

    def test_raises_when_file_missing_in_existing_dir(self, service, tmp_path):
        adapter_dir = tmp_path / "1"
        adapter_dir.mkdir()

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapter_dir)):
            with pytest.raises(FileNotFoundError):
                service.get_adapter_file(model_key="m", adapter_version=1, file_name="missing.bin")


class TestDeleteAdapterVersion:
    def test_raises_when_adapter_does_not_exist(self, service, tmp_path):
        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path / "nonexistent")):
            with pytest.raises(FileNotFoundError) as exc_info:
                service.delete_adapter_version(model_key="m", adapter_version=99)

        assert "m" in str(exc_info.value)
        assert "99" in str(exc_info.value)

    def test_removes_directory_on_success(self, service, tmp_path):
        adapter_dir = tmp_path / "1"
        adapter_dir.mkdir()
        (adapter_dir / "f.bin").write_bytes(b"x")

        with patch("services.adapter.adapter_registry_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(adapter_dir)):
            service.delete_adapter_version(model_key="m", adapter_version=1)

        assert not adapter_dir.exists()
