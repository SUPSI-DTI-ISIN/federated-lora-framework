#!/bin/bash
set -e

cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
flwr run .