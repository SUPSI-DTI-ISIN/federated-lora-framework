from typing import Optional

from pydantic import BaseModel


class ModelPathDTO(BaseModel):
    model_base_path: str
    adapter_path: Optional[str] = None