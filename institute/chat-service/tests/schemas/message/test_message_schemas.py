import pytest
from datetime import datetime, timezone

from entities import MessageRole
from schemas.message import MessageDTO, MessageCreationRequestDTO, InferenceRequestDTO


class TestMessageDTO:
    def _make_dto(self, **kwargs):
        defaults = dict(
            id=1,
            chat_id=10,
            role="user",
            content="Hello",
            model_key="model-v1",
            adapter_version=2,
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        defaults.update(kwargs)
        return MessageDTO(**defaults)

    def test_valid_dto(self):
        dto = self._make_dto()
        assert dto.id == 1
        assert dto.chat_id == 10
        assert dto.role == "user"
        assert dto.content == "Hello"
        assert dto.model_key == "model-v1"
        assert dto.adapter_version == 2

    def test_adapter_version_can_be_none(self):
        dto = self._make_dto(adapter_version=None)
        assert dto.adapter_version is None

    def test_from_attributes(self):
        from entities import MessageModel
        msg = MessageModel()
        msg.id = 3
        msg.chat_id = 7
        msg.role = MessageRole.ASSISTANT
        msg.content = "Hi there"
        msg.model_key = "model-v2"
        msg.adapter_version = None
        msg.created_at = datetime(2024, 3, 1, tzinfo=timezone.utc)

        dto = MessageDTO.model_validate(msg)
        assert dto.id == 3
        assert dto.chat_id == 7
        assert dto.content == "Hi there"


class TestMessageCreationRequestDTO:
    def test_valid_dto(self):
        dto = MessageCreationRequestDTO(
            chat_id=1,
            role=MessageRole.USER,
            content="Hello",
            model_key="model-v1",
            adapter_version=1,
        )
        assert dto.chat_id == 1
        assert dto.role == MessageRole.USER
        assert dto.content == "Hello"

    def test_adapter_version_can_be_none(self):
        dto = MessageCreationRequestDTO(
            chat_id=1,
            role=MessageRole.USER,
            content="Hello",
            model_key="model-v1",
            adapter_version=None,
        )
        assert dto.adapter_version is None

    def test_missing_required_field_raises(self):
        with pytest.raises(Exception):
            MessageCreationRequestDTO(role=MessageRole.USER, content="Hello", model_key="k")


class TestInferenceRequestDTO:
    def test_valid_dto(self):
        dto = InferenceRequestDTO(model_key="model-v1", adapter_version=1, prompt="What is AI?")
        assert dto.model_key == "model-v1"
        assert dto.adapter_version == 1
        assert dto.prompt == "What is AI?"

    def test_adapter_version_can_be_none(self):
        dto = InferenceRequestDTO(model_key="model-v1", adapter_version=None, prompt="Hello")
        assert dto.adapter_version is None

    def test_missing_prompt_raises(self):
        with pytest.raises(Exception):
            InferenceRequestDTO(model_key="model-v1", adapter_version=1)


class TestSchemaMessageInit:
    def test_exports_message_dto(self):
        from schemas.message import MessageDTO as D
        assert D is MessageDTO

    def test_exports_message_creation_request_dto(self):
        from schemas.message import MessageCreationRequestDTO as D
        assert D is MessageCreationRequestDTO

    def test_exports_inference_request_dto(self):
        from schemas.message import InferenceRequestDTO as D
        assert D is InferenceRequestDTO

    def test_version(self):
        import schemas.message as sm
        assert sm.__version__ == "1.0.0"
