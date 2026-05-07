class DocumentNotFoundError(Exception):
    def __init__(self, document_id: int):
        self.document_id = document_id
        super().__init__(f"Document with id '{document_id}' not found.")


class DocumentAlreadyExistsError(Exception):
    def __init__(self, document_id: int):
        self.document_id = document_id
        super().__init__(f"Document with id '{document_id}' already exists.")

class InvalidFileError(Exception):
    def __init__(self, message: str):
        super().__init__(message)