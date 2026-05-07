import pytest
from unittest.mock import AsyncMock

from models import SectionModel
from schemas.documents import SectionDTO, UpdateSectionRequestDTO
from schemas.exceptions import SectionNotFoundError
from services.sections.sections_service import SectionsService


def _section_model(id=1, title="1. Intro", content="Content"):
    m = SectionModel()
    m.id = id
    m.document_id = 10
    m.title = title
    m.content = content
    return m


@pytest.fixture()
def repo():
    return AsyncMock()


@pytest.fixture()
def service(repo):
    return SectionsService(sections_repository=repo)


class TestDeleteById:
    async def test_deletes_successfully(self, service, repo):
        section = _section_model(id=1)
        repo.get_by_id = AsyncMock(return_value=section)

        await service.delete_by_id(section_id=1)

        repo.delete_section.assert_awaited_once_with(section_model=section)

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(SectionNotFoundError) as exc_info:
            await service.delete_by_id(section_id=99)

        assert exc_info.value.section_id == 99


class TestUpdateSectionContent:
    async def test_updates_and_returns_dto(self, service, repo):
        section = _section_model(id=1, content="Old content")
        updated = _section_model(id=1, content="New content")
        repo.get_by_id = AsyncMock(return_value=section)
        repo.save_section = AsyncMock(return_value=updated)

        dto = await service.update_section_content(
            section_id=1,
            update_section_content_request_dto=UpdateSectionRequestDTO(updated_content="New content")
        )

        assert isinstance(dto, SectionDTO)
        assert dto.content == "New content"
        assert section.content == "New content"

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(SectionNotFoundError) as exc_info:
            await service.update_section_content(
                section_id=99,
                update_section_content_request_dto=UpdateSectionRequestDTO(updated_content="New")
            )

        assert exc_info.value.section_id == 99
