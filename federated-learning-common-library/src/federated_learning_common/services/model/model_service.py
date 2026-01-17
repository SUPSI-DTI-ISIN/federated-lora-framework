import torch

from peft import PeftModel, get_peft_model, LoraConfig
from torch import nn
from transformers import AutoTokenizer, AutoModelForCausalLM

class ModelService:
    @staticmethod
    def load_model(model_name: str, device: str, lora_config: LoraConfig) -> PeftModel:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device
        )

        for param in model.parameters():
            param.requires_grad = False
            if param.ndim == 1:
                param.data = param.data.to(torch.float32)

        model.gradient_checkpointing_disable()
        model.enable_input_require_grads()

        class CastOutputToFloat(nn.Sequential):
            def forward(self, x): return super().forward(x).to(torch.float32)

        model.lm_head = CastOutputToFloat(model.lm_head)

        model = get_peft_model(model, lora_config)

        model.to(device)
        model.eval()

        return model

    @staticmethod
    def load_tokenizer(model_name: str) -> AutoTokenizer:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        return tokenizer

    @staticmethod
    def print_trainable_parameters(model):
        trainable_params = 0
        all_param = 0
        for _, param in model.named_parameters():
            all_param += param.numel()
            if param.requires_grad:
                trainable_params += param.numel()

        print(f"Trainable parameters: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param:.2f}%")