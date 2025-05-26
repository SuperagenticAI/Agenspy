#!/usr/bin/env python3
"""Multi-protocol agent demonstration."""

import dspy
from agenspy import (
    MultiProtocolAgent,
    MCPClient,
    Agent2AgentClient,
    ProtocolType
)

def main():
    print("🚀 Multi-Protocol Agent Demo")
    print("=" * 40)

    # Configure DSPy
    try:
        lm = dspy.LM('openai/gpt-4o-mini')
    except:
        class DummyLM:
            def __call__(self, *args, **kwargs):
                return dspy.Prediction(
                    best_protocol="mcp",
                    reasoning="MCP is best for this task",
                    final_answer="Task completed successfully",
                    confidence=0.9
                )
        lm = DummyLM()

    dspy.configure(lm=lm)

    # Create multi-protocol agent
    agent = MultiProtocolAgent("demo-agent")

    # Add protocols
    mcp_client = MCPClient("mcp://github-server:8080")
    a2a_client = Agent2AgentClient("tcp://localhost:9090", "demo-agent")

    agent.add_protocol(mcp_client)
    agent.add_protocol(a2a_client)

    # Test routing
    result = agent("Analyze this GitHub repository for security issues")

    print(f"Result: {result.final_answer}")
    print(f"Protocol used: {result.protocol_used}")
    print(f"Reasoning: {result.routing_reasoning}")

    # Test using all protocols
    result_all = agent(
        "Get comprehensive analysis from all sources",
        use_all_protocols=True
    )

    print(f"Multi-protocol result: {result_all.final_answer}")
    print(f"Confidence: {result_all.confidence}")
    print(f"Protocols used: {result_all.protocols_used}")

    # Cleanup
    agent.cleanup()

if __name__ == "__main__":
    main()
