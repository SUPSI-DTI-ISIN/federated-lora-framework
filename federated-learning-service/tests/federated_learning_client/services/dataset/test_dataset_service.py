import json
import os
import pytest
from unittest.mock import patch, MagicMock

from src.federated_learning_client.clients.schemas import DocumentDTO, SectionDTO
from src.federated_learning_client.domain.training import TrainingDataset, TrainingRow, TrainingTaskType
from src.federated_learning_client.services.dataset.dataset_service import DatasetService


def _section(id=1, title="1. Intro", content="Content"):
    return SectionDTO(id=id, title=title, content=content)


def _document(id=1, number="DOC-001", title="My Project", sections=None):
    return DocumentDTO(
        id=id, number=number, title=title,
        sections=sections if sections is not None else [_section()]
    )


def _row(**kwargs):
    defaults = dict(
        instruction="sys", input="in", output="out",
        section_title="s", document_title="d",
        document_project_number="n",
        task_type=TrainingTaskType.SECTION_WRITING.value,
    )
    defaults.update(kwargs)
    return TrainingRow(**defaults)


class TestBuildDatasetFromDocuments:
    def test_returns_training_dataset(self):
        docs = [_document()]
        result = DatasetService.build_dataset_from_documents(documents=docs)
        assert isinstance(result, TrainingDataset)

    def test_aggregates_rows_from_all_documents(self):
        docs = [_document(id=1), _document(id=2, number="DOC-002")]
        result = DatasetService.build_dataset_from_documents(documents=docs)
        assert len(result.training_rows) > 0

    def test_empty_documents_returns_empty_dataset(self):
        result = DatasetService.build_dataset_from_documents(documents=[])
        assert result.training_rows == []

    def test_calls_dataset_utils_for_each_document(self):
        docs = [_document(id=1), _document(id=2, number="DOC-002")]
        with patch(
            "src.federated_learning_client.services.dataset.dataset_service.DatasetUtils.create_document_training_rows",
            return_value=[_row()]
        ) as mock_create:
            DatasetService.build_dataset_from_documents(documents=docs)

        assert mock_create.call_count == 2


class TestSaveDatasetToJsonl:
    def test_writes_jsonl_file(self, tmp_path):
        rows = [_row(instruction="sys", input="in", output="out")]
        dataset = TrainingDataset(training_rows=rows)

        with patch(
            "src.federated_learning_client.services.dataset.dataset_service.FileUtils.get_dataset_output_file",
            return_value=str(tmp_path / "dataset.jsonl")
        ):
            DatasetService.save_dataset_to_jsonl(training_dataset=dataset)

        output_file = tmp_path / "dataset.jsonl"
        assert output_file.exists()
        lines = output_file.read_text().strip().split("\n")
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["instruction"] == "sys"
        assert record["input"] == "in"
        assert record["output"] == "out"

    def test_writes_multiple_rows(self, tmp_path):
        rows = [_row(input=f"input_{i}") for i in range(3)]
        dataset = TrainingDataset(training_rows=rows)

        with patch(
            "src.federated_learning_client.services.dataset.dataset_service.FileUtils.get_dataset_output_file",
            return_value=str(tmp_path / "dataset.jsonl")
        ):
            DatasetService.save_dataset_to_jsonl(training_dataset=dataset)

        lines = (tmp_path / "dataset.jsonl").read_text().strip().split("\n")
        assert len(lines) == 3

    def test_passes_partition_id_to_file_utils(self, tmp_path):
        dataset = TrainingDataset(training_rows=[])

        with patch(
            "src.federated_learning_client.services.dataset.dataset_service.FileUtils.get_dataset_output_file",
            return_value=str(tmp_path / "dataset.jsonl")
        ) as mock_get:
            DatasetService.save_dataset_to_jsonl(training_dataset=dataset, partition_id=3)

        mock_get.assert_called_once_with(partition_id=3)


class TestLoadData:
    def test_returns_train_and_eval_datasets(self):
        with patch(
            "src.federated_learning_client.services.dataset.dataset_service.FileUtils.get_dataset_output_file",
            return_value="/tmp/dataset.jsonl"
        ):
            train, eval_ds = DatasetService.load_data()

        assert train is not None
        assert eval_ds is not None

    def test_passes_partition_id_to_file_utils(self):
        with patch(
            "src.federated_learning_client.services.dataset.dataset_service.FileUtils.get_dataset_output_file",
            return_value="/tmp/dataset.jsonl"
        ) as mock_get:
            DatasetService.load_data(partition_id=2)

        mock_get.assert_called_once_with(partition_id=2)


class TestDatasetServiceInit:
    def test_exports_dataset_service(self):
        from src.federated_learning_client.services.dataset import DatasetService as DS
        assert DS is DatasetService

    def test_version(self):
        from src.federated_learning_client.services.dataset import __version__
        assert __version__ == "1.0.0"
