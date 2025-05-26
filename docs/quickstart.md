# Quick Start Guide

## Basic Usage

### 1. Configure DSPy

```python
import dspy
from agentic_dspy import create_mcp_agent

# Configure your language model
lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)
```

### 2. Create an MCP Agent

```python
agent = create_mcp_agent("mcp://github-server:8080")

# Use the agent
result = agent(
    pr_url="https://github.com/org/repo/pull/123",
    review_focus="security"
)
print(f"Review: {result.review_comment}")
```

### 3. Multi-Protocol Agent

```python
from agentic_dspy import MultiProtocolAgent, MCPClient, Agent2AgentClient

# Create multi-protocol agent
agent = MultiProtocolAgent("my-agent")

# Add MCP protocol (production-ready)
mcp_client = MCPClient("mcp://github-server:8080")
agent.add_protocol(mcp_client)

# Add Agent2Agent protocol (MOCK implementation)
# Note: This is a mock implementation for demonstration only.
# For production, integrate with https://github.com/google/A2A
a2a_client = Agent2AgentClient("tcp://localhost:9090", "my-agent")
agent.add_protocol(a2a_client)
print("⚠️  Using MOCK implementation of Agent2Agent protocol")

# Use the agent
result = agent("Analyze this repository")

# Check which protocol was used
if hasattr(result, 'protocol_used') and 'a2a' in str(result.protocol_used).lower():
    print("ℹ️  Note: Agent2Agent protocol is running in MOCK mode")
    print("    For production use, integrate with: https://github.com/google/A2A")
```

### 4. Working with MOCK Agent2Agent

The Agent2Agent implementation included in this package is a **MOCK** implementation for demonstration and testing purposes only. It provides the same interface as the real implementation but doesn't actually communicate with other agents.

#### Key Limitations:
- No actual network communication occurs
- Messages are not delivered to other agents
- Peer discovery returns mock data
- All operations complete successfully but don't have real effects

#### For Production Use:
To use Agent2Agent in production, you'll need to integrate with the official Google A2A project:
1. Install the official A2A client: `pip install a2a`
2. Set up an A2A server
3. Replace the mock implementation with the real A2A client

```python
# Example of using the real A2A client (not included in this package)
from a2a import Agent2AgentClient as RealA2AClient

# Real A2A client would be used like this:
# a2a_client = RealA2AClient(server_address="localhost:9090", agent_id="my-agent")
```

### 5. Getting Help

For questions about the MOCK implementation or help with production integration:
- Open an issue on our [GitHub repository](https://github.com/Shashikant86/Agentic-DSPy/issues)
- Reference the [Google A2A documentation](https://github.com/google/A2A) for production use
