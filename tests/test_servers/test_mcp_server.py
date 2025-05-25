"""Tests for MCP server implementations."""  
  
import pytest  
import asyncio  
from agentic_dspy.servers.mcp_python_server import PythonMCPServer, GitHubMCPServer  
  
class TestPythonMCPServer:  
    """Test cases for Python MCP server."""  
      
    def test_server_initialization(self):  
        """Test server initialization."""  
        server = PythonMCPServer("test-server", 8080)  
        assert server.name == "test-server"  
        assert server.port == 8080  
        assert len(server.tools) == 0  
      
    def test_tool_registration(self):  
        """Test tool registration."""  
        server = PythonMCPServer("test-server", 8080)  
          
        async def test_tool(param: str):  
            return f"Test result: {param}"  
          
        server.register_tool(  
            "test_tool",  
            "A test tool",  
            {"param": "string"},  
            test_tool  
        )  
          
        assert "test_tool" in server.tools  
        assert server.tools["test_tool"].name == "test_tool"  
        assert server.tools["test_tool"].description == "A test tool"  
      
    @pytest.mark.asyncio  
    async def test_request_processing(self):  
        """Test request processing."""  
        server = PythonMCPServer("test-server", 8080)  
          
        # Test initialize request  
        init_request = {"method": "initialize", "params": {}, "id": "1"}  
        response = await server.process_request(init_request)  
          
        assert "result" in response  
        assert response["result"]["protocol_version"] == "1.0"  
        assert response["id"] == "1"  
      
    @pytest.mark.asyncio  
    async def test_list_tools_request(self):  
        """Test list tools request."""  
        server = PythonMCPServer("test-server", 8080)  
          
        async def test_tool():  
            return "test"  
          
        server.register_tool("test_tool", "Test tool", {}, test_tool)  
          
        request = {"method": "list_tools", "params": {}, "id": "2"}  
        response = await server.process_request(request)  
          
        assert "result" in response  
        assert "tools" in response["result"]  
        assert len(response["result"]["tools"]) == 1  
        assert response["result"]["tools"][0]["name"] == "test_tool"  
  
class TestGitHubMCPServer:  
    """Test cases for GitHub MCP server."""  
      
    def test_github_server_initialization(self):  
        """Test GitHub server initialization."""  
        server = GitHubMCPServer(port=8081)  
        assert server.name == "github-mcp-server"  
        assert server.port == 8081  
          
        # Check that GitHub tools are registered  
        assert "search_repositories" in server.tools  
        assert "get_repository" in server.tools  
        assert "get_file_contents" in server.tools  
        assert "list_issues" in server.tools  
      
    @pytest.mark.asyncio  
    async def test_github_tool_execution(self):  
        """Test GitHub tool execution."""  
        server = GitHubMCPServer(port=8081)  
          
        # Test search_repositories tool  
        search_tool = server.tools["search_repositories"]  
        result = await search_tool.handler(query="test", limit=5)  
          
        assert "query" in result  
        assert result["query"] == "test"  
        assert "results" in result  
        assert len(result["results"]) == 5  
  
if __name__ == "__main__":  
    pytest.main([__file__])