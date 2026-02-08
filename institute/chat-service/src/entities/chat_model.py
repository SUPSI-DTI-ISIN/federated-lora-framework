from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import BaseModel

class ChatModel(BaseModel):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)

    messages = relationship(
        "MessageModel",
        back_populates="chat",
        cascade="all, delete-orphan",
        lazy="noload"
    )
