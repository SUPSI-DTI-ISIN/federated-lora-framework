import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.federated_learning_server.services.adapter_service import AdapterService


class TestLoadAdapterStateDict:
    def test_returns_state_dict_when_safetensors_exists(self, tmp_path):
        safetensors_file = tmp_path / "adapter_model.safetensors"
        safetensors_file.write_bytes(b"fake safetensors data")

        mock_state_dict = {"weight": MagicMock()}

        with patch("src.federated_learning_server.services.adapter_service.load_file",
                   return_value=mock_state_dict) as mock_load:
            result = AdapterService.load_adapter_state_dict(adapter_path=str(tmp_path))

        mock_load.assert_called_once_with(str(safetensors_file), device="cpu")
        assert result is mock_state_dict

    def test_raises_file_not_found_when_no_safetensors(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="No adapter weights found"):
            AdapterService.load_adapter_state_dict(adapter_path=str(tmp_path))

    def test_error_message_contains_adapter_path(self, tmp_path):
        with pytest.raises(FileNotFoundError) as exc_info:
            AdapterService.load_adapter_state_dict(adapter_path=str(tmp_path))

        assert str(tmp_path) in str(exc_info.value)


class TestSaveAdapter:
    def test_creates_output_directory(self, tmp_path):
        new_adapter_path = str(tmp_path / "new_adapter")
        source_adapter_path = str(tmp_path / "source_adapter")
        os.makedirs(source_adapter_path)
        (Path(source_adapter_path) / "adapter_config.json").write_text('{"key": "value"}')

        state_dict = {"weight": MagicMock()}

        with patch("src.federated_learning_server.services.adapter_service.save_file"):
            AdapterService.save_adapter(
                state_dict=state_dict,
                new_adapter_path=new_adapter_path,
                source_adapter_path=source_adapter_path,
            )

        assert os.path.isdir(new_adapter_path)

    def test_copies_adapter_config(self, tmp_path):
        new_adapter_path = str(tmp_path / "new_adapter")
        source_adapter_path = str(tmp_path / "source_adapter")
        os.makedirs(source_adapter_path)
        config_content = '{"r": 8, "lora_alpha": 16}'
        (Path(source_adapter_path) / "adapter_config.json").write_text(config_content)

        state_dict = {"weight": MagicMock()}

        with patch("src.federated_learning_server.services.adapter_service.save_file"):
            AdapterService.save_adapter(
                state_dict=state_dict,
                new_adapter_path=new_adapter_path,
                source_adapter_path=source_adapter_path,
            )

        copied_config = Path(new_adapter_path) / "adapter_config.json"
        assert copied_config.exists()
        assert copied_config.read_text() == config_content

    def test_saves_safetensors_file(self, tmp_path):
        new_adapter_path = str(tmp_path / "new_adapter")
        source_adapter_path = str(tmp_path / "source_adapter")
        os.makedirs(source_adapter_path)
        (Path(source_adapter_path) / "adapter_config.json").write_text("{}")

        state_dict = {"weight": MagicMock()}

        with patch("src.federated_learning_server.services.adapter_service.save_file") as mock_save:
            AdapterService.save_adapter(
                state_dict=state_dict,
                new_adapter_path=new_adapter_path,
                source_adapter_path=source_adapter_path,
            )

        mock_save.assert_called_once()
        call_args = mock_save.call_args
        assert call_args[0][0] is state_dict
        assert "adapter_model.safetensors" in call_args[0][1]


class TestAdapterServiceInit:
    def test_exports_adapter_service(self):
        from src.federated_learning_server.services import AdapterService as AS
        assert AS is AdapterService

    def test_version(self):
        from src.federated_learning_server.services import __version__
        assert __version__ == "1.0.0"
