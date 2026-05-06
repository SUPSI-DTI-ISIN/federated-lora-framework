from unittest.mock import MagicMock
import numpy as np
from schemas.inference import ConversationDTO
from utils.tokenizer_utils import TokenizerUtils


class TestPromptToTokensList:
    def test_returns_token_ids_list(self):
        tokenizer = MagicMock()
        tokenizer.return_value = {"input_ids": np.array([[1, 2, 3, 4]])}
        result = TokenizerUtils.prompt_to_tokens_list(prompt="Hello", tokenizer=tokenizer)
        assert result == [1, 2, 3, 4]

    def test_calls_tokenizer_with_prompt(self):
        tokenizer = MagicMock()
        tokenizer.return_value = {"input_ids": np.array([[10, 20]])}
        TokenizerUtils.prompt_to_tokens_list(prompt="Test prompt", tokenizer=tokenizer)
        tokenizer.assert_called_once_with("Test prompt", return_tensors="np")


class TestResponseIdsToStr:
    def test_decodes_token_ids(self):
        tokenizer = MagicMock()
        tokenizer.decode.return_value = "  The answer is 42  "
        result = TokenizerUtils.response_ids_to_str(token_ids=[1, 2, 3], tokenizer=tokenizer)
        assert result == "The answer is 42"

    def test_calls_decode_with_skip_special_tokens(self):
        tokenizer = MagicMock()
        tokenizer.decode.return_value = "response"
        TokenizerUtils.response_ids_to_str(token_ids=[1, 2], tokenizer=tokenizer)
        tokenizer.decode.assert_called_once_with([1, 2], skip_special_tokens=True)


class TestBuildChatPromptToTokensList:
    def test_returns_token_ids(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = [1, 2, 3, 4, 5]

        result = TokenizerUtils.build_chat_prompt_to_tokens_list(
            prompt="What is AI?",
            tokenizer=tokenizer,
            conversation_history=[],
            system_prompt="You are a helpful assistant.",
        )

        assert result == [1, 2, 3, 4, 5]

    def test_includes_system_prompt_in_messages(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = [1]

        TokenizerUtils.build_chat_prompt_to_tokens_list(
            prompt="Hello",
            tokenizer=tokenizer,
            conversation_history=[],
            system_prompt="System instructions here.",
        )

        messages = tokenizer.apply_chat_template.call_args[0][0]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "System instructions here."

    def test_includes_conversation_history(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = [1]
        history = [
            ConversationDTO(role="user", content="Previous question"),
            ConversationDTO(role="assistant", content="Previous answer"),
        ]

        TokenizerUtils.build_chat_prompt_to_tokens_list(
            prompt="New question",
            tokenizer=tokenizer,
            conversation_history=history,
            system_prompt="System.",
        )

        messages = tokenizer.apply_chat_template.call_args[0][0]
        assert len(messages) == 4
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Previous question"
        assert messages[2]["role"] == "assistant"

    def test_appends_user_prompt_last(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = [1]

        TokenizerUtils.build_chat_prompt_to_tokens_list(
            prompt="Final question",
            tokenizer=tokenizer,
            conversation_history=[],
            system_prompt="System.",
        )

        messages = tokenizer.apply_chat_template.call_args[0][0]
        assert messages[-1]["role"] == "user"
        assert messages[-1]["content"] == "Final question"

    def test_calls_apply_chat_template_with_correct_flags(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = [1]

        TokenizerUtils.build_chat_prompt_to_tokens_list(
            prompt="Hello",
            tokenizer=tokenizer,
            conversation_history=[],
            system_prompt="System.",
        )

        call_kwargs = tokenizer.apply_chat_template.call_args.kwargs
        assert call_kwargs["tokenize"] is True
        assert call_kwargs["add_generation_prompt"] is True

    def test_empty_conversation_history(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = [1, 2]

        result = TokenizerUtils.build_chat_prompt_to_tokens_list(
            prompt="Hello",
            tokenizer=tokenizer,
            conversation_history=[],
            system_prompt="System.",
        )

        messages = tokenizer.apply_chat_template.call_args[0][0]
        assert len(messages) == 2
