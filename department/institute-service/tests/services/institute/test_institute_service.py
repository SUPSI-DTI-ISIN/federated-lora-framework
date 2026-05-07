import pytest
from unittest.mock import AsyncMock

from entities import InstituteModel
from schemas.institute import (
    InstituteDTO,
    InstituteCreationRequestDTO,
    InstituteUpdateRequestDTO,
)
from schemas.exceptions.institute_errors import (
    InstituteNotFoundError,
    InstituteNameNotFoundError,
    InstituteCannotBeDeletedError,
    InstituteCannotBeUpdatedError,
    InstituteUnreachableError,
)
from clients.schemas import InstituteTrainingParticipationDTO as ClientDTO
from services.institute.institute_service import InstituteService


def _model(id=1, name="Inst", url="http://inst.local", deletable=True, updatable=True):
    m = InstituteModel()
    m.id = id
    m.name = name
    m.url = url
    m.deletable = deletable
    m.updatable = updatable
    return m


@pytest.fixture()
def repo():
    return AsyncMock()


@pytest.fixture()
def node_client():
    return AsyncMock()


@pytest.fixture()
def service(repo, node_client):
    return InstituteService(
        institute_repository=repo,
        institute_node_client=node_client,
        department_realm_name="Department",
    )


class TestCreateNewInstitute:
    async def test_creates_and_returns_dto(self, service, repo):
        saved = _model(id=10, name="New", url="http://new.local")
        repo.save = AsyncMock(return_value=saved)

        dto = await service.create_new_institute(InstituteCreationRequestDTO(name="New", url="http://new.local"))

        repo.save.assert_awaited_once()
        assert isinstance(dto, InstituteDTO)
        assert dto.id == 10
        assert dto.name == "New"

    async def test_passes_all_fields_to_model(self, service, repo):
        saved = _model(id=1, name="X", url="http://x.local", deletable=False, updatable=False)
        repo.save = AsyncMock(return_value=saved)

        await service.create_new_institute(
            InstituteCreationRequestDTO(name="X", url="http://x.local", deletable=False, updatable=False)
        )

        call_arg: InstituteModel = repo.save.call_args.kwargs["institute_model"]
        assert call_arg.name == "X"
        assert call_arg.deletable is False
        assert call_arg.updatable is False


class TestUpdateInstitute:
    async def test_updates_name_and_url(self, service, repo):
        existing = _model(id=1, name="Old", url="http://old.local")
        updated = _model(id=1, name="New", url="http://new.local")
        repo.get_by_id = AsyncMock(return_value=existing)
        repo.save = AsyncMock(return_value=updated)

        dto = await service.update_institute(
            institute_id=1,
            institute_update_request_dto=InstituteUpdateRequestDTO(name="New", url="http://new.local"),
        )

        assert dto.name == "New"
        assert dto.url == "http://new.local"

    async def test_keeps_existing_values_when_fields_are_none(self, service, repo):
        existing = _model(id=1, name="Keep", url="http://old.local")
        repo.get_by_id = AsyncMock(return_value=existing)
        repo.save = AsyncMock(return_value=existing)

        await service.update_institute(
            institute_id=1,
            institute_update_request_dto=InstituteUpdateRequestDTO(name=None, url=None),
        )

        assert existing.name == "Keep"
        assert existing.url == "http://old.local"

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(InstituteNotFoundError):
            await service.update_institute(
                institute_id=99,
                institute_update_request_dto=InstituteUpdateRequestDTO(),
            )

    async def test_raises_cannot_be_updated_when_not_updatable(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=_model(id=1, updatable=False))

        with pytest.raises(InstituteCannotBeUpdatedError):
            await service.update_institute(
                institute_id=1,
                institute_update_request_dto=InstituteUpdateRequestDTO(name="X"),
            )


