import os
from datetime import datetime, timedelta
from pathlib import Path

import click


@click.command(
    help="""Deletes unwanted files (by name, extension or age).

Examples:
  shellman clean_files --ext tmp --older-than 7 --dry-run
  shellman clean_files --path ./build --name '~' --confirm
"""
)
@click.option(
    "--path",
    "scan_path",
    type=click.Path(exists=True, file_okay=False),
    default=".",
    help="Directory to scan",
)
@click.option("--ext", "ext_filter", help="Delete files with this extension")
@click.option(
    "--name", "name_filter", help="Delete files whose name contains this pattern"
)
@click.option(
    "--older-than", "age_days", type=int, help="Delete only files older than N days"
)
@click.option("--dry-run", is_flag=True, help="Preview: list files but do NOT delete")
@click.option("--confirm", is_flag=True, help="Ask Y/n before deleting each file")
def cli(scan_path, ext_filter, name_filter, age_days, dry_run, confirm):
    scan_path = Path(scan_path)

    if not ext_filter and not name_filter:
        click.echo("Need --ext or --name (or both) to know what to delete!", err=True)
        raise click.Abort()

    candidates = []
    cutoff_time = None
    if age_days:
        cutoff_time = datetime.now() - timedelta(days=age_days)

    for file in scan_path.rglob("*"):
        if not file.is_file():
            continue
        if ext_filter and file.suffix != f".{ext_filter}":
            continue
        if name_filter and name_filter not in file.name:
            continue
        if cutoff_time and datetime.fromtimestamp(file.stat().st_mtime) > cutoff_time:
            continue
        candidates.append(file.resolve())

    if not candidates:
        click.echo("No files matched the criteria – nothing to do.")
        return

    click.echo(f"🧹  {len(candidates)} file(s) match the criteria:")
    for f in candidates:
        click.echo(f"  {f}")
    click.echo()

    if dry_run:
        click.echo("Dry‑run mode – nothing deleted.")
        return

    for file in candidates:
        delete = True
        if confirm:
            response = input(f"Delete {file}? (Y/n): ").strip().lower()
            if response == "n":
                delete = False
        if delete:
            try:
                file.unlink()
                click.echo(f"Deleted: {file}")
            except Exception as e:
                click.echo(f"Failed to delete {file}: {e}")

    click.echo("✅ Clean-up complete.")
