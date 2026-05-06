from utils.pdf_parsing.extractor.section_extractor import SectionExtractor


class TestSectionExtractorSubSectionEmptyTitle:
    def test_skips_subsection_with_empty_title(self):
        """Covers line 80: the continue when title is empty for num2 pattern."""
        # A subsection pattern (num2) with empty title after the number
        text = "1.1 \n2. Valid Section\nContent here\n"
        raw = SectionExtractor._get_raw_sections(text)
        titles = [r.title for r in raw]
        # "1.1 " has empty title after stripping, should be skipped
        assert not any(t.strip() == "1.1" for t in titles)
        # "2. Valid Section" should be present
        assert any("Valid Section" in t for t in titles)
