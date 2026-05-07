from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from schemas.exceptions import ChatNotFoundError, InferenceRequestError


async def _chat_not_found_handler(
        request: Request,
        exc: ChatNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": str(exc),
            "chat_id": exc.chat_id
        }
    )

async def _inference_request_internal_server_error_handler(
        request: Request,
        exc: InferenceRequestError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "detailed_error": exc.detailed_err
        }
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(ChatNotFoundError, _chat_not_found_handler)
    app.add_exception_handler(InferenceRequestError, _inference_request_internal_server_error_handler)