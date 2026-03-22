from schemas.documents.section_dto import SectionDTO
from schemas.documents.document_dto import DocumentDTO
from .update_document_trainable_request_dto import UpdateDocumentTrainableRequestDTO
from .training_samples_dto import TrainingSamplesDTO
from .update_section_content_request_dto import UpdateSectionRequestDTO

__all__ = [
    'DocumentDTO',
    'SectionDTO',
    'UpdateDocumentTrainableRequestDTO',
    'TrainingSamplesDTO',
    'UpdateSectionRequestDTO',
]

__version__ = "1.0.0"