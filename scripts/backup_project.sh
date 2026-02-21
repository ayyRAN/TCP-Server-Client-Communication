#!/usr/bin/env bash
set -euo pipefail

# Creates a timestamped tar.gz of the project (excluding common junk).
# Usage: ./scripts/backup_project.sh [output_dir]
OUT_DIR="${1:-backups}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p "$OUT_DIR"
NAME="$(basename "$ROOT_DIR")"
STAMP="$(date +"%Y%m%d_%H%M%S")"
ARCHIVE="${OUT_DIR}/${NAME}_${STAMP}.tar.gz"

echo "Creating backup: $ARCHIVE"

tar \
  --exclude="./.git" \
  --exclude="./__pycache__" \
  --exclude="./.venv" \
  --exclude="./venv" \
  --exclude="./.pytest_cache" \
  --exclude="./logs" \
  -czf "$ARCHIVE" .

echo "Done."