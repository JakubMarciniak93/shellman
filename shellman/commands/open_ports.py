from __future__ import annotations

import importlib.resources
import json
import socket
from typing import Any

import click


@click.command(
    help=(
        "Show currently open TCP/UDP ports or physical serial/parallel ports "
        "(COM/LPT/tty) with process, PID, state, and device description."
    )
)
@click.option(
    "--proto",
    "-pro",
    type=click.Choice(["tcp", "udp"]),
    help="Filter by protocol",
)
@click.option(
    "--port",
    "-p",
    type=int,
    help="Filter by local port number",
)
@click.option(
    "--json",
    "-j",
    "json_out",
    is_flag=True,
    help="Output raw JSON",
)
@click.option(
    "--serial",
    "-s",
    is_flag=True,
    help="List physical serial/parallel ports instead of TCP/UDP ports",
)
@click.option(
    "--lang-help",
    "-lh",
    "lang",
    help="Show localized help (pl, eng)",
)
def cli(
    proto: str | None,
    port: int | None,
    json_out: bool,
    serial: bool,
    lang: str | None,
) -> None:
    if lang:
        _print_help_md(lang)
        return

    if serial:
        serial_ports = find_serial_ports_with_desc()

        if json_out:
            click.echo(json.dumps(serial_ports, ensure_ascii=False, indent=2))
            return

        if not serial_ports:
            click.echo("No serial (COM/LPT/tty) ports found.")
            return

        click.echo("Available serial/parallel ports:")
        for entry in serial_ports:
            description = entry["description"]
            device = entry["device"]

            if description and description != device:
                click.echo(f"  {description} ({device})")
            else:
                click.echo(f"  {device}")

        return

    network_ports = find_network_ports(proto=proto, port=port)

    if json_out:
        click.echo(json.dumps(network_ports, ensure_ascii=False, indent=2))
        return

    if not network_ports:
        click.echo("No matching open TCP/UDP ports.")
        return

    header = f"{'Proto':<4} {'PID':>6} {'Process':<18} {'Local':<24} {'Remote':<24} State"
    click.echo(header)
    click.echo("-" * len(header))

    for entry in network_ports:
        click.echo(
            f"{entry['proto']:<4} "
            f"{str(entry['pid']):>6} "
            f"{entry['process'][:17]:<18} "
            f"{entry['local']:<24} "
            f"{entry['remote']:<24} "
            f"{entry['state']}"
        )


def find_network_ports(proto: str | None, port: int | None) -> list[dict[str, Any]]:
    """Return open TCP/UDP network connections."""
    try:
        import psutil
    except ModuleNotFoundError as exc:
        raise click.ClickException(
            "Missing dependency: psutil. Install Shellman with project dependencies."
        ) from exc

    result = []

    try:
        connections = psutil.net_connections(kind="inet")
    except Exception as exc:
        raise click.ClickException(f"Failed to read network connections: {exc}") from exc

    for connection in connections:
        proto_name = "tcp" if connection.type == socket.SOCK_STREAM else "udp"

        if proto and proto_name != proto:
            continue

        local_port = _addr_port(connection.laddr)
        if port and local_port != port:
            continue

        entry = {
            "proto": proto_name,
            "pid": connection.pid or "-",
            "process": _proc_name(connection.pid),
            "local": _format_addr(connection.laddr),
            "remote": _format_addr(connection.raddr),
            "state": getattr(connection, "status", ""),
        }
        result.append(entry)

    result.sort(key=lambda item: (item["proto"], item["local"], str(item["pid"])))
    return result


def find_serial_ports_with_desc() -> list[dict[str, str]]:
    """Return available serial/parallel ports with descriptions."""
    try:
        from serial.tools import list_ports
    except ModuleNotFoundError as exc:
        raise click.ClickException(
            "Missing dependency: pyserial. Install Shellman with project dependencies."
        ) from exc

    ports = []

    for port in list_ports.comports():
        ports.append(
            {
                "device": port.device or "",
                "description": port.description or "",
                "hwid": port.hwid or "",
                "manufacturer": port.manufacturer or "",
            }
        )

    ports.sort(key=lambda item: item["device"])
    return ports


def _format_addr(addr: Any) -> str:
    """Format psutil address object as host:port."""
    if not addr:
        return ""

    ip = getattr(addr, "ip", None)
    port = getattr(addr, "port", None)

    if ip is None and len(addr) >= 1:
        ip = addr[0]

    if port is None and len(addr) >= 2:
        port = addr[1]

    if ip is None or port is None:
        return ""

    return f"{ip}:{port}"


def _addr_port(addr: Any) -> int | None:
    """Extract port number from psutil address object."""
    if not addr:
        return None

    port = getattr(addr, "port", None)
    if port is not None:
        return int(port)

    if len(addr) >= 2:
        return int(addr[1])

    return None


def _proc_name(pid: int | None) -> str:
    """Return process name for PID."""
    if pid is None:
        return "-"

    try:
        import psutil

        return psutil.Process(pid).name()
    except Exception:
        return "?"


def _print_help_md(lang: str = "eng") -> None:
    """Print localized help text for the open_ports command."""
    lang_file = f"help_{lang.lower()}.md"

    try:
        help_path = (
            importlib.resources.files("shellman")
            .joinpath("help_texts")
            .joinpath("open_ports")
            .joinpath(lang_file)
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"Help not available for language: {lang}", err=True)
        