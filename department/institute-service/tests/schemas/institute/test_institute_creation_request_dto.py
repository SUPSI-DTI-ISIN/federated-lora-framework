import pytest
from pydantic import ValidationError

from schemas.institute.institute_creation_request_dto import InstituteCreationRequestDTO


class TestInstituteCreationRequestDTO:
    def test_defaults_for_optional_fields(self):
        dto = InstituteCreationRequestDTO(name="Inst", url="http://inst.local")
        assert dto.deletable is True
        assert dto.updatable is True

    @pytest.mark.parametrize("deletable,updatable", [
        (False, False),
        (True, False),
        (False, True),
    ])
    def test_explicit_optional_fields(self, deletable, updatable):
        dto = InstituteCreationRequestDTO(name="X", url="http://x.local", deletable=deletable, updatable=updatable)
        assert dto.deletable is deletable
        assert dto.updatable is updatable

    @pytest.mark.parametrize("payload", [
        {"url": "http://x.local"},
        {"name": "X"},
        {},
    ])
    def test_missing_required_field_raises(self, payload):
        with pytest.raises(ValidationError):
            InstituteCreationRequestDTO(**payload)
