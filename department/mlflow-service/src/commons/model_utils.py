import torch

from typing import Optional
from peft import PeftModel, get_peft_model, LoraConfig
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, PreTrainedModel

from config import settings


class ModelUtils:
    @classmethod
    def load_model(cls, model_path: str, device_map: str) -> PreTrainedModel:
        if torch.cuda.is_available() and getattr(torch.cuda, "is_bf16_supported", lambda: False)():
            compute_dtype = torch.bfloat16
        else:
            compute_dtype = torch.float16

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=True,
            llm_int8_enable_fp32_cpu_offload=True
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=bnb_config,
            device_map=device_map,
            local_files_only=True,
            use_safetensors=True
        )

        model.config.use_cache = False

        return model

    @classmethod
    def get_peft_model(cls, model: PreTrainedModel, lora_config: Optional[LoraConfig] = None) -> PeftModel:
        return get_peft_model(model, lora_config if lora_config is not None else settings.lora_config)