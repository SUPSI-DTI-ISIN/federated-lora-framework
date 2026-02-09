from typing import List

from federated_learning_client.clients.schemas import DocumentDTO
from federated_learning_client.domain.training import TrainingRow


class DatasetUtils:
    @staticmethod
    def create_document_training_rows(document: DocumentDTO) -> List[TrainingRow]:
        instruction = (
            f"Write a professional PDF section for a research project to be submitted to Innosuisse.\n"
            f"The section must be well-structured, technical, and persuasive."
        )

        training_rows: List[TrainingRow] = []

        for section in document.sections:
            input_text = f"{document.title}\n\nSection to write: {section.title}"
            training_row = TrainingRow(
                instruction=instruction,
                input=input_text,
                output=section.content,
                section_title=section.title,
                document_title=document.title,
                document_project_number=document.number
            )
            training_rows.append(training_row)

        return training_rows