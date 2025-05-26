# Protocol Guide

## Supported Protocols

### Model Context Protocol (MCP)

MCP is a standardized protocol for AI model context sharing.

#### Features
- Tool discovery and execution
- Context sharing between models
- Session management
- Error handling

#### Usage
```python
from agenspy import MCPClient

client = MCPClient("mcp://server:8080")
result = client(context_request="Get repository info", tool_name="github_search")
```

### Agent2Agent Protocol

TBC


### Adding New Protocols

To add a new protocol:

- Inherit from `BaseProtocol`
- Implement required methods
- Register with the protocol registry

```python
from agenspy.protocols.base import BaseProtocol, ProtocolType

class MyProtocol(BaseProtocol):
    def connect(self) -> bool:
        # Implementation
        pass

    def disconnect(self) -> None:
        # Implementation
        pass

    # ... other methods

```
