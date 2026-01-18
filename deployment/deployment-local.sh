#!/bin/bash
set -e

cd ../institute/scripts
./sync-apis.sh

cd ../../docker
#echo "$GITLAB_DOCKER_REGISTRY_TOKEN" | docker login "$GITLAB_DOCKER_REGISTRY_HOST" -u "$GITLAB_DOCKER_REGISTRY_USERNAME" --password-stdin
docker compose down -v
docker compose build
docker compose up -d