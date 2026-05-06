#!/usr/bin/env python3
"""
wp_autopilot — WordPress Blog Scheduling Automation with DeepSeek AI
─────────────────────────────────────────────────────────────────────
Usage:
  python main.py run sample_queue.csv          # full run
  python main.py run sample_queue.csv --dry    # preview only, no API calls
  python main.py run sample_queue.csv --no-ai  # skip DeepSeek enrichment
  python main.py ping                          # test WP connection
  python main.py schedule-check               # show what's currently scheduled
  python main.py enrich sample_queue.csv      # only run AI enrichment, print results
"""
from __future__ import annotations
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Confirm
from rich import box

# Local imports
from wp_autopilot.config import Config
from wp_autopilot.models import QueuedPost, ScheduleResult
from wp_autopilot.queue_reader import read_queue
from wp_autopilot.enricher import Enricher
from wp_autopilot.scheduler import Scheduler
from wp_autopilot.wordpress import WordPressClient

console = Console()
app = typer.Typer(
    name="wp-autopilot",
    help="WordPress Blog Scheduling Automation with DeepSeek AI",
    add_completion=False,
)


# ── helpers ───────────────────────────────────────────────────────────────────

def load_config_or_exit(require_wp: bool = True, require_ai: bool = True) -> Config:
    cfg = Config.from_env()
    errors = cfg.validate(require_wp=require_wp, require_ai=require_ai)
    if errors:
        console.print(Panel(
            "\n".join(f"[red]✗[/red] {e}" for e in errors),
            title="[bold red]Configuration errors[/bold red]",
            border_style="red",
        ))
        console.print("[dim]Create a .env file from .env.example and fill in your credentials.[/dim]")
        raise typer.Exit(1)
    return cfg


def print_header(title: str) -> None:
    console.print()
    console.print(Panel(
        f"[bold white]{title}[/bold white]\n[dim]WP AutoPilot · DeepSeek AI + WordPress REST API[/dim]",
        border_style="blue",
        padding=(0, 2),
    ))
    console.print()


def print_posts_table(posts: list[QueuedPost], title: str = "Post queue") -> None:
    t = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold blue")
    t.add_column("#", width=3, justify="right")
    t.add_column("Title", min_width=30)
    t.add_column("Category")
    t.add_column("Tags", max_width=30)
    t.add_column("Keyword")
    t.add_column("Date", width=12)
    t.add_column("Priority", justify="center")

    for i, p in enumerate(posts, 1):
        tag_preview = ", ".join(p.tag_list[:3])
        if len(p.tag_list) > 3:
            tag_preview += f" +{len(p.tag_list)-3}"
        date_str = p.publish_date if p.publish_date else "[dim]auto[/dim]"
        t.add_row(
            str(i),
            p.title[:45] + ("…" if len(p.title) > 45 else ""),
            p.category or "—",
            tag_preview or "—",
            p.seo_keyword[:25] if p.seo_keyword else "—",
            date_str,
            str(p.priority),
        )
    console.print(t)


def print_enriched_table(posts: list[QueuedPost]) -> None:
    t = Table(title="AI-enriched SEO fields", box=box.ROUNDED, header_style="bold green")
    t.add_column("#", width=3, justify="right")
    t.add_column("SEO title", min_width=30)
    t.add_column("Slug")
    t.add_column("Keyword")
    t.add_column("Meta desc", max_width=35)
    t.add_column("AI tags", max_width=28)

    for i, p in enumerate(posts, 1):
        tag_str = ", ".join(p.seo_tags[:4])
        desc_preview = p.seo_description[:60] + "…" if len(p.seo_description) > 60 else p.seo_description
        t.add_row(
            str(i),
            p.seo_title[:42],
            p.seo_slug[:28] or "—",
            p.seo_keyword[:22] or "—",
            desc_preview or "—",
            tag_str or "—",
        )
    console.print(t)


def print_schedule_table(posts: list[QueuedPost], dry_run: bool = False) -> None:
    label = "[DRY RUN] " if dry_run else ""
    t = Table(
        title=f"{label}Assigned publish schedule",
        box=box.ROUNDED,
        header_style="bold yellow" if dry_run else "bold magenta",
    )
    t.add_column("#", width=3, justify="right")
    t.add_column("Title", min_width=30)
    t.add_column("Scheduled date", width=22)
    t.add_column("Category")
    t.add_column("Slug")

    for i, p in enumerate(posts, 1):
        dt = p.scheduled_datetime
        date_str = dt.strftime("%a %b %d, %Y  %H:%M") if dt else "—"
        t.add_row(
            str(i),
            p.title[:42] + ("…" if len(p.title) > 42 else ""),
            date_str,
            p.category or "—",
            p.seo_slug[:28] or "—",
        )
    console.print(t)


