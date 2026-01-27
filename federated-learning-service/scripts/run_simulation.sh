#!/bin/bash
set -e

cd ../../federated-learning-common-library
uv build

cd ../department/federated-learning-server
source .venv/bin/activate
uv add ../../federated-learning-common-library
deactivate

cd ../../institute/federated-learning-client
source .venv/bin/activate
uv add ../../federated-learning-common-library
deactivate

cd ../../federated-learning-service
source .venv/bin/activate
uv add ../department/federated-learning-server
uv add ../institute/federated-learning-client

export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uv run --env-file .env flwr run .