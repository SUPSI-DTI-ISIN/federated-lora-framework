#!/bin/bash
set -e

cd ../department/deployment
./deployment-local.sh

cd ../../institute/deployment
./deployment-local.sh