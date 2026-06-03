# WP Auto-Publisher — sourovdeb.com

**You write. This publishes.**

You write your article. The system automatically handles:
- Tags (AI-generated from content)
- Category (AI-selected)
- Yoast SEO: meta description, SEO title, focus keyphrase
- Scheduling
- Google IndexNow notification (built into the WordPress plugin)

You never touch Yoast, tags, or categories again.

---

## The 6 Methods — Choose What Fits Your Workflow

| Method | Best for | Requires |
|---|---|---|
| **A. Python Desktop App** | Daily use, non-technical | Python installed |
| **B. Google Sheets + Script** | Team use, batch scheduling | Google account |
| **C. VS Code Extension** | Developers | VS Code |
| **D. GitHub Actions** | Write → push → published | GitHub repo (this one) |
| **E. Logseq Bridge** | Logseq writers | Python + Logseq |
| **F. Open Source Tools** | Zero-code solutions | See below |

---

## Method A — Python Desktop App (Recommended)

**`tools/wp-desktop.py`** — standalone desktop GUI. One window, two modes.

### Install (one time)
```bash
pip install requests
```

### Run
```bash
python tools/wp-desktop.py
```

### How it works
**Mode 1 — AI writes everything:**
1. Type a topic: *"Day 36: Teaching Pronunciation"*
2. Click **Generate + Auto-SEO**
3. AI writes the full post, generates tags, category, meta description, SEO title
4. Click **Publish Now** or **Schedule**

**Mode 2 — You wrote it:**
1. Paste your title and content
2. Click **Auto-Fill SEO**
3. AI adds tags, category, meta description, SEO title
4. Click **Publish Now** or **Schedule**

### First-time setup
- Open the app → Settings tab
- Enter your WordPress site URL and Plugin Key
- Enter your Claude API key (or DeepSeek)
- Click Save

---

## Method B — Google Sheets + Apps Script

**`tools/sheets-publisher.js`** — paste into Google Apps Script, runs hourly automatically.

### Sheet structure
| A: Title | B: Content/Topic | C: Category | D: Status | E: Schedule Date | F: Published URL | G: Notes |

### Status values
- `READY` → publishes immediately
- `SCHEDULE` → publishes at the date/time in column E
- `DRAFT` → saves as draft in WordPress
- (After publishing: auto-changes to `DONE`, URL added to column F)

### Setup (one time, 10 minutes)
1. Open your Google Sheet
2. **Extensions → Apps Script → New Project**
3. Paste the contents of `tools/sheets-publisher.js`
4. Edit `setupCredentials()` with your real keys, run it once, then **delete that function**
5. Run `createSheetHeaders()` to format the sheet
6. Run `createHourlyTrigger()` to set up auto-run every hour

**From now on:** add rows to the sheet, set Status to `READY`, and the script publishes them within the hour.

---

## Method C — VS Code Extension

Already in this repo (`extension.js` + `webview.js`). A full AI-powered panel inside VS Code.

### Install
```bash
cd wordpress-control
npm install
# Press F5 in VS Code to run in Extension Development Host
```

### Features
- Chat tab: talk to Claude about content strategy
- Generate tab: topic → AI → review → publish
- Posts tab: view/delete scheduled posts
- Supports Claude, DeepSeek, Ollama (local, free)

---

## Method D — GitHub Actions (Write Markdown → Push → Published)

The most "write-only" workflow for technical users.

### How it works
1. Create a file in `posts/` with this format:

```markdown
---
title: "Day 37: Error Correction Techniques"
status: publish
category: ELT Masterclass
seo: auto
---

Your post body in plain Markdown here.
No tags, no categories, no SEO fields needed.
The action handles everything.
```

2. Push to GitHub
3. The action automatically publishes it to WordPress

### GitHub Secrets to configure
Go to: **GitHub repo → Settings → Secrets and variables → Actions → New secret**

| Secret | Value |
|---|---|
| `WP_URL` | `https://sourovdeb.com` |
| `WP_API_KEY` | Your plugin secret key |
| `CLAUDE_KEY` | Your Claude API key (for SEO auto-fill) |

### Frontmatter options
```yaml
title: "Post Title"
status: publish       # publish | future | draft
date: 2026-06-15T09:00:00  # only for status: future
category: ELT Masterclass
seo: auto             # auto = AI generates all SEO fields
tags: tag1, tag2      # manual tags (skips AI tagging)
meta_description: "Manual description"  # overrides AI
seo_title: "Manual SEO title"           # overrides AI
```

---

## Method E — Logseq Bridge

**`tools/logseq-bridge.py`** — converts a Logseq page to WordPress.

### Workflow
1. Write your post in Logseq normally
2. Export the page as Markdown (right-click page → Export page → Markdown)
3. Run:

```bash
# Save as draft (review in WP admin):
python tools/logseq-bridge.py "Day 37 Error Correction.md"

# Publish immediately:
python tools/logseq-bridge.py "Day 37 Error Correction.md" --publish

# Schedule for a date:
python tools/logseq-bridge.py "Day 37 Error Correction.md" --schedule 2026-06-15T09:00:00
```

### Logseq properties (optional)
Add these to your Logseq page to set metadata inline:
```
- status:: publish
- category:: ELT Masterclass
- schedule:: 2026-06-15T09:00:00
- title:: Custom title
```

The script reads these automatically — no command-line flags needed.

---

## Method F — Open Source Tools (Zero-Code)

These tools already exist and handle the full pipeline:

| Tool | What it does | Cost |
|---|---|---|
| **[n8n](https://n8n.io)** | Visual workflow: Google Sheets/Docs → WordPress, with AI nodes | Free self-hosted |
| **[Activepieces](https://activepieces.com)** | Open-source Zapier: Notion/Sheets → WordPress | Free self-hosted |
| **[PublishPress](https://publishpress.com)** | WordPress plugin: editorial calendar, scheduling, team workflow | Free tier |
| **[WP Scheduled Posts](https://wordpress.org/plugins/wp-scheduled-posts/)** | Auto-schedule + social sharing + missed publish fix | Free |
| **[Automate.io](https://automate.io)** | Connect Google Docs → WordPress automatically | Freemium |
| **[Buffer](https://buffer.com)** | Write once → schedule to WordPress + social | Paid |

**Best no-code recommendation:** Install **n8n** (self-hosted, free) and use the Google Docs → WordPress node. Write in Google Docs, the workflow publishes automatically when you add a "PUBLISH" tag.

---

## Security Notes

- **Never commit real credentials** to this repo
- Config is stored in `~/.wp-studio/config.json` on your machine (not in git)
- GitHub secrets are encrypted and never visible in logs
- The `config.example.json` file contains only placeholder values

---

## Quick Reference

```bash
# Desktop app
python tools/wp-desktop.py

# Publish a specific markdown file
WP_URL=https://sourovdeb.com WP_API_KEY=yourkey python tools/publish-from-markdown.py posts/my-post.md

# Logseq bridge
python tools/logseq-bridge.py "My Logseq Export.md" --publish

# Check all tools work
python tools/publish-from-markdown.py --help
```
