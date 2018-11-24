#!/usr/bin/env bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cortex actions invoke default/recommend --params-file "${SCRIPT_DIR}/test/test_req.json"