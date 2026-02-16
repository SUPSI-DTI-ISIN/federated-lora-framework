#!/bin/bash
set -e

sync_dev_api() {
  local SERVICE_PATH=$1
  local CLIENT_NAME=$2

  echo "Syncing $CLIENT_NAME..."
  (
    cd "$SERVICE_PATH/scripts" && ./sync_api.sh
  )
}

sync_dev_api "../mlflow-service" "mlflow-service-client"
sync_dev_api "../federated-learning-management-service" "federated-learning-management-service-client"