from schemas.exceptions.chat_errors import ChatNotFoundError
from schemas.exceptions.inference_error import InferenceRequestError


class TestChatNotFoundError:
    def test_stores_chat_id(self):
        assert ChatNotFoundError(chat_id=42).chat_id == 42

    def test_message_contains_id(self):
        assert "42" in str(ChatNotFoundError(chat_id=42))

    def test_is_exception_subclass(self):
        assert issubclass(ChatNotFoundError, Exception)


class TestInferenceRequestError:
    def test_stores_detailed_err(self):
        assert InferenceRequestError(detailed_err="timeout").detailed_err == "timeout"

    def test_message_contains_detail(self):
        assert "timeout" in str(InferenceRequestError(detailed_err="timeout"))

    def test_is_exception_subclass(self):
        assert issubclass(InferenceRequestError, Exception)


class TestSchemasExceptionsInit:
    def test_exports_chat_not_found_error(self):
        from schemas.exceptions import ChatNotFoundError as E
        assert E is ChatNotFoundError

    def test_exports_inference_request_error(self):
        from schemas.exceptions import InferenceRequestError as E
        assert E is InferenceRequestError

    def test_version(self):
        import schemas.exceptions as se
        assert se.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.exceptions as se
        assert "ChatNotFoundError" in se.__all__
        assert "InferenceRequestError" in se.__all__
