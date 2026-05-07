import pytest
from unittest.mock import MagicMock, patch

from src.federated_learning_common.services.model.model_service import ModelService


class TestLoadModel:
    def test_returns_model(self):
        with patch("src.federated_learning_common.services.model.model_service.torch") as mock_torch, \
             patch("src.federated_learning_common.services.model.model_service.AutoModelForCausalLM") as mock_auto, \
             patch("src.federated_learning_common.services.model.model_service.BitsAndBytesConfig"):
            mock_torch.cuda.is_available.return_value = False
            mock_torch.float16 = "float16"
            mock_model = MagicMock()
            mock_auto.from_pretrained.return_value = mock_model

            result = ModelService.load_model(model_path="/models/llama", device_map="cpu")

        assert result is mock_model
        mock_model.config.use_cache = False

    def test_uses_bfloat16_when_cuda_and_bf16_supported(self):
        with patch("src.federated_learning_common.services.model.model_service.torch") as mock_torch, \
             patch("src.federated_learning_common.services.model.model_service.AutoModelForCausalLM") as mock_auto, \
             patch("src.federated_learning_common.services.model.model_service.BitsAndBytesConfig") as mock_bnb:
            mock_torch.cuda.is_available.return_value = True
            mock_torch.cuda.is_bf16_supported.return_value = True
            mock_torch.bfloat16 = "bfloat16"
            mock_auto.from_pretrained.return_value = MagicMock()

            ModelService.load_model(model_path="/models/llama", device_map="auto")

        call_kwargs = mock_bnb.call_args.kwargs
        assert call_kwargs["bnb_4bit_compute_dtype"] == "bfloat16"

    def test_uses_float16_when_cuda_not_available(self):
        with patch("src.federated_learning_common.services.model.model_service.torch") as mock_torch, \
             patch("src.federated_learning_common.services.model.model_service.AutoModelForCausalLM") as mock_auto, \
             patch("src.federated_learning_common.services.model.model_service.BitsAndBytesConfig") as mock_bnb:
            mock_torch.cuda.is_available.return_value = False
            mock_torch.float16 = "float16"
            mock_auto.from_pretrained.return_value = MagicMock()

            ModelService.load_model(model_path="/models/llama", device_map="cpu")

        call_kwargs = mock_bnb.call_args.kwargs
        assert call_kwargs["bnb_4bit_compute_dtype"] == "float16"

    def test_sets_use_cache_false(self):
        with patch("src.federated_learning_common.services.model.model_service.torch") as mock_torch, \
             patch("src.federated_learning_common.services.model.model_service.AutoModelForCausalLM") as mock_auto, \
             patch("src.federated_learning_common.services.model.model_service.BitsAndBytesConfig"):
            mock_torch.cuda.is_available.return_value = False
            mock_torch.float16 = "float16"
            mock_model = MagicMock()
            mock_auto.from_pretrained.return_value = mock_model

            ModelService.load_model(model_path="/models/llama", device_map="cpu")

        assert mock_model.config.use_cache is False


class TestGetPeftModel:
    def test_returns_peft_model(self):
        model = MagicMock()
        lora_config = MagicMock()

        with patch("src.federated_learning_common.services.model.model_service.get_peft_model",
                   return_value=MagicMock()) as mock_get_peft:
            result = ModelService.get_peft_model(model=model, lora_config=lora_config)

        mock_get_peft.assert_called_once_with(model, lora_config)
        assert result is not None

    def test_uses_settings_lora_config_when_none_provided(self):
        model = MagicMock()

        with patch("src.federated_learning_common.services.model.model_service.get_peft_model",
                   return_value=MagicMock()) as mock_get_peft, \
             patch("src.federated_learning_common.services.model.model_service.settings") as mock_settings:
            mock_settings.lora_config = MagicMock()
            ModelService.get_peft_model(model=model, lora_config=None)

        call_args = mock_get_peft.call_args[0]
        assert call_args[1] is mock_settings.lora_config


class TestLoadPeftModel:
    def test_returns_peft_model_from_pretrained(self):
        model = MagicMock()

        with patch("src.federated_learning_common.services.model.model_service.PeftModel") as mock_peft:
            mock_peft.from_pretrained.return_value = MagicMock()
            result = ModelService.load_peft_model(model=model, adapter_path="/adapters/v1")

        mock_peft.from_pretrained.assert_called_once_with(model, "/adapters/v1", is_trainable=True)
        assert result is not None


class TestLoadTokenizer:
    def test_returns_tokenizer(self):
        with patch("src.federated_learning_common.services.model.model_service.AutoTokenizer") as mock_auto:
            mock_tokenizer = MagicMock()
            mock_tokenizer.pad_token = "<pad>"
            mock_auto.from_pretrained.return_value = mock_tokenizer

            result = ModelService.load_tokenizer(model_path="/models/llama")

        assert result is mock_tokenizer

    def test_sets_pad_token_when_none(self):
        with patch("src.federated_learning_common.services.model.model_service.AutoTokenizer") as mock_auto:
            mock_tokenizer = MagicMock()
            mock_tokenizer.pad_token = None
            mock_tokenizer.eos_token = "<eos>"
            mock_auto.from_pretrained.return_value = mock_tokenizer

            result = ModelService.load_tokenizer(model_path="/models/llama")

        assert result.pad_token == "<eos>"
        assert result.padding_side == "right"

    def test_does_not_override_existing_pad_token(self):
        with patch("src.federated_learning_common.services.model.model_service.AutoTokenizer") as mock_auto:
            mock_tokenizer = MagicMock()
            mock_tokenizer.pad_token = "<pad>"
            mock_auto.from_pretrained.return_value = mock_tokenizer

            ModelService.load_tokenizer(model_path="/models/llama")

        assert mock_tokenizer.pad_token == "<pad>"


class TestPrintTrainableParameters:
    def test_prints_without_error(self):
        model = MagicMock()
        model.named_parameters.return_value = [
            ("layer.weight", MagicMock(numel=MagicMock(return_value=100), requires_grad=True)),
            ("layer.bias", MagicMock(numel=MagicMock(return_value=10), requires_grad=False)),
        ]
        ModelService.print_trainable_parameters(model=model)


class TestModelServiceInit:
    def test_exports_model_service(self):
        from src.federated_learning_common.services.model import ModelService as MS
        assert MS is ModelService

    def test_version(self):
        from src.federated_learning_common.services.model import __version__
        assert __version__ == "1.0.0"
