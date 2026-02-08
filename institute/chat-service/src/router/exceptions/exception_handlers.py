from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from schemas.exceptions import ChatNotFoundError


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

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(ChatNotFoundError, _chat_not_found_handler)