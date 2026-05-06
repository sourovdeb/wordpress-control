# WordPress Control

PostFlow-style WordPress automation workspace with two parts:

1. VS Code extension (`extension.js`, `webview.js`) for dashboard/publishing control.
2. Python automation engine in [automation](automation) for queue ingestion, AI SEO enrichment, scheduling, and WordPress REST publishing.

Setup guide:

- [docs/USER_GUIDE_CREDENTIALS_AND_LOGINS.md](docs/USER_GUIDE_CREDENTIALS_AND_LOGINS.md)

Final setup helper:

- `bash scripts/finalize_setup.sh`

## Quick Start

1. `git checkout docs/llm-surgical-playbook`
2. `bash scripts/setup_automation_env.sh`
3. `bash scripts/finalize_setup.sh`
4. If the finalizer reports a config problem, edit `automation/.env`
5. Rerun `bash scripts/finalize_setup.sh` until ping and dry run succeed

## Automation Commands

From [automation/main.py](automation/main.py):

- `python main.py ping`
- `python main.py schedule-check`
- `python main.py enrich sample_queue.csv`
- `python main.py run sample_queue.csv --dry`
- `python main.py run sample_queue.csv`
