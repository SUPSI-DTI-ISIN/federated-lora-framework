#!/bin/bash
set -e

cd ..

set -a
source .env
set +a

flwr run .