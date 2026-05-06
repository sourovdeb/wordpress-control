#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUTO_DIR="$ROOT_DIR/automation"

cd "$AUTO_DIR"
python3 -m venv .venv
"$AUTO_DIR/.venv/bin/pip" install --upgrade pip
"$AUTO_DIR/.venv/bin/pip" install -r requirements.txt

echo "Automation environment ready at: $AUTO_DIR/.venv"
echo "Next: cp $AUTO_DIR/.env.example $AUTO_DIR/.env && edit credentials"
