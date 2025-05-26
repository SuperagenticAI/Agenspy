"""Workflow management commands."""

import json
from pathlib import Path

import click
import yaml


@click.group(name="workflow")
def workflow_group():
    """Manage agent workflows."""
    pass


@workflow_group.command("create")
@click.argument("name")
@click.option("--template", "-t", help="Workflow template to use")
@click.option("--description", "-d", help="Workflow description")
def create_workflow(name, template, description):
    """Create a new workflow."""
    workflow_dir = Path.cwd() / "workflows"
    workflow_dir.mkdir(exist_ok=True)

    workflow_file = workflow_dir / f"{name}.yaml"

    if workflow_file.exists():
        click.echo(f"❌ Workflow '{name}' already exists")
        return

    if template == "github-review":
        workflow_config = {
            "name": name,
            "description": description or "GitHub PR review workflow",
            "version": "1.0",
            "agents": [
                {
                    "name": "pr-reviewer",
                    "type": "github-pr-review",
                    "config": {"mcp_server": "mcp://github-server:8080", "review_focus": "security"},
                }
            ],
            "steps": [{"name": "review-pr", "agent": "pr-reviewer", "input": "${pr_url}", "output": "review_result"}],
            "outputs": ["review_result"],
        }
    elif template == "multi-protocol":
        workflow_config = {
            "name": name,
            "description": description or "Multi-protocol analysis workflow",
            "version": "1.0",
            "agents": [{"name": "analyzer", "type": "multi-protocol", "config": {"protocols": ["mcp", "agent2agent"]}}],
            "steps": [
                {"name": "analyze", "agent": "analyzer", "input": "${analysis_request}", "output": "analysis_result"}
            ],
            "outputs": ["analysis_result"],
        }
    else:
        workflow_config = {
            "name": name,
            "description": description or "Custom workflow",
            "version": "1.0",
            "agents": [],
            "steps": [],
            "outputs": [],
        }

    with open(workflow_file, "w") as f:
        yaml.dump(workflow_config, f, default_flow_style=False, indent=2)

    click.echo(f"✅ Workflow created: {workflow_file}")
    click.echo(f"📝 Template: {template or 'custom'}")


@workflow_group.command("run")
@click.argument("workflow_name")
@click.option("--input", "-i", help="Input parameters as JSON")
@click.option("--dry-run", is_flag=True, help="Show what would be executed without running")
@click.pass_context
def run_workflow(ctx, workflow_name, input, dry_run):
    """Run a workflow."""
    workflow_file = Path.cwd() / "workflows" / f"{workflow_name}.yaml"

    if not workflow_file.exists():
        click.echo(f"❌ Workflow '{workflow_name}' not found")
        return

    try:
        with open(workflow_file, "r") as f:
            workflow = yaml.safe_load(f)

        # Parse input parameters
        params = {}
        if input:
            try:
                params = json.loads(input)
            except json.JSONDecodeError:
                click.echo("❌ Invalid JSON input")
                return

        if dry_run:
            click.echo(f"🔍 Dry run for workflow: {workflow['name']}")
            click.echo(f"📝 Description: {workflow.get('description', 'No description')}")
            click.echo(f"🤖 Agents: {len(workflow.get('agents', []))}")
            click.echo(f"📋 Steps: {len(workflow.get('steps', []))}")
            click.echo(f"📊 Parameters: {params}")
            return

        click.echo(f"🚀 Running workflow: {workflow['name']}")

        # Execute workflow steps
        results = {}
        for step in workflow.get("steps", []):
            step_name = step["name"]
            agent_name = step["agent"]

            click.echo(f"⚡ Executing step: {step_name}")

            # Find agent configuration
            agent_config = None
            for agent in workflow.get("agents", []):
                if agent["name"] == agent_name:
                    agent_config = agent
                    break

            if not agent_config:
                click.echo(f"❌ Agent '{agent_name}' not found in workflow")
                continue

            # Simulate step execution
            results[step["output"]] = f"Result from {step_name}"
            click.echo(f"✅ Step '{step_name}' completed")

        click.echo("🎉 Workflow completed successfully!")

    except Exception as e:
        click.echo(f"❌ Workflow execution failed: {e}")


