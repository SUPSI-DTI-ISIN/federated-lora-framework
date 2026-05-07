import requests
from pydantic import ValidationError

from clients.schemas import InstituteTrainingParticipationDTO
from schemas.exceptions import InstituteUnreachableError
from .institute_node_client_interface import InstituteNodeClientInterface


class InstituteNodeClient(InstituteNodeClientInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    async def get_institute_training_participation(self, institute_base_url: str) -> InstituteTrainingParticipationDTO:
        institute_node_url: str = f"{institute_base_url}/api_data/documents/training-samples"
        try:
            resp = requests.get(institute_node_url, headers={"Accept": "application/json"}, timeout=5)
            resp.raise_for_status()
        except (requests.exceptions.HTTPError, requests.RequestException):
            raise InstituteUnreachableError(institute_url=institute_base_url)

        data = resp.json()
        try:
            return InstituteTrainingParticipationDTO.model_validate(data)
        except ValidationError as e:
            raise RuntimeError(f"Invalid response shape: {e}")