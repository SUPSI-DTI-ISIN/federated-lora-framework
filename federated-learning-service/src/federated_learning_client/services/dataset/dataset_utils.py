import random

from typing import List

from federated_learning_client.domain.training import TrainingTaskType
from src.federated_learning_client.clients.schemas import DocumentDTO
from src.federated_learning_client.domain.training import TrainingRow

LLAMA2_SYSTEM = (
    "You are an expert in Swiss research funding and Innosuisse project proposals. "
    "You help researchers write, review, and improve their project submissions."
)

class DatasetUtils:
    @staticmethod
    def create_document_training_rows(document: DocumentDTO) -> List[TrainingRow]:
        rows: List[TrainingRow] = []
        rows.extend(DatasetUtils.__section_writing_rows(document))
        rows.extend(DatasetUtils.__structure_qa_rows(document))
        rows.extend(DatasetUtils.__content_qa_rows(document))
        rows.extend(DatasetUtils.__critique_rows(document))
        rows.extend(DatasetUtils.__summary_rows(document))
        return rows

    @staticmethod
    def __section_writing_rows(document: DocumentDTO) -> List[TrainingRow]:
        rows = []
        for section in document.sections:
            prompt = (
                f"I am writing an Innosuisse project proposal titled \"{document.title}\".\n"
                f"Write the \"{section.title}\" section in a professional, technical, and persuasive style."
            )
            rows.append(TrainingRow(
                instruction=LLAMA2_SYSTEM,
                input=prompt,
                output=section.content,
                section_title=section.title,
                document_title=document.title,
                document_project_number=document.number,
                task_type=TrainingTaskType.SECTION_WRITING.value
            ))
        return rows

    @staticmethod
    def __structure_qa_rows(document: DocumentDTO) -> List[TrainingRow]:
        section_list = "\n".join(
            f"- {s.title}" for s in document.sections
        )
        questions = [
            "What are the required sections for an Innosuisse project proposal?",
            "What sections should I include when writing an Innosuisse proposal?",
            f"What sections are present in the proposal \"{document.title}\"?",
            "How should I structure a new Innosuisse project proposal?",
        ]
        rows = []
        for question in random.sample(questions, k=min(2, len(questions))):
            answer = (
                f"An Innosuisse project proposal typically includes the following sections:\n"
                f"{section_list}\n\n"
                f"Each section serves a specific purpose in demonstrating the scientific merit, "
                f"innovation potential, and implementation plan to the reviewers."
            )
            rows.append(TrainingRow(
                instruction=LLAMA2_SYSTEM,
                input=question,
                output=answer,
                section_title="",
                document_title=document.title,
                document_project_number=document.number,
                task_type=TrainingTaskType.STRUCTURE_QA.value
            ))
        return rows

    @staticmethod
    def __content_qa_rows(document: DocumentDTO) -> List[TrainingRow]:
        rows = []
        for section in document.sections:
            if len(section.content.strip()) < 100:
                continue
            questions = [
                f"What does the \"{section.title}\" section of an Innosuisse proposal describe?",
                f"What should be written in the \"{section.title}\" section?",
                f"Summarise the key points of the \"{section.title}\" section from the proposal \"{document.title}\".",
            ]
            question = random.choice(questions)
            answer = (
                f"In an Innosuisse project proposal, the \"{section.title}\" section covers:\n\n"
                f"{section.content.strip()}"
            )
            rows.append(TrainingRow(
                instruction=LLAMA2_SYSTEM,
                input=question,
                output=answer,
                section_title=section.title,
                document_title=document.title,
                document_project_number=document.number,
                task_type=TrainingTaskType.CONTENT_QA.value
            ))
        return rows

    @staticmethod
    def __critique_rows(document: DocumentDTO) -> List[TrainingRow]:
        rows = []
        for section in document.sections:
            content = section.content.strip()
            if len(content) < 150:
                continue
            weak_version = content.split('\n')[0][:300]
            if len(weak_version) < 80:
                continue

            prompt = (
                f"Below is a draft of the \"{section.title}\" section for an Innosuisse proposal "
                f"titled \"{document.title}\". Review it and provide an improved version.\n\n"
                f"Draft:\n{weak_version}"
            )
            output = (
                f"The draft is too brief and lacks the required depth for an Innosuisse submission. "
                f"Here is a more complete version:\n\n{content}"
            )
            rows.append(TrainingRow(
                instruction=LLAMA2_SYSTEM,
                input=prompt,
                output=output,
                section_title=section.title,
                document_title=document.title,
                document_project_number=document.number,
                task_type=TrainingTaskType.CRITIQUE.value
            ))
        return rows

    @staticmethod
    def __summary_rows(document: DocumentDTO) -> List[TrainingRow]:
        all_content = "\n\n".join(
            f"### {s.title}\n{s.content}" for s in document.sections
        )
        if len(all_content) < 300:
            return []

        prompt = (
            f"Summarise the key objectives, innovation, and expected impact of the Innosuisse "
            f"project proposal titled \"{document.title}\"."
        )
        summary_parts = []
        for section in document.sections:
            if section.content.strip():
                first_paragraph = section.content.strip().split('\n')[0]
                summary_parts.append(f"**{section.title}**: {first_paragraph[:200]}")

        output = (
                f"The proposal \"{document.title}\" presents the following:\n\n"
                + "\n\n".join(summary_parts)
        )
        return [TrainingRow(
            instruction=LLAMA2_SYSTEM,
            input=prompt,
            output=output,
            section_title="",
            document_title=document.title,
            document_project_number=document.number,
            task_type="summary"
        )]