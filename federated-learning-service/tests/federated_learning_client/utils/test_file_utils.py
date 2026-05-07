import os
import pytest
from unittest.mock import patch

from src.federated_learning_client.utils.file_utils import FileUtils


class TestGetDatasetOutputFile:
    def test_returns_path_with_partition_id(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_dataset_output_file(partition_id=2)

        assert "2" in result
        assert result.endswith("dataset.jsonl")

    def test_returns_path_without_partition_id(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_dataset_output_file(partition_id=None)

        assert result.endswith("dataset.jsonl")
        assert "None" not in result

    def test_creates_directory(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_dataset_output_file(partition_id=5)

        assert os.path.isdir(os.path.dirname(result))


class TestGetTrainingFolder:
    def test_returns_path_with_partition_id(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_training_folder(partition_id=1)

        assert "1" in result
        assert "training" in result

    def test_returns_path_without_partition_id(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_training_folder(partition_id=None)

        assert "training" in result
        assert "None" not in result

    def test_creates_directory(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_training_folder(partition_id=3)

        assert os.path.isdir(result)


class TestGetAdapterFolder:
    def test_returns_path_with_partition_id(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_adapter_folder(partition_id=1)

        assert "1" in result
        assert "adapter" in result

    def test_returns_path_without_partition_id(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_adapter_folder(partition_id=None)

        assert "adapter" in result
        assert "None" not in result

    def test_creates_directory(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.get_adapter_folder(partition_id=2)

        assert os.path.isdir(result)


class TestDeleteOutputFolder:
    def test_returns_true_when_folder_exists_and_deleted(self, tmp_path):
        folder = tmp_path / "1"
        folder.mkdir()

        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.delete_output_folder(partition_id=1)

        assert result is True
        assert not folder.exists()

    def test_returns_false_when_folder_does_not_exist(self, tmp_path):
        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.delete_output_folder(partition_id=99)

        assert result is False

    def test_returns_false_on_exception(self, tmp_path):
        folder = tmp_path / "partition_err"
        folder.mkdir()

        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings, \
             patch("src.federated_learning_client.utils.file_utils.shutil.rmtree",
                   side_effect=PermissionError("denied")):
            mock_settings.dataset_output_folder = str(tmp_path)
            result = FileUtils.delete_output_folder(partition_id="err")

        assert result is False

    def test_deletes_base_folder_when_no_partition_id(self, tmp_path):
        base = tmp_path / "output"
        base.mkdir()

        with patch("src.federated_learning_client.utils.file_utils.settings") as mock_settings:
            mock_settings.dataset_output_folder = str(base)
            result = FileUtils.delete_output_folder(partition_id=None)

        assert result is True
        assert not base.exists()


class TestFileUtilsInit:
    def test_exports_file_utils(self):
        from src.federated_learning_client.utils import FileUtils as FU
        assert FU is FileUtils

    def test_version(self):
        from src.federated_learning_client.utils import __version__
        assert __version__ == "1.0.0"
