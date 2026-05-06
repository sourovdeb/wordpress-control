"""
wp_autopilot/enricher.py
Orchestrates the full SEO enrichment pipeline for a batch of posts.

Steps per post:
  1. Convert markdown content → HTML (if needed)
  2. Call DeepSeek to generate SEO fields
  3. Apply generated fields back to post
"""
from __future__ import annotations
import re
from typing import TYPE_CHECKING

from .models import QueuedPost
from .deepseek import DeepSeekEnricher

if TYPE_CHECKING:
    from .config import Config


def _is_html(text: str) -> bool:
    """Heuristic: does this look like HTML already?"""
    return bool(re.search(r"<(p|h[1-6]|div|ul|ol|li|strong|em|a)\b", text, re.I))


def _markdown_to_html(md_text: str) -> str:
    """Convert markdown to HTML using python-markdown."""
    try:
        import markdown
        return markdown.markdown(
            md_text,
            extensions=["extra", "codehilite", "toc", "nl2br"],
        )
    except ImportError:
        # Fallback: very basic markdown-like conversion
        text = md_text
        text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", text, flags=re.M)
        text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", text, flags=re.M)
        text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", text, flags=re.M)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        paragraphs = re.split(r"\n{2,}", text)
        return "\n".join(
            p if p.startswith("<") else f"<p>{p.strip()}</p>"
            for p in paragraphs if p.strip()
        )


class Enricher:
    """Full enrichment pipeline: markdown → HTML, then DeepSeek SEO generation."""

    def __init__(self, config: "Config") -> None:
        self.deepseek = DeepSeekEnricher(config)

    def enrich_post(self, post: QueuedPost) -> None:
        """Enrich a single post in-place."""
        # Step 1: Convert content to HTML
        if post.content and not _is_html(post.content):
            post.content_html = _markdown_to_html(post.content)
        else:
            post.content_html = post.content

        # Step 2: DeepSeek generates SEO fields
        seo = self.deepseek.enrich(post)

        # Step 3: Apply back to post
        self.deepseek.apply_to_post(post, seo)

    def enrich_batch(
        self,
        posts: list[QueuedPost],
        on_progress=None,
    ) -> list[QueuedPost]:
        """
        Enrich all posts. Calls on_progress(i, total, post) after each.
        Returns the same list (mutated in-place).
        """
        for i, post in enumerate(posts, 1):
            self.enrich_post(post)
            if on_progress:
                on_progress(i, len(posts), post)
        return posts
