#!/bin/bash
set -e
set -o pipefail

set -a
source .env
set +a
uv sync --reinstall

cd ..

uv build
twine upload --config-file .pypirc --verbose --repository gitlab dist/*