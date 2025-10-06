from app.pdf_reader import PdfReader

def main():
    pdf_reader: PdfReader = PdfReader()
    pdf_reader.parse_pdf()


if __name__ == "__main__":
    main()