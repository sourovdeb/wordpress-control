#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUTO_DIR="$ROOT_DIR/automation"
PY="$AUTO_DIR/.venv/bin/python"
ENV_FILE="$AUTO_DIR/.env"
ENV_EXAMPLE="$AUTO_DIR/.env.example"
QUEUE_FILE="$AUTO_DIR/sample_queue.csv"
GUIDE_FILE="$ROOT_DIR/docs/USER_GUIDE_CREDENTIALS_AND_LOGINS.md"

print_section() {
  printf '\n== %s ==\n' "$1"
}

status_ok() {
  printf '[OK] %s\n' "$1"
}

status_warn() {
  printf '[WARN] %s\n' "$1"
}

status_fail() {
  printf '[FAIL] %s\n' "$1"
}

print_section "WordPress Control Finalizer"
printf 'Project: %s\n' "$ROOT_DIR"
printf 'Guide:   %s\n' "$GUIDE_FILE"

print_section "Preflight"
if [[ -x "$PY" ]]; then
  status_ok "Automation venv present"
else
  status_fail "Missing automation venv"
  printf 'Run: bash %s/scripts/setup_automation_env.sh\n' "$ROOT_DIR"
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  status_warn "Created automation/.env from template"
  printf 'Edit: %s\n' "$ENV_FILE"
  printf 'Then rerun this script.\n'
  exit 1
fi
status_ok "automation/.env present"

print_section "Configuration"
CONFIG_OUTPUT="$($PY - <<'PY'
from pathlib import Path
from dotenv import dotenv_values
from urllib.parse import urlparse
import requests

root = Path.cwd()
env_path = root / '.env'
cfg = dotenv_values(env_path)
wp_url = (cfg.get('WP_URL') or '').strip().rstrip('/')
wp_user = (cfg.get('WP_USERNAME') or '').strip()
wp_pass = (cfg.get('WP_APP_PASSWORD') or '').strip()
deepseek = (cfg.get('DEEPSEEK_API_KEY') or '').strip()

print(f"WP_URL_SET={'yes' if wp_url else 'no'}")
print(f"WP_USERNAME_SET={'yes' if wp_user else 'no'}")
print(f"WP_APP_PASSWORD_SET={'yes' if wp_pass else 'no'}")
print(f"DEEPSEEK_API_KEY_SET={'yes' if deepseek else 'no'}")

if wp_url:
    parsed = urlparse(wp_url)
    print(f"WP_URL_SCHEME_OK={'yes' if parsed.scheme in ('http','https') else 'no'}")
    print(f"WP_URL_HOST_OK={'yes' if bool(parsed.netloc) else 'no'}")
    print(f"WP_URL_PATH={parsed.path or '/'}")
    try:
        r = requests.get(f"{wp_url}/wp-json/", timeout=10)
        print(f"WP_JSON_STATUS={r.status_code}")
        print(f"WP_JSON_JSON={'yes' if 'application/json' in (r.headers.get('content-type') or '').lower() else 'no'}")
    except Exception:
        print("WP_JSON_STATUS=ERR")
        print("WP_JSON_JSON=no")
else:
    print("WP_URL_SCHEME_OK=no")
    print("WP_URL_HOST_OK=no")
    print("WP_URL_PATH=/")
    print("WP_JSON_STATUS=ERR")
    print("WP_JSON_JSON=no")
PY
)"
printf '%s\n' "$CONFIG_OUTPUT"

wp_json_status="$(printf '%s\n' "$CONFIG_OUTPUT" | awk -F= '/^WP_JSON_STATUS=/{print $2}')"
wp_url_set="$(printf '%s\n' "$CONFIG_OUTPUT" | awk -F= '/^WP_URL_SET=/{print $2}')"
wp_user_set="$(printf '%s\n' "$CONFIG_OUTPUT" | awk -F= '/^WP_USERNAME_SET=/{print $2}')"
wp_pass_set="$(printf '%s\n' "$CONFIG_OUTPUT" | awk -F= '/^WP_APP_PASSWORD_SET=/{print $2}')"

if [[ "$wp_url_set" != "yes" || "$wp_user_set" != "yes" || "$wp_pass_set" != "yes" ]]; then
  status_fail "Required WordPress credentials are incomplete"
  printf 'Guide: %s\n' "$GUIDE_FILE"
  exit 1
fi
status_ok "Required WordPress credentials are present"

print_section "Connection Test"
if "$PY" "$AUTO_DIR/main.py" ping; then
  status_ok "WordPress ping succeeded"
else
  status_warn "WordPress ping failed"
  if [[ "$wp_json_status" == "404" ]]; then
    printf 'Likely cause: WP_URL is not the correct WordPress site root, or REST is unavailable.\n'
  fi
  printf 'Guide: %s\n' "$GUIDE_FILE"
  exit 1
fi

print_section "Dry Run"
"$PY" "$AUTO_DIR/main.py" run "$QUEUE_FILE" --dry
status_ok "Dry run completed"

print_section "Ready"
status_ok "Automation setup is valid"
printf 'Next live run: %s/main.py run %s\n' "$AUTO_DIR" "$QUEUE_FILE"
