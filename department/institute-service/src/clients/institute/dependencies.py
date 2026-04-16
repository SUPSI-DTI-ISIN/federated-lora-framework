
from .institute_node_client import InstituteNodeClient
from .institute_node_client_interface import InstituteNodeClientInterface

def get_institute_node_client() -> InstituteNodeClientInterface:
    return InstituteNodeClient.get_instance()