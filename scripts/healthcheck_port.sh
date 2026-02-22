# scripts/healthcheck_port.sh
#!/usr/bin/env bash
set -euo pipefail

# Checks whether a host:port is reachable and prints actionable diagnostics.
# Usage:
#   ./scripts/healthcheck_port.sh <host> <port> [timeout_seconds]
#
# Examples:
#   ./scripts/healthcheck_port.sh 127.0.0.1 5000
#   ./scripts/healthcheck_port.sh localhost 22 2

HOST="${1:-}"
PORT="${2:-}"
TIMEOUT="${3:-2}"
LOG_DIR="logs"

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

STAMP="$(date +"%Y%m%d_%H%M%S")"
LOG_FILE="$LOG_DIR/healthcheck_${STAMP}.log"

exec > >(tee -a "$LOG_FILE") 2>&1

if [[ -z "$HOST" || -z "$PORT" ]]; then
  echo "Usage: $0 <host> <port> [timeout_seconds]"
  exit 2
fi

echo "Checking connectivity to ${HOST}:${PORT} (timeout=${TIMEOUT}s)..."


# Fallback: bash /dev/tcp (works in many bash builds)
if (echo >/dev/tcp/"$HOST"/"$PORT") >/dev/null 2>&1; then
  echo "OK: ${HOST}:${PORT} is reachable."
  exit 0
else
  echo "FAIL: Cannot reach ${HOST}:${PORT}."
  echo "Tip: install netcat for better diagnostics (nc)."
  exit 1
fi