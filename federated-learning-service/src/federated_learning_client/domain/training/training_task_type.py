from enum import Enum


class TrainingTaskType(Enum):
    SECTION_WRITING = 'section_writing'
    STRUCTURE_QA = 'structure_qa'
    CONTENT_QA = 'content_qa'
    CRITIQUE = 'critique'
    SUMMARY = 'summary'