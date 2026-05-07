from unittest.mock import MagicMock
from src.federated_learning_client.services.training.training_service import TrainingService


def _make_tokenizer(full_ids=None, prompt_ids=None):
    """Build a mock tokenizer that returns predictable token IDs."""
    tokenizer = MagicMock()
    tokenizer.apply_chat_template.side_effect = [
        "full text",   # first call: full messages
        "prompt text", # second call: prompt messages
    ]

    def _tokenize(text, **kwargs):
        if text == "full text":
            return {"input_ids": full_ids or [1, 2, 3, 4, 5],
                    "attention_mask": [1] * len(full_ids or [1, 2, 3, 4, 5])}
        return {"input_ids": prompt_ids or [1, 2],
                "attention_mask": [1] * len(prompt_ids or [1, 2])}

    tokenizer.side_effect = _tokenize
    return tokenizer


class TestPreprocess:
    def test_returns_input_ids_attention_masks_and_labels(self):
        tokenizer = _make_tokenizer(full_ids=[1, 2, 3, 4, 5], prompt_ids=[1, 2])
        examples = {
            "instruction": ["sys"],
            "input": ["user"],
            "output": ["assistant"],
        }

        result = TrainingService._TrainingService__preprocess(examples, tokenizer)

        assert "input_ids" in result
        assert "attention_mask" in result
        assert "labels" in result

    def test_labels_mask_prompt_tokens_with_minus_100(self):
        full_ids = [1, 2, 3, 4, 5]
        prompt_ids = [1, 2]
        tokenizer = _make_tokenizer(full_ids=full_ids, prompt_ids=prompt_ids)
        examples = {
            "instruction": ["sys"],
            "input": ["user"],
            "output": ["assistant"],
        }

        result = TrainingService._TrainingService__preprocess(examples, tokenizer)

        labels = result["labels"][0]
        assert labels[:len(prompt_ids)] == [-100, -100]
        assert labels[len(prompt_ids):] == full_ids[len(prompt_ids):]

    def test_processes_multiple_examples(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = "text"
        tokenizer.return_value = {"input_ids": [1, 2, 3], "attention_mask": [1, 1, 1]}

        examples = {
            "instruction": ["sys1", "sys2"],
            "input": ["user1", "user2"],
            "output": ["out1", "out2"],
        }

        result = TrainingService._TrainingService__preprocess(examples, tokenizer)

        assert len(result["input_ids"]) == 2
        assert len(result["attention_mask"]) == 2
        assert len(result["labels"]) == 2

    def test_respects_max_length_truncation(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = "text"
        tokenizer.return_value = {"input_ids": [1, 2, 3], "attention_mask": [1, 1, 1]}

        examples = {
            "instruction": ["sys"],
            "input": ["user"],
            "output": ["out"],
        }

        result = TrainingService._TrainingService__preprocess(examples, tokenizer, max_length=512)
        assert result is not None

    def test_calls_apply_chat_template_twice_per_example(self):
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = "text"
        tokenizer.return_value = {"input_ids": [1, 2], "attention_mask": [1, 1]}

        examples = {
            "instruction": ["sys"],
            "input": ["user"],
            "output": ["out"],
        }

        TrainingService._TrainingService__preprocess(examples, tokenizer)

        assert tokenizer.apply_chat_template.call_count == 2
