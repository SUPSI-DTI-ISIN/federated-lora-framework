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

sync_dev_api "../../institute/data-service" "data-service-client"
#sync_dev_api "../inference-service" "inference-service-client"
sync_dev_api "../../institute/model-service" "model-service-client"
sync_dev_api "../../institute/chat-service" "chat-service-client"

sync_dev_api "../../department/mlflow-service" "mlflow-service-client"
sync_dev_api "../../department/institute-service" "institute-service-client"
sync_dev_api "../../department/federated-learning-management-service" "federated-learning-management-service-client"