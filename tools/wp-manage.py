#!/usr/bin/env python3
"""
WordPress Management CLI — sourovdeb.com
- List and publish scheduled/stuck posts
- Verify active plugins
- Check site health
- Create draft posts (tools list, complaint guidelines)

Usage:
  export WP_URL=https://sourovdeb.com
  export WP_API_KEY=your-plugin-key
  python tools/wp-manage.py status
  python tools/wp-manage.py publish-scheduled
  python tools/wp-manage.py plugins
  python tools/wp-manage.py create-drafts
"""

import os, sys, json, requests
from datetime import datetime
from argparse import ArgumentParser

WP_URL = os.environ.get("WP_URL", "https://sourovdeb.com")
WP_KEY = os.environ.get("WP_API_KEY", "")


def wp_api(path, method="GET", body=None):
    if not WP_KEY:
        print("✗ WP_API_KEY not set")
        sys.exit(1)
    url = WP_URL.rstrip("/") + "/wp-json/sourov/v1" + path
    headers = {"X-Sourov-Key": WP_KEY, "Content-Type": "application/json"}
    r = requests.request(method, url, headers=headers, json=body, timeout=30)
    if r.status_code >= 400:
        print(f"Error {r.status_code}: {r.text[:300]}")
        sys.exit(1)
    return r.json()


def cmd_status():
    """Check site health and post counts"""
    print("\n📊 Site Status")
    print("=" * 60)
    try:
        data = wp_api("/status")
        for key, val in data.items():
            print(f"  {key:.<40} {val}")
    except Exception as e:
        print(f"✗ Error: {e}")


def cmd_list_scheduled():
    """List all scheduled and draft posts"""
    print("\n📋 Scheduled & Draft Posts")
    print("=" * 60)
    try:
        data = wp_api("/scheduled")
        posts = data.get("posts", []) if isinstance(data, dict) else data
        if not posts:
            print("  (none)")
            return
        for p in posts:
            status = p.get("status", "unknown")
            date_str = str(p.get("scheduled", ""))[:16]
            title = p.get("title", "(untitled)")[:50]
            print(f"  ID {p.get('id'):>4} | {status:>7} | {date_str} | {title}")
    except Exception as e:
        print(f"✗ Error: {e}")


def cmd_publish_scheduled():
    """Publish all past-scheduled posts"""
    print("\n🚀 Publishing Scheduled Posts")
    print("=" * 60)
    try:
        data = wp_api("/scheduled")
        posts = data.get("posts", []) if isinstance(data, dict) else data
        futures = [p for p in posts if p.get("status") == "future"]
        if not futures:
            print("  ✓ No scheduled posts to publish")
            return

        print(f"  Found {len(futures)} scheduled post(s)")
        for p in futures:
            pid = p.get("id")
            title = p.get("title", "(untitled)")
            scheduled = str(p.get("scheduled", ""))[:16]
            print(f"    • ID {pid} | {scheduled} | {title}")

        print("\n  ⚠️  Note: Manually publish via WordPress admin:")
        print("      go to /wp-admin → Posts → select each post → Publish")
        print("      or use the Bulk action to publish multiple at once")
    except Exception as e:
        print(f"✗ Error: {e}")


def cmd_plugins():
    """List active plugins"""
    print("\n🔌 Active Plugins")
    print("=" * 60)
    try:
        data = wp_api("/status")

        # Check the diagnostic endpoint instead for more details
        diag = requests.get(f"{WP_URL}/wp-json/sourov-diagnostic/v1/health", timeout=10).json()
        plugins = diag.get("plugins", data.get("plugins", []))

        if isinstance(plugins, dict):
            for name, info in plugins.items():
                status = "✓" if info.get("active") else "○"
                version = info.get("version", "")
                print(f"  {status} {name} {version}")
        elif isinstance(plugins, list):
            for p in plugins:
                print(f"  ✓ {p}")
        else:
            print(f"  {plugins}")

        print("\n  Expected plugins:")
        print("    ✓ sourov-ai-controller (create/schedule posts)")
        print("    ✓ sourov-automation-agent (SEO automation)")
        print("    ✓ sourov-diagnostic-agent (monitoring)")
        print("    ✓ aicu-engine-reach (IndexNow notifications)")
    except Exception as e:
        print(f"✗ Error: {e}")


