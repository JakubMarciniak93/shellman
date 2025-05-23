import click
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

@click.command(help="""Work with dates: add/subtract time, compare or format.

Examples:
  shellman date_utils --add 5d
  shellman date_utils --date "2024-12-01 13:00" --sub 2h
  shellman date_utils --date "2024-01-01" --diff "2025-04-18 09:15:00"
  shellman date_utils --format "%A, %d %B %Y, %T"
""")
@click.option("--date", "base_date", help="Base date (default: now)", default=None)
@click.option("--add", "add_input", help="Add duration (e.g. 5d, 3w, 2h, 10min)")
@click.option("--sub", "sub_input", help="Subtract duration")
@click.option("--diff", "diff_date", help="Date to compare to (diff mode)")
@click.option("--format", "format_pattern", help="Format output using strftime")
def cli(base_date, add_input, sub_input, diff_date, format_pattern):
    if base_date:
        try:
            dt = datetime.strptime(base_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                dt = datetime.strptime(base_date, "%Y-%m-%d")
            except ValueError:
                raise click.ClickException(f"Invalid base date: {base_date}")
    else:
        dt = datetime.now()

    result = dt

    def parse_duration(dur):
        match = re.match(r"(\d+)([a-zA-Z]+)", dur)
        if not match:
            raise click.ClickException(f"Invalid duration format: {dur}")
        num = int(match.group(1))
        unit = match.group(2).lower()
        return num, unit

    def apply_delta(dt, num, unit, sign):
        if sign == "-":
            num *= -1
        if unit == "d":
            return dt + timedelta(days=num)
        elif unit == "w":
            return dt + timedelta(weeks=num)
        elif unit == "m":
            return dt + relativedelta(months=num)
        elif unit == "y":
            return dt + relativedelta(years=num)
        elif unit == "q":
            return dt + relativedelta(months=3 * num)
        elif unit == "h":
            return dt + timedelta(hours=num)
        elif unit == "min":
            return dt + timedelta(minutes=num)
        elif unit == "s":
            return dt + timedelta(seconds=num)
        else:
            raise click.ClickException(f"Unsupported unit: {unit}")

    if add_input:
        n, u = parse_duration(add_input)
        result = apply_delta(dt, n, u, "+")
        click.echo(f"→ {n}{u} after {dt.strftime('%F %T')}: {result.strftime('%F %T')}")

    if sub_input:
        n, u = parse_duration(sub_input)
        result = apply_delta(dt, n, u, "-")
        click.echo(f"→ {n}{u} before {dt.strftime('%F %T')}: {result.strftime('%F %T')}")

    if diff_date:
        try:
            other = datetime.strptime(diff_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                other = datetime.strptime(diff_date, "%Y-%m-%d")
            except ValueError:
                raise click.ClickException(f"Invalid comparison date: {diff_date}")
        delta = other - dt
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        click.echo(f"→ Difference between {dt.strftime('%F %T')} and {other.strftime('%F %T')}:\n  {days} days, {hours} hours, {minutes} minutes, {secs} seconds")

    if format_pattern:
        if result != dt:
            click.echo(f"→ base:    {dt.strftime(format_pattern)}")
            click.echo(f"→ result:  {result.strftime(format_pattern)}")
        else:
            click.echo(f"→ formatted: {dt.strftime(format_pattern)}")
            