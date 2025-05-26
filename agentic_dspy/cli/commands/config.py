"""Configuration management commands."""

import json
from pathlib import Path

import click


@click.group(name="config")
def config_group():
    """Manage configuration settings."""
    pass


@config_group.command("init")
@click.option("--force", is_flag=True, help="Overwrite existing configuration")
def init_config(force):
    """Initialize configuration file."""
    config_path = Path.home() / ".adspy" / "config.json"

    if config_path.exists() and not force:
        click.echo("❌ Configuration already exists. Use --force to overwrite.")
        return

    # Create config directory
    config_path.parent.mkdir(exist_ok=True)

    default_config = {
        "default_lm": "openai/gpt-4o-mini",
        "default_mcp_server": "mcp://localhost:8080",
        "github_token": "",
        "verbose": False,
        "agents": {"github-pr-review": {"mcp_server": "mcp://github-server:8080", "use_real_mcp": False}},
        "servers": {"github-mcp": {"port": 8080, "type": "mcp"}, "python-mcp": {"port": 8081, "type": "mcp"}},
    }

    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=2)

    click.echo(f"✅ Configuration initialized at {config_path}")


@config_group.command("show")
def show_config():
    """Show current configuration."""
    config_path = Path.home() / ".adspy" / "config.json"

    if not config_path.exists():
        click.echo("❌ No configuration found. Run 'adspy config init' first.")
        return

    with open(config_path, "r") as f:
        config = json.load(f)

    click.echo("📋 Current Configuration:")
    click.echo(json.dumps(config, indent=2))


@config_group.command("set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Set a configuration value."""
    config_path = Path.home() / ".adspy" / "config.json"

    if not config_path.exists():
        click.echo("❌ No configuration found. Run 'adspy config init' first.")
        return

    with open(config_path, "r") as f:
        config = json.load(f)

    # Handle nested keys like agents.github-pr-review.mcp_server
    keys = key.split(".")
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]

    # Convert value to appropriate type
    if value.lower() in ["true", "false"]:
        value = value.lower() == "true"
    elif value.isdigit():
        value = int(value)

    current[keys[-1]] = value

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    click.echo(f"✅ Set {key} = {value}")


@config_group.command("get")
@click.argument("key")
def get_config(key):
    """Get a configuration value."""
    config_path = Path.home() / ".adspy" / "config.json"

    if not config_path.exists():
        click.echo("❌ No configuration found. Run 'adspy config init' first.")
        return

    with open(config_path, "r") as f:
        config = json.load(f)

    keys = key.split(".")
    current = config
    try:
        for k in keys:
            current = current[k]
        click.echo(f"{key}: {current}")
    except KeyError:
        click.echo(f"❌ Key '{key}' not found")
