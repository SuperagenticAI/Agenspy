#!/usr/bin/env python3  
"""Basic MCP protocol demonstration."""  
  
import dspy  
from agentic_dspy import MCPClient, create_mcp_agent  
  
def main():  
    print("🚀 Basic MCP Demo")  
    print("=" * 30)  
      
    # Configure DSPy  
    try:  
        lm = dspy.LM('openai/gpt-4o-mini')  
        print("✅ Using OpenAI GPT-4o-mini")  
    except:  
        print("⚠️ Using dummy LM for demo")  
        class DummyLM:  
            def __call__(self, *args, **kwargs):  
                return dspy.Prediction(  
                    review_comment="This looks good!",  
                    approval_status="Approved"  
                )  
        lm = DummyLM()  
      
    dspy.configure(lm=lm)  
      
    # Create MCP agent  
    agent = create_mcp_agent("mcp://demo-server:8080")  
      
    # Test the agent  
    result = agent(  
        pr_url="https://github.com/example/repo/pull/1",  
        review_focus="code_quality"  
    )  
      
    print(f"Review: {result.review_comment}")  
    print(f"Status: {result.approval_status}")  
      
    # Cleanup  
    agent.cleanup()  
  
if __name__ == "__main__":  
    main()