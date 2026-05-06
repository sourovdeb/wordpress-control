# WP AutoPilot 🚀

> WordPress blog scheduling automation powered by **DeepSeek AI** + **WordPress REST API**  
> Hybrid pipeline: AI SEO generation → smart queue → scheduled publishing

---

## What it does

| Step | What happens |
|------|-------------|
| **1. Read queue** | Loads posts from CSV, JSON, or Google Sheets |
| **2. AI enrichment** | DeepSeek generates SEO title, meta description, slug, focus keyword, tags, excerpt |
| **3. Smart scheduling** | Assigns publish slots without conflicts, respects preferred days/hours |
| **4. Duplicate detection** | Checks WordPress before creating to avoid double-posting |
| **5. REST API posting** | Creates posts with `status: future`, injects Yoast/Rank Math meta |
| **6. Rollback** | If any post fails, optionally deletes the successful ones |

---

## Why DeepSeek?

- **Cost**: DeepSeek-chat is ~30× cheaper than GPT-4o for the same structured output tasks
- **Quality**: Excellent at structured JSON output for SEO field generation
- **Speed**: Fast enough for batch processing dozens of posts
- **API compatibility**: OpenAI-compatible — easy to swap models

---

## Quick start

```bash
# 1. Clone / copy the project
cd wp_autopilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env with your WordPress URL, username, app password, and DeepSeek key

# 4. Test the connection
python main.py ping

# 5. Preview what would be scheduled (no changes made)
python main.py run sample_queue.csv --dry

# 6. Run for real
python main.py run sample_queue.csv
```

---

## Commands

```
python main.py ping                        # Test WP connection
python main.py schedule-check             # Show existing schedule
python main.py enrich queue.csv           # Run AI only, preview SEO fields
python main.py enrich queue.csv -o out.json  # Save enriched data to JSON
python main.py run queue.csv              # Full pipeline
python main.py run queue.csv --dry        # Dry run — safe preview
python main.py run queue.csv --no-ai      # Skip DeepSeek (use existing metadata)
python main.py run queue.csv --yes        # Skip confirmation prompts (for automation)
python main.py run queue.csv --log run.json  # Save results log to JSON
python main.py run gsheet                 # Use Google Sheets as queue source
```

---

## Queue format (CSV)

```csv
title,content,publish_date,category,tags,seo_keyword,status,priority
"My Post Title","# Markdown or HTML content here","2026-05-10","Tech,Blog","python,tips","python tips",ready,1
"Another Post","Content...","","Productivity","focus,adhd","focus techniques",ready,2
```

| Column | Required | Description |
|--------|----------|-------------|
| `title` | ✓ | Post title |
| `content` | ✓ | Markdown or HTML body |
| `publish_date` | — | ISO date (e.g. 2026-05-10). Leave blank for auto-schedule |
| `category` | — | Comma-separated category names (created if missing) |
| `tags` | — | Comma-separated tag names (merged with AI suggestions) |
| `seo_keyword` | — | Focus keyword hint for DeepSeek |
| `status` | — | Must be `ready` to be processed |
| `priority` | — | Lower number = scheduled first |

---

## Environment variables

```env
# Required
WP_URL=https://yourblog.com
WP_USERNAME=your_wp_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
DEEPSEEK_MODEL=deepseek-chat        # or deepseek-reasoner
PUBLISH_DAYS=1,3                    # 0=Mon … 6=Sun
PUBLISH_HOUR=9                      # 24h format, site timezone
MIN_GAP_HOURS=48
SEO_PLUGIN=yoast                    # yoast | rankmath | aioseo | none
```

---

## WordPress setup

1. Go to **WP Admin → Users → Your Profile → Application Passwords**
2. Enter name `WP AutoPilot` and click **Add New Application Password**
3. Copy the generated password (spaces included) into `WP_APP_PASSWORD`
4. Ensure your site uses **HTTPS** and has **pretty permalinks** enabled
5. Verify the REST API is accessible: `https://yoursite.com/wp-json/wp/v2/`

---

## Supported SEO plugins

| Plugin | Keys written |
|--------|-------------|
| **Yoast SEO** | `_yoast_wpseo_title`, `_yoast_wpseo_metadesc`, `_yoast_wpseo_focuskw` |
| **Rank Math** | `rank_math_title`, `rank_math_description`, `rank_math_focus_keyword` |
| **AIOSEO** | `_aioseo_title`, `_aioseo_description`, `_aioseo_keywords` |
| **none** | No SEO meta written |

---

## Google Sheets setup (optional)

1. Create a Google Cloud project and enable the Sheets + Drive APIs
2. Create a service account and download `credentials.json`
3. Share your sheet with the service account email
4. Set `GSHEET_CREDENTIALS_JSON`, `GSHEET_ID`, `GSHEET_SHEET_NAME` in `.env`
5. Use `python main.py run gsheet`

Sheet columns must match the CSV format. After scheduling, the tool writes back:
`status`, `wp_post_id`, `scheduled_date`, `wp_url` to each processed row.

---

## Project structure

```
wp_autopilot/
├── main.py                  # CLI entry point (typer + rich)
├── requirements.txt
├── .env.example
├── sample_queue.csv
└── wp_autopilot/
    ├── __init__.py
    ├── config.py            # Config from .env
    ├── models.py            # QueuedPost, EnrichedSEO, ScheduleResult
    ├── deepseek.py          # DeepSeek API client → SEO field generation
    ├── enricher.py          # Markdown→HTML + DeepSeek pipeline
    ├── scheduler.py         # Smart slot assignment, conflict detection
    ├── wordpress.py         # WP REST API client (posts, taxonomy, media)
    └── queue_reader.py      # CSV / JSON / Google Sheets readers
```

---

## Improvements over existing tools

| Feature | OpenClaw | n8n | Zapier | **WP AutoPilot** |
|---------|---------|-----|--------|-----------------|
| DeepSeek AI | ✗ | ✗ | ✗ | ✓ |
| Open source | ✗ | ✓ | ✗ | ✓ |
| Multi-post queue | limited | ✓ | ✓ | ✓ |
| Conflict detection | ✗ | ✗ | ✗ | ✓ |
| Dry-run mode | ✗ | ✗ | ✗ | ✓ |
| Rollback | ✗ | ✗ | ✗ | ✓ |
| Yoast + Rank Math | ✓ | partial | ✗ | ✓ |
| CSV / JSON / Sheets | ✗ | ✓ | ✓ | ✓ |
| Self-hosted | ✗ | ✓ | ✗ | ✓ |
| No monthly fee | ✗ | ✓ | ✗ | ✓ |
