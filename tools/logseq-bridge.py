#!/usr/bin/env python3
"""
Logseq → WordPress Bridge — sourovdeb.com
Converts a Logseq markdown export to HTML and posts to WordPress.
Auto-fills tags, category, meta description, and SEO title via Claude AI.

Requirements: pip install requests
Config: ~/.wp-studio/config.json (created by wp-desktop.py)

Usage:
  python logseq-bridge.py "Day 36 Pronunciation.md"
  python logseq-bridge.py "Day 36 Pronunciation.md" --publish
  python logseq-bridge.py "Day 36 Pronunciation.md" --schedule 2026-06-15T09:00:00
  python logseq-bridge.py "Day 36 Pronunciation.md" --no-seo   (skip AI, publish as-is)

Logseq frontmatter properties supported (optional — add to the top of your Logseq page):
  - status:: publish      (publish | draft | future)
  - category:: ELT Masterclass
  - schedule:: 2026-06-15T09:00:00
  - title:: Custom title  (default: filename)
"""

import sys, os, re, json, argparse
import requests

CONFIG_FILE = os.path.expanduser("~/.wp-studio/config.json")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"\nConfig not found at: {CONFIG_FILE}")
        print("Run wp-desktop.py first and save your settings (Settings tab).\n")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)


# ── Logseq Markdown Parser ────────────────────────────────────────────────────
def parse_logseq_file(path):
    """
    Returns: (title, html_content, props_dict)
    Handles Logseq-specific syntax: property lines, [[wiki links]], bullet structure.
    """
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    props = {}
    body_lines = []

    for line in raw.splitlines():
        # Logseq property: "- key:: value" or "key:: value"
        m = re.match(r'^[-\s]*([a-zA-Z][\w-]*)::[ \t]+(.*)', line)
        if m:
            props[m.group(1).lower()] = m.group(2).strip()
        else:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    # Strip wiki links: [[link text]] → link text
    body = re.sub(r'\[\[(.+?)\]\]', r'\1', body)

    # Strip Logseq task keywords
    body = re.sub(r'^(\s*[-*]\s+)(TODO|DONE|LATER|NOW|WAITING)\s+', r'\1', body, flags=re.MULTILINE)

    # Strip Logseq block IDs: id:: uuid lines
    body = re.sub(r'\n\s*id::\s*[^\n]+', '', body)

    html = _md_to_html(body)

    title = (
        props.get("title")
        or os.path.splitext(os.path.basename(path))[0]
            .replace("-", " ").replace("_", " ").strip()
    )

    return title, html, props


def _md_to_html(md):
    """Minimal but practical Markdown → HTML converter."""
    lines  = md.splitlines()
    output = []
    in_ul  = False
    in_p   = False

    def close_open():
        nonlocal in_ul, in_p
        if in_ul:  output.append("</ul>"); in_ul = False
        if in_p:   output.append("</p>"); in_p = False

    def inline(text):
        # Bold, italic, code
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         text)
        text = re.sub(r'`(.+?)`',       r'<code>\1</code>',     text)
        return text

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            close_open()
            continue

        # Headings (## or # or ### → h2/h3/h4 to avoid duplicating h1)
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            close_open()
            level = min(len(m.group(1)) + 1, 5)
            output.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        # Bullet list (Logseq format: "- " or "* ")
        m = re.match(r'^[-*]\s+(.*)', line)
        if m:
            if in_p: close_open()
            if not in_ul:
                output.append("<ul>")
                in_ul = True
            output.append(f"  <li>{inline(m.group(1))}</li>")
            continue

        # Ordered list: "1. "
        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            if in_ul or in_p: close_open()
            output.append(f"<ol><li>{inline(m.group(1))}</li></ol>")
            continue

        # Blockquote
        if line.startswith(">"):
            close_open()
            output.append(f"<blockquote>{inline(line[1:].strip())}</blockquote>")
            continue

        # Regular paragraph text
        if in_ul:
            output.append("</ul>")
            in_ul = False
        if not in_p:
            output.append("<p>")
            in_p = True
        output.append(inline(line))

    close_open()
    return "\n".join(output)


