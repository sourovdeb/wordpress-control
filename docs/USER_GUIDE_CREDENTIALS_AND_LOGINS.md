# User Guide: Credentials and Logins

This project does not run a full local WordPress stack by itself.
It connects to an existing WordPress site over the REST API.

## What You Need

For the automation engine in `automation/.env`:

- `WP_URL`: your WordPress site root, for example `https://example.com`
- `WP_USERNAME`: the WordPress user that owns the application password
- `WP_APP_PASSWORD`: the WordPress application password from your profile
- `DEEPSEEK_API_KEY`: required if you use the Python automation with DeepSeek

For the VS Code extension settings:

- `wpai.wordpressUrl`
- `wpai.wpUser`
- `wpai.wpAppPassword`
- One AI provider credential:
  - `wpai.deepseekKey`, or
  - `wpai.claudeKey`, or
  - `wpai.ollamaUrl` and `wpai.ollamaModel`

## How To Get WordPress Credentials

1. Open your WordPress admin dashboard.
2. Go to `Users -> Profile`.
3. Find `Application Passwords`.
4. Create a new application password named `WP AutoPilot`.
5. Copy the generated password exactly as shown.

Use the same WordPress username from that profile as `WP_USERNAME`.

## Required Login Targets

- WordPress admin login: used to create the application password
- WordPress REST API: `WP_URL/wp-json/`
- AI provider login or key source:
  - DeepSeek account for `DEEPSEEK_API_KEY`, or
  - Anthropic account for `claudeKey`, or
  - local Ollama service running on your machine

## Fill The Automation File

Copy the template first:

```bash
cp automation/.env.example automation/.env
```

Then set at minimum:

```env
WP_URL=https://example.com
WP_USERNAME=your_wp_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Important:

- `WP_URL` must be the site root, not the admin URL, and not the `/wp-json/` endpoint
- `WP_URL/wp-json/` must return JSON, not `404`
- the application password must belong to `WP_USERNAME`

## Fill The VS Code Extension Settings

Open the project in VS Code, then set:

- `WP AI Studio: WordPress Url`
- `WP AI Studio: WP User`
- `WP AI Studio: WP App Password`
- your chosen AI provider fields

The extension is best for interactive control.
The Python automation is best for queue-based batch publishing.

## Fast Start

From the project root:

```bash
bash scripts/setup_automation_env.sh
bash scripts/run_connection_test.sh
bash scripts/run_autopilot_dry.sh
```

Or use the launcher:

```bash
bash scripts/click_and_play.sh
```

## What "Ready" Looks Like

- `python main.py ping` succeeds
- `WP_URL/wp-json/` returns JSON
- dry run completes without posting
- live run only starts after you confirm

## Common Failures

### HTTP 404 from ping

Usually means one of these:

- `WP_URL` is not the actual WordPress site root
- the target site is not WordPress
- REST API is blocked or permalinks are misconfigured

### Authentication fails

Usually means one of these:

- wrong `WP_USERNAME`
- wrong application password
- application password belongs to a different user

### AI generation fails

Usually means one of these:

- missing `DEEPSEEK_API_KEY`
- invalid provider key in extension settings
- local Ollama is not running

## Current Scope

The active project in this workspace is:

- `user/development/tools/wordpress-control`

There is no local checkout here of:

- `WordPress/WordPress`
- `EasyEngine/easyengine`

This project currently targets an existing WordPress site through the REST API instead of provisioning WordPress locally.