def print_results_table(results: list[ScheduleResult], dry_run: bool = False) -> None:
    t = Table(
        title="Results" + (" [dry run — nothing posted]" if dry_run else ""),
        box=box.ROUNDED,
        header_style="bold",
    )
    t.add_column("#", width=3, justify="right")
    t.add_column("Title", min_width=28)
    t.add_column("Status", width=9)
    t.add_column("WP post ID", width=10, justify="center")
    t.add_column("Scheduled date", width=22)
    t.add_column("URL / error", max_width=38)

    for i, r in enumerate(results, 1):
        if r.success:
            status = "[green]✓ OK[/green]"
            detail = r.wp_post_url or "[dim]dry run[/dim]"
            pid = str(r.wp_post_id) if r.wp_post_id else "[dim]—[/dim]"
        else:
            status = "[red]✗ FAIL[/red]"
            detail = f"[red]{r.error[:55]}[/red]"
            pid = "—"

        t.add_row(
            str(i),
            r.post.title[:40] + ("…" if len(r.post.title) > 40 else ""),
            status,
            pid,
            r.scheduled_date[:19].replace("T", "  ") if r.scheduled_date else "—",
            detail,
        )
    console.print(t)


# ── commands ──────────────────────────────────────────────────────────────────

@app.command()
def ping():
    """Test WordPress connection and show site info."""
    print_header("Connection test")
    cfg = load_config_or_exit(require_wp=True, require_ai=False)
    wp = WordPressClient(cfg)

    with console.status("[blue]Connecting to WordPress...[/blue]"):
        ok, detail = wp.ping()

    if ok:
        console.print(f"[green]✓ Connected[/green]  →  {cfg.wp_url}")
        console.print(f"[green]✓ Authenticated[/green] as [bold]{detail}[/bold]")
        day_names = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        days_str = ", ".join(day_names[d] for d in cfg.publish_days)
        console.print(f"[dim]SEO plugin: {cfg.seo_plugin}  ·  Publish days: {days_str}  ·  Hour: {cfg.publish_hour:02d}:00  ·  Gap: {cfg.min_gap_hours}h[/dim]")
    else:
        console.print(f"[red]✗ Connection failed[/red]: {detail}")
        raise typer.Exit(1)


@app.command("schedule-check")
def schedule_check():
    """Show all posts currently scheduled in WordPress."""
    print_header("Current WordPress schedule")
    cfg = load_config_or_exit(require_wp=True, require_ai=False)
    wp = WordPressClient(cfg)

    with console.status("[blue]Fetching scheduled posts...[/blue]"):
        dates = wp.get_scheduled_dates()

    if not dates:
        console.print("[yellow]No posts currently scheduled.[/yellow]")
        return

    t = Table(title="Scheduled posts", box=box.ROUNDED, header_style="bold blue")
    t.add_column("#", width=3, justify="right")
    t.add_column("Date", width=22)
    t.add_column("Day of week", width=12)

    for i, dt in enumerate(dates, 1):
        t.add_row(str(i), dt.strftime("%Y-%m-%d  %H:%M"), dt.strftime("%A"))
    console.print(t)
    console.print(f"\n[dim]{len(dates)} post(s) scheduled[/dim]")


