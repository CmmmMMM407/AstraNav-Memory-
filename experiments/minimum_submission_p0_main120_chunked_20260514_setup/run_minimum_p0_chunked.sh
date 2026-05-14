#!/usr/bin/env bash
set -eo pipefail
export NVCC_PREPEND_FLAGS="${NVCC_PREPEND_FLAGS-}"
source /root/autodl-tmp/experiments/_tools/astranav_env_official.sh
export PYTHONUNBUFFERED=1
python /root/autodl-tmp/experiments/run_minimum_p0_chunked_controller.py
