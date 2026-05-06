from unittest.mock import AsyncMock

from repositories.sections.dependencies import get_sections_repository
from repositories.sections.sections_repository import SectionsRepository


class TestGetSectionsRepository:
    def test_returns_sections_repository_instance(self):
        mock_session = AsyncMock()
        repo = get_sections_repository(db=mock_session)
        assert isinstance(repo, SectionsRepository)
