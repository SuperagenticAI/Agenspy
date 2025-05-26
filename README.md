# Agentic-DSPy 🚀

[![PyPI Version](https://img.shields.io/pypi/v/agentic-dspy.svg)](https://pypi.org/project/agentic-dspy/)
[![Python Version](https://img.shields.io/pypi/pyversions/agentic-dspy.svg)](https://pypi.org/project/agentic-dspy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**Agentic-DSPy** is a protocol-first AI agent framework built on top of DSPy, designed to create sophisticated, production-ready AI agents with support for multiple communication protocols including MCP (Model Context Protocol) and Agent2Agent.

## 🌟 Features

- **Protocol-First Architecture**: Built around communication protocols rather than individual tools
- **Multi-Protocol Support**: Native support for MCP, Agent2Agent, and extensible for future protocols
- **DSPy Integration**: Leverages DSPy's powerful optimization and module composition
- **Comprehensive CLI**: Full-featured command-line interface for managing agents and workflows
- **Python & JavaScript Servers**: Support for both Python and Node.js MCP servers
- **Automatic Connection Management**: Protocol-level session and capability handling

## 📦 Installation

### Basic Installation
```bash
pip install agentic-dspy
```

### With MCP Support
```bash
pip install "agentic-dspy[mcp]"
```

### Development Installation
```bash
git clone https://github.com/Shashikant86/Agentic-DSPy.git
cd Agentic-DSPy
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Basic MCP Agent

```python
import dspy
from agentic_dspy import create_mcp_agent

# Configure DSPy with your preferred language model
lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)

# Create an MCP agent
agent = create_mcp_agent("mcp://github-server:8080")

# Use the agent to review a pull request
result = agent(
    pr_url="https://github.com/org/repo/pull/123",
    review_focus="security"
)

print(f"Review: {result.review_comment}")
print(f"Status: {result.approval_status}")
```

### Multi-Protocol Agent (Experimental)

```python
from agentic_dspy import MultiProtocolAgent, MCPClient, Agent2AgentClient

# Create a multi-protocol agent
agent = MultiProtocolAgent("my-agent")

# Add protocol clients
mcp_client = MCPClient("mcp://github-server:8080")
a2a_client = Agent2AgentClient("tcp://localhost:9090", "my-agent")

agent.add_protocol(mcp_client)
agent.add_protocol(a2a_client)

# The agent will automatically route to the best protocol
result = agent("Analyze this repository for security issues")
```

### Custom Agent with Tools

```python
from agentic_dspy import BaseAgent
from typing import Dict, Any

class CodeReviewAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.register_tool("review_code", self.review_code)

    async def review_code(self, code: str, language: str) -> Dict[str, Any]:
        """Review code for potential issues."""
        # Your custom review logic here
        return {
            "score": 0.85,
            "issues": ["Consider adding error handling", "Document this function"],
            "suggestions": ["Use list comprehension for better performance"]
        }

# Usage
agent = CodeReviewAgent("code-reviewer")
result = await agent.review_code("def add(a, b): return a + b", "python")
```

# 🏗️ Architecture

Agentic-DSPy provides a protocol-first approach to building AI agents:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   DSPy Agent    │───>│  Protocol Layer  │───>│  MCP/A2A/etc    │
│                 │    │                  │    │                 │
│ • ChainOfThought│    │ • Connection Mgmt│    │ • GitHub Tools  │
│ • Predict       │    │ • Capabilities   │    │ • File Access   │
│ • ReAct         │    │ • Session State  │    │ • Web Search    │
└─────────────────┘    └──────────────────┘    └─────────────────┘

```

### Core Components

1. **DSPy Agent Layer**
   - Implements the core agent logic
   - Handles tool registration and execution
   - Manages conversation state

2. **Protocol Layer**
   - Handles communication between agents
   - Manages protocol-specific details
   - Provides consistent interface to agents

3. **Protocol Implementations**
   - MCP (Model Context Protocol)
   - Agent2Agent Protocol
   - Extensible for custom protocols

### Advanced Usage Example: Custom MCP Server

```python
from agentic_dspy.servers import BaseMCPServer
import asyncio

class CustomMCPServer(BaseMCPServer):
    def __init__(self, port: int = 8080):
        super().__init__(port=port)
        self.register_tool("custom_operation", self.handle_custom_op)

    async def handle_custom_op(self, param1: str, param2: int) -> dict:
        """Handle custom operation with parameters."""
        return {"result": f"Processed {param1} with {param2}"}

# Start the server
server = CustomMCPServer(port=8080)
print("Starting MCP server on port 8080...")
server.start()
```

## 🖥️ Command Line Interface

Agentic-DSPy provides a command-line interface for managing agents and protocols:

### Basic Commands
```bash
# Show help and available commands
adspy --help

# Show version information
adspy --version
```

### Agent Management
```bash
# List available agents
adspy agent --help
```

### Protocol Management
```bash
# List available protocols
adspy protocol --help

# Test protocol connection
adspy protocol test [PROTOCOL] [--server SERVER]

# Get detailed information about a protocol
adspy protocol info [PROTOCOL_NAME]
```

### Server Management
```bash
# Start the server
adspy server --help
```

## 📚 Documentation

For detailed documentation, including API reference, examples, and advanced usage, please visit our [documentation site](TBC).

## 🧪 Testing

Run the test suite with:
```bash
pytest tests/
```

## 📚 Examples

See the examples/ directory for complete examples:

- `basic_mcp_demo.py` - Simple MCP agent
- `comprehensive_mcp_demo.py` - Comprehensive MCP agent
- `github_pr_review.py` - GitHub PR review agent
- `multi_protocol_demo.py` - Multi-protocol agent (Experimental Mock)
- `python_server_demo.py` - Python MCP server



## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to contribute to the project.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [DSPy Documentation](https://dspy.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent2Agent Protocol](https://google.github.io/A2A/)
- [GitHub Repository](https://github.com/Shashikant86/Agentic-DSPy)

## 📬 Contact

For questions and support, please open an issue on our [GitHub repository](https://github.com/Shashikant86/Agentic-DSPy/issues).

## 🙏 Acknowledgments

- The DSPy team for their amazing framework
