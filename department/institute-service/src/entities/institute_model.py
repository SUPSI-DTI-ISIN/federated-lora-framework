from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel

class InstituteModel(BaseModel):
    __tablename__ = "institutes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(36), nullable=False, index=True, unique=True)
    url: Mapped[str] = mapped_column(String(25), nullable=False)
    deletable: Mapped[bool] = mapped_column(Boolean)
    updatable: Mapped[bool] = mapped_column(Boolean)