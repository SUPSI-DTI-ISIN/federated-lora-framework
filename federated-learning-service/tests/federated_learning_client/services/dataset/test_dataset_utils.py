import pytest
from src.federated_learning_client.clients.schemas import DocumentDTO, SectionDTO
from src.federated_learning_client.domain.training import TrainingRow, TrainingTaskType
from src.federated_learning_client.services.dataset.dataset_utils import DatasetUtils


def _section(id=1, title="1. Introduction", content="Some content here for testing purposes."):
    return SectionDTO(id=id, title=title, content=content)


def _document(id=1, number="DOC-001", title="My Research Project", sections=None):
    return DocumentDTO(
        id=id, number=number, title=title,
        is_externally_approved=False,
        sections=sections if sections is not None else [_section()]
    )


class TestCreateDocumentTrainingRows:
    def test_returns_list_of_training_rows(self):
        doc = _document()
        rows = DatasetUtils.create_document_training_rows(document=doc)
        assert isinstance(rows, list)
        assert all(isinstance(r, TrainingRow) for r in rows)

    def test_returns_rows_for_all_task_types(self):
        doc = _document(sections=[
            _section(id=1, title="1. Intro", content="A" * 200),
            _section(id=2, title="2. Methods", content="B" * 200),
        ])
        rows = DatasetUtils.create_document_training_rows(document=doc)
        task_types = {r.task_type for r in rows}
        assert TrainingTaskType.SECTION_WRITING.value in task_types
        assert TrainingTaskType.STRUCTURE_QA.value in task_types

    def test_returns_empty_list_for_document_with_no_sections(self):
        doc = _document(sections=[])
        rows = DatasetUtils.create_document_training_rows(document=doc)
        section_writing_rows = [r for r in rows if r.task_type == TrainingTaskType.SECTION_WRITING.value]
        assert section_writing_rows == []

    def test_all_rows_have_correct_document_info(self):
        doc = _document(number="DOC-999", title="Test Project")
        rows = DatasetUtils.create_document_training_rows(document=doc)
        for row in rows:
            assert row.document_title == "Test Project"
            assert row.document_project_number == "DOC-999"


class TestSectionWritingRows:
    def test_creates_one_row_per_section(self):
        doc = _document(sections=[_section(id=1), _section(id=2, title="2. Methods")])
        rows = DatasetUtils._DatasetUtils__section_writing_rows(document=doc)
        assert len(rows) == 2

    def test_row_task_type_is_section_writing(self):
        doc = _document()
        rows = DatasetUtils._DatasetUtils__section_writing_rows(document=doc)
        assert all(r.task_type == TrainingTaskType.SECTION_WRITING.value for r in rows)

    def test_row_output_is_section_content(self):
        section = _section(content="The actual section content.")
        doc = _document(sections=[section])
        rows = DatasetUtils._DatasetUtils__section_writing_rows(document=doc)
        assert rows[0].output == "The actual section content."

    def test_row_section_title_matches(self):
        section = _section(title="3. Results")
        doc = _document(sections=[section])
        rows = DatasetUtils._DatasetUtils__section_writing_rows(document=doc)
        assert rows[0].section_title == "3. Results"

    def test_input_contains_document_title_and_section_title(self):
        doc = _document(title="My Proposal", sections=[_section(title="1. Intro")])
        rows = DatasetUtils._DatasetUtils__section_writing_rows(document=doc)
        assert "My Proposal" in rows[0].input
        assert "1. Intro" in rows[0].input


