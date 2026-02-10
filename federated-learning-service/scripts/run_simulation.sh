#!/bin/bash
set -e

set -a
source .env
set +a
uv sync --reinstall

cd ..

export PYTHONPATH=src
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
#export RAY_DISABLE_METRICS=1
export RAY_DEDUP_LOGS=0
uv run --link-mode=copy --active flwr run .