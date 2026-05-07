from commons.documents import ParsedDocument, ParsedSection


class TestParsedSection:
    def test_can_be_created(self):
        section = ParsedSection(title="1. Intro", content="Some content")
        assert section.title == "1. Intro"
        assert section.content == "Some content"

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ParsedSection)


class TestParsedDocument:
    def test_can_be_created(self):
        sections = [ParsedSection(title="1. Intro", content="Content")]
        doc = ParsedDocument(number="DOC-001", title="My Project", sections=sections)
        assert doc.number == "DOC-001"
        assert doc.title == "My Project"
        assert len(doc.sections) == 1

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ParsedDocument)

    def test_empty_sections(self):
        doc = ParsedDocument(number="DOC-001", title="My Project", sections=[])
        assert doc.sections == []


class TestCommonsDocumentsInit:
    def test_exports_parsed_document(self):
        from commons.documents import ParsedDocument as PD
        assert PD is ParsedDocument

    def test_exports_parsed_section(self):
        from commons.documents import ParsedSection as PS
        assert PS is ParsedSection

    def test_all_list(self):
        import commons.documents as cd
        assert "ParsedDocument" in cd.__all__
        assert "ParsedSection" in cd.__all__
