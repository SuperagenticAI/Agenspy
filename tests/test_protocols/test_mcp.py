"""Tests for MCP protocol implementation."""

import pytest

from agentic_dspy.protocols.mcp.client import MCPClient, RealMCPClient
from agentic_dspy.protocols.mcp.session import MockMCPSession


class TestMCPClient:
    """Test cases for MCP client."""

    def test_mcp_client_initialization(self):
        """Test MCP client initialization."""
        client = MCPClient("mcp://test-server:8080")
        assert client.server_url == "mcp://test-server:8080"
        assert client.timeout == 30
        assert not client._connected

    def test_mcp_connection(self):
        """Test MCP connection."""
        client = MCPClient("mcp://test-server:8080")

        # Test connection
        assert client.connect()
        assert client._connected
        assert len(client.available_tools) > 0

    def test_mcp_capabilities(self):
        """Test MCP capabilities."""
        client = MCPClient("mcp://test-server:8080")
        client.connect()

        capabilities = client.get_capabilities()
        assert capabilities["protocol"] == "mcp"
        assert capabilities["version"] == "1.0"
        assert "tools" in capabilities
        assert capabilities["context_sharing"] is True
        assert capabilities["session_management"] is True

    def test_mcp_tool_discovery(self):
        """Test MCP tool discovery."""
        client = MCPClient("mcp://test-server:8080")
        client.connect()

        tools = client.available_tools
        assert "github_search" in tools
        assert "file_reader" in tools
        assert "code_analyzer" in tools

    def test_mcp_request_handling(self):
        """Test MCP request handling."""
        client = MCPClient("mcp://test-server:8080")
        client.connect()

        result = client(context_request="Test request", tool_name="github_search")

        assert hasattr(result, "context_data")
        assert hasattr(result, "tool_result")
        assert hasattr(result, "capabilities")

    def test_mcp_disconnect(self):
        """Test MCP disconnection."""
        client = MCPClient("mcp://test-server:8080")
        client.connect()
        assert client._connected

        client.disconnect()
        assert not client._connected


class TestRealMCPClient:
    """Test cases for real MCP client."""

    def test_real_mcp_initialization(self):
        """Test real MCP client initialization."""
        command = ["npx", "-y", "@modelcontextprotocol/server-github"]
        client = RealMCPClient(command)

        assert client.server_command == command
        assert not client._connected

    def test_real_mcp_capabilities(self):
        """Test real MCP capabilities."""
        command = ["echo", "test"]  # Use simple command for testing
        client = RealMCPClient(command)

        capabilities = client.get_capabilities()
        assert capabilities["protocol"] == "real_mcp_background"
        assert "background_server" in capabilities
        assert capabilities["background_server"] is True


class TestMockMCPSession:
    """Test cases for mock MCP session."""

    def test_session_initialization(self):
        """Test session initialization."""
        session = MockMCPSession("mcp://test-server:8080")
        assert session.server_url == "mcp://test-server:8080"
        assert len(session.tools) > 0

    def test_tool_listing(self):
        """Test tool listing."""
        session = MockMCPSession("mcp://test-server:8080")
        tools = session.list_tools()

        assert "github_search" in tools
        assert "file_reader" in tools
        assert "code_analyzer" in tools

    def test_context_retrieval(self):
        """Test context retrieval."""
        session = MockMCPSession("mcp://test-server:8080")

        # Test PR details context
        pr_context = session.get_context("Get PR details for test")
        assert "PR #123" in pr_context
        assert "authentication" in pr_context

        # Test file changes context
        file_context = session.get_context("Get file changes for test")
        assert "Modified files" in file_context
        assert "oauth.py" in file_context

    def test_tool_execution(self):
        """Test tool execution."""
        session = MockMCPSession("mcp://test-server:8080")

        # Test github_search tool
        result = session.execute_tool("github_search", {"query": "test"})
        assert "Found 3 related PRs" in result

        # Test file_reader tool
        result = session.execute_tool("file_reader", {"path": "test.py"})
        assert "OAuth2 implementation" in result

        # Test code_analyzer tool
        result = session.execute_tool("code_analyzer", {"code": "test"})
        assert "Code quality: Good" in result


if __name__ == "__main__":
    pytest.main([__file__])
