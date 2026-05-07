import pytest
from unittest.mock import MagicMock, patch


class TestModelUtils:
    @pytest.fixture(autouse=True)
    def reset_cuda_stubs(self):
        import torch
        torch.cuda.is_available = MagicMock(return_value=False)
        if hasattr(torch.cuda, "is_bf16_supported"):
            del torch.cuda.is_bf16_supported
        yield
        torch.cuda.is_available = MagicMock(return_value=False)
        if hasattr(torch.cuda, "is_bf16_supported"):
            del torch.cuda.is_bf16_supported

    def _fake_model(self):
        m = MagicMock()
        m.config = MagicMock()
        return m

    def test_load_model_passes_correct_kwargs(self):
        from commons.model_utils import ModelUtils
        fake_model = self._fake_model()

        with patch("transformers.AutoModelForCausalLM.from_pretrained", return_value=fake_model) as mock_fp:
            result = ModelUtils.load_model(model_path="/tmp/model", device_map="cpu")

        kwargs = mock_fp.call_args.kwargs
        assert kwargs["device_map"] == "cpu"
        assert kwargs["local_files_only"] is True
        assert kwargs["use_safetensors"] is True
        assert fake_model.config.use_cache is False
        assert result is fake_model

    def test_load_model_uses_float16_when_cuda_unavailable(self):
        import torch
        from commons.model_utils import ModelUtils
        torch.cuda.is_available = MagicMock(return_value=False)

        fake_model = self._fake_model()
        with patch("transformers.AutoModelForCausalLM.from_pretrained", return_value=fake_model):
            result = ModelUtils.load_model(model_path="/tmp/model", device_map="cpu")

        assert result is fake_model

    def test_load_model_uses_bfloat16_when_cuda_and_bf16_supported(self):
        import torch
        from commons.model_utils import ModelUtils
        torch.cuda.is_available = MagicMock(return_value=True)
        torch.cuda.is_bf16_supported = MagicMock(return_value=True)

        fake_model = self._fake_model()
        with patch("transformers.AutoModelForCausalLM.from_pretrained", return_value=fake_model) as mock_fp:
            result = ModelUtils.load_model(model_path="/tmp/model", device_map="auto")

        assert mock_fp.call_args.kwargs.get("quantization_config") is not None
        assert result is fake_model

    def test_load_model_uses_float16_when_cuda_available_but_bf16_not_supported(self):
        import torch
        from commons.model_utils import ModelUtils
        torch.cuda.is_available = MagicMock(return_value=True)
        torch.cuda.is_bf16_supported = MagicMock(return_value=False)

        fake_model = self._fake_model()
        with patch("transformers.AutoModelForCausalLM.from_pretrained", return_value=fake_model):
            result = ModelUtils.load_model(model_path="/tmp/model", device_map="auto")

        assert result is fake_model

    def test_load_model_uses_float16_when_bf16_attr_absent(self):
        import torch
        from commons.model_utils import ModelUtils
        torch.cuda.is_available = MagicMock(return_value=True)

        fake_model = self._fake_model()
        with patch("transformers.AutoModelForCausalLM.from_pretrained", return_value=fake_model):
            result = ModelUtils.load_model(model_path="/tmp/model", device_map="auto")

        assert result is fake_model

    def test_get_peft_model_with_explicit_lora_config(self):
        from commons.model_utils import ModelUtils
        from peft import LoraConfig
        fake_base_model = MagicMock()
        fake_lora_config = LoraConfig(r=4, lora_alpha=8, lora_dropout=0.05, bias="none")

        with patch("commons.model_utils.get_peft_model") as mock_get_peft:
            mock_get_peft.return_value = MagicMock()
            ModelUtils.get_peft_model(model=fake_base_model, lora_config=fake_lora_config)

        mock_get_peft.assert_called_once_with(fake_base_model, fake_lora_config)

    def test_get_peft_model_falls_back_to_settings_lora_config_when_none(self):
        from commons.model_utils import ModelUtils
        fake_base_model = MagicMock()

        with patch("commons.model_utils.get_peft_model") as mock_get_peft, \
             patch("commons.model_utils.settings") as mock_settings:
            mock_settings.lora_config = MagicMock()
            mock_get_peft.return_value = MagicMock()
            ModelUtils.get_peft_model(model=fake_base_model, lora_config=None)

        mock_get_peft.assert_called_once_with(fake_base_model, mock_settings.lora_config)
