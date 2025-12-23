import argparse
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from config import settings
from router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Inference Service",
        description="Inference Service used for query the LLM model",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    app.include_router(router=api_router, prefix="/api_inference")

    return app

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, default=9000, help="The port the server is listening")
    args = parser.parse_args()
    app = create_app()

    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=args.port,
        access_log=True,
    )