from unittest.mock import patch, MagicMock
from utils.quantization_utils import QuantizationUtils


class TestQuantizationUtils:
    def test_returns_bits_and_bytes_config(self):
        with patch("utils.quantization_utils.TorchDtypeUtils.get_torch_dtype", return_value="float16"), \
             patch("utils.quantization_utils.BitsAndBytesConfig") as mock_bnb:
            mock_bnb.return_value = MagicMock()
            result = QuantizationUtils.get_quantization_config()

        mock_bnb.assert_called_once_with(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype="float16",
            bnb_4bit_use_double_quant=True,
            llm_int8_enable_fp32_cpu_offload=True,
        )
        assert result is not None

    def test_uses_torch_dtype_for_compute_dtype(self):
        with patch("utils.quantization_utils.TorchDtypeUtils.get_torch_dtype", return_value="bfloat16"), \
             patch("utils.quantization_utils.BitsAndBytesConfig") as mock_bnb:
            mock_bnb.return_value = MagicMock()
            QuantizationUtils.get_quantization_config()

        call_kwargs = mock_bnb.call_args.kwargs
        assert call_kwargs["bnb_4bit_compute_dtype"] == "bfloat16"
