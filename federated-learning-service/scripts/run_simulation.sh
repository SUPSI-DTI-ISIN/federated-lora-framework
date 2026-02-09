#!/bin/bash
set -e

set -a
source .env
set +a
uv sync --reinstall

cd ..

set -a
source .env
set +a

uv run --active flwr run .