from pydantic import BaseModel


class InstituteTrainingParticipationDTO(BaseModel):
    institute_name: str
    trainable_samples_number: int