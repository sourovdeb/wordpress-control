"""
wp_autopilot/scheduler.py
Smart queue manager — assigns publish slots to 2+ posts without conflicts.

Algorithm:
  1. Pull existing scheduled dates from WordPress.
  2. Starting from "now + min_gap", find the next open preferred slot.
  3. Preferred slots: configured days of week at configured hour.
  4. Skip a slot if it's within min_gap_hours of any existing scheduled post.
  5. Assign slots sequentially to the queue.
"""
from __future__ import annotations
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .models import QueuedPost

if TYPE_CHECKING:
    from .config import Config


class Scheduler:
    def __init__(self, config: "Config", existing_dates: list[datetime] | None = None) -> None:
        self.config = config
        self.existing_dates: list[datetime] = existing_dates or []

    def _is_slot_free(self, candidate: datetime, min_gap_h: int) -> bool:
        """Return True if no scheduled post is within min_gap_h of candidate."""
        for existing in self.existing_dates:
            diff = abs((candidate - existing).total_seconds()) / 3600
            if diff < min_gap_h:
                return False
        return True

    def _next_preferred_slot(self, after: datetime) -> datetime:
        """Walk forward day by day until we land on a preferred weekday + hour."""
        cfg = self.config
        candidate = after.replace(
            hour=cfg.publish_hour,
            minute=0,
            second=0,
            microsecond=0,
        )
        # Move to at least tomorrow if we'd be publishing in the past or too soon
        if candidate <= after:
            candidate += timedelta(days=1)

        # Walk until we find a preferred weekday
        for _ in range(365):  # safety cap
            if candidate.weekday() in cfg.publish_days:
                if self._is_slot_free(candidate, cfg.min_gap_hours):
                    return candidate
            candidate += timedelta(days=1)

        # Fallback: any free slot (shouldn't happen in practice)
        candidate = after + timedelta(hours=cfg.min_gap_hours)
        return candidate

    def assign_slots(self, posts: list[QueuedPost]) -> list[QueuedPost]:
        """
        Assign a scheduled_datetime to each post in order.
        Posts with an explicit publish_date keep it (if it's in the future).
        Posts without one get the next available preferred slot.
        """
        last_assigned = datetime.now()
        assigned = []

        for post in sorted(posts, key=lambda p: p.priority):
            # If the user specified an explicit publish date
            if post.publish_date:
                try:
                    explicit_dt = datetime.fromisoformat(post.publish_date)
                    if explicit_dt > datetime.now():
                        post.scheduled_datetime = explicit_dt
                        # Advance our pointer so the next auto-slot is after this
                        if explicit_dt > last_assigned:
                            last_assigned = explicit_dt
                        self.existing_dates.append(explicit_dt)
                        assigned.append(post)
                        continue
                except ValueError:
                    pass  # Fall through to auto-scheduling

            # Auto-schedule: find next open slot after last_assigned
            slot = self._next_preferred_slot(last_assigned)
            post.scheduled_datetime = slot
            last_assigned = slot
            self.existing_dates.append(slot)
            assigned.append(post)

        return assigned

    def preview_schedule(self, posts: list[QueuedPost]) -> list[dict]:
        """Return a list of dicts suitable for table display."""
        rows = []
        for i, post in enumerate(posts, 1):
            dt = post.scheduled_datetime
            rows.append({
                "#":        i,
                "title":    post.title[:48] + ("…" if len(post.title) > 48 else ""),
                "date":     dt.strftime("%a %b %d, %Y") if dt else "—",
                "time":     dt.strftime("%H:%M") if dt else "—",
                "category": post.category or "—",
                "keyword":  post.seo_keyword[:30] if post.seo_keyword else "—",
            })
        return rows