def cmd_create_drafts():
    """Create tools/software list and complaint guidelines as drafts"""
    print("\n✏️  Creating Draft Posts")
    print("=" * 60)

    posts = [
        {
            "title": "WordPress Remote Control & Publishing Automation Tools",
            "category": "AI Tools",
            "tags": "automation, wordpress, tools, publishing, AI, remote-control",
            "content": TOOLS_LIST,
        },
        {
            "title": "Feedback & Complaint Guidelines",
            "category": "Personal",
            "tags": "guidelines, feedback, complaints, communication",
            "content": COMPLAINT_GUIDELINES,
        },
    ]

    for post in posts:
        post["status"] = "draft"
        try:
            result = wp_api("/ai-post", "POST", post)
            pid = result.get("id") or result.get("post_id")
            print(f"  ✓ Created draft: {post['title']}")
            print(f"    ID: {pid} | URL: {result.get('link', 'N/A')}")
        except Exception as e:
            print(f"  ✗ Failed: {post['title']}")
            print(f"    {e}")


TOOLS_LIST = """<h2>Complete Publishing Automation Toolkit</h2>

<p>This document describes all the tools, scripts, and integrations available for <strong>sourovdeb.com</strong>.</p>

<h3>1. Core Tools (Installed)</h3>

<h4>Python Desktop App</h4>
<ul>
<li><strong>File:</strong> <code>tools/wp-desktop.py</code></li>
<li><strong>Type:</strong> Standalone GUI (Tkinter)</li>
<li><strong>Use case:</strong> Daily writing, non-technical users</li>
<li><strong>Features:</strong> Two modes (AI generates or you write), auto SEO fill, scheduling, post manager</li>
<li><strong>Run:</strong> <code>python tools/wp-desktop.py</code></li>
<li><strong>Config storage:</strong> <code>~/.wp-studio/config.json</code></li>
</ul>

<h4>Google Sheets + Apps Script</h4>
<ul>
<li><strong>File:</strong> <code>tools/sheets-publisher.js</code></li>
<li><strong>Type:</strong> Google Apps Script</li>
<li><strong>Use case:</strong> Batch publishing, team collaboration, scheduled content calendar</li>
<li><strong>Features:</strong> Hourly auto-run, status tracking per row, AI SEO auto-fill</li>
<li><strong>Setup:</strong> Paste into Google Apps Script, run setup functions once</li>
<li><strong>Publishing:</strong> Add row with Status=READY or SCHEDULE, wait for hourly trigger</li>
</ul>

<h4>GitHub Actions + Markdown</h4>
<ul>
<li><strong>File:</strong> <code>.github/workflows/wp-publish.yml</code></li>
<li><strong>Type:</strong> CI/CD workflow</li>
<li><strong>Use case:</strong> Write → push → published (developers)</li>
<li><strong>Features:</strong> YAML frontmatter, automatic AI SEO, supports scheduling</li>
<li><strong>Secrets needed:</strong> WP_URL, WP_API_KEY, CLAUDE_KEY</li>
<li><strong>Usage:</strong> Create <code>posts/my-post.md</code>, push to GitHub</li>
</ul>

<h4>Logseq Bridge</h4>
<ul>
<li><strong>File:</strong> <code>tools/logseq-bridge.py</code></li>
<li><strong>Type:</strong> CLI tool</li>
<li><strong>Use case:</strong> Logseq writers who export to Markdown</li>
<li><strong>Features:</strong> Converts Logseq syntax to HTML, reads inline properties, auto SEO</li>
<li><strong>Usage:</strong> <code>python tools/logseq-bridge.py "Day 37.md" --publish</code></li>
</ul>

<h4>Markdown Publisher</h4>
<ul>
<li><strong>File:</strong> <code>tools/publish-from-markdown.py</code></li>
<li><strong>Type:</strong> CLI tool</li>
<li><strong>Use case:</strong> Bulk publishing, GitHub Actions backend</li>
<li><strong>Features:</strong> YAML frontmatter parsing, Markdown→HTML conversion, AI SEO</li>
<li><strong>Usage:</strong> <code>python tools/publish-from-markdown.py posts/ --all</code></li>
</ul>

<h3>2. AI Providers Supported</h3>

<ul>
<li><strong>Claude (Anthropic)</strong> – <code>claude-haiku-4-5-20251001</code> (lightweight, fast)</li>
<li><strong>DeepSeek</strong> – open-source alternative</li>
<li><strong>Ollama (local)</strong> – free, runs on your machine</li>
</ul>

<h3>3. WordPress Plugins (Deployed)</h3>

<table>
<thead>
<tr>
<th>Plugin</th>
<th>Function</th>
<th>Auth</th>
<th>Endpoint</th>
</tr>
</thead>
<tbody>
<tr>
<td>sourov-ai-controller</td>
<td>Create/schedule/delete posts via API</td>
<td>X-Sourov-Key header</td>
<td>POST /wp-json/sourov/v1/ai-post</td>
</tr>
<tr>
<td>sourov-automation-agent</td>
<td>Search engine verification meta tags</td>
<td>X-Sourov-Key header</td>
<td>/wp-json/sourov/v1/verify</td>
</tr>
<tr>
<td>sourov-diagnostic-agent</td>
<td>System monitoring (read-only)</td>
<td>None (public)</td>
<td>GET /wp-json/sourov-diagnostic/v1/health</td>
</tr>
<tr>
<td>aicu-engine-reach</td>
<td>IndexNow auto-notification</td>
<td>Automatic</td>
<td>(hook-based)</td>
</tr>
</tbody>
</table>

<h3>4. External Integrations (Optional)</h3>

<ul>
<li><strong>n8n</strong> (self-hosted, free) – Google Docs → WordPress with AI nodes</li>
<li><strong>Activepieces</strong> (open-source) – workflow automation</li>
<li><strong>Buffer</strong> (paid) – social media + WordPress scheduling</li>
<li><strong>Zapier</strong> (paid) – email-to-post, form-to-post workflows</li>
</ul>

<h3>5. SEO & Indexing</h3>

<ul>
<li><strong>Auto-generated by each tool:</strong>
<ul>
<li>5 relevant tags</li>
<li>SEO-optimized title (max 60 chars)</li>
<li>Meta description (120–155 chars)</li>
<li>Focus keyphrase</li>
</ul>
</li>
<li><strong>IndexNow:</strong> Automatic via WordPress plugin on publish</li>
<li><strong>Google Search Console:</strong> Verify site, submit sitemap</li>
<li><strong>Bing Webmaster:</strong> Verify site, add to index</li>
</ul>

<h3>6. Recommended Workflow</h3>

<ol>
<li><strong>Daily writing:</strong> Use Python Desktop App or Google Sheets</li>
<li><strong>Batch publishing:</strong> GitHub Actions (push Markdown files)</li>
<li><strong>Logseq integration:</strong> Export → Logseq Bridge → publish</li>
<li><strong>Team collaboration:</strong> Google Sheets with hourly auto-run</li>
<li><strong>Advanced automation:</strong> n8n for complex workflows</li>
</ol>

<h3>7. Configuration</h3>

<ul>
<li><strong>Example config:</strong> <code>config.example.json</code></li>
<li><strong>Desktop app storage:</strong> <code>~/.wp-studio/config.json</code></li>
<li><strong>GitHub Secrets:</strong> WP_URL, WP_API_KEY, CLAUDE_KEY</li>
<li><strong>Google Sheets:</strong> Properties Service (encrypted)</li>
</ul>

<h3>8. Support & Troubleshooting</h3>

<ul>
<li>Check site status: <code>python tools/wp-manage.py status</code></li>
<li>List scheduled posts: <code>python tools/wp-manage.py list-scheduled</code></li>
<li>View active plugins: <code>python tools/wp-manage.py plugins</code></li>
</ul>
"""

