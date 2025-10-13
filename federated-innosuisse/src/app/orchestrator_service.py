import json
from pathlib import Path
from typing import List
from app.use_cases.pdf_reader.base_pdf_reader import BasePdfReader
from app.config.settings import settings
from app.model.document import Document

class OrchestratorService:
    def __init__(self, pdf_reader: BasePdfReader):
        self._pdf_reader: BasePdfReader = pdf_reader

    def execute_service(self):
        documents: List[Document] = self._pdf_reader.parse_folder(Path(settings.pdf_folder))
        for doc in documents:
            print(json.dumps(doc.to_json(), indent=4))