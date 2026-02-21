#!/usr/bin/env bash
set -euo pipefail

# Runs the TCP server with logging and a clean shutdown.
# Usage: ./scripts/run_server.sh [PORT]
PORT="${1:-5000}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

STAMP="$(date +"%Y%m%d_%H%M%S")"
LOG_FILE="$LOG_DIR/server_${PORT}_${STAMP}.log"

echo "Starting server on port $PORT"
echo "Logging to: $LOG_FILE"
echo "Press Ctrl+C to stop."

cleanup() {
  echo "Stopping server..."
}
trap cleanup INT TERM

# Adjust server entrypoint as needed:
python3 server.py --port "$PORT" 2>&1 | tee "$LOG_FILE"