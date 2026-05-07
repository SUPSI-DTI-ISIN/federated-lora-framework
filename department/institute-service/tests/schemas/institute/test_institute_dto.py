import pytest
from pydantic import ValidationError

from schemas.institute.institute_dto import InstituteDTO


class TestInstituteDTO:
    def test_valid_construction(self):
        dto = InstituteDTO(id=1, name="A", url="http://a.local", deletable=True, updatable=False)
        assert dto.id == 1
        assert dto.name == "A"
        assert dto.url == "http://a.local"
        assert dto.deletable is True
        assert dto.updatable is False

    def test_model_validate_from_orm_object(self):
        class FakeOrm:
            id = 5
            name = "ORM"
            url = "http://orm.local"
            deletable = False
            updatable = True

        dto = InstituteDTO.model_validate(FakeOrm())
        assert dto.id == 5
        assert dto.name == "ORM"

    def test_missing_required_field_raises(self):
        with pytest.raises(ValidationError):
            InstituteDTO(name="A", url="http://a.local", deletable=True, updatable=True)
