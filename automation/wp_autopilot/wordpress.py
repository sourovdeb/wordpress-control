"""
wp_autopilot/wordpress.py
WordPress REST API client.

Handles:
  - Auth (application passwords)
  - Category / tag resolution + creation
  - Post creation with scheduling
  - SEO meta injection (Yoast, Rank Math, AIOSEO)
  - Featured image upload from URL or local file
  - Duplicate detection
  - Existing schedule inspection
"""
from __future__ import annotations
import base64
import mimetypes
import re
import urllib.request
from datetime import datetime
from typing import Optional, TYPE_CHECKING

import requests
from slugify import slugify

from .models import QueuedPost, ScheduleResult

if TYPE_CHECKING:
    from .config import Config

# SEO plugin meta key maps
SEO_META_MAPS: dict[str, dict[str, str]] = {
    "yoast": {
        "title":    "_yoast_wpseo_title",
        "desc":     "_yoast_wpseo_metadesc",
        "keyword":  "_yoast_wpseo_focuskw",
        "og_desc":  "_yoast_wpseo_opengraph-description",
        "og_title": "_yoast_wpseo_opengraph-title",
    },
    "rankmath": {
        "title":    "rank_math_title",
        "desc":     "rank_math_description",
        "keyword":  "rank_math_focus_keyword",
        "og_desc":  "rank_math_og_description",
        "og_title": "rank_math_og_title",
    },
    "aioseo": {
        "title":    "_aioseo_title",
        "desc":     "_aioseo_description",
        "keyword":  "_aioseo_keywords",
        "og_desc":  "_aioseo_og_description",
        "og_title": "_aioseo_og_title",
    },
}


