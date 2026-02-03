#!/bin/bash
set -e

cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
uv run --env-file .env flwr run .