@workflow_group.command("list")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information")
def list_workflows(verbose):
    """List all workflows."""
    workflow_dir = Path.cwd() / "workflows"

    if not workflow_dir.exists():
        click.echo("📁 No workflows directory found")
        return

    workflow_files = list(workflow_dir.glob("*.yaml"))

    if not workflow_files:
        click.echo("📋 No workflows found")
        return

    click.echo("📋 Available Workflows:")
    click.echo()

    for workflow_file in workflow_files:
        try:
            with open(workflow_file, "r") as f:
                workflow = yaml.safe_load(f)

            name = workflow.get("name", workflow_file.stem)
            description = workflow.get("description", "No description")

            click.echo(f"🔄 {name}")
            click.echo(f"   Description: {description}")

            if verbose:
                agents = workflow.get("agents", [])
                steps = workflow.get("steps", [])
                click.echo(f"   Agents: {len(agents)}")
                click.echo(f"   Steps: {len(steps)}")
                click.echo(f"   File: {workflow_file}")

            click.echo()

        except Exception as e:
            click.echo(f"❌ Error reading {workflow_file}: {e}")


@workflow_group.command("validate")
@click.argument("workflow_name")
def validate_workflow(workflow_name):
    """Validate a workflow configuration."""
    workflow_file = Path.cwd() / "workflows" / f"{workflow_name}.yaml"

    if not workflow_file.exists():
        click.echo(f"❌ Workflow '{workflow_name}' not found")
        return

    try:
        with open(workflow_file, "r") as f:
            workflow = yaml.safe_load(f)

        errors = []
        warnings = []

        # Required fields
        if "name" not in workflow:
            errors.append("Missing required field: 'name'")

        if "agents" not in workflow:
            errors.append("Missing required field: 'agents'")

        if "steps" not in workflow:
            errors.append("Missing required field: 'steps'")

        # Validate agents
        agent_names = set()
        for agent in workflow.get("agents", []):
            if "name" not in agent:
                errors.append("Agent missing 'name' field")
            else:
                if agent["name"] in agent_names:
                    errors.append(f"Duplicate agent name: {agent['name']}")
                agent_names.add(agent["name"])

            if "type" not in agent:
                errors.append(f"Agent '{agent.get('name', 'unknown')}' missing 'type' field")

        # Validate steps
        for i, step in enumerate(workflow.get("steps", [])):
            if "name" not in step:
                errors.append(f"Step {i} missing 'name' field")

            if "agent" not in step:
                errors.append(f"Step {i} missing 'agent' field")
            elif step["agent"] not in agent_names:
                errors.append(f"Step {i} references unknown agent: {step['agent']}")

        # Report results
        if errors:
            click.echo("❌ Validation failed:")
            for error in errors:
                click.echo(f"   • {error}")
        else:
            click.echo("✅ Workflow validation passed")

        if warnings:
            click.echo("⚠️ Warnings:")
            for warning in warnings:
                click.echo(f"   • {warning}")
    except yaml.YAMLError as e:
        click.echo(f"❌ Invalid YAML: {e}")
    except Exception as e:
        click.echo(f"❌ Validation error: {e}")


@workflow_group.command("delete")
@click.argument("workflow_name")
@click.option("--force", is_flag=True, help="Delete without confirmation")
def delete_workflow(workflow_name, force):
    """Delete a workflow."""
    workflow_file = Path.cwd() / "workflows" / f"{workflow_name}.yaml"

    if not workflow_file.exists():
        click.echo(f"❌ Workflow '{workflow_name}' not found")
        return

    if not force:
        if not click.confirm(f"Delete workflow '{workflow_name}'?"):
            click.echo("❌ Cancelled")
            return

    workflow_file.unlink()
    click.echo(f"✅ Workflow '{workflow_name}' deleted")
