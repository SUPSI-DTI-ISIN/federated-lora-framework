from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from schemas.exceptions import (
    DocumentNotFoundError,
    DocumentAlreadyExistsError,
    InvalidFileError,
)


async def _document_not_found_handler(
        request: Request,
        exc: DocumentNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": str(exc),
            "document_id": exc.document_id
        }
    )


async def _document_already_exists_handler(
        request: Request,
        exc: DocumentAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": str(exc),
            "document_id": exc.document_id
        }
    )


async def _invalid_file_handler(
        request: Request,
        exc: InvalidFileError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc)
        }
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DocumentNotFoundError, _document_not_found_handler)
    app.add_exception_handler(DocumentAlreadyExistsError, _document_already_exists_handler)
    app.add_exception_handler(InvalidFileError, _invalid_file_handler)