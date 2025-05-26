"""Demo and example commands."""

import os
import subprocess

import click


@click.group(name="demo")
def demo_group():
    """Run demos and examples."""
    pass


@demo_group.command("github-pr")
@click.option("--real-mcp", is_flag=True, help="Use real MCP server")
@click.option("--github-token", envvar="GITHUB_TOKEN", help="GitHub token")
def demo_github_pr(real_mcp, github_token):
    """Run GitHub PR review demo."""
    click.echo("🚀 Running GitHub PR Review Demo")

    # This would run the github_pr_review.py example
    demo_script = os.path.join(os.path.dirname(__file__), "..", "..", "..", "examples", "github_pr_review.py")

    env = os.environ.copy()
    if github_token:
        env["GITHUB_TOKEN"] = github_token

    try:
        subprocess.run(["python", demo_script], env=env, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Demo failed: {e}")


@demo_group.command("comprehensive")
def demo_comprehensive():
    """Run comprehensive MCP demo."""
    click.echo("🚀 Running Comprehensive MCP Demo")

    demo_script = os.path.join(os.path.dirname(__file__), "..", "..", "..", "examples", "comprehensive_mcp_demo.py")

    try:
        subprocess.run(["python", demo_script], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Demo failed: {e}")


@demo_group.command("list")
def list_demos():
    """List available demos."""
    click.echo("📋 Available Demos:")
    click.echo()
    click.echo("🔍 github-pr     - GitHub PR review using MCP")
    click.echo("🔬 comprehensive - Full MCP client/server demo")
    click.echo("🐍 python-server - Python MCP server demo")
