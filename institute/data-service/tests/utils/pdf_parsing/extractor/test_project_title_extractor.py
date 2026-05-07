import pytest
from utils.pdf_parsing.extractor.project_title_extractor import ProjectTitleExtractor
from schemas.exceptions import ExtractorError


class TestProjectTitleExtractor:
    def test_extracts_project_title(self):
        text = "Title:\n My Awesome Project\nSome other content"
        result = ProjectTitleExtractor.extract_project_title(text_document=text)
        assert result == "My Awesome Project"

    def test_extracts_title_with_whitespace(self):
        text = "Title:\n   AI Research Project  \nMore content"
        result = ProjectTitleExtractor.extract_project_title(text_document=text)
        assert result == "AI Research Project"

    def test_raises_extractor_error_when_not_found(self):
        text = "This document has no title field"
        with pytest.raises(ExtractorError):
            ProjectTitleExtractor.extract_project_title(text_document=text)

    def test_raises_extractor_error_on_empty_text(self):
        with pytest.raises(ExtractorError):
            ProjectTitleExtractor.extract_project_title(text_document="")

    def test_returns_first_match(self):
        text = "Title:\n First Title\nTitle:\n Second Title\n"
        result = ProjectTitleExtractor.extract_project_title(text_document=text)
        assert result == "First Title"

    def test_title_with_colon_in_key(self):
        text = "Title of project:\n My Project\n"
        result = ProjectTitleExtractor.extract_project_title(text_document=text)
        assert result == "My Project"
