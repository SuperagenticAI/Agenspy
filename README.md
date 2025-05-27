# Agenspy (Agentic DSPy) 🚀

[![PyPI Version](https://img.shields.io/pypi/v/agenspy.svg)](https://pypi.org/project/agenspy/)
[![Python Version](https://img.shields.io/pypi/pyversions/agenspy.svg)](https://pypi.org/project/agenspy/)
[![Documentation](https://img.shields.io/badge/Documentation-orange)](https://super-agentic.ai/agenspy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Agenspy** (Agentic DSPy) is a protocol-first AI agent framework built on top of DSPy, designed to create sophisticated, production-ready AI agents with support for multiple communication protocols including MCP (Model Context Protocol) and Agent2Agent.

## 🌟 Features

- **Protocol-First Architecture**: Built around communication protocols rather than individual tools
- **Multi-Protocol Support**: Native support for MCP, Agent2Agent, and extensible for future protocols
- **DSPy Integration**: Leverages DSPy's powerful optimization and module composition
- **Comprehensive CLI**: Full-featured command-line interface for managing agents and workflows
- **Python & JavaScript Servers**: Support for both Python and Node.js MCP servers
- **Automatic Connection Management**: Protocol-level session and capability handling

## 🤔 Motivation

All other agent frameworks are using the MCP as integraed client servers. They are using both both tool-first and protocol first approach but DSPy was still using tool-first approach. All the MCP tools needs to converted into DSPy.Tools. Also DSPy Agents are not in the list o Google's A2A Agent Directory [here](https://github.com/google/A2A/blob/main/samples/python/agents/README.md). So filed Enhancemnt Proposal on DSPy Github repo [here](https://github.com/stanfordnlp/dspy/issues/8273) and Agenspy born to demonstrate how DSPy can use protocol first approach for building agents those are ready for next generaton of protocols. 


## 📦 Installation

### Basic Installation
```bash
pip install agenspy
```

### With MCP Support
For enhanced functionality with the Model Context Protocol, install with MCP support:
```bash
pip install "agenspy[mcp]"
```

### Development Installation
To contribute to Agenspy or work with the latest development version:
```bash
git clone https://github.com/superagenticai/Agenspy.git
cd Agenspy
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Basic MCP Agent
Agenspy makes it easy to create AI agents that can interact with MCP servers. Here's a simple example of creating a pull request review agent:

```python
import dspy
from agenspy import create_mcp_pr_review_agent

# Configure DSPy with your preferred language model
lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)

# Create an MCP agent connected to a GitHub server
agent = create_mcp_pr_review_agent("mcp://github-server:8080")

# Use the agent to review a pull request
result = agent(
    pr_url="https://github.com/org/repo/pull/123",
    review_focus="security"
)

print(f"Review: {result.review_comment}")
print(f"Status: {result.approval_status}")
```

### Multi-Protocol Agent (Experimental)
Agenspy supports multiple communication protocols simultaneously. Here's how to create an agent that can use both MCP and Agent2Agent protocols:

```python
from agenspy import MultiProtocolAgent, MCPClient, Agent2AgentClient

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
You can create custom agents with specialized functionality. Here's an example of a code review agent:

```python
import asyncio
import dspy
from agenspy import BaseAgent
from typing import Dict, Any

class CodeReviewAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        
    async def review_code(self, code: str, language: str) -> Dict[str, Any]:
        """Review code for potential issues."""
        # Your custom review logic here
        return {
            "score": 0.85,
            "issues": ["Consider adding error handling", "Document this function"],
            "suggestions": ["Use list comprehension for better performance"]
        }
    
    async def forward(self, **kwargs) -> dspy.Prediction:
        """Process agent request."""
        code = kwargs.get("code", "")
        language = kwargs.get("language", "python")
        result = await self.review_code(code, language)
        return dspy.Prediction(**result)

async def main():
    # Configure DSPy with your preferred language model
    lm = dspy.LM('openai/gpt-4o-mini')
    dspy.configure(lm=lm)
    
    # Create and use the agent
    agent = CodeReviewAgent("code-reviewer")
    result = await agent(code="def add(a, b): return a + b", language="python")
    print("Review Results:", result)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
```


### Python MCP Server

Launch a Python MCP server with custom tools:

```python

from agentic_dspy.servers import GitHubMCPServer  
  
# Create and start Python MCP server 
server = GitHubMCPServer(port=8080)  
  
# Add custom tools 
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

Agenspy provides a protocol-first approach to building AI agents:

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
   - **MCP (Model Context Protocol)**: For tool and model interactions
   - **Agent2Agent Protocol**: For direct agent-to-agent communication
   - Extensible architecture for custom protocol implementations

## Advanced Usage

### Custom MCP Server

Agenspy allows you to create custom MCP servers with specialized functionality. Here's an example of creating a custom MCP server with a custom operation:

```python
from agenspy.servers.mcp_python_server import PythonMCPServer
import asyncio

class CustomMCPServer(PythonMCPServer):
    def __init__(self, port: int = 8080):
        super().__init__(name="custom-mcp-server", port=port)
        self.register_tool(
            name="custom_operation",
            description="A custom operation that processes parameters",
            parameters={
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "First parameter"},
                    "param2": {"type": "integer", "description": "Second parameter"}
                },
                "required": ["param1", "param2"]
            },
            handler=self.handle_custom_op
        )

    async def handle_custom_op(self, **kwargs):
        """Handle custom operation with parameters."""
        param1 = kwargs.get("param1")
        param2 = kwargs.get("param2")
        return f"Processed {param1} with {param2}"

# Start the server
if __name__ == "__main__":
    server = CustomMCPServer(port=8080)
    print("Starting MCP server on port 8080...")
    server.start()
```

## 🖥️ Command Line Interface

Agenspy provides a command-line interface for managing agents and protocols:

```bash
# Show help and available commands
agenspy --help
```

### Some Useful CLI Commands

- Run agent PR Review Agent using Real MCP server:

```bash
agenspy agent run "Review PR https://github.com/stanfordnlp/dspy/pull/8277" --real-mcp
```

- Test protocol server:

```bash
agenspy protocol test mcp   
```

- Run example:

```bash
agenspy demo github-pr
```


## 📚 Documentation

For detailed documentation, including API reference, examples, and advanced usage, we need to wait but for now please visit our [website](https://super-agentic.ai/agenspy).

## 🧪 Testing

Run the test suite with:
```bash
pytest tests/
```

## 📚 Examples

See the examples/ directory for complete examples:
Get your OpenAI API key OPENAI_API_KEY from [here](https://platform.openai.com/api-keys) and optionally GITHUB_TOKEN from [here](https://github.com/settings/tokens) and set as ENV variables. You might also need to install nodejs and npm to run the nodejs server.

- `basic_mcp_demo.py` - Simple MCP agent
- `comprehensive_mcp_demo.py` - Comprehensive MCP agent
- `github_pr_review.py` - GitHub PR review agent
- `multi_protocol_demo.py` - Multi-protocol agent (Experimental Mock)
- `python_server_demo.py` - Python MCP server

Run the examples with:

```bash
agenspy demo github-pr
```
Or Run manually using Python:

```bash
python examples/github_pr_review.py
```

## 🔗 Resources
  [Superagentic Agenspy](https://super-agentic.ai/agenspy)
- [DSPy Documentation](https://dspy.ai/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent2Agent Protocol](https://google.github.io/A2A/)
- [GitHub Repository](https://github.com/superagenticai/Agenspy)


## 🚀 Future Roadmap

### Merge into DSPy

The end goal is to merge this tool in the dspy main repo and make it a first-class citizen of the DSPy ecosystem. However, if it doesn't fit there then it can be used independently as a protocol-first AI agent framework. 

### Get DSPy Listed in Google A2A Agent Directory

Implementations of A2A and Get DSPy Listed in A2A Agent Directory [here](https://github.com/google/A2A/blob/main/samples/python/agents/README.md) by building DSPy agents that utilize the A2A protocol.

### Future Work

Alternately, Agenspy can be developed independently as a protocol-first AI agent framework. Here are some food for thought for future work:

- **Protocol Layer**: WebSocket and gRPC support for real-time, high-performance agent communication
- **Agent Framework**: Enhanced orchestration, state management, and network discovery
- **Production Readiness**: Monitoring, load balancing, and fault tolerance features
- **Developer Tools**: Improved CLI, web dashboard, and debugging utilities
- **Ecosystem**: Cloud integrations and database adapters for popular services

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to contribute to the project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 📬 Contact

For questions and support, please open an issue on our [GitHub repository](https://github.com/superagenticai/Agenspy/issues).

## 🙏 Acknowledgments

- The DSPy team for their amazing framework
