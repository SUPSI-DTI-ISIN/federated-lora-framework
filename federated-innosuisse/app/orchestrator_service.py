import json
from pathlib import Path
from typing import List

from app.config.settings import settings
from app.domain.entities.document import Document
from app.use_cases.process_pdf_documents.process_pdf_documents_use_case import ProcessPdfDocumentsUseCase


class OrchestratorService:
    def __init__(self, process_pdf_documents_use_case: ProcessPdfDocumentsUseCase):
        self._process_pdf_documents_use_case: ProcessPdfDocumentsUseCase = process_pdf_documents_use_case

    def execute_service(self):
        documents: List[Document] = self._process_pdf_documents_use_case.parse_folder(Path(settings.pdf_folder))
        for doc in documents:
            print(json.dumps(doc.to_json(), indent=4))