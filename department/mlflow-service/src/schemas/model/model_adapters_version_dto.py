from typing import List

from pydantic import BaseModel


class ModelAdaptersVersion(BaseModel):
    model_key: str
    adapters_version: List[int]