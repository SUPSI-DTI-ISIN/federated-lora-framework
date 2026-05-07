import pytest
from datetime import datetime, timezone

from schemas.chat import ChatDTO, ChatCreationRequestDTO, ConversationDTO


class TestChatDTO:
    def _make_dto(self, **kwargs):
        defaults = dict(
            id=1,
            user_id="user-abc",
            title="My Chat",
            is_doing_inference=False,
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        defaults.update(kwargs)
        return ChatDTO(**defaults)

    def test_valid_dto(self):
        dto = self._make_dto()
        assert dto.id == 1
        assert dto.user_id == "user-abc"
        assert dto.title == "My Chat"
        assert dto.is_doing_inference is False

    def test_title_can_be_none(self):
        dto = self._make_dto(title=None)
        assert dto.title is None

    def test_from_attributes(self):
        from entities import ChatModel
        chat = ChatModel()
        chat.id = 5
        chat.user_id = "u-1"
        chat.title = "Test"
        chat.is_doing_inference = True
        chat.created_at = datetime(2024, 6, 1, tzinfo=timezone.utc)
        chat.updated_at = datetime(2024, 6, 1, tzinfo=timezone.utc)

        dto = ChatDTO.model_validate(chat)
        assert dto.id == 5
        assert dto.user_id == "u-1"
        assert dto.is_doing_inference is True


class TestChatCreationRequestDTO:
    def test_title_defaults_to_none(self):
        dto = ChatCreationRequestDTO()
        assert dto.title is None

    def test_title_can_be_set(self):
        dto = ChatCreationRequestDTO(title="New Chat")
        assert dto.title == "New Chat"


class TestConversationDTO:
    def test_valid_dto(self):
        dto = ConversationDTO(role="user", content="Hello")
        assert dto.role == "user"
        assert dto.content == "Hello"

    def test_missing_role_raises(self):
        with pytest.raises(Exception):
            ConversationDTO(content="Hello")

    def test_missing_content_raises(self):
        with pytest.raises(Exception):
            ConversationDTO(role="user")


class TestSchemaChatInit:
    def test_exports_chat_dto(self):
        from schemas.chat import ChatDTO as D
        assert D is ChatDTO

    def test_exports_chat_creation_request_dto(self):
        from schemas.chat import ChatCreationRequestDTO as D
        assert D is ChatCreationRequestDTO

    def test_exports_conversation_dto(self):
        from schemas.chat import ConversationDTO as D
        assert D is ConversationDTO

    def test_version(self):
        import schemas.chat as sc
        assert sc.__version__ == "1.0.0"
