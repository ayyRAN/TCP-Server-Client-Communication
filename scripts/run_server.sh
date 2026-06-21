#!/usr/bin/env bash
set -euo pipefail

# Runs the TCP server tests and saves them to a log file
# Usage: ./scripts/run_server.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

STAMP="$(date +"%Y%m%d_%H%M%S")"
LOG_FILE="$LOG_DIR/servertests_${STAMP}.log"

echo "Running tests"
echo "Logging to: $LOG_FILE"


# Adjust server entrypoint as needed:
pytest test_server.py -v 2>&1 | tee "$LOG_FILE"