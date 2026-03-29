class Llama31Utils:
    @classmethod
    def format_chat(cls, system: str, user: str, assistant: str) -> dict:
        prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>\n"
            f"{system}<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>\n"
            f"{user}<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>\n"
        )

        full_text = prompt + assistant + "<|eot_id|>"

        return {
            "text": full_text,
            "prompt_length": len(prompt)
        }