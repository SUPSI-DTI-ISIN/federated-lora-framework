#!/bin/bash
set -e

SERVICE_NAME="chat-service"
SDKS_DIR="../sdks"
CLIENT_DIR="${SDKS_DIR}/${SERVICE_NAME}-client"
OPENAPI_JSON_PATH="${SDKS_DIR}/openapi.json"
NPM_SCOPE="@isin"

echo "Cleaning previous client..."
rm -rf "$SDKS_DIR"
mkdir -p "$SDKS_DIR"

echo "Generating OpenAPI json..."
uv sync --reinstall
uv run --env-file ../.env.dev ../src/extract_openapi.py --output "$OPENAPI_JSON_PATH"

if [ ! -f "$OPENAPI_JSON_PATH" ]; then
    echo "OpenAPI spec not found at $OPENAPI_JSON_PATH"
    exit 1
fi

VERSION=$(jq -r '.info.version' "$OPENAPI_JSON_PATH")
echo "Version from toml: $VERSION"

echo "Generating TypeScript client..."
SDKS_ABS_PATH=$(cd "$SDKS_DIR" && pwd)

docker run --rm \
    -u $(id -u):$(id -g) \
    -v "${SDKS_ABS_PATH}:/local" \
    openapitools/openapi-generator-cli generate \
    -i /local/openapi.json \
    -g typescript-axios \
    -o /local/${SERVICE_NAME}-client \
    --additional-properties=npmName="${NPM_SCOPE}/${SERVICE_NAME}-client",npmVersion="${VERSION}",withSeparateModelsAndApi=true,apiPackage=api,modelPackage=models,supportsES6=true

echo "Building TypeScript..."
cd "$CLIENT_DIR"
npm install
npm run build

cd ../../../frontend
npm install "../${SERVICE_NAME}/sdks/${SERVICE_NAME}-client"

echo "Sync $SERVICE_NAME done with version: $VERSION"