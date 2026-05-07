import pytest
from schemas.inference import QueryRequestDTO, QueryResponseDTO, ConversationDTO


class TestConversationDTO:
    def test_valid(self):
        dto = ConversationDTO(role="user", content="Hello")
        assert dto.role == "user"
        assert dto.content == "Hello"

    def test_missing_field_raises(self):
        with pytest.raises(Exception):
            ConversationDTO(role="user")


class TestQueryRequestDTO:
    def _make(self, **kwargs):
        defaults = dict(
            user_id="u-1", chat_id=1, model_key="llama-3",
            adapter_version=None, prompt="Hello", conversation_history=[],
        )
        defaults.update(kwargs)
        return QueryRequestDTO(**defaults)

    def test_valid(self):
        dto = self._make()
        assert dto.user_id == "u-1"
        assert dto.chat_id == 1
        assert dto.model_key == "llama-3"
        assert dto.adapter_version is None
        assert dto.prompt == "Hello"
        assert dto.conversation_history == []

    def test_with_adapter_version(self):
        dto = self._make(adapter_version=3)
        assert dto.adapter_version == 3

    def test_with_conversation_history(self):
        history = [ConversationDTO(role="user", content="Hi")]
        dto = self._make(conversation_history=history)
        assert len(dto.conversation_history) == 1

    def test_json_roundtrip(self):
        dto = self._make(prompt="What is AI?")
        restored = QueryRequestDTO.model_validate_json(dto.model_dump_json())
        assert restored.prompt == "What is AI?"

    def test_missing_required_field_raises(self):
        with pytest.raises(Exception):
            QueryRequestDTO(chat_id=1, model_key="k", prompt="p", conversation_history=[])


class TestQueryResponseDTO:
    def _make(self, **kwargs):
        defaults = dict(
            user_id="u-1", chat_id=1, prompt="Hello",
            response="Hi", model_key="llama-3", adapter_version=None,
        )
        defaults.update(kwargs)
        return QueryResponseDTO(**defaults)

    def test_valid(self):
        dto = self._make()
        assert dto.user_id == "u-1"
        assert dto.response == "Hi"

    def test_adapter_version_can_be_set(self):
        dto = self._make(adapter_version=2)
        assert dto.adapter_version == 2

    def test_json_roundtrip(self):
        dto = self._make(response="The answer is 42")
        restored = QueryResponseDTO.model_validate_json(dto.model_dump_json())
        assert restored.response == "The answer is 42"


class TestSchemaInferenceInit:
    def test_exports(self):
        import schemas.inference as si
        assert "QueryRequestDTO" in si.__all__
        assert "QueryResponseDTO" in si.__all__
        assert "ConversationDTO" in si.__all__

    def test_version(self):
        import schemas.inference as si
        assert si.__version__ == "1.0.0"
