from pathlib import Path
from typing import List

from app.domain.entities.document import Document
from app.domain.entities.metadata import Metadata
from app.domain.entities.section import Section
from app.services.pdf_parser.base_pdf_parser import BasePdfParser
from app.services.project_number_detector.base_project_number_detector import BaseProjectNumberDetector
from app.services.section_detector.base_section_extractor import BaseSectionExtractor


def _is_folder_valid(folder_path: Path) -> bool:
    if not folder_path.exists():
        print("Folder does not exist")
        return False

    if not folder_path.is_dir():
        print("Folder passed is not a directory")
        return False

    return True


def _get_pdf_files_from_folder(folder_path: Path) -> List[Path]:
    return list(folder_path.glob("*.pdf"))


class ProcessPdfDocumentsUseCase:
    def __init__(self, 
                 pdf_parser: BasePdfParser, 
                 project_number_detector: BaseProjectNumberDetector,
                 section_detector: BaseSectionExtractor
                ) -> None:
        self._pdf_parser: BasePdfParser = pdf_parser
        self._project_number_detector: BaseProjectNumberDetector = project_number_detector
        self._section_detector: BaseSectionExtractor = section_detector

    def parse_folder(self, folder_path: Path) -> List[Document]:
        print(f"Start parsing pdf files from folder {folder_path}")

        if not _is_folder_valid(folder_path):
            return []
        
        documents: List[Document] = []
        
        for pdf_file in _get_pdf_files_from_folder(folder_path):
            try:
                self._pdf_parser.load(pdf_file)

                metadata: Metadata = Metadata(pdf_file.name)

                project_number = self._get_project_number()

                full_text = self._pdf_parser.get_all_text_document()

                sections: List[Section] = self._section_detector.extract_document_sections(full_text, project_number)

                document: Document = Document(metadata, sections)
                documents.append(document)
            finally:
                self._pdf_parser.close()
        
        return documents

    def _get_project_number(self) -> str:
        pages = self._pdf_parser.get_pages()
        return self._project_number_detector.extract_project_number(pages[0].get_textpage().extractText())