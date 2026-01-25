import torch

from schemas.model import LoadedModel


class ModelResponseUtils:
    @classmethod
    def generate_model_response(cls, loaded_model: LoadedModel, prompt: str) -> str:
        inputs = loaded_model.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(loaded_model.model.device)

        with torch.no_grad():
            outputs = loaded_model.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                do_sample=True,
                top_p=0.9
            )

        response = loaded_model.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        if response.startswith(prompt):
            response = response[len(prompt):].strip()

        return response