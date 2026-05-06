from schemas.exceptions import (
    DocumentNotFoundError,
    DocumentAlreadyExistsError,
    InvalidFileError,
    SectionNotFoundError,
    ExtractorError,
)


class TestDocumentNotFoundError:
    def test_stores_document_id(self):
        assert DocumentNotFoundError(document_id=42).document_id == 42

    def test_message_contains_id(self):
        assert "42" in str(DocumentNotFoundError(document_id=42))

    def test_is_exception_subclass(self):
        assert issubclass(DocumentNotFoundError, Exception)


class TestDocumentAlreadyExistsError:
    def test_stores_document_id(self):
        assert DocumentAlreadyExistsError(document_id=7).document_id == 7

    def test_message_contains_id(self):
        assert "7" in str(DocumentAlreadyExistsError(document_id=7))

    def test_is_exception_subclass(self):
        assert issubclass(DocumentAlreadyExistsError, Exception)


class TestInvalidFileError:
    def test_message_is_stored(self):
        assert "bad file" in str(InvalidFileError(message="bad file"))

    def test_is_exception_subclass(self):
        assert issubclass(InvalidFileError, Exception)


class TestSectionNotFoundError:
    def test_stores_section_id(self):
        assert SectionNotFoundError(section_id=99).section_id == 99

    def test_message_contains_id(self):
        assert "99" in str(SectionNotFoundError(section_id=99))

    def test_is_exception_subclass(self):
        assert issubclass(SectionNotFoundError, Exception)


class TestExtractorError:
    def test_message_is_stored(self):
        assert "parse failed" in str(ExtractorError(message="parse failed"))

    def test_is_exception_subclass(self):
        assert issubclass(ExtractorError, Exception)


class TestSchemasExceptionsInit:
    def test_exports_all_errors(self):
        import schemas.exceptions as se
        assert "DocumentNotFoundError" in se.__all__
        assert "DocumentAlreadyExistsError" in se.__all__
        assert "InvalidFileError" in se.__all__
        assert "SectionNotFoundError" in se.__all__
        assert "ExtractorError" in se.__all__

    def test_version(self):
        import schemas.exceptions as se
        assert se.__version__ == "1.0.0"
