from utils.pdf_parsing.extractor.section_extractor import SectionExtractor


class TestSectionExtractorSubSectionEmptyTitle:
    def test_skips_subsection_with_empty_title(self):
        """Covers line 80: the continue when title is empty for num2 pattern."""
        text = "1.1 \n2. Valid Section\nContent here\n"
        raw = SectionExtractor._get_raw_sections(text)
        titles = [r.title for r in raw]
        assert not any(t.strip() == "1.1" for t in titles)
        assert any("Valid Section" in t for t in titles)
