from unittest.mock import patch, MagicMock
from utils.torch_dtype_utils import TorchDtypeUtils


class TestTorchDtypeUtils:
    def test_returns_bfloat16_when_cuda_available_and_bf16_supported(self):
        with patch("utils.torch_dtype_utils.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = True
            mock_torch.cuda.is_bf16_supported.return_value = True
            mock_torch.bfloat16 = "bfloat16"
            mock_torch.float16 = "float16"
            result = TorchDtypeUtils.get_torch_dtype()
        assert result == "bfloat16"

    def test_returns_float16_when_cuda_not_available(self):
        with patch("utils.torch_dtype_utils.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = False
            mock_torch.float16 = "float16"
            result = TorchDtypeUtils.get_torch_dtype()
        assert result == "float16"

    def test_returns_float16_when_bf16_not_supported(self):
        with patch("utils.torch_dtype_utils.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = True
            mock_torch.cuda.is_bf16_supported.return_value = False
            mock_torch.float16 = "float16"
            result = TorchDtypeUtils.get_torch_dtype()
        assert result == "float16"

    def test_returns_float16_when_bf16_supported_attr_missing(self):
        with patch("utils.torch_dtype_utils.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = True
            # is_bf16_supported not present — getattr fallback returns False
            del mock_torch.cuda.is_bf16_supported
            mock_torch.float16 = "float16"
            result = TorchDtypeUtils.get_torch_dtype()
        assert result == "float16"
