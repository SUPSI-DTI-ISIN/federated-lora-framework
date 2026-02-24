import argparse
import uvicorn

from fastapi import FastAPI

from router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Federated Learning Management Service",
        description="Federated Learning Management Service used for handling the federated learning operations",
        version="1.0.0",
    )

    app.include_router(router=api_router, prefix="/api_federated_learning_management")

    return app

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, default=9015, help="The port the server is listening")
    args = parser.parse_args()
    app = create_app()

    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=args.port,
        access_log=True,
    )