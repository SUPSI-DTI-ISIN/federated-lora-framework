from transformers import BitsAndBytesConfig

from .torch_dtype_utils import TorchDtypeUtils


class QuantizationUtils:
    @classmethod
    def get_quantization_config(cls) -> BitsAndBytesConfig:
        return BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=TorchDtypeUtils.get_torch_dtype(),
            bnb_4bit_use_double_quant=True,
            llm_int8_enable_fp32_cpu_offload=True
        )