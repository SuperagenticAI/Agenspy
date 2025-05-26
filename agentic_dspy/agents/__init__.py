"""Agent implementations for Agentic-DSPy."""

from .base_agent import BaseAgent
from .github_agent import GitHubPRReviewAgent
from .multi_protocol_agent import MultiProtocolAgent

__all__ = [
    "BaseAgent",
    "GitHubPRReviewAgent",
    "MultiProtocolAgent",
]
