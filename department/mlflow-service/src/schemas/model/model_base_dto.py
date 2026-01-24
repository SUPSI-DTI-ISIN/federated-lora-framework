from pydantic import BaseModel


class ModelBaseDTO(BaseModel):
    model_base_artifact_uri: str