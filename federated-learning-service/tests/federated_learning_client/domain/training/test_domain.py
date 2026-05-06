import dataclasses
from enum import Enum

from src.federated_learning_client.domain.training import TrainingDataset, TrainingRow, TrainingTaskType


class TestTrainingTaskType:
    def test_is_enum(self):
        assert issubclass(TrainingTaskType, Enum)

    def test_values(self):
        assert TrainingTaskType.SECTION_WRITING.value == "section_writing"
        assert TrainingTaskType.STRUCTURE_QA.value == "structure_qa"
        assert TrainingTaskType.CONTENT_QA.value == "content_qa"
        assert TrainingTaskType.CRITIQUE.value == "critique"
        assert TrainingTaskType.SUMMARY.value == "summary"

    def test_all_members(self):
        assert set(TrainingTaskType.__members__) == {
            "SECTION_WRITING", "STRUCTURE_QA", "CONTENT_QA", "CRITIQUE", "SUMMARY"
        }


class TestTrainingRow:
    def _make(self, **kwargs):
        defaults = dict(
            instruction="System prompt",
            input="User input",
            output="Expected output",
            section_title="1. Intro",
            document_title="My Project",
            document_project_number="DOC-001",
            task_type=TrainingTaskType.SECTION_WRITING.value,
        )
        defaults.update(kwargs)
        return TrainingRow(**defaults)

    def test_stores_all_fields(self):
        row = self._make()
        assert row.instruction == "System prompt"
        assert row.input == "User input"
        assert row.output == "Expected output"
        assert row.section_title == "1. Intro"
        assert row.document_title == "My Project"
        assert row.document_project_number == "DOC-001"
        assert row.task_type == TrainingTaskType.SECTION_WRITING.value

    def test_text_defaults_to_empty_string(self):
        assert self._make().text == ""

    def test_prompt_length_defaults_to_zero(self):
        assert self._make().prompt_length == 0

    def test_text_can_be_set(self):
        row = self._make(text="formatted text")
        assert row.text == "formatted text"

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(TrainingRow)


class TestTrainingDataset:
    def test_stores_training_rows(self):
        rows = [
            TrainingRow(
                instruction="sys", input="in", output="out",
                section_title="s", document_title="d",
                document_project_number="n", task_type="t"
            )
        ]
        ds = TrainingDataset(training_rows=rows)
        assert len(ds.training_rows) == 1

    def test_empty_training_rows(self):
        ds = TrainingDataset(training_rows=[])
        assert ds.training_rows == []

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(TrainingDataset)


class TestDomainInit:
    def test_exports(self):
        from src.federated_learning_client.domain.training import __all__
        assert "TrainingDataset" in __all__
        assert "TrainingRow" in __all__
        assert "TrainingTaskType" in __all__

    def test_version(self):
        from src.federated_learning_client.domain.training import __version__
        assert __version__ == "1.0.0"
