"""System status and health commands."""

import subprocess
import sys

import click

from ...utils.protocol_registry import registry
from ...utils.server_manager import server_manager


@click.group(name="status")
def status_group():
    """Check system status and health."""
    pass


@status_group.command("system")
@click.pass_context
def system_status(ctx):
    """Show overall system status."""
    verbose = ctx.obj.get("verbose", False)

    click.echo("🔍 Agenspy System Status")
    click.echo("=" * 40)

    # Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    click.echo(f"🐍 Python: {python_version}")

    # DSPy status
    try:
        import dspy  # noqa: F401

        click.echo("✅ DSPy: Available")
    except ImportError:
        click.echo("❌ DSPy: Not available")

    # Protocol registry
    protocols = registry.get_available_protocols()
    click.echo(f"📡 Protocols: {len(protocols)} registered")

    # Running servers
    servers = server_manager.list_servers()
    click.echo(f"🖥️ Servers: {len(servers)} running")

    # Node.js (for MCP servers)
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            click.echo(f"✅ Node.js: {result.stdout.strip()}")
        else:
            click.echo("❌ Node.js: Not available")
    except FileNotFoundError:
        click.echo("❌ Node.js: Not found")


@status_group.command("protocols")
def protocol_status():
    """Show protocol status."""
    click.echo("📡 Protocol Status:")
    click.echo()

    protocols = registry.get_available_protocols()

    for protocol in protocols:
        click.echo(f"📡 {protocol.value.upper()}")
        click.echo("   Status: ✅ Registered")
        click.echo()


@status_group.command("servers")
def server_status():
    """Show server status."""
    click.echo("🖥️ Server Status:")
    click.echo()

    servers = server_manager.list_servers()

    if not servers:
        click.echo("⚪ No servers running")
        return

    for server_id in servers:
        status = server_manager.get_server_status(server_id)
        status_icon = "🟢" if status == "running" else "🔴"
        click.echo(f"{status_icon} {server_id}: {status}")
