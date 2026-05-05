import os

os.environ.setdefault("KEYCLOAK_URL", "http://keycloak.test")
os.environ.setdefault("REALM_NAME", "TestRealm")

import pytest
from unittest.mock import AsyncMock

from entities import InstituteModel
from schemas.institute import InstituteDTO, InstituteCreationRequestDTO, InstituteUpdateRequestDTO
from clients.schemas import InstituteTrainingParticipationDTO as ClientInstituteTrainingParticipationDTO


@pytest.fixture()
def institute_model_factory():
    def _factory(
        id: int = 1,
        name: str = "TestInstitute",
        url: str = "http://test.local",
        deletable: bool = True,
        updatable: bool = True,
    ) -> InstituteModel:
        model = InstituteModel()
        model.id = id
        model.name = name
        model.url = url
        model.deletable = deletable
        model.updatable = updatable
        return model

    return _factory


@pytest.fixture()
def mock_institute_repository():
    return AsyncMock()


@pytest.fixture()
def mock_institute_node_client():
    return AsyncMock()


@pytest.fixture()
def mock_db_session():
    return AsyncMock()
