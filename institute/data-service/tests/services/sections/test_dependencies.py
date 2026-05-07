from unittest.mock import AsyncMock

from services.sections.dependencies import get_sections_service
from services.sections.sections_service import SectionsService


class TestGetSectionsService:
    def test_returns_sections_service_instance(self):
        mock_repo = AsyncMock()
        service = get_sections_service(sections_repository=mock_repo)
        assert isinstance(service, SectionsService)