COMPLAINT_GUIDELINES = """<h2>Feedback & Complaint Guidelines</h2>

<p>Thank you for taking the time to share your thoughts. This document outlines how to provide feedback, report issues, or lodge complaints in a way that leads to the best possible resolution.</p>

<h3>1. Types of Feedback We Welcome</h3>

<h4>✓ Content Quality Issues</h4>
<ul>
<li>Factual errors or outdated information</li>
<li>Unclear explanations or confusing examples</li>
<li>Missing context or incomplete sections</li>
<li>Suggest: Provide the specific section, what was unclear, and what would help</li>
</ul>

<h4>✓ Technical Issues</h4>
<ul>
<li>Broken links or missing resources</li>
<li>Page layout or display problems</li>
<li>Slow loading or accessibility issues</li>
<li>Suggest: Screenshot + browser/device + steps to reproduce</li>
</ul>

<h4>✓ Topic Suggestions</h4>
<ul>
<li>Requests for specific teaching techniques, lesson ideas, or ELT tools</li>
<li>Topics you'd like deeper coverage on</li>
<li>Suggest: Be specific about your teaching context and what you're struggling with</li>
</ul>

<h4>✓ User Experience Feedback</h4>
<ul>
<li>Navigation confusing or unintuitive</li>
<li>Mobile experience issues</li>
<li>Search function not working</li>
<li>Suggest: Tell me what you expected vs. what happened</li>
</ul>

<h3>2. How to Report Feedback</h3>

<h4>Option A: Email</h4>
<p><strong>To:</strong> sourovdeb@zohomail.com<br/>
<strong>Subject line format:</strong> [FEEDBACK] or [BUG] or [SUGGESTION]<br/>
<strong>Best for:</strong> Detailed issues, privacy concerns</p>

<h4>Option B: GitHub Issues</h4>
<p><strong>Link:</strong> https://github.com/sourovdeb/wordpress-control/issues<br/>
<strong>Best for:</strong> Technical bugs, feature requests, tool issues<br/>
<strong>Format:</strong> Use the template provided; include steps to reproduce</p>

<h4>Option C: Direct Message (Twitter/LinkedIn)</h4>
<p><strong>Best for:</strong> Quick questions, non-urgent feedback<br/>
<strong>Note:</strong> Response time may be slower</p>

<h3>3. What Makes Effective Feedback</h3>

<table>
<thead>
<tr>
<th>❌ Unhelpful</th>
<th>✅ Helpful</th>
</tr>
</thead>
<tbody>
<tr>
<td>"This post is bad"</td>
<td>"The example in section 2.3 contradicts the lesson plan format you described earlier. Could you clarify?"</td>
</tr>
<tr>
<td>"Your site doesn't work"</td>
<td>"On Chrome/Mac, the video in 'Day 15' won't load. Error message: 'Failed to fetch resource'. Happened at 3pm GMT on June 3."</td>
</tr>
<tr>
<td>"Why didn't you cover X?"</td>
<td>"I teach teen learners with low motivation. I'd love a post on engagement strategies for this age group."</td>
</tr>
<tr>
<td>"You're wrong"</td>
<td>"Recent research (cite source) suggests a different approach to X. Could you update the post with this perspective?"</td>
</tr>
</tbody>
</table>

<h3>4. Complaint Escalation Process</h3>

<h4>Level 1: Clarification</h4>
<p>Your feedback will be read and understood. If clarification is needed, I'll ask questions.</p>

<h4>Level 2: Acknowledgment</h4>
<p>You'll receive a response within <strong>7 business days</strong> acknowledging the issue and indicating next steps.</p>

<h4>Level 3: Resolution</h4>
<ul>
<li><strong>Content errors:</strong> Corrected within 14 days; you'll be notified of changes</li>
<li><strong>Technical issues:</strong> Diagnosed and fixed or documented (with workaround if fix is pending)</li>
<li><strong>Topic requests:</strong> Added to content calendar; expect a post within 30 days or explanation of why it's deprioritized</li>
<li><strong>UX issues:</strong> Investigated and fixed in next site update (typically monthly)</li>
</ul>

<h4>Level 4: Dispute Resolution</h4>
<p>If you disagree with a resolution, you can request a second opinion from another colleague. Response within 10 business days.</p>

<h3>5. Privacy & Data</h3>

<ul>
<li><strong>Your feedback:</strong> Used only to improve the site and content</li>
<li><strong>Your email:</strong> Never shared with third parties; used only for direct reply</li>
<li><strong>Public issues:</strong> GitHub issues are public; don't include sensitive personal information</li>
<li><strong>Confidential matters:</strong> Email preferred over public channels</li>
</ul>

<h3>6. What We Cannot Address</h3>

<ul>
<li>Requests for immediate one-on-one tutoring (I offer coaching separately)</li>
<li>Issues unrelated to the site or content (e.g., general CELTA exam prep)</li>
<li>Spam, harassment, or abusive messages (will be deleted without response)</li>
<li>Demands for refunds (all content is free and always will be)</li>
</ul>

<h3>7. Community Standards</h3>

<p>To keep the feedback process constructive:</p>

<ul>
<li><strong>Be respectful.</strong> Disagree with ideas, not people.</li>
<li><strong>Be specific.</strong> Vague complaints waste everyone's time.</li>
<li><strong>Be constructive.</strong> Suggest solutions, not just problems.</li>
<li><strong>Be patient.</strong> I manage this site alone; responses aren't instant.</li>
</ul>

<h3>8. Thank You</h3>

<p>This site exists because people like you care about teaching and learning. Your feedback makes it better. Thank you for taking the time to contribute. 🙏</p>

<p><strong>Sourov DEB</strong><br/>
June 2026</p>
"""


def main():
    parser = ArgumentParser(description="WordPress Management CLI")
    parser.add_argument("command", nargs="?", default="help",
                        choices=["help", "status", "list-scheduled", "publish-scheduled", "plugins", "create-drafts"])
    args = parser.parse_args()

    commands = {
        "status":            cmd_status,
        "list-scheduled":    cmd_list_scheduled,
        "publish-scheduled": cmd_publish_scheduled,
        "plugins":           cmd_plugins,
        "create-drafts":     cmd_create_drafts,
    }

    if args.command == "help":
        parser.print_help()
        print("\nExamples:")
        print("  python tools/wp-manage.py status")
        print("  python tools/wp-manage.py list-scheduled")
        print("  python tools/wp-manage.py create-drafts")
        return

    cmd = commands.get(args.command)
    if cmd:
        cmd()
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
