#!/bin/bash
set -e
set -o pipefail

IMAGE_TAG="latest"
#PLATFORM_ARG="--platform=linux/amd64,linux/arm64"
PLATFORM_ARG=""
SERVICES_ENV_PATH=".env.local"
FRONTEND_ENV_PATH=".env.local"

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

if [[ "$IMAGE_TAG" == "nvidia" ]]; then
  FRONTEND_ENV_PATH=".env.local-nvidia"
fi

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

#if ! docker buildx inspect multiarch-builder > /dev/null 2>&1; then
#  docker buildx create --use --name multiarch-builder --driver docker-container --driver-opt network=host
#else
#  docker buildx use multiarch-builder
#fi
#
#docker buildx inspect --bootstrap

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/department/mlflow-service:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../department/mlflow-service/docker/Dockerfile --build-arg ENV_PATH="$SERVICES_ENV_PATH" --build-arg UV_INDEX_GITLAB_USERNAME="$UV_INDEX_GITLAB_USERNAME" --build-arg UV_INDEX_GITLAB_PASSWORD="$UV_INDEX_GITLAB_PASSWORD" ../department/mlflow-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/department/institute-service:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../department/institute-service/docker/Dockerfile --build-arg ENV_PATH="$SERVICES_ENV_PATH" --build-arg UV_INDEX_GITLAB_USERNAME="$UV_INDEX_GITLAB_USERNAME" --build-arg UV_INDEX_GITLAB_PASSWORD="$UV_INDEX_GITLAB_PASSWORD" ../department/institute-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/department/federated-learning-management-service:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../department/federated-learning-management-service/docker/Dockerfile --build-arg ENV_PATH="$SERVICES_ENV_PATH" --build-arg UV_INDEX_GITLAB_USERNAME="$UV_INDEX_GITLAB_USERNAME" --build-arg UV_INDEX_GITLAB_PASSWORD="$UV_INDEX_GITLAB_PASSWORD" ../department/federated-learning-management-service

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/frontend:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../frontend/docker/Dockerfile --build-arg ENV_PATH="$FRONTEND_ENV_PATH" --build-arg NPM_TOKEN="$GITLAB_TOKEN" ../frontend

docker buildx build -t "${GITLAB_DOCKER_REGISTRY_URL}/superexec:${IMAGE_TAG}" $PLATFORM_ARG --push --provenance=false --sbom=false -f ../federated-learning-service/docker/superexec.Dockerfile ../federated-learning-service