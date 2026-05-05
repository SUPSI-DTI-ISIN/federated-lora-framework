from unittest.mock import AsyncMock

from services.institute.dependencies import get_institute_service, build_institute_service
from services.institute.institute_service_interface import InstituteServiceInterface


class TestGetInstituteService:
    def test_returns_institute_service_interface(self):
        assert isinstance(
            get_institute_service(
                institute_repository=AsyncMock(),
                institute_node_client=AsyncMock(),
                department_realm_name="TestRealm",
            ),
            InstituteServiceInterface,
        )

    def test_institute_init_exports(self):
        from services.institute import InstituteServiceInterface, get_institute_service as fn
        assert InstituteServiceInterface is not None
        assert fn is not None

    def test_institute_init_version(self):
        import services.institute as si
        assert si.__version__ == "1.0.0"


class TestBuildInstituteService:
    def test_returns_institute_service_interface(self):
        assert isinstance(
            build_institute_service(
                institute_repository=AsyncMock(),
                institute_node_client=AsyncMock(),
                department_realm_name="TestRealm",
            ),
            InstituteServiceInterface,
        )
