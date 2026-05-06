"""
wp_autopilot/deepseek.py
DeepSeek API client — generates all SEO fields for a post.

Uses the OpenAI-compatible API endpoint:
  https://api.deepseek.com  (base_url)
  Model: deepseek-chat  (fast, cheap, great for structured tasks)
         deepseek-reasoner  (slower, stronger reasoning — use for complex posts)
"""
from __future__ import annotations
import json
import re
from typing import TYPE_CHECKING

from openai import OpenAI
from slugify import slugify

from .models import EnrichedSEO, QueuedPost

if TYPE_CHECKING:
    from .config import Config


SYSTEM_PROMPT = """You are an expert SEO content strategist. 
Your job is to analyse a blog post and return optimised SEO metadata.
Always respond with a single valid JSON object — no markdown fences, no extra text.

JSON schema:
{
  "seo_title": "60 chars max, include focus keyword naturally",
  "seo_description": "150–160 chars, compelling, includes keyword, no quotes",
  "slug": "lowercase-hyphens-only-5-6-words-include-keyword",
  "focus_keyword": "primary search term, 2–4 words",
  "suggested_tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "excerpt": "2–3 engaging sentences summarising the post for readers",
  "og_description": "Slightly different from meta desc — written for social sharing"
}

Rules:
- slug: only lowercase letters, numbers, hyphens. No special chars.
- suggested_tags: 4–6 tags, lowercase, specific and search-friendly
- seo_title: must not exceed 60 characters
- seo_description: must be between 150–160 characters
- focus_keyword: the single most important search phrase the post targets
"""


class DeepSeekEnricher:
    """Calls DeepSeek to generate SEO metadata for a queued post."""

    def __init__(self, config: "Config") -> None:
        self.config = config
        self.client = OpenAI(
            api_key=config.deepseek_api_key,
            base_url="https://api.deepseek.com",
        )
        self.model = config.deepseek_model

    def enrich(self, post: QueuedPost) -> EnrichedSEO:
        """Generate all SEO fields for a post. Returns EnrichedSEO."""
        user_message = self._build_prompt(post)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,      # low temp = more consistent structured output
            max_tokens=600,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content or "{}"
        data = self._parse_response(raw, post)
        return data

    def _build_prompt(self, post: QueuedPost) -> str:
        # Truncate content to ~1200 chars to save tokens
        content_preview = post.content[:1200].strip()
        if len(post.content) > 1200:
            content_preview += "\n... [truncated]"

        parts = [
            f"Title: {post.title}",
            f"Focus keyword hint: {post.seo_keyword}" if post.seo_keyword else "",
            f"Categories: {post.category}" if post.category else "",
            f"Existing tags: {post.tags}" if post.tags else "",
            "",
            "--- Post content ---",
            content_preview,
        ]
        return "\n".join(p for p in parts if p is not None)

    def _parse_response(self, raw: str, post: QueuedPost) -> EnrichedSEO:
        """Parse the JSON response, falling back gracefully on errors."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Try to extract JSON from response if wrapped in text
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            data = json.loads(match.group(0)) if match else {}

        # Fallbacks for every field
        seo_title = data.get("seo_title", post.title)[:60]
        seo_desc = data.get("seo_description", "")[:160]
        slug = data.get("slug") or slugify(post.title)[:60]
        focus_kw = data.get("focus_keyword", post.seo_keyword or post.title.split()[0])
        tags = data.get("suggested_tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        excerpt = data.get("excerpt", "")
        og_desc = data.get("og_description", seo_desc)

        return EnrichedSEO(
            seo_title=seo_title,
            seo_description=seo_desc,
            slug=slug,
            focus_keyword=focus_kw,
            suggested_tags=[str(t).lower().strip() for t in tags[:6]],
            excerpt=excerpt,
            og_description=og_desc,
        )

    def apply_to_post(self, post: QueuedPost, seo: EnrichedSEO) -> None:
        """Write EnrichedSEO fields back onto the post object in-place."""
        post.seo_title = seo.seo_title
        post.seo_description = seo.seo_description
        post.seo_slug = seo.slug
        post.excerpt = seo.excerpt
        # Merge AI tags with any existing ones from the queue
        post.seo_tags = seo.suggested_tags
        # Keep focus keyword from AI if post didn't have one
        if not post.seo_keyword:
            post.seo_keyword = seo.focus_keyword
