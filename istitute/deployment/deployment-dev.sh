#!/bin/bash
set -e

if [ ! -f .env.config ]; then
  echo "Error: .env.config file not found"
  exit 1
fi
source .env.config

publish_sdk() {
  local SERVICE_PATH=$1
  local CLIENT_NAME=$2

  echo "Syncing $CLIENT_NAME..."

  (
    cd "$SERVICE_PATH/scripts" && ./sync_api.sh

    VERSION=$(jq -r '.info.version' "../sdks/openapi.json")
    echo "Version from toml: $VERSION"
    TIMESTAMP=$(date +%s)
    DEV_VERSION="$VERSION-dev.$TIMESTAMP"

    cd "../sdks/$CLIENT_NAME"
    npm version "$DEV_VERSION" --no-git-tag-version
    echo "@isin:registry=https://gitlab-edu.supsi.ch/api/v4/projects/1401/packages/npm/" > .npmrc
    echo "//gitlab-edu.supsi.ch/api/v4/projects/1401/packages/npm/:_authToken=${GITLAB_TOKEN}" >> .npmrc
    npm publish --tag dev
    cd ../../../frontend
    npm install --save-exact "@isin/${CLIENT_NAME}@${DEV_VERSION}"
  )
  echo "Published $CLIENT_NAME@$DEV_VERSION"
}

publish_sdk "../data-service" "data-service-client"
publish_sdk "../inference-service" "inference-service-client"

cd ../docker

#echo "$GITLAB_DOCKER_REGISTRY_TOKEN" | docker login "$GITLAB_DOCKER_REGISTRY_HOST" -u "$GITLAB_DOCKER_REGISTRY_USERNAME" --password-stdin
docker compose down -v
docker compose build
docker compose up -d