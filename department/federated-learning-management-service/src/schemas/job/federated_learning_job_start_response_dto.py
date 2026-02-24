from pydantic import BaseModel


class FederatedLearningJobStartResponseDTO(BaseModel):
    job_id: str