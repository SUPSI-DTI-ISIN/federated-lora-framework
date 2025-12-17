#!/bin/bash

#if [ ! -f .env.config ]; then
#  echo "Error: .env.config file not found"
#  exit 1
#fi
source .env.config

#echo "$GITLAB_DOCKER_REGISTRY_TOKEN" | docker login "$GITLAB_DOCKER_REGISTRY_HOST" -u "$GITLAB_DOCKER_REGISTRY_USERNAME" --password-stdin
cd ../docker ; docker compose down -v
cd ../docker ; docker compose build
cd ../docker ; docker compose up -d