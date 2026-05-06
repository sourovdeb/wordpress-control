# WordPress Control

PostFlow-style WordPress automation workspace with two parts:

1. VS Code extension (`extension.js`, `webview.js`) for dashboard/publishing control.
2. Python automation engine in [automation](automation) for queue ingestion, AI SEO enrichment, scheduling, and WordPress REST publishing.

Setup guide:

- [docs/USER_GUIDE_CREDENTIALS_AND_LOGINS.md](docs/USER_GUIDE_CREDENTIALS_AND_LOGINS.md)

## Quick Start

1. `git checkout docs/llm-surgical-playbook`
2. `bash scripts/setup_automation_env.sh`
3. `cp automation/.env.example automation/.env` and set credentials
4. `bash scripts/run_connection_test.sh`
5. `bash scripts/run_autopilot_dry.sh`

## Automation Commands

From [automation/main.py](automation/main.py):

- `python main.py ping`
- `python main.py schedule-check`
- `python main.py enrich sample_queue.csv`
- `python main.py run sample_queue.csv --dry`
- `python main.py run sample_queue.csv`
