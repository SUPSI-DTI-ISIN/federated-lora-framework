import pytest

from schemas.institute.institute_update_request_dto import InstituteUpdateRequestDTO


class TestInstituteUpdateRequestDTO:
    def test_all_fields_default_to_none(self):
        dto = InstituteUpdateRequestDTO()
        assert dto.name is None
        assert dto.url is None

    @pytest.mark.parametrize("name,url", [
        ("NewName", None),
        (None, "http://new.local"),
        ("NewName", "http://new.local"),
    ])
    def test_partial_and_full_updates(self, name, url):
        dto = InstituteUpdateRequestDTO(name=name, url=url)
        assert dto.name == name
        assert dto.url == url
