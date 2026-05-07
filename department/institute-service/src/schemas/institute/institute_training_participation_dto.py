from typing import Optional

from pydantic import BaseModel

class InstituteTrainingParticipationDTO(BaseModel):
    id: int
    institute_name: str
    trainable_samples_number: Optional[int]
    is_reachable: bool