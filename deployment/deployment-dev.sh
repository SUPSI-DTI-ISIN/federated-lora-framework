#!/bin/bash
set -e
set -o pipefail

if [ ! -f .env.docker ]; then
  echo "Error: .env.docker file not found"
  exit 1
fi

set -a
source .env.docker
set +a

docker compose -f ../docker/docker-compose.dev.yml down -v
docker compose -f ../docker/docker-compose.dev.yml build
docker compose -f ../docker/docker-compose.dev.yml up -d