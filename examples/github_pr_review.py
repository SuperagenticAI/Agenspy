#!/usr/bin/env python3  
"""GitHub PR Review example using Agentic-DSPy."""  
  
import dspy  
import os  
from agentic_dspy import GitHubPRReviewAgent, RealMCPClient  
  
def setup_dspy():  
    """Setup DSPy with available LM."""  
    try:  
        lm = dspy.LM('openai/gpt-4o-mini')  
        print("✅ Using OpenAI GPT-4o-mini")  
    except Exception as e:  
        print(f"⚠️ OpenAI not available ({e}), using dummy LM")  
        class DummyLM:  
            def __call__(self, *args, **kwargs):  
                return dspy.Prediction(  
                    analysis="The PR introduces authentication features with proper error handling.",  
                    suggestions=["Add input validation", "Consider rate limiting", "Add unit tests"],  
                    review_comment="Good implementation overall. The OAuth2 integration looks solid, but consider adding more comprehensive error handling and input validation.",  
                    approval_status="Approved with suggestions"  
                )  
        lm = DummyLM()  
      
    dspy.configure(lm=lm)  
    return lm  
  
def demo_mock_mcp():  
    """Demo using mock MCP server."""  
    print("\n" + "="*50)  
    print("DEMO 1: Mock MCP Server")  
    print("="*50)  
      
    # Create agent with mock MCP  
    agent = GitHubPRReviewAgent("mcp://mock-github-server:8080", use_real_mcp=False)  
      
    # Review a PR  
    result = agent(  
        pr_url="https://github.com/example/awesome-project/pull/42",  
        review_focus="security"  
    )  
      
    print(f"\n📊 Mock MCP Results:")  
    print(f"Review: {result.review_comment}")  
    print(f"Status: {result.approval_status}")  
    print(f"Tools Used: {result.mcp_tools_used}")  
    print(f"Protocol Info: {result.protocol_info}")  
      
    agent.cleanup()  
    return result  
  
def demo_real_mcp():  
    """Demo using real MCP server (requires Node.js)."""  
    print("\n" + "="*50)  
    print("DEMO 2: Real MCP Server")  
    print("="*50)  
      
    github_token = os.environ.get('GITHUB_TOKEN')  
    if not github_token:  
        print("⚠️ No GITHUB_TOKEN found. Using mock responses.")  
        return None  
      
    try:  
        # Create agent with real MCP  
        agent = GitHubPRReviewAgent(  
            "mcp://real-github-server:8080",   
            use_real_mcp=True,  
            github_token=github_token  
        )  
          
        # Review a real PR  
        result = agent(  
            pr_url="https://github.com/microsoft/vscode/pull/12345",  
            review_focus="code_quality"  
        )  
          
        print(f"\n📊 Real MCP Results:")  
        print(f"Review: {result.review_comment}")  
        print(f"Status: {result.approval_status}")  
        print(f"Capabilities: {result.protocol_capabilities}")  
          
        agent.cleanup()  
        return result  
          
    except Exception as e:  
        print(f"❌ Real MCP demo failed: {e}")  
        print("💡 Make sure Node.js is installed and GitHub MCP server is available")  
        return None  
  
def compare_approaches():  
    """Compare protocol-first vs traditional tool-based approach."""  
    print("\n" + "="*50)  
    print("COMPARISON: Protocol vs Tool Approach")  
    print("="*50)  
      
    print("\n🔧 Traditional Tool Approach:")  
    print("- Manual tool creation for each MCP function")  
    print("- No session management")  
    print("- No capability discovery")  
    print("- Limited error handling")  
      
    print("\n🚀 Protocol-First Approach:")  
    print("- Automatic connection management")  
    print("- Built-in session handling")  
    print("- Dynamic capability discovery")  
    print("- Standardized error handling")  
    print("- Future protocol extensibility")  
  
def main():  
    print("🚀 GitHub PR Review Demo with Agentic-DSPy")  
    print("=" * 60)  
      
    # Setup DSPy  
    lm = setup_dspy()  
      
    # Run demos  
    mock_result = demo_mock_mcp()  
    real_result = demo_real_mcp()  
      
    # Show comparison  
    compare_approaches()  
      
    # Summary  
    print("\n" + "="*60)  
    print("DEMO SUMMARY")  
    print("="*60)  
    print("✅ Mock MCP demo completed successfully")  
    if real_result:  
        print("✅ Real MCP demo completed successfully")  
    else:  
        print("⚠️ Real MCP demo skipped (requires setup)")  
      
    print("\n🎯 Key Takeaways:")  
    print("1. Protocol layer provides richer semantics than individual tools")  
    print("2. Automatic connection and session management")  
    print("3. Works seamlessly with DSPy's optimization system")  
    print("4. Extensible for future protocols (Agent2Agent, etc.)")  
      
    print(f"\n📈 Performance Benefits:")  
    if mock_result:  
        print(f"- Protocol capabilities: {len(mock_result.protocol_capabilities.get('tools', []))} tools discovered")  
        print(f"- Session management: {mock_result.protocol_capabilities.get('session_management', False)}")  
        print(f"- Context sharing: {mock_result.protocol_capabilities.get('context_sharing', False)}")  
  
if __name__ == "__main__":  
    main()