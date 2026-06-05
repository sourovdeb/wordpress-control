#!/usr/bin/env python3
"""
WordPress Category & Tag Cleanup
Fixes: creates missing categories, splits malformed tags, reassigns posts

Run once:
  export WP_URL=https://sourovdeb.com
  export WP_API_KEY=0767044896thevenet_
  python tools/wp-fix-taxonomy.py fix-all
"""

import os, sys, requests, json
from argparse import ArgumentParser

WP_URL = os.environ.get("WP_URL", "https://sourovdeb.com")
WP_KEY = os.environ.get("WP_API_KEY", "")

# Standard categories for your site
STANDARD_CATEGORIES = {
    "ELT Masterclass": "Complete 60-day English teaching course",
    "ELT": "General English language teaching",
    "CELTA": "CELTA certification topics",
    "Job Hunting": "Job search and career advice",
    "AI Tools": "AI tools and automation",
    "Teaching Resources": "Lesson plans and materials",
    "Personal": "Personal reflections and life",
    "English Teaching": "English teaching techniques",
}

# Tag fixes (malformed tags that need splitting)
TAG_FIXES = {
    49: ["adhd", "bipolar", "mental-health", "routine", "productivity", "morning-routine"],
    50: ["ielts", "teaching", "adhd", "english", "celta", "writing-task-2", "band-7"],
    51: ["la-reunion", "remote-teaching", "bilingual", "freelance", "english-training", "positioning"],
    52: ["automation", "wordpress", "tools", "publishing", "ai", "remote-control"],
    53: ["guidelines", "feedback", "complaints", "communication"],
}


def wp_api(path, method="GET", body=None, is_v2=False):
    """WordPress REST API call"""
    if not WP_KEY:
        print("✗ WP_API_KEY not set")
        sys.exit(1)

    version = "wp/v2" if is_v2 else "sourov/v1"
    url = WP_URL.rstrip("/") + f"/wp-json/{version}{path}"

    headers = {"Content-Type": "application/json"}
    if not is_v2:
        headers["X-Sourov-Key"] = WP_KEY

    r = requests.request(method, url, headers=headers, json=body, timeout=30)

    if r.status_code >= 400:
        print(f"✗ Error {r.status_code}: {r.text[:200]}")
        return None

    try:
        return r.json()
    except:
        return {"success": True}


def create_missing_categories():
    """Create categories that don't exist"""
    print("\n📂 Creating Missing Categories")
    print("=" * 60)

    existing = wp_api("/categories?per_page=100", is_v2=True)
    existing_names = {c["name"].lower(): c["id"] for c in existing}

    for cat_name, cat_desc in STANDARD_CATEGORIES.items():
        if cat_name.lower() in existing_names:
            print(f"  ✓ {cat_name} (already exists)")
        else:
            result = wp_api("/categories", method="POST", body={
                "name": cat_name,
                "description": cat_desc,
                "slug": cat_name.lower().replace(" ", "-"),
            }, is_v2=True)
            if result:
                print(f"  ✓ Created: {cat_name}")
            else:
                print(f"  ✗ Failed: {cat_name}")


def split_malformed_tags():
    """Split comma-separated tag strings into individual tags"""
    print("\n🏷️  Splitting Malformed Tags")
    print("=" * 60)

    for bad_tag_id, good_tags in TAG_FIXES.items():
        print(f"\n  Tag ID {bad_tag_id}:")
        print(f"    Splitting into: {', '.join(good_tags)}")

        # Create individual tags if they don't exist
        created_ids = []
        for tag_name in good_tags:
            # Check if tag exists
            existing = wp_api(f"/tags?search={tag_name}", is_v2=True)
            if existing:
                created_ids.append(existing[0]["id"])
                print(f"    ✓ {tag_name} (id={existing[0]['id']})")
            else:
                # Create new tag
                result = wp_api("/tags", method="POST", body={
                    "name": tag_name,
                    "slug": tag_name.lower().replace(" ", "-"),
                }, is_v2=True)
                if result and "id" in result:
                    created_ids.append(result["id"])
                    print(f"    ✓ Created {tag_name} (id={result['id']})")

        # Delete the malformed tag
        delete_result = wp_api(f"/tags/{bad_tag_id}", method="DELETE", is_v2=True)
        if delete_result is not None:
            print(f"    ✓ Deleted malformed tag id={bad_tag_id}")


