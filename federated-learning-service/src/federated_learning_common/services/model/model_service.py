import torch

from typing import Optional
from peft import PeftModel, get_peft_model, LoraConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer, BitsAndBytesConfig, PreTrainedModel

from src.federated_learning_common.config import settings


class ModelService:
    @classmethod
    def load_model(cls, model_path: str, device_map: str, access_token: Optional[str] = None) -> PreTrainedModel:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
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
        model.gradient_checkpointing_enable()

        return model

    @classmethod
    def get_peft_model(cls, model: PreTrainedModel, lora_config: Optional[LoraConfig] = None) -> PeftModel:
        return get_peft_model(model, lora_config if lora_config is not None else settings.lora_config)

    @classmethod
    def load_tokenizer(cls, model_path: str, access_token: Optional[str] = None) -> PreTrainedTokenizer:
        tokenizer = AutoTokenizer.from_pretrained(model_path,
                                                  #token=access_token
                                                  local_files_only=True
                                                  )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.padding_side = "right"
        return tokenizer

    @classmethod
    def print_trainable_parameters(cls, model):
        trainable_params = 0
        all_param = 0
        for _, param in model.named_parameters():
            all_param += param.numel()
            if param.requires_grad:
                trainable_params += param.numel()

        print(
            f"Trainable parameters: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param:.2f}%")