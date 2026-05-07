from abc import ABC, abstractmethod

from clients.schemas import InstituteTrainingParticipationDTO


class InstituteNodeClientInterface(ABC):
    @abstractmethod
    async def get_institute_training_participation(self, institute_base_url: str) -> InstituteTrainingParticipationDTO:
        raise NotImplementedError