from typing import override
from app.service.ollama.ollama_service import OllamaService
from app.service.project_number_detector.base_project_number_detector import BaseProjectNumberDetector


def build_system_prompt() -> str:
    return """
You are a string-only extractor: your task is to take as input the text of page 0 (introduction) of a PDF and return exactly the project number as a string. You must follow these rules strictly.

INPUT:
A block of text (text extracted from page 0 of the PDF) which contains key - value components.

RECOGNITION:
The project number does not contain only numbers but can contain also alphabetic characters. 
It is usually the value of the key "Number:" (e.g. "Number:\n103.518 IP-ICT" -> the project number to return is "103.518 IP-ICT").

REQUESTED OUTPUT:
Only the string that represents the project number. 

OUTPUT RULES: 
You must return ONLY the string which rapresents the Project Number: <project_number>.
No explanations, no JSON, no other characters, no additional newlines.
If you do not find a project number with sufficient certainty, return an empty string "".
"""

class ProjectNumberDetector(BaseProjectNumberDetector):
    def __init__(self):
        self._ollama_service = OllamaService()

    @override
    def extract_project_number(self, text_document: str) -> str:
        return self._ollama_service.call_model(system_prompt=build_system_prompt(), user_prompt=text_document)