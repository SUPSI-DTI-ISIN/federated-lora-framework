from dependency_injector import containers, providers

from app.orchestrator_service import OrchestratorService
from app.services.pdf_parser.pymupdf_parser import PyMuPdfParser
from app.services.project_number_detector.project_number_detector import ProjectNumberDetector
from app.services.section_detector.section_extractor import SectionExtractor
from app.use_cases.process_pdf_documents.process_pdf_documents_use_case import ProcessPdfDocumentsUseCase


class Container(containers.DeclarativeContainer):
    pdf_parser = providers.Singleton(PyMuPdfParser)
    project_number_detector = providers.Singleton(ProjectNumberDetector)
    section_detector = providers.Singleton(SectionExtractor)

    process_pdf_documents_use_case = providers.Factory(
        ProcessPdfDocumentsUseCase,
        pdf_parser=pdf_parser,
        project_number_detector=project_number_detector,
        section_detector=section_detector,
    )

    orchestrator_service = providers.Factory(
        OrchestratorService,
        process_pdf_documents_use_case=process_pdf_documents_use_case,
    )