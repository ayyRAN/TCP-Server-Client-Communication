#!/usr/bin/env bash
set -euo pipefail

# Lints/format-checks Python files in the repo.
# Usage: ./scripts/lint_py.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found"
  exit 1
fi

python3 -m pip -q install --upgrade pip >/dev/null
python3 -m pip -q install ruff >/dev/null

echo "Running ruff..."
ruff check .

echo "OK"