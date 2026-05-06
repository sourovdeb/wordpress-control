"""
wp_autopilot/config.py
Centralised configuration loaded from .env
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    # WordPress
    wp_url: str = ""
    wp_username: str = ""
    wp_app_password: str = ""

    # DeepSeek
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"

    # Scheduling
    publish_days: list[int] = field(default_factory=lambda: [1, 3])   # Tue, Thu
    publish_hour: int = 9
    min_gap_hours: int = 48

    # SEO plugin
    seo_plugin: str = "yoast"   # yoast | rankmath | aioseo | none

    # Google Sheets (optional)
    gsheet_credentials_json: str = ""
    gsheet_id: str = ""
    gsheet_sheet_name: str = "Queue"

    @classmethod
    def from_env(cls) -> "Config":
        raw_days = os.getenv("PUBLISH_DAYS", "1,3")
        days = [int(d.strip()) for d in raw_days.split(",") if d.strip().isdigit()]
        return cls(
            wp_url=os.getenv("WP_URL", "").rstrip("/"),
            wp_username=os.getenv("WP_USERNAME", ""),
            wp_app_password=os.getenv("WP_APP_PASSWORD", ""),
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            publish_days=days,
            publish_hour=int(os.getenv("PUBLISH_HOUR", "9")),
            min_gap_hours=int(os.getenv("MIN_GAP_HOURS", "48")),
            seo_plugin=os.getenv("SEO_PLUGIN", "yoast").lower(),
            gsheet_credentials_json=os.getenv("GSHEET_CREDENTIALS_JSON", ""),
            gsheet_id=os.getenv("GSHEET_ID", ""),
            gsheet_sheet_name=os.getenv("GSHEET_SHEET_NAME", "Queue"),
        )

    def validate(self, require_wp: bool = True, require_ai: bool = True) -> list[str]:
        """Return list of validation errors (empty = all good)."""
        errors = []
        if require_wp:
            if not self.wp_url:
                errors.append("WP_URL is not set")
            if not self.wp_username:
                errors.append("WP_USERNAME is not set")
            if not self.wp_app_password:
                errors.append("WP_APP_PASSWORD is not set")
        if require_ai and not self.deepseek_api_key:
            errors.append("DEEPSEEK_API_KEY is not set")
        if self.seo_plugin not in ("yoast", "rankmath", "aioseo", "none"):
            errors.append(f"SEO_PLUGIN '{self.seo_plugin}' is invalid — use yoast, rankmath, aioseo, or none")
        return errors

    @property
    def wp_api_base(self) -> str:
        return f"{self.wp_url}/wp-json/wp/v2"

    @property
    def wp_auth(self) -> tuple[str, str]:
        return (self.wp_username, self.wp_app_password)
