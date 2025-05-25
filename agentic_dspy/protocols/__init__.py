"""Protocol implementations for Agentic-DSPy."""  
  
from .base import BaseProtocol, ProtocolType  
from .mcp.client import MCPClient, RealMCPClient  
from .agent2agent.client import Agent2AgentClient  
  
__all__ = [  
    "BaseProtocol",  
    "ProtocolType",   
    "MCPClient",  
    "RealMCPClient",  
    "Agent2AgentClient",  
]