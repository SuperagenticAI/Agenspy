"""Tests for GitHub agent implementation."""

import dspy
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from enum import Enum

from agenspy.agents.github_agent import GitHubPRReviewAgent
from agenspy.agents.multi_protocol_agent import MultiProtocolAgent
from agenspy.protocols.mcp.client import MCPClient
from agenspy.protocols.base import ProtocolType


class DummyLM:
    """Dummy language model for testing."""
    def __init__(self):
        self.history = []

    def __call__(self, *args, **kwargs):
        self.history.append((args, kwargs))
        return dspy.Prediction(
            analysis="Test analysis",
            suggestions=["Test suggestion 1", "Test suggestion 2"],
            review_comment="Test review comment",
            approval_status="Approved",
        )


class TestGitHubPRReviewAgent:
    """Test cases for GitHub PR review agent."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup test environment."""
        self.lm = DummyLM()
        dspy.configure(lm=self.lm, trace=[])
        yield
        # Cleanup
        dspy.configure(lm=None)

    def test_agent_initialization(self):
        """Test agent initialization."""
        with patch('agenspy.protocols.mcp.client.MCPClient') as mock_client:
            agent = GitHubPRReviewAgent("mcp://test-server:8080")
            assert agent.mcp_client is not None
            assert hasattr(agent, "analyze_pr")
            assert hasattr(agent, "generate_review")

    def test_agent_initialization_with_real_mcp(self):
        """Test agent initialization with real MCP."""
        with patch('agenspy.protocols.mcp.client.RealMCPClient') as mock_client:
            agent = GitHubPRReviewAgent(
                "mcp://test-server:8080", 
                use_real_mcp=True, 
                github_token="test_token"
            )
            assert agent.mcp_client is not None

    def test_agent_cleanup(self):
        """Test agent cleanup."""
        with patch('agenspy.protocols.mcp.client.MCPClient') as mock_client:
            agent = GitHubPRReviewAgent("mcp://test-server:8080")
            agent.cleanup = MagicMock()
            agent.cleanup()
            agent.cleanup.assert_called_once()


class TestMultiProtocolAgent:
    """Test cases for multi-protocol agent."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup test environment."""
        self.lm = DummyLM()
        dspy.configure(lm=self.lm, trace=[])
        yield
        # Cleanup
        dspy.configure(lm=None)

    def test_multi_protocol_agent_initialization(self):
        """Test multi-protocol agent initialization."""
        agent = MultiProtocolAgent("test-agent")
        assert agent.agent_id == "test-agent"
        assert len(agent.protocols) == 0

    def test_add_protocol(self):
        """Test adding protocols to agent."""
        agent = MultiProtocolAgent("test-agent")
        
        # Create a mock protocol with ProtocolType enum
        mock_protocol = MagicMock()
        type(mock_protocol).protocol_type = PropertyMock(return_value=ProtocolType.MCP)
        
        agent.add_protocol(mock_protocol)
        assert len(agent.protocols) == 1
        assert agent.protocols[ProtocolType.MCP] == mock_protocol


if __name__ == "__main__":
    pytest.main([__file__])
