#!/usr/bin/env python3  
"""Fixed GitHub PR Review example with real MCP support."""  
  
import dspy  
import os  
import subprocess  
import sys  
import time  
from agentic_dspy import GitHubPRReviewAgent  
  
def check_prerequisites():  
    """Check if all prerequisites are available."""  
    issues = []  
      
    # Check Node.js  
    try:  
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)  
        print(f"✅ Node.js found: {result.stdout.strip()}")  
    except (subprocess.CalledProcessError, FileNotFoundError):  
        issues.append("Node.js not found. Install from https://nodejs.org/")  
      
    # Check npm/npx  
    try:  
        subprocess.run(["npx", "--version"], capture_output=True, check=True)  
        print("✅ npx found")  
    except (subprocess.CalledProcessError, FileNotFoundError):  
        issues.append("npx not found. Ensure Node.js is properly installed")  
      
    # Check GitHub token  
    github_token = os.environ.get('GITHUB_TOKEN')  
    if not github_token:  
        print("⚠️ GITHUB_TOKEN not found in environment")  
        github_token = input("Enter your GitHub token (or press Enter to use mock): ").strip()  
        if github_token:  
            os.environ['GITHUB_TOKEN'] = github_token  
            print("✅ GitHub token provided")  
        else:  
            print("⚠️ No GitHub token - will use mock responses")  
    else:  
        print("✅ GitHub token found in environment")  
      
    return issues, github_token  
  
def setup_mcp_server():  
    """Install and verify MCP server."""  
    try:  
        print("📦 Installing GitHub MCP server...")  
        result = subprocess.run(  
            ["npm", "install", " ", "@modelcontextprotocol/server-github"],  
            capture_output=True,  
            text=True,  
            timeout=60  
        )  
          
        if result.returncode == 0:  
            print("✅ GitHub MCP server installed successfully")  
            return True  
        else:  
            print(f"❌ Failed to install MCP server: {result.stderr}")  
            return False  
              
    except subprocess.TimeoutExpired:  
        print("❌ MCP server installation timed out")  
        return False  
    except Exception as e:  
        print(f"❌ Error installing MCP server: {e}")  
        return False  
  
def setup_dspy():  
    """Setup DSPy with available LM."""  
    try:  
        lm = dspy.LM('openai/gpt-4o-mini')  
        print("✅ Using OpenAI GPT-4o-mini")  
        dspy.configure(lm=lm)
        return lm  
    except Exception as e:  
        print(f"⚠️ OpenAI not available ({e}), using dummy LM")  
          
        class DummyLM:  
            def __call__(self, *args, **kwargs):  
                return dspy.Prediction(  
                    analysis="The PR introduces authentication features with proper error handling and follows security best practices.",  
                    suggestions=[  
                        "Add comprehensive input validation for OAuth parameters",  
                        "Implement rate limiting for authentication endpoints",   
                        "Add unit tests for edge cases",  
                        "Consider adding audit logging for authentication events"  
                    ],  
                    review_comment="Good implementation overall. The OAuth2 integration looks solid with proper error handling. Consider adding more comprehensive input validation and rate limiting for production use.",  
                    approval_status="Approved with suggestions"  
                )  
          
        lm = DummyLM()  
        dspy.configure(lm=lm)  
        return lm  
  
def demo_real_mcp_with_retry(github_token):  
    """Demo using real MCP server with retry logic."""  
    print("\n" + "="*60)  
    print("DEMO: Real MCP Server with GitHub Integration")  
    print("="*60)  
      
    max_retries = 3  
    for attempt in range(max_retries):  
        try:  
            print(f"\n🔄 Attempt {attempt + 1}/{max_retries}")  
              
            # Create agent with real MCP  
            agent = GitHubPRReviewAgent(  
                "mcp://real-github-server:8080",   
                use_real_mcp=True,  
                github_token=github_token  
            )  
              
            # Test with a real repository  
            test_repos = [  
                "https://github.com/microsoft/vscode/pull/200000",  # Likely to exist  
                "https://github.com/facebook/react/pull/25000",    # Fallback  
                "https://github.com/example/test-repo/pull/1"      # Mock fallback  
            ]  
              
            for repo_url in test_repos:  
                try:  
                    print(f"\n🔍 Testing with: {repo_url}")  
                      
                    result = agent(  
                        pr_url=repo_url,  
                        review_focus="security"  
                    )  
                      
                    print(f"\n📊 Real MCP Results:")  
                    print(f"Review: {result.review_comment}")  
                    print(f"Status: {result.approval_status}")  
                    print(f"Tools Used: {result.mcp_tools_used}")  
                    print(f"Protocol Capabilities: {result.protocol_capabilities}")  
                    print(f"Protocol Info: {result.protocol_info}")  
                      
                    agent.cleanup()  
                    return result  
                      
                except Exception as e:  
                    print(f"⚠️ Failed with {repo_url}: {e}")  
                    continue  
              
            print("❌ All test repositories failed")  
            return None  
              
        except Exception as e:  
            print(f"❌ Attempt {attempt + 1} failed: {e}")  
            if attempt < max_retries - 1:  
                print("⏳ Waiting 5 seconds before retry...")  
                time.sleep(5)  
            continue  
      
    print("❌ All attempts failed")  
    return None  
  
def demo_mock_mcp():  
    """Demo using mock MCP server for comparison."""  
    print("\n" + "="*60)  
    print("DEMO: Mock MCP Server (Fallback)")  
    print("="*60)  
      
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
  
def main():  
    print("🚀 GitHub PR Review Demo with Real MCP")  
    print("=" * 60)  
      
    # Check prerequisites  
    issues, github_token = check_prerequisites()  
      
    if issues:  
        print("\n❌ Prerequisites not met:")  
        for issue in issues:  
            print(f"  - {issue}")  
        print("\nPlease fix these issues and try again.")  
        return  
      
    # Setup MCP server  
    if not setup_mcp_server():  
        print("❌ Cannot proceed without MCP server")  
        return  
      
    # Setup DSPy  
    lm = setup_dspy()  
      
    # Try real MCP first, fallback to mock  
    real_result = None  
    if github_token:  
        real_result = demo_real_mcp_with_retry(github_token)  
      
    if not real_result:  
        print("\n🔄 Falling back to mock MCP demo...")  
        mock_result = demo_mock_mcp()  
      
    # Summary  
    print("\n" + "="*60)  
    print("DEMO SUMMARY")  
    print("="*60)  
      
    if real_result:  
        print("✅ Real MCP demo completed successfully")  
        print("🎯 Key Benefits Demonstrated:")  
        print("  - Real GitHub API integration via MCP")  
        print("  - Protocol-level session management")  
        print("  - Dynamic tool discovery")  
        print("  - Standardized error handling")  
    else:  
        print("⚠️ Real MCP demo failed, mock demo completed")  
        print("💡 To enable real MCP:")  
        print("  1. Set GITHUB_TOKEN environment variable")  
        print("  2. Ensure stable internet connection")  
        print("  3. Verify GitHub API access")  
  
if __name__ == "__main__":  
    main()