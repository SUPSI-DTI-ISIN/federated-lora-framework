from sqlalchemy import Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import BaseModel
from .message_role import MessageRole

class MessageModel(BaseModel):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)

    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    model_key: Mapped[str] = mapped_column(String, nullable=True)
    adapter_version: Mapped[str] = mapped_column(String, nullable=True)

    chat = relationship("ChatModel", back_populates="messages", lazy="select")