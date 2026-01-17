import argparse
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from router import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="MlFlow Service",
        description="MlFlow Service used for manage MlFlow server interactions and operations",
        version="1.0.0",
    )

    app.add_middleware(GZipMiddleware, minimum_size=1000)

    app.include_router(router=api_router, prefix="/api_mlflow")

    return app

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, default=9010, help="The port the server is listening")
    args = parser.parse_args()
    app = create_app()

    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=args.port,
        access_log=True,
    )