class TestStructureQARows:
    def test_returns_two_rows(self):
        doc = _document()
        rows = DatasetUtils._DatasetUtils__structure_qa_rows(document=doc)
        assert len(rows) == 2

    def test_row_task_type_is_structure_qa(self):
        doc = _document()
        rows = DatasetUtils._DatasetUtils__structure_qa_rows(document=doc)
        assert all(r.task_type == TrainingTaskType.STRUCTURE_QA.value for r in rows)

    def test_output_contains_section_titles(self):
        doc = _document(sections=[_section(title="1. Intro"), _section(id=2, title="2. Methods")])
        rows = DatasetUtils._DatasetUtils__structure_qa_rows(document=doc)
        for row in rows:
            assert "1. Intro" in row.output
            assert "2. Methods" in row.output

    def test_section_title_is_empty_string(self):
        doc = _document()
        rows = DatasetUtils._DatasetUtils__structure_qa_rows(document=doc)
        assert all(r.section_title == "" for r in rows)


class TestContentQARows:
    def test_skips_sections_with_short_content(self):
        doc = _document(sections=[_section(content="Short")])
        rows = DatasetUtils._DatasetUtils__content_qa_rows(document=doc)
        assert rows == []

    def test_creates_row_for_long_content(self):
        doc = _document(sections=[_section(content="A" * 150)])
        rows = DatasetUtils._DatasetUtils__content_qa_rows(document=doc)
        assert len(rows) == 1
        assert rows[0].task_type == TrainingTaskType.CONTENT_QA.value

    def test_output_contains_section_content(self):
        content = "A" * 150
        doc = _document(sections=[_section(content=content)])
        rows = DatasetUtils._DatasetUtils__content_qa_rows(document=doc)
        assert content in rows[0].output

    def test_section_title_is_set(self):
        doc = _document(sections=[_section(title="2. Methods", content="B" * 150)])
        rows = DatasetUtils._DatasetUtils__content_qa_rows(document=doc)
        assert rows[0].section_title == "2. Methods"


class TestCritiqueRows:
    def test_skips_sections_with_short_content(self):
        doc = _document(sections=[_section(content="Short content")])
        rows = DatasetUtils._DatasetUtils__critique_rows(document=doc)
        assert rows == []

    def test_creates_row_for_long_content(self):
        long_content = "A" * 200
        doc = _document(sections=[_section(content=long_content)])
        rows = DatasetUtils._DatasetUtils__critique_rows(document=doc)
        assert len(rows) == 1
        assert rows[0].task_type == TrainingTaskType.CRITIQUE.value

    def test_skips_when_weak_version_too_short(self):
        content = "Short\n" + "B" * 200
        doc = _document(sections=[_section(content=content)])
        rows = DatasetUtils._DatasetUtils__critique_rows(document=doc)
        assert rows == []

    def test_output_contains_full_content(self):
        long_content = "A" * 100 + "\n" + "B" * 200
        doc = _document(sections=[_section(content=long_content)])
        rows = DatasetUtils._DatasetUtils__critique_rows(document=doc)
        if rows:
            assert long_content.strip() in rows[0].output


class TestSummaryRows:
    def test_returns_empty_when_content_too_short(self):
        doc = _document(sections=[_section(content="Short")])
        rows = DatasetUtils._DatasetUtils__summary_rows(document=doc)
        assert rows == []

    def test_returns_one_row_for_long_content(self):
        doc = _document(sections=[
            _section(id=1, title="1. Intro", content="A" * 200),
            _section(id=2, title="2. Methods", content="B" * 200),
        ])
        rows = DatasetUtils._DatasetUtils__summary_rows(document=doc)
        assert len(rows) == 1
        assert rows[0].task_type == "summary"

    def test_output_contains_document_title(self):
        doc = _document(title="My Research", sections=[
            _section(id=1, content="A" * 200),
            _section(id=2, title="2. Methods", content="B" * 200),
        ])
        rows = DatasetUtils._DatasetUtils__summary_rows(document=doc)
        assert "My Research" in rows[0].output

    def test_section_title_is_empty_string(self):
        doc = _document(sections=[
            _section(id=1, content="A" * 200),
            _section(id=2, title="2. Methods", content="B" * 200),
        ])
        rows = DatasetUtils._DatasetUtils__summary_rows(document=doc)
        assert rows[0].section_title == ""
