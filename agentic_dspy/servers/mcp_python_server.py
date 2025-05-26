"""Python-based MCP server implementation."""

import json
import logging
from typing import Any, Callable, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class MCPTool(BaseModel):
    """MCP Tool definition."""

    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Optional[Callable] = None


class MCPRequest(BaseModel):
    """MCP Request format."""

    method: str
    params: Dict[str, Any]
    id: Optional[str] = None


class MCPResponse(BaseModel):
    """MCP Response format."""

    result: Any
    error: Optional[str] = None
    id: Optional[str] = None


class PythonMCPServer:
    """Python implementation of MCP server."""

    def __init__(self, name: str = "python-mcp-server", port: int = 8080):
        self.name = name
        self.port = port
        self.tools: Dict[str, MCPTool] = {}
        self.app = FastAPI(title=f"MCP Server - {name}")
        self.active_connections: List[WebSocket] = []

        # Setup WebSocket endpoint
        @self.app.websocket("/mcp")
        async def websocket_endpoint(websocket: WebSocket):
            await self.handle_websocket(websocket)

    def register_tool(self, name: str, description: str, parameters: Dict[str, Any], handler: Callable):
        """Register a new tool with the MCP server."""
        tool = MCPTool(name=name, description=description, parameters=parameters, handler=handler)
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")

    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connections for MCP protocol."""
        await websocket.accept()
        self.active_connections.append(websocket)

        try:
            while True:
                data = await websocket.receive_text()
                request = json.loads(data)

                response = await self.process_request(request)
                await websocket.send_text(json.dumps(response))

        except WebSocketDisconnect:
            self.active_connections.remove(websocket)
            logger.info("Client disconnected")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process MCP requests."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                result = await self.handle_initialize(params)
            elif method == "list_tools":
                result = await self.handle_list_tools()
            elif method == "call_tool":
                result = await self.handle_call_tool(params)
            else:
                raise ValueError(f"Unknown method: {method}")

            return {"result": result, "id": request_id}

        except Exception as e:
            return {"error": str(e), "id": request_id}

    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialization."""
        return {
            "protocol_version": "1.0",
            "server_info": {"name": self.name, "version": "0.1.0"},
            "capabilities": {"tools": True, "context": True},
        }

    async def handle_list_tools(self) -> Dict[str, Any]:
        """Handle tool listing."""
        tools = []
        for tool in self.tools.values():
            tools.append({"name": tool.name, "description": tool.description, "parameters": tool.parameters})

        return {"tools": tools}

    async def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution."""
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})

        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")

        tool = self.tools[tool_name]
        if tool.handler:
            result = await tool.handler(**tool_args)
        else:
            result = f"Tool {tool_name} executed with args: {tool_args}"

        return {"content": result, "isError": False}

    def start(self):
        """Start the MCP server."""
        logger.info(f"Starting MCP server on port {self.port}")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)


class GitHubMCPServer(PythonMCPServer):
    """GitHub-specific MCP server implementation."""

    def __init__(self, github_token: Optional[str] = None, port: int = 8080):
        super().__init__("github-mcp-server", port)
        self.github_token = github_token
        self._register_github_tools()

    def _register_github_tools(self):
        """Register GitHub-specific tools."""

        async def search_repositories(query: str, limit: int = 10):
            """Search GitHub repositories."""
            # Simulate GitHub API call
            return f"Found {limit} repositories matching '{query}'"

        async def get_repository(owner: str, repo: str):
            """Get repository information."""
            return f"Repository info for {owner}/{repo}"

        async def get_file_contents(owner: str, repo: str, path: str):
            """Get file contents from repository."""
            return f"File contents from {owner}/{repo}/{path}"

        async def list_issues(owner: str, repo: str, state: str = "open"):
            """List repository issues."""
            return f"Issues in {owner}/{repo} (state: {state})"

        # Register tools
        self.register_tool(
            "search_repositories",
            "Search GitHub repositories",
            {"query": "string", "limit": "integer"},
            search_repositories,
        )

        self.register_tool(
            "get_repository", "Get repository information", {"owner": "string", "repo": "string"}, get_repository
        )

        self.register_tool(
            "get_file_contents",
            "Get file contents from repository",
            {"owner": "string", "repo": "string", "path": "string"},
            get_file_contents,
        )

        self.register_tool(
            "list_issues",
            "List repository issues",
            {"owner": "string", "repo": "string", "state": "string"},
            list_issues,
        )