# ── AI SEO Auto-fill ──────────────────────────────────────────────────────────
def autofill_seo(cfg, title, html_preview):
    provider = cfg.get("ai_provider", "claude")
    system   = "You are an SEO expert for an ELT educator's blog. Return ONLY valid JSON."
    prompt   = f"""Title: {title}
Content preview: {html_preview[:800]}

Return exactly:
{{"tags": ["tag1","tag2","tag3","tag4","tag5"],
  "category": "ELT Masterclass",
  "meta_description": "120-155 char SEO description",
  "seo_title": "max 60 char SEO title"}}"""

    if provider == "claude":
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key":         cfg["claude_key"],
                "anthropic-version": "2023-06-01",
                "content-type":      "application/json",
            },
            json={
                "model":      "claude-haiku-4-5-20251001",
                "max_tokens": 500,
                "system":     system,
                "messages":   [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        r.raise_for_status()
        raw = r.json()["content"][0]["text"]
    elif provider == "deepseek":
        r = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {cfg['deepseek_key']}",
                "Content-Type":  "application/json",
            },
            json={
                "model":    "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt},
                ],
            },
            timeout=30,
        )
        r.raise_for_status()
        raw = r.json()["choices"][0]["message"]["content"]
    else:
        return {}

    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)


# ── WordPress Publisher ───────────────────────────────────────────────────────
def post_to_wp(cfg, post_data):
    url = cfg["wp_url"].rstrip("/") + "/wp-json/sourov/v1/ai-post"
    r   = requests.post(
        url,
        headers={"X-Sourov-Key": cfg["plugin_key"], "Content-Type": "application/json"},
        json=post_data,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Publish a Logseq markdown file to WordPress",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("file",       help="Path to .md file exported from Logseq")
    parser.add_argument("--publish",  action="store_true", help="Publish immediately")
    parser.add_argument("--draft",    action="store_true", help="Save as draft (default if no flag)")
    parser.add_argument("--schedule", metavar="DATETIME",  help="Schedule: 2026-06-15T09:00:00")
    parser.add_argument("--no-seo",   action="store_true", help="Skip AI SEO auto-fill")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)

    cfg = load_config()
    print(f"\nReading: {args.file}")

    title, html, props = parse_logseq_file(args.file)
    print(f"Title:   {title}")

    # Determine status (CLI flag > Logseq property > default draft)
    if args.schedule:
        status = "future"
    elif args.publish:
        status = "publish"
    elif props.get("status"):
        status = props["status"]
    else:
        status = "draft"

    schedule_date = args.schedule or props.get("schedule", "")

    seo = {}
    if not args.no_seo:
        ai_key = cfg.get("claude_key") or cfg.get("deepseek_key")
        if ai_key:
            print("Auto-filling SEO…")
            try:
                seo = autofill_seo(cfg, title, html)
                print(f"  Tags:     {', '.join(seo.get('tags', []))}")
                print(f"  Category: {seo.get('category','')}")
                print(f"  SEO title:{seo.get('seo_title','')}")
            except Exception as e:
                print(f"  SEO auto-fill failed (skipping): {e}")
        else:
            print("No AI key configured — skipping SEO auto-fill.")

    post = {
        "title":            title,
        "content":          html,
        "status":           status,
        "category":         props.get("category") or seo.get("category") or "ELT",
        "tags":             ", ".join(seo.get("tags", [])),
        "meta_description": seo.get("meta_description", ""),
        "seo_title":        seo.get("seo_title") or title,
    }
    if schedule_date:
        post["date"] = schedule_date

    print(f"\nPosting as '{status}'…")
    try:
        result = post_to_wp(cfg, post)
        pid    = result.get("id") or result.get("post_id")
        link   = result.get("link", "")
        print(f"\n✓ Success! Post ID: {pid}")
        if link:
            print(f"  URL: {link}")
    except requests.HTTPError as e:
        print(f"\n✗ Failed: {e}")
        print(f"  Response: {e.response.text[:400]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
