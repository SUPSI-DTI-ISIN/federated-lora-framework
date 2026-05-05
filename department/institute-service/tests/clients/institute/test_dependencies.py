import pytest

from clients.institute.dependencies import get_institute_node_client
from clients.institute.institute_node_client_interface import InstituteNodeClientInterface
from clients.institute.institute_node_client import InstituteNodeClient


@pytest.fixture(autouse=True)
def reset_singleton():
    InstituteNodeClient._InstituteNodeClient__INSTANCE = None
    yield
    InstituteNodeClient._InstituteNodeClient__INSTANCE = None


class TestGetInstituteNodeClient:
    def test_returns_institute_node_client_interface(self):
        assert isinstance(get_institute_node_client(), InstituteNodeClientInterface)

    def test_returns_singleton(self):
        assert get_institute_node_client() is get_institute_node_client()

    def test_client_init_exports(self):
        from clients.institute import InstituteNodeClientInterface, get_institute_node_client as fn
        assert InstituteNodeClientInterface is not None
        assert fn is not None

    def test_client_init_version(self):
        import clients.institute as ci
        assert ci.__version__ == "1.0.0"
