from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from schemas.exceptions import InstituteNotFoundError, InstituteNameNotFoundError, InstituteCannotBeDeletedError


async def _institute_not_found_handler(
        request: Request,
        exc: InstituteNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": str(exc),
            "institute_id": exc.institute_id
        }
    )

async def _institute_with_name_not_found_handler(
        request: Request,
        exc: InstituteNameNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": str(exc),
            "institute_name": exc.institute_name
        }
    )


async def _institute_cannot_be_deleted_handler(
        request: Request,
        exc: InstituteCannotBeDeletedError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "institute_id": exc.institute_id
        }
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(InstituteNotFoundError, _institute_not_found_handler)
    app.add_exception_handler(InstituteNameNotFoundError, _institute_with_name_not_found_handler)
    app.add_exception_handler(InstituteCannotBeDeletedError, _institute_cannot_be_deleted_handler)