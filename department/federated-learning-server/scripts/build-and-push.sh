#!/bin/bash
set -e
set -o pipefail

set -a
source .env
set +a

cd ..
uv sync --reinstall

rm -rf build/
rm -rf dist/

uv build
twine upload --config-file .pypirc --verbose --repository gitlab dist/*