#!/usr/bin/env bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the build
#${SCRIPT_DIR}/build-function.sh

# Deploy our function to Cortex
#cortex actions deploy default/fair-topK --code "${SCRIPT_DIR}/build/function.zip" --kind python:3

docker build -t hguptacs/cortex-skill:recommend-2.0 .
docker push hguptacs/cortex-skill:recommend-2.0
cortex actions deploy default/recommend --actionType daemon --docker hguptacs/cortex-skill:recommend-2.0 --timeout 300000 --port '6000' --cmd '[]'
