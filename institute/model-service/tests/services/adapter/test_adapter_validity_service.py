import hashlib
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

from clients.schemas import ManifestDTO, FileDTO
from services.adapter.adapter_validity_service import AdapterValidityService


def _file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _manifest(files=None):
    return ManifestDTO(model_key="llama-3", files=files or [])


class TestFetchAdapter:
    def test_returns_completed_transfers_count(self, tmp_path):
        manifest = _manifest(files=[
            FileDTO(size=10, rel_path="adapter.bin", hash="abc"),
        ])
        mlflow_client = MagicMock()

        with patch("services.adapter.adapter_validity_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch.object(AdapterValidityService, "download_adapter_file", return_value=True):
            result = AdapterValidityService.fetch_adapter(
                mlflow_service_client=mlflow_client,
                model_key="llama-3",
                adapter_version=1,
                manifest=manifest,
            )

        assert result == 1

    def test_creates_target_folder_if_missing(self, tmp_path):
        target = tmp_path / "new_adapter_dir"
        manifest = _manifest()
        mlflow_client = MagicMock()

        with patch("services.adapter.adapter_validity_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(target)):
            AdapterValidityService.fetch_adapter(
                mlflow_service_client=mlflow_client,
                model_key="llama-3",
                adapter_version=1,
                manifest=manifest,
            )

        assert target.exists()

    def test_raises_value_error_when_not_all_files_downloaded(self, tmp_path):
        manifest = _manifest(files=[
            FileDTO(size=10, rel_path="a.bin", hash="abc"),
            FileDTO(size=10, rel_path="b.bin", hash="def"),
        ])
        mlflow_client = MagicMock()

        with patch("services.adapter.adapter_validity_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch.object(AdapterValidityService, "download_adapter_file", return_value=False):
            with pytest.raises(ValueError, match="could not be found"):
                AdapterValidityService.fetch_adapter(
                    mlflow_service_client=mlflow_client,
                    model_key="llama-3",
                    adapter_version=1,
                    manifest=manifest,
                )

    def test_filters_files_to_download_when_provided(self, tmp_path):
        manifest = _manifest(files=[
            FileDTO(size=10, rel_path="a.bin", hash="abc"),
            FileDTO(size=10, rel_path="b.bin", hash="def"),
        ])
        mlflow_client = MagicMock()

        with patch("services.adapter.adapter_validity_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch.object(AdapterValidityService, "download_adapter_file", return_value=True) as mock_dl:
            AdapterValidityService.fetch_adapter(
                mlflow_service_client=mlflow_client,
                model_key="llama-3",
                adapter_version=1,
                manifest=manifest,
                files_to_download=["a.bin"],
            )

        assert mock_dl.call_count == 1
        assert mock_dl.call_args[0][3] == "a.bin"


class TestDownloadAdapterFile:
    def test_returns_true_when_hash_matches(self, tmp_path):
        content = b"adapter weights"
        expected_hash = _file_hash(content)

        mock_response = MagicMock()
        mock_response.headers = {"content-length": str(len(content))}
        mock_response.iter_content.return_value = [content]

        mlflow_client = MagicMock()
        mlflow_client.get_adapter_file.return_value = mock_response

        with patch("services.adapter.adapter_validity_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch("services.adapter.adapter_validity_service.FileHashUtils.get_file_hash",
                   return_value=expected_hash), \
             patch("builtins.open", mock_open()), \
             patch("services.adapter.adapter_validity_service.tqdm") as mock_tqdm:
            mock_tqdm.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_tqdm.return_value.__exit__ = MagicMock(return_value=False)

            result = AdapterValidityService.download_adapter_file(
                mlflow_service_client=mlflow_client,
                model_key="llama-3",
                adapter_version=1,
                adapter_file_path="adapter.bin",
                adapter_file_hash=expected_hash,
                position=0,
            )

        assert result is True

    def test_returns_false_and_unlinks_when_hash_mismatch(self, tmp_path):
        content = b"adapter weights"
        target_file = tmp_path / "adapter.bin"
        target_file.write_bytes(content)

        mock_response = MagicMock()
        mock_response.headers = {"content-length": str(len(content))}
        mock_response.iter_content.return_value = [content]

        mlflow_client = MagicMock()
        mlflow_client.get_adapter_file.return_value = mock_response

        with patch("services.adapter.adapter_validity_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch("services.adapter.adapter_validity_service.FileHashUtils.get_file_hash",
                   return_value="wrong_hash"), \
             patch("builtins.open", mock_open()), \
             patch("services.adapter.adapter_validity_service.tqdm") as mock_tqdm, \
             patch("services.adapter.adapter_validity_service.os.unlink") as mock_unlink:
            mock_tqdm.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_tqdm.return_value.__exit__ = MagicMock(return_value=False)

            result = AdapterValidityService.download_adapter_file(
                mlflow_service_client=mlflow_client,
                model_key="llama-3",
                adapter_version=1,
                adapter_file_path="adapter.bin",
                adapter_file_hash="correct_hash",
                position=0,
            )

        assert result is False
        mock_unlink.assert_called_once()

    def test_skips_empty_chunks(self, tmp_path):
        content = b"data"
        expected_hash = _file_hash(content)

        mock_response = MagicMock()
        mock_response.headers = {"content-length": str(len(content))}
        mock_response.iter_content.return_value = [b"", content, b""]

        mlflow_client = MagicMock()
        mlflow_client.get_adapter_file.return_value = mock_response

        with patch("services.adapter.adapter_validity_service.ModelPathUtils.get_model_adapter_path_by_version",
                   return_value=str(tmp_path)), \
             patch("services.adapter.adapter_validity_service.FileHashUtils.get_file_hash",
                   return_value=expected_hash), \
             patch("builtins.open", mock_open()), \
             patch("services.adapter.adapter_validity_service.tqdm") as mock_tqdm:
            mock_tqdm.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_tqdm.return_value.__exit__ = MagicMock(return_value=False)

            result = AdapterValidityService.download_adapter_file(
                mlflow_service_client=mlflow_client,
                model_key="llama-3",
                adapter_version=1,
                adapter_file_path="adapter.bin",
                adapter_file_hash=expected_hash,
                position=0,
            )

        assert result is True
