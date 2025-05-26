"""MCP Server implementation for Agenspy."""

from typing import Any, Callable, Dict, List, Optional

import dspy

from ..base import BaseProtocol, ProtocolType


class MCPServer(BaseProtocol):
    """MCP Server implementation as DSPy Module."""

    def __init__(self, port: int = 8080, context_providers: Optional[List[Callable]] = None, **kwargs):
        protocol_config = {"type": ProtocolType.MCP, "port": port, "server_mode": True}
        super().__init__(protocol_config, **kwargs)
        self.port = port
        self.context_providers = context_providers or []
        self.server_instance = None
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.clients: List[Any] = []

    def connect(self) -> bool:
        """Start MCP server."""
        try:
            print(f"🚀 Starting MCP server on port {self.port}")
            self.server_instance = self._create_server()
            self._register_default_tools()
            self._connected = True
            print(f"✅ MCP Server started on port {self.port}")
            return True
        except Exception as e:
            print(f"❌ Failed to start MCP server: {e}")
            return False

    def disconnect(self) -> None:
        """Stop MCP server."""
        if self.server_instance:
            self.server_instance.stop()
            self._connected = False
            print("🛑 MCP server stopped")

    def get_capabilities(self) -> Dict[str, Any]:
        """Get MCP server capabilities."""
        return {
            "protocol": "mcp_server",
            "version": "1.0",
            "tools": list(self.tools.keys()),
            "context_providers": len(self.context_providers),
            "port": self.port,
            "clients_connected": len(self.clients),
        }

    def discover_peers(self) -> List[str]:
        """Discover connected clients."""
        return [f"client_{i}" for i in range(len(self.clients))]

    def register_tool(
        self, name: str, description: str, handler: Callable, parameters: Optional[Dict[str, Any]] = None
    ):
        """Register a tool with the MCP server."""
        self.tools[name] = {"description": description, "handler": handler, "parameters": parameters or {}}
        print(f"📝 Registered MCP tool: {name}")

    def register_context_provider(self, provider: Callable):
        """Register a context provider."""
        self.context_providers.append(provider)
        print("📝 Registered context provider")

    def _create_server(self):
        """Create the actual MCP server instance."""
        # This would create a real MCP server
        # For demo purposes, we'll use a mock server
        return MockMCPServerInstance(self.port, self.tools)

    def _register_default_tools(self):
        """Register default tools."""

        def echo_tool(message: str) -> str:
            return f"Echo: {message}"

        def status_tool() -> str:
            return f"Server running on port {self.port} with {len(self.tools)} tools"

        self.register_tool("echo", "Echo a message", echo_tool, {"message": "string"})
        self.register_tool("status", "Get server status", status_tool)

    def _handle_request(self, **kwargs) -> dspy.Prediction:
        """Handle server requests."""
        request_type = kwargs.get("request_type", "status")

        if request_type == "status":
            return dspy.Prediction(
                server_status="running",
                capabilities=self.get_capabilities(),
                protocol_info=f"MCP server with {len(self.tools)} tools",
            )
        elif request_type == "tools":
            return dspy.Prediction(
                available_tools=list(self.tools.keys()),
                tool_details=self.tools,
                protocol_info="Tool listing from MCP server",
            )
        else:
            return dspy.Prediction(
                error=f"Unknown request type: {request_type}", protocol_info="MCP server error response"
            )


class MockMCPServerInstance:
    """Mock MCP server instance for demonstration."""

    def __init__(self, port: int, tools: Dict[str, Any]):
        self.port = port
        self.tools = tools
        self.running = False

    def start(self):
        """Start the mock server."""
        self.running = True
        print(f"Mock MCP server started on port {self.port}")

    def stop(self):
        """Stop the mock server."""
        self.running = False
        print("Mock MCP server stopped")
