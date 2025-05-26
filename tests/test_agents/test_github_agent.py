"""Tests for GitHub agent implementation."""

import dspy
import pytest

from agenspy.agents.github_agent import GitHubPRReviewAgent


class TestGitHubPRReviewAgent:
    """Test cases for GitHub PR review agent."""

    def setup_method(self):
        """Setup test environment."""

        # Configure dummy LM for testing
        class DummyLM:
            def __call__(self, *args, **kwargs):
                return dspy.Prediction(
                    analysis="Test analysis",
                    suggestions=["Test suggestion 1", "Test suggestion 2"],
                    review_comment="Test review comment",
                    approval_status="Approved",
                )

        dspy.configure(lm=DummyLM())

    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = GitHubPRReviewAgent("mcp://test-server:8080")
        assert agent.mcp_client is not None
        assert hasattr(agent, "analyze_pr")
        assert hasattr(agent, "generate_review")

    def test_agent_initialization_with_real_mcp(self):
        """Test agent initialization with real MCP."""
        agent = GitHubPRReviewAgent("mcp://test-server:8080", use_real_mcp=True, github_token="test_token")
        assert agent.mcp_client is not None

    def test_pr_review_process(self):
        """Test PR review process."""
        agent = GitHubPRReviewAgent("mcp://test-server:8080")

        result = agent(pr_url="https://github.com/test/repo/pull/123", review_focus="security")

        assert hasattr(result, "review_comment")
        assert hasattr(result, "approval_status")
        assert hasattr(result, "protocol_capabilities")
        assert hasattr(result, "mcp_tools_used")
        assert result.mcp_tools_used == ["github_search", "file_reader"]

    def test_agent_cleanup(self):
        """Test agent cleanup."""
        agent = GitHubPRReviewAgent("mcp://test-server:8080")
        agent.mcp_client.connect()
        assert agent.mcp_client._connected

        agent.cleanup()
        assert not agent.mcp_client._connected


class TestMultiProtocolAgent:
    """Test cases for multi-protocol agent."""

    def setup_method(self):
        """Setup test environment."""

        class DummyLM:
            def __call__(self, *args, **kwargs):
                return dspy.Prediction(
                    best_protocol="mcp",
                    reasoning="MCP is best for this task",
                    final_answer="Task completed",
                    confidence=0.9,
                )

        dspy.configure(lm=DummyLM())

    def test_multi_protocol_agent_initialization(self):
        """Test multi-protocol agent initialization."""
        from agenspy.agents.multi_protocol_agent import MultiProtocolAgent

        agent = MultiProtocolAgent("test-agent")
        assert agent.agent_id == "test-agent"
        assert len(agent.protocols) == 0

    def test_add_protocol(self):
        """Test adding protocols to agent."""
        from agenspy.agents.multi_protocol_agent import MultiProtocolAgent
        from agenspy.protocols.mcp.client import MCPClient

        agent = MultiProtocolAgent("test-agent")
        mcp_client = MCPClient("mcp://test-server:8080")

        agent.add_protocol(mcp_client)
        assert len(agent.protocols) == 1

    def test_protocol_routing(self):
        """Test protocol routing."""
        from agenspy.agents.multi_protocol_agent import MultiProtocolAgent
        from agenspy.protocols.mcp.client import MCPClient

        agent = MultiProtocolAgent("test-agent")
        mcp_client = MCPClient("mcp://test-server:8080")
        agent.add_protocol(mcp_client)

        result = agent("Test request")
        assert hasattr(result, "final_answer")
        assert hasattr(result, "protocol_used")


if __name__ == "__main__":
    pytest.main([__file__])
