#!/bin/sh

# shellcheck disable=SC2016
envsubst '$INFERENCE_SERVICE_URL $DATA_SERVICE_URL $MODEL_SERVICE_URL $PORT' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf

exec nginx -g 'daemon off;'