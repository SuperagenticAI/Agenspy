"""Protocol management commands."""

import click

from ...utils.protocol_registry import registry


@click.group(name="protocol")
def protocol_group():
    """Manage communication protocols."""
    pass


@protocol_group.command("list")
@click.option("--mcp", is_flag=True, help="Show only MCP protocols")
@click.option("--a2a", is_flag=True, help="Show only Agent2Agent protocols")
@click.option("--all", "show_all", is_flag=True, help="Show all protocols")
@click.pass_context
def list_protocols(ctx, mcp, a2a, show_all):
    """List available protocols."""
    verbose = ctx.obj.get("verbose", False)

    click.echo("📡 Available Protocols:")
    click.echo()

    protocols = [
        {
            "name": "MCP",
            "type": "mcp",
            "description": "Model Context Protocol for AI model context sharing by Anthropic",
            "features": ["Tool discovery", "Context sharing", "Session management"],
            "status": "Active",
        },
        {
            "name": "Agent2Agent",
            "type": "a2a",
            "description": "Agent2Agent Protocol for AI agent communication by Google",
            "features": ["Agent communication", "Message routing"],
            "status": "Beta",
        },
    ]

    for protocol in protocols:
        # Filter based on flags
        if mcp and protocol["type"] != "mcp":
            continue
        if a2a and protocol["type"] != "a2a":
            continue
        if not show_all and not mcp and not a2a:
            # Show all by default
            pass

        click.echo(f"📡 {protocol['name']} ({protocol['type'].upper()})")
        click.echo(f"   Description: {protocol['description']}")
        click.echo(f"   Features: {', '.join(protocol['features'])}")
        click.echo(f"   Status: {protocol['status']}")

        if verbose:
            click.echo(f"   Registry: {protocol['name'] in [p.value for p in registry.get_available_protocols()]}")

        click.echo()


@protocol_group.command("test")
@click.argument("protocol_type")
@click.option("--server", "-s", help="Server URL or address")
@click.pass_context
def test_protocol(ctx, protocol_type, server):
    """Test protocol connection."""
    verbose = ctx.obj.get("verbose", False)

    click.echo(f"🧪 Testing {protocol_type.upper()} protocol...")

    try:
        if protocol_type.lower() == "mcp":
            from ...protocols.mcp.client import MCPClient

            client = MCPClient(server or "mcp://test-server:8080")

            if client.connect():
                click.echo("✅ MCP connection successful!")
                capabilities = client.get_capabilities()
                click.echo(f"📋 Tools available: {len(capabilities.get('tools', []))}")
                client.disconnect()
            else:
                click.echo("❌ MCP connection failed")

        elif protocol_type.lower() == "a2a":
            from ...protocols.agent2agent.client import Agent2AgentClient

            client = Agent2AgentClient(server or "tcp://localhost:9090", "test-agent")

            if client.connect():
                click.echo("✅ Agent2Agent connection successful!")
                peers = client.discover_peers()
                click.echo(f"👥 Peers discovered: {len(peers)}")
                client.disconnect()
            else:
                click.echo("❌ Agent2Agent connection failed")
        else:
            click.echo(f"❌ Unknown protocol: {protocol_type}")

    except Exception as e:
        click.echo(f"❌ Protocol test failed: {e}")
        if verbose:
            import traceback

            traceback.print_exc()


@protocol_group.command("info")
@click.argument("protocol_name")
def protocol_info(protocol_name):
    """Get detailed information about a protocol."""
    click.echo(f"📡 Protocol Information: {protocol_name.upper()}")
    click.echo()

    if protocol_name.lower() == "mcp":
        click.echo("Model Context Protocol (MCP)")
        click.echo("Description: Standardized protocol for AI model context sharing")
        click.echo("Version: 1.0")
        click.echo("Features:")
        click.echo("  - Tool discovery and execution")
        click.echo("  - Context sharing between models")
        click.echo("  - Session management")
        click.echo("  - Error handling")
        click.echo()
        click.echo("Usage:")
        click.echo("  adspy agent run --agent github-pr-review 'Analyze PR <url>'")

    elif protocol_name.lower() == "a2a":
        click.echo("Agent2Agent Protocol")
        click.echo("Description: Direct communication between AI agents")
        click.echo("Version: 0.9 (Beta)")
        click.echo("Features:")
        click.echo("  - Peer discovery")
        click.echo("  - Message routing")
        click.echo("  - Broadcast capabilities")
        click.echo()
        click.echo("Usage:")
        click.echo("  adspy protocol test a2a --server tcp://localhost:9090")
    else:
        click.echo(f"❌ Unknown protocol: {protocol_name}")
