from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from schemas.exceptions import StartFederatedLearningJobFoundError


async def _start_federated_learning_job_bad_request_handler(
        request: Request,
        exc: StartFederatedLearningJobFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
        }
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(StartFederatedLearningJobFoundError, _start_federated_learning_job_bad_request_handler)