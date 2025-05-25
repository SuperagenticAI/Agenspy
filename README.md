# Agentic-DSPy  
  
Protocol-first AI agent framework built on DSPy, supporting MCP, Agent2Agent, and future protocols.  
  
## 🚀 Features  
  
- **Protocol-First Design**: Built around communication protocols rather than individual tools  
- **Multi-Protocol Support**: MCP, Agent2Agent, and extensible for future protocols  
- **DSPy Integration**: Leverages DSPy's optimization and module composition  
- **Python & JavaScript Servers**: Support for both Python and Node.js MCP servers  
- **Automatic Connection Management**: Protocol-level session and capability management  
  
## 📦 Installation  
  
```bash  
pip install agentic-dspy
```
### For MCP support:
```bash  
pip install agentic-dspy[mcp]
```

### For development:
```bash  
pip install agentic-dspy[dev]
```

# 🔧 Quick Start

### Basic MCP Agent

```python
import dspy  
from agentic_dspy import create_mcp_agent  
  
# Configure DSPy  [header-5](#header-5)
lm = dspy.LM('openai/gpt-4o-mini')  
dspy.configure(lm=lm)  
  
# Create MCP agent  [header-6](#header-6)
agent = create_mcp_agent("mcp://github-server:8080")  
  
# Use the agent  [header-7](#header-7)
result = agent(  
    pr_url="https://github.com/org/repo/pull/123",  
    review_focus="security"  
)  
  
print(f"Review: {result.review_comment}")  
print(f"Status: {result.approval_status}")

```

### Multi-Protocol Agent

```python
from agentic_dspy import MultiProtocolAgent, MCPClient, Agent2AgentClient  
  
# Create multi-protocol agent  [header-8](#header-8)
agent = MultiProtocolAgent("my-agent")  
  
# Add protocols  [header-9](#header-9)
mcp_client = MCPClient("mcp://github-server:8080")  
a2a_client = Agent2AgentClient("tcp://localhost:9090", "my-agent")  
  
agent.add_protocol(mcp_client)  
agent.add_protocol(a2a_client)  
  
# Use the agent (automatically routes to best protocol)  [header-10](#header-10)
result = agent("Analyze this repository for security issues")

```


### Python MCP Server

```python

from agentic_dspy.servers import GitHubMCPServer  
  
# Create and start Python MCP server  [header-11](#header-11)
server = GitHubMCPServer(port=8080)  
  
# Add custom tools  [header-12](#header-12)
async def custom_tool(param: str):  
    return f"Processed: {param}"  
  
server.register_tool(  
    "custom_tool",  
    "A custom tool",  
    {"param": "string"},  
    custom_tool  
)  
  
server.start()

```

# 🏗️ Architecture

Agentic-DSPy provides a protocol-first approach to building AI agents:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐  
│   DSPy Agent    │────│  Protocol Layer  │────│  MCP/A2A/etc    │  
│                 │    │                  │    │                 │  
│ • ChainOfThought│    │ • Connection Mgmt│    │ • GitHub Tools  │  
│ • Predict       │    │ • Capabilities   │    │ • File Access   │  
│ • ReAct         │    │ • Session State  │    │ • Web Search    │  
└─────────────────┘    └──────────────────┘    └─────────────────┘  

```


## 📚 Examples

See the examples/ directory for complete examples:

- basic_mcp_demo.py - Simple MCP agent
- github_pr_review.py - GitHub PR review agent
- multi_protocol_demo.py - Multi-protocol agent
- python_server_demo.py - Python MCP server


## 🤝 Contributing

- Fork the repository
- Create a feature branch
- Make your changes
- Add tests
- Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Links

[DSPy Documentation](https://dspy.ai/)
[Model Context Protocol](https://modelcontextprotocol.io/)
[Agent2Agent Protocol](https://google.github.io/A2A/)