class WordPressClient:
    """Thin wrapper around the WordPress REST API."""

    def __init__(self, config: "Config") -> None:
        self.config = config
        self.base = config.wp_api_base
        self.auth = config.wp_auth
        self.seo_plugin = config.seo_plugin
        self._session = requests.Session()
        self._session.auth = self.auth
        self._session.headers.update({
            "User-Agent": "WPAutoPilot/1.0",
            "Accept": "application/json",
        })
        # In-memory cache: name → id
        self._category_cache: dict[str, int] = {}
        self._tag_cache: dict[str, int] = {}

    # ── connectivity ─────────────────────────────────────────────────────────

    def ping(self) -> tuple[bool, str]:
        """Verify the site is reachable and credentials work."""
        try:
            r = self._session.get(f"{self.base}/users/me", timeout=10)
            if r.status_code == 200:
                data = r.json()
                return True, data.get("name", "unknown user")
            return False, f"HTTP {r.status_code}: {r.text[:200]}"
        except requests.RequestException as e:
            return False, str(e)

    # ── taxonomy helpers ──────────────────────────────────────────────────────

    def resolve_taxonomy(self, endpoint: str, name: str, cache: dict[str, int]) -> int:
        """Return existing term ID or create the term and return the new ID."""
        name = name.strip()
        key = name.lower()
        if key in cache:
            return cache[key]

        # Search first
        r = self._session.get(
            f"{self.base}/{endpoint}",
            params={"search": name, "per_page": 5},
            timeout=10,
        )
        r.raise_for_status()
        items = r.json()
        for item in items:
            if item["name"].lower() == key:
                cache[key] = item["id"]
                return item["id"]

        # Create if not found
        r = self._session.post(
            f"{self.base}/{endpoint}",
            json={"name": name, "slug": slugify(name)},
            timeout=10,
        )
        r.raise_for_status()
        new_id = r.json()["id"]
        cache[key] = new_id
        return new_id

    def resolve_categories(self, names: list[str]) -> list[int]:
        return [self.resolve_taxonomy("categories", n, self._category_cache) for n in names if n]

    def resolve_tags(self, names: list[str]) -> list[int]:
        return [self.resolve_taxonomy("tags", n, self._tag_cache) for n in names if n]

    # ── duplicate detection ───────────────────────────────────────────────────

    def post_exists(self, title: str, slug: str) -> Optional[int]:
        """Return post ID if a post with this slug or very similar title exists, else None."""
        # Check by slug
        r = self._session.get(f"{self.base}/posts", params={"slug": slug, "per_page": 1}, timeout=10)
        if r.ok and r.json():
            return r.json()[0]["id"]

        # Fuzzy title check (search WP)
        words = " ".join(title.split()[:4])
        r = self._session.get(f"{self.base}/posts", params={"search": words, "per_page": 5}, timeout=10)
        if r.ok:
            for p in r.json():
                if p["title"]["rendered"].lower().strip() == title.lower().strip():
                    return p["id"]
        return None

    # ── scheduled post inspection ─────────────────────────────────────────────

    def get_scheduled_dates(self) -> list[datetime]:
        """Return list of datetimes for all currently scheduled (future) posts."""
        r = self._session.get(
            f"{self.base}/posts",
            params={"status": "future", "per_page": 100},
            timeout=15,
        )
        if not r.ok:
            return []
        dates = []
        for post in r.json():
            raw = post.get("date", "")
            try:
                dates.append(datetime.fromisoformat(raw))
            except ValueError:
                pass
        return sorted(dates)

    # ── media upload ──────────────────────────────────────────────────────────

    def upload_image_from_url(self, image_url: str, alt_text: str = "", filename: str = "") -> Optional[int]:
        """Download an image from a URL and upload it to WP media library."""
        try:
            with urllib.request.urlopen(image_url, timeout=15) as resp:
                image_data = resp.read()
                content_type = resp.headers.get("Content-Type", "image/jpeg")
        except Exception:
            return None

        if not filename:
            filename = image_url.split("/")[-1].split("?")[0] or "featured.jpg"
        if not re.search(r"\.\w{2,4}$", filename):
            ext = mimetypes.guess_extension(content_type.split(";")[0]) or ".jpg"
            filename += ext

        r = self._session.post(
            f"{self.base}/media",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": content_type,
            },
            data=image_data,
            timeout=30,
        )
        if not r.ok:
            return None
        media_id = r.json()["id"]

        # Set alt text
        if alt_text:
            self._session.post(f"{self.base}/media/{media_id}", json={"alt_text": alt_text}, timeout=10)

        return media_id

    # ── post creation ─────────────────────────────────────────────────────────

    def build_seo_meta(self, post: QueuedPost) -> dict[str, str]:
        """Build SEO plugin meta dict based on configured plugin."""
        keys = SEO_META_MAPS.get(self.seo_plugin, {})
        if not keys:
            return {}
        return {
            keys["title"]:    post.seo_title or post.title,
            keys["desc"]:     post.seo_description,
            keys["keyword"]:  post.seo_keyword,
            keys["og_title"]: post.seo_title or post.title,
            keys["og_desc"]:  post.seo_description,
        }

    def create_post(
        self,
        post: QueuedPost,
        scheduled_dt: datetime,
        featured_media_id: Optional[int] = None,
        dry_run: bool = False,
    ) -> ScheduleResult:
        """Create a scheduled WordPress post. Returns ScheduleResult."""

        # Resolve taxonomy IDs
        cat_ids = self.resolve_categories(post.category_list)
        tag_ids = self.resolve_tags(post.tag_list)

        seo_meta = self.build_seo_meta(post)

        payload: dict = {
            "title":      post.title,
            "content":    post.content_html or post.content,
            "excerpt":    post.excerpt,
            "slug":       post.seo_slug or slugify(post.title)[:60],
            "status":     "future",
            "date":       scheduled_dt.isoformat(),
            "categories": cat_ids,
            "tags":       tag_ids,
            "meta":       seo_meta,
        }
        if featured_media_id:
            payload["featured_media"] = featured_media_id

        if dry_run:
            return ScheduleResult(
                post=post,
                success=True,
                wp_post_id=None,
                scheduled_date=scheduled_dt.isoformat(),
            )

        r = self._session.post(f"{self.base}/posts", json=payload, timeout=20)
        if not r.ok:
            return ScheduleResult(
                post=post,
                success=False,
                error=f"HTTP {r.status_code}: {r.text[:300]}",
            )

        data = r.json()
        return ScheduleResult(
            post=post,
            success=True,
            wp_post_id=data["id"],
            wp_post_url=data.get("link", ""),
            scheduled_date=data.get("date", scheduled_dt.isoformat()),
        )

    def delete_post(self, post_id: int) -> bool:
        """Permanently delete a post (for rollback)."""
        r = self._session.delete(
            f"{self.base}/posts/{post_id}",
            params={"force": True},
            timeout=10,
        )
        return r.ok
