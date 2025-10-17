from typing import List

from app.domain import Document, TrainingRow, TrainingDataset, Section, Metadata


def build_dataset_from_documents(documents: List[Document]):
    training_row_list: List[TrainingRow] = []

    for document in documents:
        for section in document.sections:
            example = _create_training_row(
                section,
                document.metadata
            )
            training_row_list.append(example)

    return TrainingDataset(training_row_list)

def _create_training_row(section: Section, document_metadata: Metadata) -> TrainingRow:
    instruction = (
        f"Write a professional PDF section for a research project to be submitted to Innosuisse.\n"
        f"The section must be well-structured, technical, and persuasive."
    )

    input_text = f"{document_metadata.title}\n\nSection to write: {section.title}"

    return TrainingRow(
        instruction=instruction,
        input=input_text,
        output=section.content,
        section_title=section.title,
        document_title=document_metadata.title,
    )