class TestGetAll:
    async def test_returns_list_of_dtos(self, service, repo):
        repo.get_all = AsyncMock(return_value=[_model(id=1), _model(id=2, name="B")])

        result = await service.get_all()

        assert len(result) == 2
        assert all(isinstance(d, InstituteDTO) for d in result)

    async def test_returns_empty_list(self, service, repo):
        repo.get_all = AsyncMock(return_value=[])

        assert await service.get_all() == []


class TestGetById:
    async def test_returns_dto_when_found(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=_model(id=5))

        assert (await service.get_by_id(institute_id=5)).id == 5

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(InstituteNotFoundError):
            await service.get_by_id(institute_id=999)


class TestGetByName:
    async def test_returns_dto_when_found(self, service, repo):
        repo.get_by_name = AsyncMock(return_value=_model(name="Alpha"))

        assert (await service.get_by_name(institute_name="Alpha")).name == "Alpha"

    async def test_raises_name_not_found_when_missing(self, service, repo):
        repo.get_by_name = AsyncMock(return_value=None)

        with pytest.raises(InstituteNameNotFoundError):
            await service.get_by_name(institute_name="Ghost")


class TestDeleteInstituteById:
    async def test_deletes_successfully(self, service, repo):
        model = _model(id=1, deletable=True)
        repo.get_by_id = AsyncMock(return_value=model)

        await service.delete_institute_by_id(institute_id=1)

        repo.delete_institute_by_id.assert_awaited_once_with(institute_model=model)

    async def test_raises_not_found_when_missing(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(InstituteNotFoundError):
            await service.delete_institute_by_id(institute_id=99)

    async def test_raises_cannot_be_deleted_when_not_deletable(self, service, repo):
        repo.get_by_id = AsyncMock(return_value=_model(id=1, deletable=False))

        with pytest.raises(InstituteCannotBeDeletedError):
            await service.delete_institute_by_id(institute_id=1)


class TestGetInstitutesTrainingParticipation:
    async def test_skips_department_realm(self, service, repo, node_client):
        repo.get_all = AsyncMock(return_value=[_model(id=1, name="Department")])

        result = await service.get_institutes_training_participation()

        assert result == []
        node_client.get_institute_training_participation.assert_not_awaited()

    async def test_reachable_institute_included_with_data(self, service, repo, node_client):
        repo.get_all = AsyncMock(return_value=[_model(id=2, name="Alpha", url="http://alpha.local")])
        node_client.get_institute_training_participation = AsyncMock(
            return_value=ClientDTO(institute_name="Alpha", trainable_samples_number=100)
        )

        result = await service.get_institutes_training_participation()

        assert len(result) == 1
        assert result[0].is_reachable is True
        assert result[0].trainable_samples_number == 100
        assert result[0].institute_name == "Alpha"

    async def test_unreachable_institute_included_with_flag_false(self, service, repo, node_client):
        repo.get_all = AsyncMock(return_value=[_model(id=3, name="Beta", url="http://beta.local")])
        node_client.get_institute_training_participation = AsyncMock(
            side_effect=InstituteUnreachableError(institute_url="http://beta.local")
        )

        result = await service.get_institutes_training_participation()

        assert len(result) == 1
        assert result[0].is_reachable is False
        assert result[0].trainable_samples_number is None
        assert result[0].institute_name == "Beta"

    async def test_mixed_reachable_and_unreachable(self, service, repo, node_client):
        repo.get_all = AsyncMock(return_value=[
            _model(id=2, name="Alpha", url="http://alpha.local"),
            _model(id=3, name="Beta", url="http://beta.local"),
        ])
        node_client.get_institute_training_participation = AsyncMock(side_effect=[
            ClientDTO(institute_name="Alpha", trainable_samples_number=50),
            InstituteUnreachableError(institute_url="http://beta.local"),
        ])

        result = await service.get_institutes_training_participation()

        assert len(result) == 2
        assert sum(1 for r in result if r.is_reachable) == 1
        assert sum(1 for r in result if not r.is_reachable) == 1

    async def test_empty_institutes_list(self, service, repo):
        repo.get_all = AsyncMock(return_value=[])

        assert await service.get_institutes_training_participation() == []
