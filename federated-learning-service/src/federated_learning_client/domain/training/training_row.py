from dataclasses import dataclass

from .training_task_type import TrainingTaskType


@dataclass
class TrainingRow:
    instruction: str
    input: str
    output: str
    section_title: str
    document_title: str
    document_project_number: str
    task_type: str
    text: str = ""
    prompt_length: int = 0