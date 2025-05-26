"""Agentic-DSPy: Protocol-first AI agent framework built on DSPy."""

from .agents.base_agent import BaseAgent
from .agents.github_agent import GitHubPRReviewAgent
from .agents.multi_protocol_agent import MultiProtocolAgent
from .protocols.agent2agent.client import Agent2AgentClient
from .protocols.base import BaseProtocol, ProtocolType
from .protocols.mcp.client import MCPClient, RealMCPClient
from .servers.mcp_python_server import GitHubMCPServer, PythonMCPServer
from .utils.protocol_registry import ProtocolRegistry, registry
from .utils.server_manager import ServerManager, server_manager

__version__ = "0.1.0"
__author__ = "Agentic-DSPy Contributors"
__description__ = "Protocol-first AI agent framework built on DSPy"

__all__ = [
    # Core protocols
    "BaseProtocol",
    "ProtocolType",
    "MCPClient",
    "RealMCPClient",
    "Agent2AgentClient",
    # Agents
    "BaseAgent",
    "GitHubPRReviewAgent",
    "MultiProtocolAgent",
    # Servers
    "PythonMCPServer",
    "GitHubMCPServer",
    # Utils
    "registry",
    "ProtocolRegistry",
    "server_manager",
    "ServerManager",
]


def create_mcp_agent(server_url: str, **kwargs):
    """Convenience function to create MCP agent."""
    return GitHubPRReviewAgent(server_url, **kwargs)


def create_multi_protocol_agent(agent_id: str = "multi-agent"):
    """Convenience function to create multi-protocol agent."""
    return MultiProtocolAgent(agent_id)
