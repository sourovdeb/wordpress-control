#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUTO_DIR="$ROOT_DIR/automation"
PY="$AUTO_DIR/.venv/bin/python"
QUEUE_FILE="$AUTO_DIR/sample_queue.csv"
GUIDE_FILE="$ROOT_DIR/docs/USER_GUIDE_CREDENTIALS_AND_LOGINS.md"

print_header() {
  echo "============================================================"
  echo "WordPress AutoPilot - Click and Play"
  echo "============================================================"
}

precheck() {
  if [[ ! -x "$PY" ]]; then
    echo "Missing virtual environment: $AUTO_DIR/.venv"
    echo "Run: bash $ROOT_DIR/scripts/setup_automation_env.sh"
    echo "Guide: $GUIDE_FILE"
    return 1
  fi

  if [[ ! -f "$AUTO_DIR/.env" ]]; then
    echo "Missing automation/.env"
    echo "Run: cp $AUTO_DIR/.env.example $AUTO_DIR/.env"
    echo "Then set WP_URL, WP_USERNAME, WP_APP_PASSWORD, and DEEPSEEK_API_KEY"
    echo "Guide: $GUIDE_FILE"
    return 1
  fi

  return 0
}

connection_test() {
  echo
  echo "Running connection test..."
  if "$PY" "$AUTO_DIR/main.py" ping; then
    return 0
  fi

  echo
  echo "Not ready: WordPress connection failed."
  echo "Common fixes:"
  echo "1) Set WP_URL to the WordPress site root (example: https://example.com)"
  echo "2) Confirm this endpoint returns JSON in a browser: <WP_URL>/wp-json/"
  echo "3) Verify WP application password belongs to WP_USERNAME"
  echo "Guide: $GUIDE_FILE"
  return 1
}

run_dry() {
  echo
  echo "Starting dry run with sample queue..."
  "$PY" "$AUTO_DIR/main.py" run "$QUEUE_FILE" --dry
}

run_live() {
  echo
  read -r -p "This will create scheduled posts on WordPress. Continue? [y/N] " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then
    "$PY" "$AUTO_DIR/main.py" run "$QUEUE_FILE"
  else
    echo "Cancelled."
  fi
}

open_workspace() {
  if command -v code >/dev/null 2>&1; then
    code "$ROOT_DIR" >/dev/null 2>&1 &
    echo "Opened WordPress Control in VS Code."
  else
    echo "VS Code command 'code' is not available in PATH."
  fi
}

open_guide() {
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$GUIDE_FILE" >/dev/null 2>&1 &
    echo "Opened setup guide."
  else
    echo "Guide: $GUIDE_FILE"
  fi
}

run_finalizer() {
  bash "$ROOT_DIR/scripts/finalize_setup.sh"
}

main_menu() {
  echo
  echo "Choose action:"
  echo "1) Run final setup check"
  echo "2) Dry run sample queue"
  echo "3) Live run sample queue"
  echo "4) Open WordPress Control workspace"
  echo "5) Open credentials guide"
  echo "6) Exit"
  read -r -p "Select [1-6]: " choice

  case "$choice" in
    1) run_finalizer ;;
    2) run_dry ;;
    3) run_live ;;
    4) open_workspace ;;
    5) open_guide ;;
    6) echo "Done." ;;
    *) echo "Invalid choice." ;;
  esac
}

print_header
precheck
connection_test
main_menu
