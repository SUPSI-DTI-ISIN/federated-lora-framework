#!/bin/bash

if [ ! -f .env.config ]; then
  echo "Error: .env.config file not found"
  exit 1
fi
source .env.config

SSH_KEY="$HOME/.ssh/id_ed25519_nvidia"
LOCAL_KEYCLOAK_INITIAL_CONFIGURATION_PATH="../keycloak-initial-configuration"
LOCAL_DOCKER_COMPOSE_PATH="../docker/docker-compose.nvidia.yml"
LOCAL_DOCKER_COMPOSE_ENV_FILE_PATH=".env.docker"

REMOTE_USER="admin"
REMOTE_HOST="10.11.13.6"

REMOTE_BASE_PATH="/home/${REMOTE_USER}/decentralised-ai-docker"

scp -i "${SSH_KEY}" "${LOCAL_DOCKER_COMPOSE_ENV_FILE_PATH}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE_PATH}/.env"
scp -i "${SSH_KEY}" "${LOCAL_DOCKER_COMPOSE_PATH}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE_PATH}/docker-compose.yml"
ssh -i "${SSH_KEY}" "${REMOTE_USER}@${REMOTE_HOST}" "rm -rf ${REMOTE_BASE_PATH}/keycloak-initial-configuration"
scp -i "${SSH_KEY}" -r "${LOCAL_KEYCLOAK_INITIAL_CONFIGURATION_PATH}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE_PATH}"
ssh -i "${SSH_KEY}" "${REMOTE_USER}@${REMOTE_HOST}" " echo '${GITLAB_DOCKER_REGISTRY_TOKEN}' | docker login '${GITLAB_DOCKER_REGISTRY_HOST}' -u '${GITLAB_DOCKER_REGISTRY_USERNAME}' --password-stdin"
ssh -i "${SSH_KEY}" "${REMOTE_USER}@${REMOTE_HOST}" "cd '${REMOTE_BASE_PATH}' ; docker compose down"
ssh -i "${SSH_KEY}" "${REMOTE_USER}@${REMOTE_HOST}" "docker rmi \$(docker images --format '{{.Repository}}:{{.Tag}}' | grep 'decentralised-')"
ssh -i "${SSH_KEY}" "${REMOTE_USER}@${REMOTE_HOST}" "cd '${REMOTE_BASE_PATH}' ; docker compose up -d"