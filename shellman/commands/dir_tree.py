from __future__ import annotations

import fnmatch
import importlib.resources
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

import click


@click.command(help="Print a visual directory tree.")
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--files", "-f", is_flag=True, help="Include files, not just folders")
@click.option("--depth", "-d", type=int, help="Limit recursion depth (0 = root only)")
@click.option("--output", "-o", type=click.Path(), help="Save result to file")
@click.option("--hidden", "-hd", is_flag=True, help="Include hidden files/folders")
@click.option(
    "--exclude",
    "-x",
    multiple=True,
    help=(
        "Exclude patterns, for example: __pycache__, *.txt, *.pyc. "
        "Can be used multiple times."
    ),
)
@click.option("--lang-help", "lang", help="Show localized help (pl, eng)")
@click.option(
    "--ascii",
    "-a",
    "use_ascii",
    is_flag=True,
    help="Use ASCII instead of Unicode box lines",
)
def cli(path, files, depth, output, hidden, exclude, lang, use_ascii):
    """
    Print a visual tree of directories and optionally files.
    """
    if lang:
        _print_help_md(lang)
        return

    if depth is not None and depth < 0:
        raise click.BadParameter("Depth must be 0 or greater.", param_hint="--depth")

    default_excludes = ["__pycache__", "*.pyc"]
    exclude_patterns = list(default_excludes) + list(exclude)

    root = Path(path).resolve()
    tree = _build_tree(
        root=root,
        include_files=files,
        max_depth=depth,
        show_hidden=hidden,
        ascii_mode=use_ascii,
        exclude_patterns=exclude_patterns,
    )

    if output:
        output_path = Path(output)
        if output_path.parent != Path("."):
            output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(tree, encoding="utf-8")
        click.echo(f"Saved to {output_path}")
        return

    click.echo(tree)


def _build_tree(
    *,
    root: Path,
    include_files: bool,
    max_depth: Optional[int],
    show_hidden: bool,
    ascii_mode: bool,
    exclude_patterns: Iterable[str],
) -> str:
    """Build a directory tree representation."""
    if ascii_mode:
        elbow = "+-- "
        tee = "|-- "
        pipe = "|   "
        space = "    "
    else:
        elbow = "└── "
        tee = "├── "
        pipe = "│   "
        space = "    "

    lines: list[str] = []

    def is_excluded(entry: Path) -> bool:
        """Return True if entry matches any exclude pattern."""
        name = entry.name
        path_str = str(entry)

        for pattern in exclude_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True

            if fnmatch.fnmatch(path_str, pattern):
                return True

        return False

    def list_entries(dir_path: Path) -> list[Path]:
        """List directory entries with filters applied."""
        try:
            items = list(dir_path.iterdir())
        except PermissionError:
            return []

        if not show_hidden:
            items = [entry for entry in items if not entry.name.startswith(".")]

        items = [entry for entry in items if not is_excluded(entry)]

        if not include_files:
            items = [entry for entry in items if entry.is_dir()]

        items.sort(key=lambda entry: (entry.is_file(), entry.name.lower()))
        return items

    def walk(dir_path: Path, prefix: str, level: int) -> None:
        """Walk through directories and append formatted tree lines."""
        if max_depth is not None and level >= max_depth:
            return

        entries = list_entries(dir_path)

        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = elbow if is_last else tee

            display_name = f"{entry.name}/" if entry.is_dir() else entry.name
            lines.append(f"{prefix}{connector}{display_name}")

            if entry.is_dir():
                child_prefix = prefix + (space if is_last else pipe)
                walk(entry, child_prefix, level + 1)

    lines.append(f"{root.name}/")

    if max_depth is None or max_depth > 0:
        walk(root, prefix="", level=0)

    return "\n".join(lines)


def _print_help_md(lang: str) -> None:
    """Print localized help text for the dir_tree command."""
    lang_file = f"help_{lang.lower()}.md"

    try:
        help_path = (
            importlib.resources.files("shellman")
            .joinpath("help_texts")
            .joinpath("dir_tree")
            .joinpath(lang_file)
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"Help not available for language: {lang}", err=True)