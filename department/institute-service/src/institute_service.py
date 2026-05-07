import argparse
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from config import settings
from router import api_router, lifespan
from router.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Institute Service",
        description="Institute Service module which handles the institute in the system",
        version="1.0.0",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    register_exception_handlers(app=app)

    app.include_router(router=api_router, prefix="/api_institute")

    return app

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, default=9020, help="The port the server is listening")
    args = parser.parse_args()
    app = create_app()

    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=args.port,
        access_log=True,
    )