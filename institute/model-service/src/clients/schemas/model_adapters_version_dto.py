from typing import List, Optional

from pydantic import BaseModel


class ModelAdaptersVersionDTO(BaseModel):
    model_key: str
    adapters_version: Optional[List[int]] = None