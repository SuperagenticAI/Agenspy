#!/usr/bin/env python3
"""Main CLI entry point for agenspy."""

import os
import sys

import click

# Add package to path for development
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .commands.agent import agent_group
from .commands.config import config_group
from .commands.protocols import protocol_group
from .commands.server import server_group


@click.group()
@click.version_option(version="0.0.1", prog_name="agenspy")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--config", "-c", help="Path to configuration file")
@click.pass_context
def cli(ctx, verbose, config):
    """Agenspy CLI - Protocol-first AI agent framework."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config"] = config

    if verbose:
        click.echo("🚀 Agenspy CLI v0.0.1")


# Add command groups
cli.add_command(agent_group)
cli.add_command(protocol_group)
cli.add_command(server_group)
cli.add_command(config_group)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
