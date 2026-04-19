from typing import Optional

from pydantic import BaseModel


class FederatedDataDTO(BaseModel):
    new_adapter_path: str
    latest_adapter_path: str