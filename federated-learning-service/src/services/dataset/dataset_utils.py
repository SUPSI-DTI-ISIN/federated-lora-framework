from domain.document import Section, Metadata
from domain.training import TrainingRow


class DatasetUtils:
    @staticmethod
    def create_training_row(section: Section, metadata: Metadata) -> TrainingRow:
        instruction = (
            f"Write a professional PDF section for a research project to be submitted to Innosuisse.\n"
            f"The section must be well-structured, technical, and persuasive."
        )

        input_text = f"{metadata.title}\n\nSection to write: {section.title}"

        return TrainingRow(
            instruction=instruction,
            input=input_text,
            output=section.content,
            section_title=section.title,
            document_title=metadata.title,
        )