#!/bin/bash
set -e
set -o pipefail

cd ..
uv build
twine upload --config-file .pypirc --verbose --repository gitlab dist/*