# Quick Start Guide  
  
## Basic Usage  
  
### 1. Configure DSPy  
  
```python  
import dspy  
from agentic_dspy import create_mcp_agent  
  
# Configure your language model  [header-3](#header-3)
lm = dspy.LM('openai/gpt-4o-mini')  
dspy.configure(lm=lm)  
```

### 2. Create an MCP Agent

```python  
agent = create_mcp_agent("mcp://github-server:8080")  
  
# Use the agent  [header-5](#header-5)
result = agent(  
    pr_url="https://github.com/org/repo/pull/123",  
    review_focus="security"  
)  
print(f"Review: {result.review_comment}")
```

### 3. Multi-Protocol Agent

```python  
from agentic_dspy import MultiProtocolAgent, MCPClient, Agent2AgentClient  
  
# Create multi-protocol agent  [header-6](#header-6)
agent = MultiProtocolAgent("my-agent")  
  
# Add protocols  [header-7](#header-7)
mcp_client = MCPClient("mcp://github-server:8080")  
a2a_client = Agent2AgentClient("tcp://localhost:9090", "my-agent")  
  
agent.add_protocol(mcp_client)  
agent.add_protocol(a2a_client)  
  
# Use the agent  [header-8](#header-8)
result = agent("Analyze this repository")
```





