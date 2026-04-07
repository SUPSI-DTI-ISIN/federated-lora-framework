#TODO: fix using strategy pattern
class Llama2Utils:
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    @classmethod
    def format_chat(cls, system: str, user: str, assistant: str) -> dict:
        prompt = f"{cls.B_INST} {cls.B_SYS}{system}{cls.E_SYS}{user} {cls.E_INST} "
        full_text = prompt + assistant + " </s>"
        return {
            "text": full_text,
            "prompt_length": len(prompt)
        }