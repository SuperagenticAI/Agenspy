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
🚀 Agentic-DSPy Quickstart Guide
================================

1. Initialize configuration:
   adspy config init

2. List available agents:
   adspy agent list

3. Run a GitHub PR review:
   adspy agent run "Analyze PR https://github.com/org/repo/pull/123"

4. Start an MCP server:
   adspy server run --mcp github-mcp --port 8080

5. Test protocol connection:
   adspy protocol test mcp --server mcp://localhost:8080

6. Create a workflow:
   adspy workflow create my-workflow --template github-review

7. Run a workflow:
   adspy workflow run my-workflow --input '{"pr_url": "..."}'

For more help: adspy help commands
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
   adspy agent list                    - List available agents
   adspy agent run <task>              - Run an agent with a task
   adspy agent create <name>           - Create agent configuration

📡 Protocol Management:
   adspy protocol list [--mcp|--a2a]  - List protocols
   adspy protocol test <type>          - Test protocol connection
   adspy protocol info <name>          - Get protocol information

🖥️ Server Management:
   adspy server list [--running]      - List available servers
   adspy server run --mcp <name>      - Start an MCP server
   adspy server stop <name>            - Stop a running server
   adspy server status <name>          - Check server status
   adspy server logs <name>            - View server logs

🔄 Workflow Management:
   adspy workflow list                 - List all workflows
   adspy workflow create <name>        - Create new workflow
   adspy workflow run <name>           - Execute a workflow
   adspy workflow validate <name>      - Validate workflow config
   adspy workflow delete <name>        - Delete a workflow

⚙️ Configuration:
   adspy config init                   - Initialize configuration
   adspy config show                   - Show current config
   adspy config set <key> <value>      - Set config value
   adspy config get <key>              - Get config value

🎯 Demos & Examples:
   adspy demo list                     - List available demos
   adspy demo github-pr                - Run GitHub PR demo
   adspy demo comprehensive            - Run full MCP demo

📊 System Status:
   adspy status system                 - Show system status
   adspy status protocols              - Show protocol status
   adspy status servers                - Show server status

❓ Help & Documentation:
   adspy help quickstart               - Show quickstart guide
   adspy help commands                 - Show all commands
   adspy help examples                 - Show usage examples
   adspy help troubleshooting          - Common issues & solutions
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
   adspy agent run "Analyze this PR https://github.com/org/repo/pull/123"

   # Use specific agent type
   adspy agent run --agent multi-protocol "Analyze repository security"

🖥️ Server Management:
   # Start GitHub MCP server
   adspy server run --mcp github-mcp --port 8080 --background

   # Check server status
   adspy server status github-mcp

📡 Protocol Testing:
   # Test MCP connection
   adspy protocol test mcp --server mcp://localhost:8080

   # Test Agent2Agent protocol
   adspy protocol test a2a --server tcp://localhost:9090

🔄 Workflow Examples:
   # Create GitHub review workflow
   adspy workflow create pr-review --template github-review

   # Run workflow with parameters
   adspy workflow run pr-review --input '{"pr_url": "https://github.com/org/repo/pull/123"}'

⚙️ Configuration:
   # Set GitHub token
   adspy config set github_token "ghp_xxxxxxxxxxxx"

   # Configure default MCP server
   adspy config set default_mcp_server "mcp://localhost:8080"

🎯 Running Demos:
   # Quick GitHub PR demo
   adspy demo github-pr --real-mcp --github-token $GITHUB_TOKEN

   # Full comprehensive demo
   adspy demo comprehensive
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
   adspy config set default_lm "openai/gpt-4o-mini"
   export OPENAI_API_KEY="your-api-key"

2. MCP Server Connection Failed:
   - Check if Node.js is installed: node --version
   - Verify MCP server is running: adspy server status github-mcp
   - Test connection: adspy protocol test mcp --server mcp://localhost:8080

3. GitHub Token Issues:
   - Set token: adspy config set github_token "your-token"
   - Or use environment: export GITHUB_TOKEN="your-token"
   - Verify permissions: Token needs repo read access

4. Workflow Validation Errors:
   - Check YAML syntax: adspy workflow validate <name>
   - Ensure all referenced agents exist
   - Verify step dependencies are correct

5. Agent Execution Failures:
   - Run with verbose mode: adspy -v agent run "task"
   - Check system status: adspy status system
   - Verify protocol connections: adspy status protocols

🔍 Debugging Commands:
   adspy status system                 - Check overall health
   adspy -v <command>                  - Enable verbose output
   adspy protocol test <type>          - Test protocol connections
   adspy server logs <name>            - View server logs

📚 Getting Help:
   - Check documentation: adspy help commands
   - Run examples: adspy help examples
   - View system status: adspy status system

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
   adspy protocol list --mcp          - List MCP protocols
   adspy protocol test mcp            - Test MCP connection
   adspy server run --mcp github-mcp  - Start MCP server

   Example:
   adspy agent run --real-mcp "Analyze PR <url>"

🤝 Agent2Agent Protocol (A2A):
   Description: Direct communication between AI agents
   Status: Beta

   Commands:
   adspy protocol list --a2a          - List A2A protocols
   adspy protocol test a2a            - Test A2A connection

   Example:
   adspy agent run --agent multi-protocol "Coordinate with other agents"

🔧 Adding Custom Protocols:
   1. Extend BaseProtocol class
   2. Implement required methods
   3. Register with protocol registry

   See documentation for detailed implementation guide.
"""
    )
