#!/bin/sh

# shellcheck disable=SC2016
envsubst '$MLFLOW_SERVICE_URL $INSTITUTE_SERVICE_URL $FEDERATED_LEARNING_MANAGEMENT_SERVICE_URL $PORT' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx -g 'daemon off;'