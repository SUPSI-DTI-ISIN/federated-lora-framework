from pydantic import BaseModel, ConfigDict

class ModelPathDTO(BaseModel):
    model_base_path: str
    adapter_path: str