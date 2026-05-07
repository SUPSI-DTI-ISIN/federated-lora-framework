import pytest
from clients.schemas import QueryRequestDTO, QueryResponseDTO
from clients.schemas.conversation_dto import ConversationDTO


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


class TestQueryRequestDTO:
    def test_valid_dto(self):
        from schemas.chat import ConversationDTO as ChatConversationDTO
        dto = QueryRequestDTO(
            user_id="u-1",
            chat_id=1,
            model_key="model-v1",
            adapter_version=1,
            prompt="Hello",
            conversation_history=[ChatConversationDTO(role="user", content="Hi")],
        )
        assert dto.user_id == "u-1"
        assert dto.chat_id == 1
        assert len(dto.conversation_history) == 1

    def test_adapter_version_can_be_none(self):
        dto = QueryRequestDTO(
            user_id="u-1",
            chat_id=1,
            model_key="model-v1",
            adapter_version=None,
            prompt="Hello",
            conversation_history=[],
        )
        assert dto.adapter_version is None

    def test_empty_conversation_history(self):
        dto = QueryRequestDTO(
            user_id="u-1",
            chat_id=1,
            model_key="model-v1",
            adapter_version=1,
            prompt="Hello",
            conversation_history=[],
        )
        assert dto.conversation_history == []


class TestQueryResponseDTO:
    def test_valid_dto(self):
        dto = QueryResponseDTO(
            prompt="Hello",
            response="Hi",
            model_key="model-v1",
            adapter_version=2,
        )
        assert dto.prompt == "Hello"
        assert dto.response == "Hi"

    def test_adapter_version_can_be_none(self):
        dto = QueryResponseDTO(
            prompt="Hello",
            response="Hi",
            model_key="model-v1",
            adapter_version=None,
        )
        assert dto.adapter_version is None


class TestClientSchemasInit:
    def test_exports_query_request_dto(self):
        from clients.schemas import QueryRequestDTO as D
        assert D is QueryRequestDTO

    def test_exports_query_response_dto(self):
        from clients.schemas import QueryResponseDTO as D
        assert D is QueryResponseDTO

    def test_version(self):
        import clients.schemas as cs
        assert cs.__version__ == "1.0.0"
