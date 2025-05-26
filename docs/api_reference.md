# API Reference

## Core Classes

### BaseProtocol

Base class for all protocol implementations.

```python
class BaseProtocol(dspy.Module):
    def connect(self) -> bool
    def disconnect(self) -> None
    def get_capabilities(self) -> Dict[str, Any]
    def discover_peers(self) -> List[str]
```

### MCPClient

Model Context Protocol client implementation.

```python
class MCPClient(BaseProtocol):
    def __init__(self, server_url: str, timeout: int = 30)
# MultiProtocolAgent
# Agent supporting multiple protocols simultaneously.

class MultiProtocolAgent(dspy.Module):
    def add_protocol(self, protocol: BaseProtocol)
    def forward(self, request: str, use_all_protocols: bool = False)
```



### Utility Functions

create_mcp_agent
Convenience function to create MCP agents.

```python

def create_mcp_agent(server_url: str, **kwargs) -> GitHubPRReviewAgent
# create_multi_protocol_agent
# Convenience function to create multi-protocol agents.

def create_multi_protocol_agent(agent_id: str = "multi-agent") -> MultiProtocolAgent
```

### Protocol Registry

Global registry for managing protocol implementations.

```python
from agentic_dspy.utils import registry

# Register a protocol
registry.register_protocol(ProtocolType.CUSTOM, MyProtocol)

# Create protocol instance
protocol = registry.create_protocol(ProtocolType.MCP, server_url="...")

```
