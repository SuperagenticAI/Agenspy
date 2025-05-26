"""Help and documentation commands."""

import click


@click.group(name="help")
def help_group():
    """Get help and documentation."""
    pass


@help_group.command("quickstart")
def quickstart():
    """Show quickstart guide."""
    click.echo(
        """
🚀 Agenspy Quickstart Guide
================================

1. Initialize configuration:
   agenspy config init

2. List available agents:
   agenspy agent list

3. Run a GitHub PR review:
   agenspy agent run "Analyze PR https://github.com/org/repo/pull/123"

4. Start an MCP server:
   agenspy server run --mcp github-mcp --port 8080

5. Test protocol connection:
   agenspy protocol test mcp --server mcp://localhost:8080

6. Create a workflow:
   agenspy workflow create my-workflow --template github-review

7. Run a workflow:
   agenspy workflow run my-workflow --input '{"pr_url": "..."}'

For more help: agenspy help commands
"""
    )


@help_group.command("commands")
def list_commands():
    """Show all available commands."""
    click.echo(
        """
📋 Available Commands
====================

🤖 Agent Management:
   agenspy agent list                    - List available agents
   agenspy agent run <task>              - Run an agent with a task
   agenspy agent create <name>           - Create agent configuration

📡 Protocol Management:
   agenspy protocol list [--mcp|--a2a]  - List protocols
   agenspy protocol test <type>          - Test protocol connection
   agenspy protocol info <name>          - Get protocol information

🖥️ Server Management:
   agenspy server list [--running]      - List available servers
   agenspy server run --mcp <name>      - Start an MCP server
   agenspy server stop <name>            - Stop a running server
   agenspy server status <name>          - Check server status
   agenspy server logs <name>            - View server logs

🔄 Workflow Management:
   agenspy workflow list                 - List all workflows
   agenspy workflow create <name>        - Create new workflow
   agenspy workflow run <name>           - Execute a workflow
   agenspy workflow validate <name>      - Validate workflow config
   agenspy workflow delete <name>        - Delete a workflow

⚙️ Configuration:
   agenspy config init                   - Initialize configuration
   agenspy config show                   - Show current config
   agenspy config set <key> <value>      - Set config value
   agenspy config get <key>              - Get config value

🎯 Demos & Examples:
   agenspy demo list                     - List available demos
   agenspy demo github-pr                - Run GitHub PR demo
   agenspy demo comprehensive            - Run full MCP demo

📊 System Status:
   agenspy status system                 - Show system status
   agenspy status protocols              - Show protocol status
   agenspy status servers                - Show server status

❓ Help & Documentation:
   agenspy help quickstart               - Show quickstart guide
   agenspy help commands                 - Show all commands
   agenspy help examples                 - Show usage examples
   agenspy help troubleshooting          - Common issues & solutions
"""
    )


@help_group.command("examples")
def show_examples():
    """Show usage examples."""
    click.echo(
        """
💡 Usage Examples
================

🔍 Basic Agent Usage:
   # Review a GitHub PR
   agenspy agent run "Analyze this PR https://github.com/org/repo/pull/123"

   # Use specific agent type
   agenspy agent run --agent multi-protocol "Analyze repository security"

🖥️ Server Management:
   # Start GitHub MCP server
   agenspy server run --mcp github-mcp --port 8080 --background

   # Check server status
   agenspy server status github-mcp

📡 Protocol Testing:
   # Test MCP connection
   agenspy protocol test mcp --server mcp://localhost:8080

   # Test Agent2Agent protocol
   agenspy protocol test a2a --server tcp://localhost:9090

🔄 Workflow Examples:
   # Create GitHub review workflow
   agenspy workflow create pr-review --template github-review

   # Run workflow with parameters
   agenspy workflow run pr-review --input '{"pr_url": "https://github.com/org/repo/pull/123"}'

⚙️ Configuration:
   # Set GitHub token
   agenspy config set github_token "ghp_xxxxxxxxxxxx"

   # Configure default MCP server
   agenspy config set default_mcp_server "mcp://localhost:8080"

🎯 Running Demos:
   # Quick GitHub PR demo
   agenspy demo github-pr --real-mcp --github-token $GITHUB_TOKEN

   # Full comprehensive demo
   agenspy demo comprehensive
"""
    )


@help_group.command("troubleshooting")
def troubleshooting():
    """Show troubleshooting guide."""
    click.echo(
        """
🔧 Troubleshooting Guide
=======================

❌ Common Issues:

1. "No LM is loaded" Error:
   Solution: Ensure you have configured DSPy with a language model
   agenspy config set default_lm "openai/gpt-4o-mini"
   export OPENAI_API_KEY="your-api-key"

2. MCP Server Connection Failed:
   - Check if Node.js is installed: node --version
   - Verify MCP server is running: agenspy server status github-mcp
   - Test connection: agenspy protocol test mcp --server mcp://localhost:8080

3. GitHub Token Issues:
   - Set token: agenspy config set github_token "your-token"
   - Or use environment: export GITHUB_TOKEN="your-token"
   - Verify permissions: Token needs repo read access

4. Workflow Validation Errors:
   - Check YAML syntax: agenspy workflow validate <name>
   - Ensure all referenced agents exist
   - Verify step dependencies are correct

5. Agent Execution Failures:
   - Run with verbose mode: agenspy -v agent run "task"
   - Check system status: agenspy status system
   - Verify protocol connections: agenspy status protocols

🔍 Debugging Commands:
   agenspy status system                 - Check overall health
   agenspy -v <command>                  - Enable verbose output
   agenspy protocol test <type>          - Test protocol connections
   agenspy server logs <name>            - View server logs

📚 Getting Help:
   - Check documentation: agenspy help commands
   - Run examples: agenspy help examples
   - View system status: agenspy status system

🌐 Environment Setup:
   Required:
   - Python 3.9+
   - DSPy package

   Optional:
   - Node.js (for real MCP servers)
   - OpenAI API key (for LLM features)
   - GitHub token (for GitHub integration)
"""
    )


@help_group.command("protocols")
def protocol_help():
    """Show protocol-specific help."""
    click.echo(
        """
📡 Protocol Guide
================

🔗 Model Context Protocol (MCP):
   Description: Standardized protocol for AI model context sharing
   Status: Active

   Commands:
   agenspy protocol list --mcp          - List MCP protocols
   agenspy protocol test mcp            - Test MCP connection
   agenspy server run --mcp github-mcp  - Start MCP server

   Example:
   agenspy agent run --real-mcp "Analyze PR <url>"

🤝 Agent2Agent Protocol (A2A):
   Description: Direct communication between AI agents
   Status: Beta

   Commands:
   agenspy protocol list --a2a          - List A2A protocols
   agenspy protocol test a2a            - Test A2A connection

   Example:
   agenspy agent run --agent multi-protocol "Coordinate with other agents"

🔧 Adding Custom Protocols:
   1. Extend BaseProtocol class
   2. Implement required methods
   3. Register with protocol registry

   See documentation for detailed implementation guide.
"""
    )
