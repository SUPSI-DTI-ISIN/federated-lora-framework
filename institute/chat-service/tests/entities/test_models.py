from datetime import datetime, timezone

from entities import ChatModel, MessageModel, MessageRole, BaseModel


class TestChatModel:
    def test_tablename(self):
        assert ChatModel.__tablename__ == "chats"

    def test_can_be_instantiated_with_fields(self):
        chat = ChatModel()
        chat.id = 1
        chat.user_id = "user-abc"
        chat.title = "My Chat"
        chat.is_doing_inference = False
        chat.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        chat.updated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)

        assert chat.id == 1
        assert chat.user_id == "user-abc"
        assert chat.title == "My Chat"
        assert chat.is_doing_inference is False

    def test_title_can_be_none(self):
        chat = ChatModel()
        chat.title = None
        assert chat.title is None

    def test_is_subclass_of_base_model(self):
        assert issubclass(ChatModel, BaseModel)


class TestMessageModel:
    def test_tablename(self):
        assert MessageModel.__tablename__ == "messages"

    def test_can_be_instantiated_with_fields(self):
        msg = MessageModel()
        msg.id = 1
        msg.chat_id = 10
        msg.role = MessageRole.USER
        msg.content = "Hello"
        msg.model_key = "model-v1"
        msg.adapter_version = 2
        msg.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)

        assert msg.id == 1
        assert msg.chat_id == 10
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello"
        assert msg.model_key == "model-v1"
        assert msg.adapter_version == 2

    def test_adapter_version_can_be_none(self):
        msg = MessageModel()
        msg.adapter_version = None
        assert msg.adapter_version is None

    def test_is_subclass_of_base_model(self):
        assert issubclass(MessageModel, BaseModel)


class TestMessageRole:
    def test_user_value(self):
        assert MessageRole.USER.value == "user"

    def test_assistant_value(self):
        assert MessageRole.ASSISTANT.value == "assistant"

    def test_all_members(self):
        assert set(MessageRole.__members__) == {"USER", "ASSISTANT"}


class TestEntitiesInit:
    def test_exports_chat_model(self):
        from entities import ChatModel as CM
        assert CM is ChatModel

    def test_exports_message_model(self):
        from entities import MessageModel as MM
        assert MM is MessageModel

    def test_exports_message_role(self):
        from entities import MessageRole as MR
        assert MR is MessageRole

    def test_exports_base_model(self):
        from entities import BaseModel as BM
        assert BM is BaseModel

    def test_version(self):
        import entities
        assert entities.__version__ == "1.0.0"

    def test_all_list(self):
        import entities
        assert "ChatModel" in entities.__all__
        assert "MessageModel" in entities.__all__
        assert "MessageRole" in entities.__all__
        assert "BaseModel" in entities.__all__
