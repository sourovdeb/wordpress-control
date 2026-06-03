#!/usr/bin/env python3
"""
GitHub Actions Publisher — sourovdeb.com
Reads .md files from posts/ and publishes to WordPress via the custom API.

Used by .github/workflows/wp-publish.yml on every push.
Can also be run manually:
  python tools/publish-from-markdown.py posts/my-post.md
  python tools/publish-from-markdown.py --all
  python tools/publish-from-markdown.py --changed-only   (GitHub Actions mode)

Env vars (set as GitHub Secrets or export locally):
  WP_URL        https://sourovdeb.com
  WP_API_KEY    your-plugin-secret-key
  CLAUDE_KEY    sk-ant-...  (optional, for auto SEO)

Post frontmatter example:
  ---
  title: "Day 36: Teaching Pronunciation"
  status: publish          # publish | future | draft
  date: 2026-06-15T09:00:00  # required if status: future
  category: ELT Masterclass
  seo: auto                # auto = AI generates tags/meta/seo_title
  tags: pronunciation, ELT, phonology   # manual tags (overrides auto)
  ---
  Write your post content here in plain Markdown.
"""

import os, sys, re, json, subprocess, argparse
import requests

WP_URL     = os.environ.get("WP_URL",     "https://sourovdeb.com")
WP_API_KEY = os.environ.get("WP_API_KEY", "")
CLAUDE_KEY = os.environ.get("CLAUDE_KEY", "")

try:
    import yaml
    import markdown as md_lib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML", "markdown"])
    import yaml
    import markdown as md_lib


# ── Markdown file parser ──────────────────────────────────────────────────────
def parse_post_file(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    frontmatter = {}
    body        = raw

    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', raw, re.DOTALL)
    if m:
        frontmatter = yaml.safe_load(m.group(1)) or {}
        body        = m.group(2).strip()

    html = md_lib.markdown(
        body,
        extensions=["extra", "toc"],
        extension_configs={"toc": {"toc_depth": "2-4"}},
    )
    return frontmatter, html, body


# ── AI SEO auto-fill ──────────────────────────────────────────────────────────
def autofill_seo(title, content_preview):
    if not CLAUDE_KEY:
        return {}
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key":         CLAUDE_KEY,
            "anthropic-version": "2023-06-01",
            "content-type":      "application/json",
        },
        json={
            "model":      "claude-haiku-4-5-20251001",
            "max_tokens": 500,
            "system":     "SEO expert for ELT educator blog. Return ONLY valid JSON.",
            "messages": [{
                "role":    "user",
                "content": f'Title: "{title}"\nContent: {content_preview[:600]}\nReturn: {{"tags":["t1","t2","t3","t4","t5"],"category":"ELT Masterclass","meta_description":"120-155 chars","seo_title":"max 60 chars"}}',
            }],
        },
        timeout=30,
    )
    r.raise_for_status()
    raw = r.json()["content"][0]["text"].strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(raw)


# ── WordPress publisher ───────────────────────────────────────────────────────
def publish_post(title, html, fm, seo):
    status = str(fm.get("status", "draft"))
    tags_fm = fm.get("tags", "")
    if isinstance(tags_fm, list):
        tags_fm = ", ".join(str(t) for t in tags_fm)

    post = {
        "title":            title,
        "content":          html,
        "status":           status,
        "category":         str(fm.get("category") or seo.get("category") or "ELT"),
        "tags":             tags_fm or ", ".join(seo.get("tags", [])),
        "meta_description": str(fm.get("meta_description") or seo.get("meta_description") or ""),
        "seo_title":        str(fm.get("seo_title")        or seo.get("seo_title")        or title),
    }
    if status == "future" and fm.get("date"):
        post["date"] = str(fm["date"])

    url = WP_URL.rstrip("/") + "/wp-json/sourov/v1/ai-post"
    r   = requests.post(
        url,
        headers={"X-Sourov-Key": WP_API_KEY, "Content-Type": "application/json"},
        json=post,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


# ── Git helpers ───────────────────────────────────────────────────────────────
def get_changed_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=AM", "HEAD~1", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return [f for f in result.stdout.strip().splitlines()
                if f.startswith("posts/") and f.endswith(".md")]
    except subprocess.CalledProcessError:
        # First commit — get all tracked files
        result = subprocess.run(
            ["git", "show", "--name-only", "--format=", "HEAD"],
            capture_output=True, text=True,
        )
        return [f for f in result.stdout.strip().splitlines()
                if f.startswith("posts/") and f.endswith(".md")]


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Publish markdown posts to WordPress")
    group  = parser.add_mutually_exclusive_group()
    group.add_argument("--changed-only", action="store_true",
                       help="Process only files changed in the last git commit (GitHub Actions mode)")
    group.add_argument("--all",          action="store_true",
                       help="Process all .md files in posts/")
    parser.add_argument("files", nargs="*", metavar="FILE",
                        help="Specific file(s) to process")
    args = parser.parse_args()

    if not WP_API_KEY:
        print("✗ WP_API_KEY env var not set")
        sys.exit(1)

    # Determine which files to process
    if args.changed_only:
        files = get_changed_files()
        print(f"Changed post files: {files or 'none'}")
    elif args.all:
        files = []
        for root, _, fnames in os.walk("posts"):
            for fn in fnames:
                if fn.endswith(".md") and not fn.startswith("."):
                    files.append(os.path.join(root, fn))
    elif args.files:
        files = args.files
    else:
        parser.print_help()
        sys.exit(0)

    if not files:
        print("No markdown files to process.")
        sys.exit(0)

    failed = False
    for fpath in files:
        if not os.path.exists(fpath):
            print(f"\nSkip (not found): {fpath}")
            continue

        print(f"\nProcessing: {fpath}")
        fm, html, body = parse_post_file(fpath)

        status = str(fm.get("status", "draft"))
        if status not in ("publish", "future", "draft"):
            print(f"  Skip: status='{status}' (not publish/future/draft)")
            continue

        title = (
            str(fm.get("title") or "")
            or os.path.splitext(os.path.basename(fpath))[0]
                .replace("-", " ").replace("_", " ").title()
        )
        print(f"  Title:  {title}")
        print(f"  Status: {status}")

        seo = {}
        if fm.get("seo") == "auto":
            if CLAUDE_KEY:
                print("  Auto-filling SEO…")
                try:
                    seo = autofill_seo(title, body)
                    print(f"  Tags: {seo.get('tags', [])}")
                except Exception as e:
                    print(f"  SEO auto-fill failed (continuing): {e}")
            else:
                print("  CLAUDE_KEY not set — skipping SEO auto-fill")

        try:
            result = publish_post(title, html, fm, seo)
            pid    = result.get("id") or result.get("post_id")
            link   = result.get("link", "")
            print(f"  ✓ Published! ID:{pid}  {link}")
        except requests.HTTPError as e:
            print(f"  ✗ HTTP error: {e}")
            print(f"    Response: {e.response.text[:300]}")
            failed = True
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed = True

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