def reassign_uncategorized_posts():
    """Move posts from Uncategorized to appropriate categories"""
    print("\n🔄 Reassigning Posts")
    print("=" * 60)

    # Get all uncategorized posts
    uncats = wp_api("/posts?categories=1&per_page=100", is_v2=True)
    if not uncats:
        print("  No uncategorized posts found")
        return

    # Simple mapping based on post title/content
    # Posts with "Day X" → ELT Masterclass
    # Posts with "Job" → Job Hunting
    # Default → English Teaching

    for post in uncats:
        title = post.get("title", {}).get("rendered", "").lower()

        if "day" in title and "of 60" in title:
            new_cat_name = "ELT Masterclass"
        elif any(w in title for w in ["job", "hiring", "resume", "interview", "career", "contact"]):
            new_cat_name = "Job Hunting"
        elif any(w in title for w in ["tool", "ai", "automation", "github", "python"]):
            new_cat_name = "AI Tools"
        elif any(w in title for w in ["guide", "guideline", "feedback", "complaint", "remote", "control"]):
            new_cat_name = "Teaching Resources"
        else:
            new_cat_name = "English Teaching"

        # Get category ID
        cats = wp_api(f"/categories?search={new_cat_name}", is_v2=True)
        if cats:
            cat_id = cats[0]["id"]
            # Update post
            result = wp_api(f"/posts/{post['id']}", method="POST", body={
                "categories": [cat_id],
            }, is_v2=True)
            if result:
                print(f"  ✓ ID {post['id']:>4} → {new_cat_name}")


def fix_plugin_tag_handling():
    """Guidance on fixing the plugin to split tags properly"""
    print("\n🔧 Plugin Tag Handling Fix")
    print("=" * 60)
    print("""
  The sourov-ai-controller plugin concatenates comma-separated tags
  as a single tag string instead of splitting them.

  To fix (requires plugin code edit):

  1. Edit: /wp-content/plugins/sourov-ai-controller/sourov-ai-controller.php

  2. Find the line that receives tags from the API (around line 80-100)

  3. Change from:
     $tags = isset($data['tags']) ? $data['tags'] : '';
     wp_set_post_tags($post_id, $tags);

  4. To:
     $tags = isset($data['tags']) ? $data['tags'] : '';
     if (is_string($tags)) {
       $tags = array_map('trim', explode(',', $tags));
     }
     wp_set_post_tags($post_id, $tags);

  5. Test with:
     POST /wp-json/sourov/v1/ai-post
     with tags: "tag1, tag2, tag3"
     Should create 3 separate tags, not 1 concatenated tag

  Alternatively, use deploy.php to update the plugin file:

  export CONTENT=$(base64 -w 0 < fixed-plugin.php)
  curl -X POST "https://www.sourovdeb.com/deploy.php?key=0767044896thevenet_" \\
    --data-urlencode "action=upload" \\
    --data-urlencode "path=wp-content/plugins/sourov-ai-controller/sourov-ai-controller.php" \\
    --data-urlencode "encoded=true" \\
    --data-urlencode "content=$CONTENT"
""")


def cmd_status():
    """Check taxonomy status"""
    print("\n📊 Taxonomy Status")
    print("=" * 60)

    cats = wp_api("/categories?per_page=100", is_v2=True)
    print(f"\n  Categories ({len(cats)} total):")
    for c in cats:
        print(f"    {c['name']:.<30} {c['count']} posts")

    tags = wp_api("/tags?per_page=100", is_v2=True)
    print(f"\n  Tags ({len(tags)} total):")
    malformed = []
    for t in tags:
        if t['count'] == 0 and any(c in t['name'] for c in [',', 'bipolar', 'adhd', 'automation', 'guidelines']):
            malformed.append(t)

    if malformed:
        print(f"\n  ⚠️  Malformed tags found ({len(malformed)}):")
        for t in malformed:
            print(f"    id={t['id']:>3}  {t['name']}")

    uncats = wp_api("/posts?categories=1&per_page=100", is_v2=True)
    print(f"\n  Uncategorized posts: {len(uncats)}")


def cmd_fix_all():
    """Run all fixes"""
    create_missing_categories()
    split_malformed_tags()
    reassign_uncategorized_posts()
    fix_plugin_tag_handling()
    print("\n✓ Taxonomy cleanup complete!")


def main():
    parser = ArgumentParser(description="Fix WordPress taxonomy issues")
    parser.add_argument("command", nargs="?", default="status",
                        choices=["status", "fix-all", "fix-categories", "fix-tags", "fix-posts"])
    args = parser.parse_args()

    commands = {
        "status":         cmd_status,
        "fix-all":        cmd_fix_all,
        "fix-categories": create_missing_categories,
        "fix-tags":       split_malformed_tags,
        "fix-posts":      reassign_uncategorized_posts,
    }

    cmd = commands.get(args.command)
    if cmd:
        cmd()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
