from typing import List

from pydantic import BaseModel


class NewAdapterPathDTO(BaseModel):
    new_adapter_path: str