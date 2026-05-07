#!/bin/bash
set -e
set -o pipefail

IMAGE_TAG="latest"
#PLATFORM_ARG="--platform=linux/amd64,linux/arm64"
PLATFORM_ARG=""
SERVICES_ENV_PATH=".env.local"

usage() {
  echo "Usage: $0 [--platform <platform>] [--tag <tag>]"
  echo "  --platform <platform>   Pass platform to docker buildx (e.g. linux/amd64)"
  echo "  --tag <tag>             Image tag to use (default: latest)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)
      [[ -z "${2:-}" ]] && { echo "Error: --platform requires an argument."; usage; }
      PLATFORM_ARG="--platform=$2"
      shift 2
      ;;
    --tag)
      [[ -z "${2:-}" ]] && { echo "Error: --tag requires an argument."; usage; }
      IMAGE_TAG="$2"
      shift 2
      ;;
    --tag=*)
      IMAGE_TAG="${1#--tag=}"
      shift
      ;;
    --help|-h)
      usage
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      ;;
  esac
done

if [ ! -f .env.config ]; then
  echo "Error: .env.config file not found"
  exit 1
fi
source .env.config


if [ ! -f .env.docker.build-time ]; then
  echo "Error: .env.docker.build-time file not found"
  exit 1
fi
source .env.docker.build-time

GITLAB_DOCKER_REGISTRY_URL="${GITLAB_DOCKER_REGISTRY_HOST}${GITLAB_DOCKER_REGISTRY_PATH}"

echo "$GITLAB_DOCKER_REGISTRY_TOKEN" | docker login "$GITLAB_DOCKER_REGISTRY_HOST" -u "$GITLAB_DOCKER_REGISTRY_USERNAME" --password-stdin

if ! docker buildx inspect multiarch-builder > /dev/null 2>&1; then
  docker buildx create --use --name multiarch-builder --driver docker-container --driver-opt network=host
else
  docker buildx use multiarch-builder
fi

docker buildx inspect --bootstrap

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/institute/chat-service:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../institute/chat-service/docker/Dockerfile --build-arg ENV_PATH="$SERVICES_ENV_PATH" --build-arg UV_INDEX_GITLAB_USERNAME="$UV_INDEX_GITLAB_USERNAME" --build-arg UV_INDEX_GITLAB_PASSWORD="$UV_INDEX_GITLAB_PASSWORD" ../institute/chat-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/institute/data-service:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../institute/data-service/docker/Dockerfile --build-arg ENV_PATH="$SERVICES_ENV_PATH" --build-arg UV_INDEX_GITLAB_USERNAME="$UV_INDEX_GITLAB_USERNAME" --build-arg UV_INDEX_GITLAB_PASSWORD="$UV_INDEX_GITLAB_PASSWORD" ../institute/data-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/institute/inference-service:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../institute/inference-service/docker/Dockerfile --build-arg ENV_PATH="$SERVICES_ENV_PATH" --build-arg UV_INDEX_GITLAB_USERNAME="$UV_INDEX_GITLAB_USERNAME" --build-arg UV_INDEX_GITLAB_PASSWORD="$UV_INDEX_GITLAB_PASSWORD" ../institute/inference-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/institute/model-service:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../institute/model-service/docker/Dockerfile --build-arg ENV_PATH="$SERVICES_ENV_PATH" --build-arg UV_INDEX_GITLAB_USERNAME="$UV_INDEX_GITLAB_USERNAME" --build-arg UV_INDEX_GITLAB_PASSWORD="$UV_INDEX_GITLAB_PASSWORD" ../institute/model-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/institute/nginx:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../institute/nginx-service/docker/Dockerfile ../institute/nginx-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/superexec:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../federated-learning-service/docker/superexec.uv.Dockerfile ../federated-learning-service