from pydantic import BaseModel, ConfigDict

class ModelPathDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    model_base_path: str
    model_adapter_path: str