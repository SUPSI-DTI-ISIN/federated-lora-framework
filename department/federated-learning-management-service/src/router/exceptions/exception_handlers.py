from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse

from schemas.exceptions import FederatedLearningJobNotFoundError, StartFederatedLearningJobFoundError


async def _federated_learning_job_not_found_handler(
        request: Request,
        exc: FederatedLearningJobNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": str(exc),
            "federated_learning_job_id": exc.federated_learning_job_id
        }
    )

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
    app.add_exception_handler(FederatedLearningJobNotFoundError, _federated_learning_job_not_found_handler)
    app.add_exception_handler(StartFederatedLearningJobFoundError, _start_federated_learning_job_bad_request_handler)