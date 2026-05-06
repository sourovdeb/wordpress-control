#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUTO_DIR="$ROOT_DIR/automation"

[[ -x "$AUTO_DIR/.venv/bin/python" ]] || { echo "Missing venv. Run scripts/setup_automation_env.sh" >&2; exit 1; }
[[ -f "$AUTO_DIR/.env" ]] || { echo "Missing .env. Copy automation/.env.example to automation/.env and fill values." >&2; exit 1; }

cd "$AUTO_DIR"
"$AUTO_DIR/.venv/bin/python" main.py ping
