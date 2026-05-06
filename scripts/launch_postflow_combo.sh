#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUTO_DIR="$ROOT_DIR/automation"
PY="$AUTO_DIR/.venv/bin/python"
HTML_IN_REPO="$ROOT_DIR/dashboard/PostFlow-wordpress.html"
HTML_FALLBACK="/home/sourov/PostFlow-wordpress.html"
PORT="8765"
LOG_FILE="$ROOT_DIR/.postflow_http.log"
PING_LOG="$ROOT_DIR/.postflow_ping.log"

find_html() {
  if [[ -f "$HTML_IN_REPO" ]]; then
    echo "$HTML_IN_REPO"
    return 0
  fi
  if [[ -f "$HTML_FALLBACK" ]]; then
    echo "$HTML_FALLBACK"
    return 0
  fi
  echo ""
}

if [[ ! -x "$PY" ]]; then
  echo "Missing Python venv: $PY"
  echo "Run: bash $ROOT_DIR/scripts/setup_automation_env.sh"
  exit 1
fi

HTML_FILE="$(find_html)"
if [[ -z "$HTML_FILE" ]]; then
  echo "PostFlow HTML not found."
  echo "Expected one of:"
  echo "  - $HTML_IN_REPO"
  echo "  - $HTML_FALLBACK"
  exit 1
fi

HTML_DIR="$(dirname "$HTML_FILE")"
HTML_NAME="$(basename "$HTML_FILE")"
URL="http://127.0.0.1:$PORT/$HTML_NAME"

# Ensure the local UI endpoint actually serves the expected HTML.
if pgrep -f "http.server $PORT" >/dev/null 2>&1; then
  if ! curl -fsS "$URL" >/dev/null 2>&1; then
    pkill -f "http.server $PORT" || true
    nohup "$PY" -m http.server "$PORT" --directory "$HTML_DIR" >"$LOG_FILE" 2>&1 &
  fi
else
  nohup "$PY" -m http.server "$PORT" --directory "$HTML_DIR" >"$LOG_FILE" 2>&1 &
fi

# Fire a backend connectivity check in background so Python automation is active.
nohup "$PY" "$AUTO_DIR/main.py" ping >"$PING_LOG" 2>&1 || true

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 &
fi

echo "PostFlow combo started."
echo "UI:  $URL"
echo "HTTP server log: $LOG_FILE"
echo "Python ping log: $PING_LOG"
echo "Tip: check credentials in $AUTO_DIR/.env if ping reports HTTP 404."
