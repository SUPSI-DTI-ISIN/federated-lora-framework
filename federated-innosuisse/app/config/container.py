from dependency_injector import containers, providers

from app.parser.pdf_parser import PdfParser


class Container(containers.DeclarativeContainer):
    pdf_parser = providers.Singleton(PdfParser)

    process_pdf_documents_use_case = providers.Factory(
        pdf_parser=pdf_parser
    )