@app.command()
def enrich(
    source: str = typer.Argument("sample_queue.csv", help="Path to CSV/JSON queue file"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Save enriched results to JSON"),
):
    """Run only AI enrichment on the queue and display SEO fields."""
    print_header("SEO enrichment preview")
    cfg = load_config_or_exit(require_wp=False, require_ai=True)

    # Load queue
    with console.status(f"[blue]Reading queue from {source}...[/blue]"):
        posts = read_queue(source, cfg)

    if not posts:
        console.print("[yellow]No ready posts found in queue.[/yellow]")
        return

    console.print(f"[green]Found {len(posts)} post(s)[/green]")
    print_posts_table(posts, "Input queue")
    console.print()

    enricher = Enricher(cfg)

    with Progress(
        SpinnerColumn(),
        TextColumn("[blue]{task.description}[/blue]"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Enriching with DeepSeek...", total=len(posts))
        def on_progress(i, total, post):
            progress.update(task, completed=i, description=f"Enriched: {post.title[:35]}")
        enricher.enrich_batch(posts, on_progress=on_progress)

    console.print()
    print_enriched_table(posts)

    if output:
        data = []
        for p in posts:
            data.append({
                "title": p.title,
                "seo_title": p.seo_title,
                "seo_description": p.seo_description,
                "slug": p.seo_slug,
                "focus_keyword": p.seo_keyword,
                "excerpt": p.excerpt,
                "ai_tags": p.seo_tags,
                "all_tags": p.tag_list,
            })
        Path(output).write_text(json.dumps(data, indent=2, ensure_ascii=False))
        console.print(f"\n[green]✓ Saved to {output}[/green]")


@app.command()
def run(
    source: str = typer.Argument("sample_queue.csv", help="Path to CSV/JSON queue, or 'gsheet'"),
    dry: bool = typer.Option(False, "--dry", "-d", help="Preview only — no API calls to WordPress"),
    no_ai: bool = typer.Option(False, "--no-ai", help="Skip DeepSeek enrichment"),
    no_confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    rollback_on_fail: bool = typer.Option(True, "--rollback/--no-rollback", help="Delete successful posts if any post fails"),
    output_log: Optional[str] = typer.Option(None, "--log", help="Save results JSON to file"),
):
    """
    Full pipeline: read queue → AI enrich → schedule → post to WordPress.
    """
    print_header("WP AutoPilot — Full Pipeline" + (" [DRY RUN]" if dry else ""))
    cfg = load_config_or_exit(require_wp=not dry, require_ai=not no_ai)

    # ── Step 1: Read queue ────────────────────────────────────────────────────
    console.rule("[blue]Step 1 · Reading queue[/blue]")
    with console.status(f"[blue]Loading posts from [bold]{source}[/bold]...[/blue]"):
        try:
            posts = read_queue(source, cfg)
        except FileNotFoundError as e:
            console.print(f"[red]✗ {e}[/red]")
            raise typer.Exit(1)

    if not posts:
        console.print("[yellow]No ready posts found in queue. Nothing to do.[/yellow]")
        raise typer.Exit(0)

    console.print(f"[green]✓ Loaded {len(posts)} post(s)[/green]")
    print_posts_table(posts)
    console.print()

    # ── Step 2: Connect to WordPress ─────────────────────────────────────────
    console.rule("[blue]Step 2 · WordPress connection[/blue]")
    wp = WordPressClient(cfg)
    if not dry:
        with console.status("[blue]Testing connection...[/blue]"):
            ok, detail = wp.ping()
        if not ok:
            console.print(f"[red]✗ Cannot connect to WordPress: {detail}[/red]")
            raise typer.Exit(1)
        console.print(f"[green]✓ Connected as [bold]{detail}[/bold][/green]")

        # Duplicate detection
        console.print()
        with console.status("[blue]Checking for duplicate posts...[/blue]"):
            dupes = []
            from slugify import slugify
            for p in posts:
                slug = p.seo_slug or slugify(p.title)[:60]
                existing_id = wp.post_exists(p.title, slug)
                if existing_id:
                    dupes.append((p, existing_id))

        if dupes:
            console.print(f"[yellow]⚠ Found {len(dupes)} potential duplicate(s):[/yellow]")
            for p, pid in dupes:
                console.print(f"  [yellow]·[/yellow] '{p.title}' → already exists (ID: {pid})")
            if not Confirm.ask("Continue anyway?"):
                raise typer.Exit(0)
    else:
        console.print("[dim]Dry run — skipping WP connection[/dim]")

    # ── Step 3: AI enrichment ─────────────────────────────────────────────────
    if no_ai:
        console.print()
        console.rule("[dim]Step 3 · AI enrichment (skipped)[/dim]")
    else:
        console.print()
        console.rule("[blue]Step 3 · DeepSeek AI enrichment[/blue]")
        enricher = Enricher(cfg)

        with Progress(
            SpinnerColumn(),
            TextColumn("[blue]{task.description}[/blue]"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Generating SEO fields...", total=len(posts))
            errors_in_enrichment = []

            def on_progress(i, total, post):
                progress.update(task, completed=i, description=f"[bold]{post.title[:35]}[/bold]")

            try:
                enricher.enrich_batch(posts, on_progress=on_progress)
            except Exception as e:
                console.print(f"[red]✗ Enrichment error: {e}[/red]")
                if not Confirm.ask("Continue without full SEO enrichment?"):
                    raise typer.Exit(1)

        console.print()
        print_enriched_table(posts)

    # ── Step 4: Scheduling ────────────────────────────────────────────────────
    console.print()
    console.rule("[blue]Step 4 · Slot assignment[/blue]")

    existing_dates = []
    if not dry:
        with console.status("[blue]Loading existing schedule...[/blue]"):
            existing_dates = wp.get_scheduled_dates()
        if existing_dates:
            console.print(f"[dim]{len(existing_dates)} post(s) already scheduled — avoiding conflicts[/dim]")

    scheduler = Scheduler(cfg, existing_dates)
    posts = scheduler.assign_slots(posts)

    console.print()
    print_schedule_table(posts, dry_run=dry)

    # ── Confirmation ──────────────────────────────────────────────────────────
    console.print()
    if dry:
        console.print(Panel(
            "[yellow]DRY RUN complete.[/yellow] No posts were sent to WordPress.\n"
            "Remove [bold]--dry[/bold] to publish for real.",
            border_style="yellow",
        ))
        if output_log:
            _save_log(posts, [], output_log)
        return

    if not no_confirm:
        console.print(f"[bold]Ready to schedule {len(posts)} post(s) to {cfg.wp_url}[/bold]")
        if not Confirm.ask("Proceed?"):
            console.print("[dim]Aborted.[/dim]")
            raise typer.Exit(0)

    # ── Step 5: Post to WordPress ─────────────────────────────────────────────
    console.print()
    console.rule("[blue]Step 5 · Posting to WordPress[/blue]")

    results: list[ScheduleResult] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[blue]{task.description}[/blue]"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scheduling posts...", total=len(posts))

        for i, post in enumerate(posts, 1):
            progress.update(task, description=f"Posting: {post.title[:35]}")

            result = wp.create_post(
                post=post,
                scheduled_dt=post.scheduled_datetime,
                dry_run=False,
            )
            results.append(result)
            progress.advance(task)

            # Small delay to avoid hammering the API
            if i < len(posts):
                time.sleep(0.5)

    # ── Results ───────────────────────────────────────────────────────────────
    console.print()
    print_results_table(results)

    failed = [r for r in results if not r.success]
    succeeded = [r for r in results if r.success]

    if failed and rollback_on_fail and succeeded:
        console.print(f"\n[red]{len(failed)} post(s) failed.[/red]")
        if Confirm.ask(f"[yellow]Roll back {len(succeeded)} successful post(s)?[/yellow]"):
            with console.status("[yellow]Rolling back...[/yellow]"):
                for r in succeeded:
                    if r.wp_post_id:
                        deleted = wp.delete_post(r.wp_post_id)
                        status = "[green]deleted[/green]" if deleted else "[red]failed to delete[/red]"
                        console.print(f"  Post {r.wp_post_id}: {status}")

    # Summary
    console.print()
    if not failed:
        console.print(Panel(
            f"[green]✓ All {len(results)} post(s) scheduled successfully![/green]\n"
            f"[dim]Check your WordPress dashboard to review.[/dim]",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[green]✓ {len(succeeded)} succeeded[/green]  [red]✗ {len(failed)} failed[/red]\n"
            + "\n".join(f"[red]  · {r.post.title}: {r.error}[/red]" for r in failed),
            border_style="red",
        ))

    if output_log:
        _save_log(posts, results, output_log)
        console.print(f"[dim]Log saved to {output_log}[/dim]")


# ── log helper ────────────────────────────────────────────────────────────────

def _save_log(posts: list[QueuedPost], results: list[ScheduleResult], path: str) -> None:
    data = {
        "run_at": datetime.now().isoformat(),
        "posts": [
            {
                "title": p.title,
                "seo_title": p.seo_title,
                "seo_slug": p.seo_slug,
                "seo_keyword": p.seo_keyword,
                "tags": p.tag_list,
                "scheduled": p.scheduled_datetime.isoformat() if p.scheduled_datetime else None,
            }
            for p in posts
        ],
        "results": [
            {
                "title": r.post.title,
                "success": r.success,
                "wp_post_id": r.wp_post_id,
                "url": r.wp_post_url,
                "scheduled_date": r.scheduled_date,
                "error": r.error,
            }
            for r in results
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False))


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()
