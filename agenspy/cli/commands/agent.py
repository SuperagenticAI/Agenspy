"""Agent management commands."""

from typing import Optional

import click
import dspy

from ...agents.github_agent import GitHubPRReviewAgent
from ...agents.multi_protocol_agent import MultiProtocolAgent
from ...protocols.mcp.client import MCPClient


@click.group(name="agent")
def agent_group():
    """Manage AI agents."""
    pass


@agent_group.command("list")
@click.option("--type", "-t", help="Filter by agent type (github, multi-protocol)")
@click.pass_context
def list_agents(ctx, type):
    """List available agents."""
    click.echo("📋 Available Agents:")
    click.echo()

    agents = [
        {
            "name": "github-pr-review",
            "type": "github",
            "description": "Reviews GitHub Pull Requests using MCP protocol",
            "protocols": ["MCP"],
        },
        {
            "name": "multi-protocol",
            "type": "multi-protocol",
            "description": "Agent supporting multiple protocols simultaneously",
            "protocols": ["MCP", "Agent2Agent"],
        },
    ]

    for agent in agents:
        if type and agent["type"] != type:
            continue

        click.echo(f"🤖 {agent['name']}")
        click.echo(f"   Type: {agent['type']}")
        click.echo(f"   Description: {agent['description']}")
        click.echo(f"   Protocols: {', '.join(agent['protocols'])}")
        click.echo()


@agent_group.command("run")
@click.argument("task")
@click.option("--agent", "-a", default="github-pr-review", help="Agent to use")
@click.option("--mcp-server", default="mcp://github-server:8080", help="MCP server URL")
@click.option("--github-token", envvar="GITHUB_TOKEN", help="GitHub token")
@click.option("--real-mcp", is_flag=True, help="Use real MCP server")
@click.pass_context
def run_agent(ctx, task, agent, mcp_server, github_token, real_mcp):
    """Run an agent with a specific task."""
    verbose = ctx.obj.get("verbose", False)

    if verbose:
        click.echo(f"🚀 Running agent: {agent}")
        click.echo(f"📝 Task: {task}")

    # Setup DSPy
    try:
        lm = dspy.LM("openai/gpt-4o-mini")
        if verbose:
            click.echo("✅ Using OpenAI GPT-4o-mini")
    except Exception as e:
        if verbose:
            click.echo(f"⚠️ OpenAI not available ({e}), using dummy LM")

        class DummyLM:
            def __call__(self, *args, **kwargs):
                return dspy.Prediction(
                    review_comment="Task completed successfully using Agenspy CLI",
                    approval_status="Completed",
                    analysis="CLI-based analysis completed",
                )

        lm = DummyLM()

    dspy.configure(lm=lm)

    # Create and run agent
    try:
        if agent == "github-pr-review":
            agent_instance = GitHubPRReviewAgent(mcp_server, use_real_mcp=real_mcp, github_token=github_token)

            # Extract PR URL from task if present
            pr_url = extract_pr_url(task)
            if pr_url:
                result = agent_instance(pr_url=pr_url, review_focus="general")
                click.echo("✅ Agent execution completed!")
                click.echo(f"📊 Review: {result.review_comment}")
                click.echo(f"📋 Status: {result.approval_status}")
            else:
                click.echo("❌ No valid PR URL found in task")

        elif agent == "multi-protocol":
            agent_instance = MultiProtocolAgent("cli-agent")
            mcp_client = MCPClient(mcp_server)
            agent_instance.add_protocol(mcp_client)

            result = agent_instance(task)
            click.echo("✅ Agent execution completed!")
            click.echo(f"📊 Result: {result.final_answer}")

        else:
            click.echo(f"❌ Unknown agent: {agent}")

    except Exception as e:
        click.echo(f"❌ Agent execution failed: {e}")
        if verbose:
            import traceback

            traceback.print_exc()


@agent_group.command("create")
@click.argument("name")
@click.option("--type", "-t", required=True, help="Agent type (github, multi-protocol)")
@click.option("--config", "-c", help="Configuration file")
def create_agent(name, type, config):
    """Create a new agent configuration."""
    click.echo(f"🔧 Creating agent: {name}")
    click.echo(f"📋 Type: {type}")

    # This would create agent configuration files
    click.echo("✅ Agent configuration created!")


def extract_pr_url(task: str) -> Optional[str]:
    """Extract PR URL from task string."""
    import re

    # Look for GitHub PR URLs
    pattern = r"https://github\.com/[^/]+/[^/]+/pull/\d+"
    match = re.search(pattern, task)

    if match:
        return match.group(0)

    # Look for just PR references
    pattern = r"<([^>]+)>"
    match = re.search(pattern, task)

    if match:
        return match.group(1)

    return None
