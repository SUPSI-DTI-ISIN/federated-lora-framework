import pytest
from utils.pdf_parsing.extractor.section_extractor import SectionExtractor
from commons.documents import ParsedSection


SAMPLE_TEXT = """Number:
 DOC-001

Title:
 My Research Project

1. Introduction
This is the introduction content.
It spans multiple lines.

2. Methods
This is the methods section.

2.1 Sub-methods
This is a sub-section.

3. Results
Final results here.
"""


class TestExtractDocumentSections:
    def test_returns_list_of_parsed_sections(self):
        sections = SectionExtractor.extract_document_sections(
            text=SAMPLE_TEXT, project_number="DOC-001"
        )
        assert isinstance(sections, list)
        assert all(isinstance(s, ParsedSection) for s in sections)

    def test_extracts_top_level_sections(self):
        sections = SectionExtractor.extract_document_sections(
            text=SAMPLE_TEXT, project_number="DOC-001"
        )
        titles = [s.title for s in sections]
        assert any("Introduction" in t for t in titles)
        assert any("Methods" in t for t in titles)
        assert any("Results" in t for t in titles)

    def test_sections_have_content(self):
        sections = SectionExtractor.extract_document_sections(
            text=SAMPLE_TEXT, project_number="DOC-001"
        )
        for section in sections:
            assert section.content is not None

    def test_returns_empty_list_for_text_without_sections(self):
        text = "This is just plain text with no numbered sections."
        sections = SectionExtractor.extract_document_sections(
            text=text, project_number="DOC-001"
        )
        assert sections == []

    def test_excludes_sections_containing_project_number(self):
        text = """1. DOC-001 Reference
Some content.

2. Introduction
Real content here.
"""
        sections = SectionExtractor.extract_document_sections(
            text=text, project_number="DOC-001"
        )
        titles = [s.title for s in sections]
        assert not any("DOC-001" in t for t in titles)

    def test_excludes_duplicate_section_titles(self):
        text = """1. Introduction
Content 1.

2. Methods
Content 2.

1. Introduction
Duplicate content.
"""
        sections = SectionExtractor.extract_document_sections(
            text=text, project_number="DOC-001"
        )
        titles = [s.title for s in sections]
        assert titles.count("1. Introduction") == 0

    def test_section_content_is_trimmed(self):
        sections = SectionExtractor.extract_document_sections(
            text=SAMPLE_TEXT, project_number="DOC-001"
        )
        for section in sections:
            assert section.content == section.content.strip()


class TestGetRawSections:
    def test_returns_sections_with_positions(self):
        raw = SectionExtractor._get_raw_sections(SAMPLE_TEXT)
        assert len(raw) > 0
        for item in raw:
            assert item.title
            assert item.start_pos is not None
            assert item.start_content_pos is not None

    def test_skips_empty_titles(self):
        text = "1. \n2. Valid Section\nContent\n"
        raw = SectionExtractor._get_raw_sections(text)
        titles = [r.title for r in raw]
        assert not any(t.strip() == "1." for t in titles)


class TestRemoveNonValidSections:
    def test_removes_duplicates(self):
        from utils.pdf_parsing.extractor.section_extractor import SectionUtil
        sections = [
            SectionUtil(title="1. Intro", start_pos=0, start_content_pos=10),
            SectionUtil(title="2. Methods", start_pos=20, start_content_pos=30),
            SectionUtil(title="1. Intro", start_pos=40, start_content_pos=50),
        ]
        result = SectionExtractor._remove_non_valid_sections(
            raw_sections=sections, project_number="DOC-001"
        )
        titles = [r.title for r in result]
        assert "1. Intro" not in titles
        assert "2. Methods" in titles

    def test_removes_sections_containing_project_number(self):
        from utils.pdf_parsing.extractor.section_extractor import SectionUtil
        sections = [
            SectionUtil(title="1. DOC-001 Reference", start_pos=0, start_content_pos=10),
            SectionUtil(title="2. Introduction", start_pos=20, start_content_pos=30),
        ]
        result = SectionExtractor._remove_non_valid_sections(
            raw_sections=sections, project_number="DOC-001"
        )
        titles = [r.title for r in result]
        assert "1. DOC-001 Reference" not in titles
        assert "2. Introduction" in titles
