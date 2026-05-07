import pytest
from utils.pdf_parsing.extractor.project_number_extractor import ProjectNumberExtractor
from schemas.exceptions import ExtractorError


class TestProjectNumberExtractor:
    def test_extracts_project_number(self):
        text = "Number:\n 12345\nSome other content"
        result = ProjectNumberExtractor.extract_project_number(text_document=text)
        assert result == "12345"

    def test_extracts_project_number_with_whitespace(self):
        text = "Number:\n   ABC-999  \nMore content"
        result = ProjectNumberExtractor.extract_project_number(text_document=text)
        assert result == "ABC-999"

    def test_raises_extractor_error_when_not_found(self):
        text = "This document has no number field"
        with pytest.raises(ExtractorError):
            ProjectNumberExtractor.extract_project_number(text_document=text)

    def test_raises_extractor_error_on_empty_text(self):
        with pytest.raises(ExtractorError):
            ProjectNumberExtractor.extract_project_number(text_document="")

    def test_returns_first_match(self):
        text = "Number:\n 111\nNumber:\n 222\n"
        result = ProjectNumberExtractor.extract_project_number(text_document=text)
        assert result == "111"
