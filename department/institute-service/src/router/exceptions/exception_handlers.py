from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from schemas.exceptions import InstituteNotFoundError


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

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(InstituteNotFoundError, _institute_not_found_handler)