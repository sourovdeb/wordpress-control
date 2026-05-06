"""
wp_autopilot/queue_reader.py
Read the post queue from multiple sources:
  - CSV file  (default, no extra deps)
  - JSON file
  - Google Sheets  (requires gspread + credentials)
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import TYPE_CHECKING

from .models import QueuedPost

if TYPE_CHECKING:
    from .config import Config


# ── CSV reader ────────────────────────────────────────────────────────────────

def _row_to_post(row: dict, index: int) -> QueuedPost | None:
    """Convert a flat CSV/JSON row dict to a QueuedPost. Returns None if status != ready."""
    status = row.get("status", "ready").strip().lower()
    if status not in ("ready", ""):
        return None
    try:
        priority = int(row.get("priority", 999))
    except (ValueError, TypeError):
        priority = 999

    return QueuedPost(
        title=row.get("title", "").strip(),
        content=row.get("content", "").strip(),
        category=row.get("category", "").strip(),
        tags=row.get("tags", "").strip(),
        seo_keyword=row.get("seo_keyword", "").strip(),
        publish_date=row.get("publish_date", "").strip(),
        status=status,
        priority=priority,
        source_row=index,
    )


def read_csv(filepath: str | Path) -> list[QueuedPost]:
    posts: list[QueuedPost] = []
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Queue file not found: {filepath}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            post = _row_to_post(row, i)
            if post and post.title:
                posts.append(post)
    return posts


# ── JSON reader ───────────────────────────────────────────────────────────────

def read_json(filepath: str | Path) -> list[QueuedPost]:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Queue file not found: {filepath}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("posts", [data])
    posts = []
    for i, row in enumerate(data, 1):
        post = _row_to_post(row, i)
        if post and post.title:
            posts.append(post)
    return posts


# ── Google Sheets reader ──────────────────────────────────────────────────────

def read_gsheet(config: "Config") -> list[QueuedPost]:
    """
    Read from a Google Sheet. Expects columns matching QueuedPost fields.
    Requires: GSHEET_CREDENTIALS_JSON, GSHEET_ID, GSHEET_SHEET_NAME in .env
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        raise ImportError("gspread and google-auth are required for Google Sheets: pip install gspread google-auth")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    creds = Credentials.from_service_account_file(config.gsheet_credentials_json, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(config.gsheet_id)
    ws = sh.worksheet(config.gsheet_sheet_name)

    records = ws.get_all_records()
    posts = []
    for i, row in enumerate(records, 2):  # row 2 = first data row (1 = header)
        # normalise keys to lowercase with underscores
        normalised = {k.lower().replace(" ", "_"): str(v) for k, v in row.items()}
        post = _row_to_post(normalised, i)
        if post and post.title:
            posts.append(post)
    return posts


def write_back_gsheet(config: "Config", results: list) -> None:
    """
    After scheduling, write post_id, scheduled_date, status back to source sheet.
    results: list of ScheduleResult
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        return

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(config.gsheet_credentials_json, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(config.gsheet_id)
    ws = sh.worksheet(config.gsheet_sheet_name)

    header = ws.row_values(1)
    col_status   = header.index("status") + 1 if "status" in header else None
    col_post_id  = header.index("wp_post_id") + 1 if "wp_post_id" in header else None
    col_sched    = header.index("scheduled_date") + 1 if "scheduled_date" in header else None
    col_url      = header.index("wp_url") + 1 if "wp_url" in header else None

    for result in results:
        if not result.success:
            continue
        row = result.post.source_row
        if col_status:
            ws.update_cell(row, col_status, "scheduled")
        if col_post_id and result.wp_post_id:
            ws.update_cell(row, col_post_id, str(result.wp_post_id))
        if col_sched and result.scheduled_date:
            ws.update_cell(row, col_sched, result.scheduled_date)
        if col_url and result.wp_post_url:
            ws.update_cell(row, col_url, result.wp_post_url)


# ── Auto-detect reader ────────────────────────────────────────────────────────

def read_queue(source: str, config: "Config") -> list[QueuedPost]:
    """Dispatch to the correct reader based on source type."""
    if source == "gsheet":
        return read_gsheet(config)
    p = Path(source)
    if p.suffix.lower() == ".json":
        return read_json(p)
    return read_csv(p)
