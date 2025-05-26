"""Server management commands."""

import threading
import time

import click

from ...servers.mcp_python_server import GitHubMCPServer
from ...utils.server_manager import server_manager


@click.group(name="server")
def server_group():
    """Manage protocol servers."""
    pass


@server_group.command("list")
@click.option("--running", is_flag=True, help="Show only running servers")
def list_servers(running):
    """List available servers."""
    click.echo("🖥️ Available Servers:")
    click.echo()

    servers = [
        {
            "name": "github-mcp",
            "type": "mcp",
            "description": "GitHub MCP server with repository tools",
            "port": 8080,
            "status": "available",
        },
        {
            "name": "python-mcp",
            "type": "mcp",
            "description": "Python-based MCP server",
            "port": 8081,
            "status": "available",
        },
    ]

    # Add running servers from server manager
    running_servers = server_manager.list_servers()

    for server in servers:
        if running and server["status"] != "running":
            continue

        status = "🟢 Running" if server["name"] in running_servers else "⚪ Available"

        click.echo(f"🖥️ {server['name']}")
        click.echo(f"   Type: {server['type'].upper()}")
        click.echo(f"   Description: {server['description']}")
        click.echo(f"   Port: {server['port']}")
        click.echo(f"   Status: {status}")
        click.echo()


@server_group.command("run")
@click.option("--mcp", "server_type", flag_value="mcp", help="Run MCP server")
@click.argument("server_name")
@click.option("--port", "-p", default=8080, help="Server port")
@click.option("--github-token", envvar="GITHUB_TOKEN", help="GitHub token for GitHub MCP server")
@click.option("--background", "-b", is_flag=True, help="Run server in background")
@click.pass_context
def run_server(ctx, server_type, server_name, port, github_token, background):
    """Run a protocol server."""
    verbose = ctx.obj.get("verbose", False)

    if verbose:
        click.echo(f"🚀 Starting {server_type} server: {server_name}")
        click.echo(f"📡 Port: {port}")

    try:
        if server_type == "mcp":
            if server_name == "github-mcp":
                # Start GitHub MCP server
                if background:

                    def start_github_server():
                        server = GitHubMCPServer(github_token, port)
                        server.start()

                    thread = threading.Thread(target=start_github_server, daemon=True)
                    thread.start()
                    click.echo(f"✅ GitHub MCP server started in background on port {port}")
                    click.echo("Press Ctrl+C to stop")

                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        click.echo("\n🛑 Stopping server...")
                else:
                    server = GitHubMCPServer(github_token, port)
                    click.echo(f"🚀 Starting GitHub MCP server on port {port}...")
                    server.start()

            elif server_name == "python-mcp":
                # Start Python MCP server
                if background:

                    def start_python_server():
                        from ...servers.mcp_python_server import PythonMCPServer

                        server = PythonMCPServer("python-mcp-server", port)
                        server.start()

                    thread = threading.Thread(target=start_python_server, daemon=True)
                    thread.start()
                    click.echo(f"✅ Python MCP server started in background on port {port}")
                else:
                    from ...servers.mcp_python_server import PythonMCPServer

                    server = PythonMCPServer("python-mcp-server", port)
                    click.echo(f"🚀 Starting Python MCP server on port {port}...")
                    server.start()
            else:
                click.echo(f"❌ Unknown MCP server: {server_name}")
        else:
            click.echo(f"❌ Unknown server type: {server_type}")

    except Exception as e:
        click.echo(f"❌ Failed to start server: {e}")
        if verbose:
            import traceback

            traceback.print_exc()


@server_group.command("stop")
@click.argument("server_name")
@click.pass_context
def stop_server(ctx, server_name):
    """Stop a running server."""
    verbose = ctx.obj.get("verbose", False)

    if verbose:
        click.echo(f"🛑 Stopping server: {server_name}")

    if server_manager.stop_server(server_name):
        click.echo(f"✅ Server {server_name} stopped successfully")
    else:
        click.echo(f"❌ Failed to stop server {server_name}")


@server_group.command("status")
@click.argument("server_name")
def server_status(server_name):
    """Get server status."""
    status = server_manager.get_server_status(server_name)

    if status == "running":
        click.echo(f"🟢 {server_name}: Running")
    elif status == "stopped":
        click.echo(f"🔴 {server_name}: Stopped")
    else:
        click.echo(f"⚪ {server_name}: Not found")


@server_group.command("logs")
@click.argument("server_name")
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
def server_logs(server_name, follow):
    """View server logs."""
    click.echo(f"📋 Logs for {server_name}:")
    click.echo("(Log viewing not implemented yet)")
