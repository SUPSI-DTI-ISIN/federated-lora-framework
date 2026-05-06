from unittest.mock import MagicMock, patch
from utils.model_response_utils import ModelResponseUtils


class TestGenerateModelResponse:
    def test_returns_new_tokens_only(self):
        """Verifies that only the generated tokens (after input) are returned."""
        model = MagicMock()
        model.device = "cpu"
        tokenizer = MagicMock()
        tokenizer.eos_token_id = 2
        tokenizer.pad_token_id = 0

        mock_input_tensor = MagicMock()
        mock_input_tensor.shape = (1, 3)

        mock_output = MagicMock()
        mock_output.__getitem__ = MagicMock(return_value=MagicMock(
            __getitem__=MagicMock(return_value=MagicMock(tolist=MagicMock(return_value=[4, 5])))
        ))
        model.generate.return_value = mock_output

        with patch("utils.model_response_utils.torch.tensor", return_value=mock_input_tensor), \
             patch("utils.model_response_utils.torch.ones_like", return_value=MagicMock()), \
             patch("utils.model_response_utils.torch.no_grad") as mock_no_grad:
            mock_no_grad.return_value.__enter__ = MagicMock(return_value=None)
            mock_no_grad.return_value.__exit__ = MagicMock(return_value=False)

            result = ModelResponseUtils.generate_model_response(
                prompt_ids=[1, 2, 3],
                model=model,
                tokenizer=tokenizer,
            )

        model.generate.assert_called_once()
        call_kwargs = model.generate.call_args.kwargs
        assert call_kwargs["max_new_tokens"] == 512
        assert call_kwargs["do_sample"] is True
        assert call_kwargs["temperature"] == 0.7
        assert call_kwargs["top_p"] == 0.9

    def test_uses_eos_token_id_as_pad_when_pad_is_none(self):
        model = MagicMock()
        model.device = "cpu"
        tokenizer = MagicMock()
        tokenizer.eos_token_id = 2
        tokenizer.pad_token_id = None  # pad_token_id is None

        mock_input_tensor = MagicMock()
        mock_input_tensor.shape = (1, 2)

        mock_output = MagicMock()
        mock_output.__getitem__ = MagicMock(return_value=MagicMock(
            __getitem__=MagicMock(return_value=MagicMock(tolist=MagicMock(return_value=[3])))
        ))
        model.generate.return_value = mock_output

        with patch("utils.model_response_utils.torch.tensor", return_value=mock_input_tensor), \
             patch("utils.model_response_utils.torch.ones_like", return_value=MagicMock()), \
             patch("utils.model_response_utils.torch.no_grad") as mock_no_grad:
            mock_no_grad.return_value.__enter__ = MagicMock(return_value=None)
            mock_no_grad.return_value.__exit__ = MagicMock(return_value=False)

            ModelResponseUtils.generate_model_response(
                prompt_ids=[1, 2],
                model=model,
                tokenizer=tokenizer,
            )

        call_kwargs = model.generate.call_args.kwargs
        assert call_kwargs["pad_token_id"] == 2
