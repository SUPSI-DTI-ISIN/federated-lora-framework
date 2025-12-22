from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

class DocumentModel(BaseModel):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))

    sections: Mapped[List["SectionModel"]] = relationship(
        back_populates="document", cascade="all, delete-orphan", lazy="selectin"
    )