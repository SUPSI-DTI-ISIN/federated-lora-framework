from dataclasses import dataclass

@dataclass
class TrainingRow:
    instruction: str
    input: str
    output: str
    section_title: str
    document_title: str
    document_project_number: str