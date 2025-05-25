"""MCP Client implementation for Agentic-DSPy."""  
  
import subprocess  
import time  
from typing import Dict, Any, List  
from ..base import BaseProtocol, ProtocolType  
import dspy  
  
class MCPClient(BaseProtocol):  
    """Model Context Protocol client implementation."""  
      
    def __init__(self, server_url: str, timeout: int = 30, **kwargs):  
        protocol_config = {  
            "type": ProtocolType.MCP,  
            "server_url": server_url,  
            "timeout": timeout  
        }  
        super().__init__(protocol_config, **kwargs)  
        self.server_url = server_url  
        self.timeout = timeout  
        self.session = None  
        self.available_tools = {}  
      
    def connect(self) -> bool:  
        """Establish MCP connection."""  
        try:  
            print(f"🔌 Connecting to MCP server: {self.server_url}")  
            # For demo purposes, using mock session  
            from .session import MockMCPSession  
            self.session = MockMCPSession(self.server_url)  
            self._discover_tools()  
            self._connected = True  
            print(f"✅ MCP Connected! Available tools: {list(self.available_tools.keys())}")  
            return True  
        except Exception as e:  
            print(f"❌ MCP connection failed: {e}")  
            return False  
      
    def disconnect(self) -> None:  
        """Close MCP connection."""  
        if self.session:  
            self.session.close()  
            self._connected = False  
            print("🔌 Disconnected from MCP server")  
      
    def get_capabilities(self) -> Dict[str, Any]:  
        """Get MCP server capabilities."""  
        self._capabilities = {  
            "protocol": "mcp",  
            "version": "1.0",  
            "tools": list(self.available_tools.keys()),  
            "context_sharing": True,  
            "session_management": True,  
            "server_url": self.server_url  
        }  
        return self._capabilities  
      
    def discover_peers(self) -> List[str]:  
        """Discover available MCP servers."""  
        # In a real implementation, this would discover MCP servers  
        return [self.server_url]  
      
    def _discover_tools(self):  
        """Discover available MCP tools."""  
        if self.session:  
            self.available_tools = self.session.list_tools()  
            print(f"🔍 Discovered {len(self.available_tools)} MCP tools")  
      
    def _handle_request(self, **kwargs) -> dspy.Prediction:  
        """Handle MCP-specific requests."""  
        context_request = kwargs.get('context_request', '')  
        tool_name = kwargs.get('tool_name', '')  
        tool_args = kwargs.get('tool_args', {})  
          
        print(f"📡 MCP Request - Context: {context_request[:50]}...")  
          
        # Get context from MCP server  
        context_data = self._get_context(context_request)  
          
        # Execute tool if specified  
        tool_result = ""  
        if tool_name and tool_name in self.available_tools:  
            print(f"🔧 Executing MCP tool: {tool_name}")  
            tool_result = self._execute_tool(tool_name, tool_args)  
          
        return dspy.Prediction(  
            context_data=context_data,  
            tool_result=tool_result,  
            capabilities=self.get_capabilities(),  
            protocol_info=f"MCP session active with {len(self.available_tools)} tools"  
        )  
      
    def _get_context(self, request: str) -> str:  
        """Get context from MCP server."""  
        if self.session:  
            return self.session.get_context(request)  
        return ""  
      
    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> str:  
        """Execute MCP tool."""  
        if self.session and tool_name in self.available_tools:  
            return self.session.execute_tool(tool_name, args)  
        return ""  
  
class RealMCPClient(BaseProtocol):  
    """Real MCP Client with background server management."""  
      
    def __init__(self, server_command: List[str], **kwargs):  
        protocol_config = {  
            "type": ProtocolType.MCP,  
            "server_command": server_command,  
            "real_server": True  
        }  
        super().__init__(protocol_config, **kwargs)  
        self.server_command = server_command  
        self.mcp_server = None  
        self.available_tools = {}  
      
    def connect(self) -> bool:  
        """Establish real MCP connection with background server."""  
        try:  
            from .session import BackgroundMCPServer  
            self.mcp_server = BackgroundMCPServer(self.server_command)  
              
            if not self.mcp_server.start_server():  
                return False  
              
            if not self.mcp_server.connect_client():  
                return False  
              
            self.available_tools = self.mcp_server.tools  
            self._connected = True  
              
            print(f"✅ Real MCP Connected! Available tools: {list(self.available_tools.keys())}")  
            return True  
              
        except Exception as e:  
            print(f"❌ Real MCP connection failed: {e}")  
            return False  
      
    def disconnect(self) -> None:  
        """Close MCP connection and stop server."""  
        if self.mcp_server:  
            self.mcp_server.stop_server()  
            self._connected = False  
            print("🔌 Disconnected from real MCP server")  
      
    def get_capabilities(self) -> Dict[str, Any]:  
        """Get MCP server capabilities."""  
        self._capabilities = {  
            "protocol": "real_mcp",  
            "version": "1.0",  
            "tools": list(self.available_tools.keys()),  
            "context_sharing": True,  
            "session_management": True,  
            "background_server": True,  
            "server_command": self.server_command  
        }  
        return self._capabilities  
      
    def discover_peers(self) -> List[str]:  
        """Discover available MCP servers."""  
        return ["background_server"]  
      
    def _handle_request(self, **kwargs) -> dspy.Prediction:  
        """Handle real MCP requests."""  
        context_request = kwargs.get('context_request', '')  
        tool_name = kwargs.get('tool_name', '')  
        tool_args = kwargs.get('tool_args', {})  
          
        print(f"📡 Real MCP Request - Context: {context_request[:50]}...")  
          
        if not self.mcp_server:  
            return dspy.Prediction(  
                context_data="No active MCP server",  
                tool_result="",  
                capabilities=self.get_capabilities()  
            )  
          
        context_data = self.mcp_server.get_context(context_request)  
          
        tool_result = ""  
        if tool_name and tool_name in self.available_tools:  
            print(f"🔧 Executing real MCP tool: {tool_name}")  
            tool_result = self.mcp_server.execute_tool(tool_name, tool_args)  
          
        return dspy.Prediction(  
            context_data=context_data,  
            tool_result=tool_result,  
            capabilities=self.get_capabilities(),  
            protocol_info=f"Real MCP server with {len(self.available_tools)} tools"  
        )