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

    REGISTRY="https://gitlab-edu.supsi.ch/api/v4/projects/1401/packages/npm/"
    echo "@isin:registry=${REGISTRY}" > .npmrc
    echo "//gitlab-edu.supsi.ch/api/v4/projects/1401/packages/npm/:_authToken=${GITLAB_TOKEN}" >> .npmrc

    npm publish --tag dev --registry "$REGISTRY"

    wait_for_npm_package() {
      local pkg="$1"
      local ver="$2"
      local registry="$3"
      local max_attempts=10
      local attempt=1
      local sleep_sec=1

      while [ $attempt -le $max_attempts ]; do
        echo "Checking registry for $pkg@$ver (attempt $attempt/$max_attempts)..."
        if npm view "$pkg@$ver" version --registry "$registry" > /dev/null 2>&1; then
          echo "Found $pkg@$ver in registry"
          return 0
        fi
        echo "Not visible yet. Sleeping ${sleep_sec}s..."
        sleep $sleep_sec
        attempt=$((attempt+1))
        sleep_sec=$((sleep_sec*2))
        if [ $sleep_sec -gt 5 ]; then sleep_sec=5; fi
      done

      echo "Package did not appear in registry after $max_attempts attempts."
      return 1
    }

    cd ../../../frontend

    PACKAGE_NAME="@isin/${CLIENT_NAME}"

    if wait_for_npm_package "$PACKAGE_NAME" "$DEV_VERSION" "$REGISTRY"; then
      echo "Installing from registry..."
      npm install --save-exact --registry "$REGISTRY" "${PACKAGE_NAME}@${DEV_VERSION}"
    else
      echo "Registry lookup failed; client package is not reachable from GitLab Package Registry."
      exit 1
    fi
  )
  echo "Published $CLIENT_NAME@$DEV_VERSION"
}

publish_sdk "../institute/data-service" "data-service-client"
publish_sdk "../institute/inference-service" "inference-service-client"
publish_sdk "../institute/model-service" "model-service-client"

cd ../docker

#echo "$GITLAB_DOCKER_REGISTRY_TOKEN" | docker login "$GITLAB_DOCKER_REGISTRY_HOST" -u "$GITLAB_DOCKER_REGISTRY_USERNAME" --password-stdin
docker compose down -v
docker compose build
docker compose up -d