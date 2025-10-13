from app.orchestrator_service import OrchestratorService
from app.service.pdf_parser.pymupdf_parser import PyMuPdfParser
from app.service.project_number_detector.project_number_detector import ProjectNumberDetector
from app.service.section_detector.section_detector import SectionDetector
from app.use_cases.pdf_reader.pdf_reader import PdfReader


def main():
    pdf_parser = PyMuPdfParser()
    project_number_detector = ProjectNumberDetector()
    section_detector = SectionDetector()

    pdf_reader = PdfReader(
        pdf_parser,
        project_number_detector,
        section_detector
    )


    orchestrator_service: OrchestratorService = OrchestratorService(pdf_reader)
    orchestrator_service.execute_service()


if __name__ == "__main__":
    main()