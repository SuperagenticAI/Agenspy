#!/usr/bin/env python3  
"""Comprehensive MCP demo showcasing Client, Server, and GitHub analysis."""  
  
import dspy  
import os  
import asyncio  
import threading  
import time  
import subprocess  
from typing import Optional  
from agentic_dspy import (  
    MCPClient,   
    RealMCPClient,   
    PythonMCPServer,   
    GitHubMCPServer,  
    MultiProtocolAgent  
)  
  
class RepositoryAnalysisAgent(dspy.Module):  
    """Advanced agent for comprehensive repository analysis."""  
      
    def __init__(self, mcp_client, github_token: Optional[str] = None):  
        super().__init__()  
        self.mcp_client = mcp_client  
        self.github_token = github_token  
          
        # Advanced DSPy modules for analysis  
        self.analyze_structure = dspy.ChainOfThought(  
            "repo_info: str, file_tree: str -> structure_analysis: str, architecture_insights: list[str]"  
        )  
          
        self.analyze_code_quality = dspy.ChainOfThought(  
            "file_contents: str, language: str -> quality_score: float, issues: list[str], recommendations: list[str]"  
        )  
          
        self.analyze_security = dspy.ChainOfThought(  
            "code_content: str, dependencies: str -> security_score: float, vulnerabilities: list[str], fixes: list[str]"  
        )  
          
        self.generate_report = dspy.ChainOfThought(  
            "structure: str, quality: str, security: str -> executive_summary: str, detailed_report: str, action_items: list[str]"  
        )  
      
    def forward(self, repo_url: str, analysis_depth: str = "comprehensive"):  
        """Perform comprehensive repository analysis."""  
        print(f"\n🔍 Analyzing repository: {repo_url}")  
        print(f"📊 Analysis depth: {analysis_depth}")  
        print("-" * 60)  
          
        # Extract repository information  
        repo_info = self.mcp_client(  
            context_request=f"Get detailed repository information for {repo_url}",  
            tool_name="get_repository",  
            tool_args={"url": repo_url}  
        )  
          
        # Get repository structure  
        file_tree = self.mcp_client(  
            context_request=f"Get file structure for {repo_url}",  
            tool_name="get_file_tree",  
            tool_args={"repo": repo_url, "depth": 3}  
        )  
          
        # Analyze main files  
        main_files = ["README.md", "package.json", "requirements.txt", "Dockerfile"]  
        file_analyses = {}  
          
        for file_path in main_files:  
            file_content = self.mcp_client(  
                context_request=f"Get {file_path} from {repo_url}",  
                tool_name="get_file_contents",  
                tool_args={"repo": repo_url, "path": file_path}  
            )  
            file_analyses[file_path] = file_content.tool_result  
          
        # Perform analyses  
        print("🏗️ Analyzing repository structure...")  
        structure_analysis = self.analyze_structure(  
            repo_info=repo_info.context_data,  
            file_tree=file_tree.tool_result  
        )  
          
        print("🔍 Analyzing code quality...")  
        quality_analysis = self.analyze_code_quality(  
            file_contents=str(file_analyses),  
            language="mixed"  
        )  
          
        print("🔒 Analyzing security...")  
        security_analysis = self.analyze_security(  
            code_content=str(file_analyses),  
            dependencies=file_analyses.get("package.json", "")  
        )  
          
        print("📝 Generating comprehensive report...")  
        final_report = self.generate_report(  
            structure=structure_analysis.structure_analysis,  
            quality=f"Quality Score: {quality_analysis.quality_score}",  
            security=f"Security Score: {security_analysis.security_score}"  
        )  
          
        return dspy.Prediction(  
            repo_url=repo_url,  
            structure_insights=structure_analysis.architecture_insights,  
            quality_score=quality_analysis.quality_score,  
            quality_issues=quality_analysis.issues,  
            quality_recommendations=quality_analysis.recommendations,  
            security_score=security_analysis.security_score,  
            vulnerabilities=security_analysis.vulnerabilities,  
            security_fixes=security_analysis.fixes,  
            executive_summary=final_report.executive_summary,  
            detailed_report=final_report.detailed_report,  
            action_items=final_report.action_items,  
            mcp_capabilities=repo_info.capabilities  
        )  
  
def setup_python_mcp_server():  
    """Setup and start Python MCP server."""  
    print("🐍 Setting up Python MCP Server...")  
      
    server = GitHubMCPServer(port=8082)  
      
    # Add custom analysis tools  
    async def analyze_repository_structure(repo_url: str):  
        """Analyze repository structure."""  
        return {  
            "structure": "well-organized",  
            "directories": ["src", "tests", "docs"],  
            "main_files": ["README.md", "setup.py"],  
            "architecture": "modular"  
        }  
      
    async def get_file_tree(repo: str, depth: int = 2):  
        """Get repository file tree."""  
        return {  
            "tree": [  
                "README.md",  
                "src/",  
                "  main.py",  
                "  utils/",  
                "    helpers.py",  
                "tests/",  
                "  test_main.py"  
            ],  
            "total_files": 25,  
            "depth": depth  
        }
    
    # Register the custom tools  
    server.register_tool(  
        "analyze_repository_structure",  
        "Analyze repository structure and architecture",  
        {"repo_url": "string"},  
        analyze_repository_structure  
    )  
      
    server.register_tool(  
        "get_file_tree",  
        "Get repository file tree structure",  
        {"repo": "string", "depth": "integer"},  
        get_file_tree  
    )  
      
    # Start server in background thread  
    def start_server():  
        server.start()  
      
    server_thread = threading.Thread(target=start_server, daemon=True)  
    server_thread.start()  
      
    print("✅ Python MCP server started on port 8082")  
    return server  
  
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
                    structure_analysis="Repository follows standard Python package structure with clear separation of concerns.",  
                    architecture_insights=["Modular design", "Clear API boundaries", "Good test coverage"],  
                    quality_score=8.5,  
                    issues=["Missing type hints in some modules", "Could use more documentation"],  
                    recommendations=["Add comprehensive type annotations", "Expand API documentation", "Consider adding integration tests"],  
                    security_score=9.0,  
                    vulnerabilities=["No critical vulnerabilities found"],  
                    fixes=["Update dependencies to latest versions", "Add security scanning to CI/CD"],  
                    executive_summary="Well-structured repository with good security practices and room for documentation improvements.",  
                    detailed_report="The repository demonstrates solid engineering practices with modular architecture, comprehensive testing, and security-conscious development. Key areas for improvement include documentation and type safety.",  
                    action_items=["Implement type hints", "Expand documentation", "Add security scanning"]  
                )  
        lm = DummyLM()  
      
    dspy.configure(lm=lm)  
    return lm  
  
def demo_python_mcp_server():  
    """Demo Python MCP server capabilities."""  
    print("\n" + "="*60)  
    print("DEMO 1: Python MCP Server")  
    print("="*60)  
      
    # Setup and start Python MCP server  
    server = setup_python_mcp_server()  
    time.sleep(2)  # Give server time to start  
      
    # Create client to connect to Python server  
    python_mcp_client = MCPClient("mcp://localhost:8082")  
      
    # Test the Python MCP server  
    result = python_mcp_client(  
        context_request="Analyze repository structure",  
        tool_name="analyze_repository_structure",  
        tool_args={"repo_url": "https://github.com/example/python-project"}  
    )  
      
    print(f"📊 Python MCP Server Results:")  
    print(f"Context: {result.context_data}")  
    print(f"Tool Result: {result.tool_result}")  
    print(f"Capabilities: {result.capabilities}")  
      
    return python_mcp_client  
  
def demo_comprehensive_analysis():  
    """Demo comprehensive repository analysis."""  
    print("\n" + "="*60)  
    print("DEMO 2: Comprehensive Repository Analysis")  
    print("="*60)  
      
    # Create MCP client for analysis  
    mcp_client = MCPClient("mcp://analysis-server:8080")  
      
    # Create repository analysis agent  
    github_token = os.environ.get('GITHUB_TOKEN')  
    agent = RepositoryAnalysisAgent(mcp_client, github_token)  
      
    # Analyze a repository  
    repo_url = "https://github.com/microsoft/vscode"  
    result = agent(repo_url=repo_url, analysis_depth="comprehensive")  
      
    print(f"\n📊 Comprehensive Analysis Results:")  
    print(f"Repository: {result.repo_url}")  
    print(f"Quality Score: {result.quality_score}/10")  
    print(f"Security Score: {result.security_score}/10")  
    print(f"\n📋 Executive Summary:")  
    print(result.executive_summary)  
    print(f"\n🏗️ Architecture Insights:")  
    for insight in result.structure_insights:  
        print(f"  - {insight}")  
    print(f"\n⚠️ Quality Issues:")  
    for issue in result.quality_issues:  
        print(f"  - {issue}")  
    print(f"\n💡 Recommendations:")  
    for rec in result.quality_recommendations:  
        print(f"  - {rec}")  
    print(f"\n🔒 Security Vulnerabilities:")  
    for vuln in result.vulnerabilities:  
        print(f"  - {vuln}")  
    print(f"\n✅ Action Items:")  
    for item in result.action_items:  
        print(f"  - {item}")  
      
    return result  
  
def demo_multi_protocol_integration():  
    """Demo multi-protocol agent with MCP and other protocols."""  
    print("\n" + "="*60)  
    print("DEMO 3: Multi-Protocol Integration")  
    print("="*60)  
      
    # Create multi-protocol agent  
    multi_agent = MultiProtocolAgent("comprehensive-analyzer")  
      
    # Add MCP protocol  
    mcp_client = MCPClient("mcp://github-server:8080")  
    multi_agent.add_protocol(mcp_client)  
      
    # Add Agent2Agent protocol (if available)  
    try:  
        from agentic_dspy import Agent2AgentClient  
        a2a_client = Agent2AgentClient("tcp://localhost:9090", "analyzer-agent")  
        multi_agent.add_protocol(a2a_client)  
        print("✅ Added Agent2Agent protocol")  
    except ImportError:  
        print("⚠️ Agent2Agent protocol not available")  
      
    # Test multi-protocol analysis  
    result = multi_agent(  
        "Perform comprehensive security analysis of the repository",  
        use_all_protocols=False  # Use best protocol routing  
    )  
      
    print(f"📊 Multi-Protocol Results:")  
    print(f"Final Answer: {result.final_answer}")  
    print(f"Protocol Used: {result.protocol_used}")  
    print(f"Routing Reasoning: {result.routing_reasoning}")  
      
    # Test using all protocols  
    all_protocols_result = multi_agent(  
        "Get comprehensive analysis from all available sources",  
        use_all_protocols=True  
    )  
      
    print(f"\n📊 All Protocols Results:")  
    print(f"Final Answer: {all_protocols_result.final_answer}")  
    print(f"Confidence: {all_protocols_result.confidence}")  
    print(f"Protocols Used: {all_protocols_result.protocols_used}")  
      
    multi_agent.cleanup()  
    return result  
  
def demo_real_github_integration():  
    """Demo real GitHub integration with MCP."""  
    print("\n" + "="*60)  
    print("DEMO 4: Real GitHub Integration")  
    print("="*60)  
      
    github_token = os.environ.get('GITHUB_TOKEN')  
    if not github_token:  
        print("⚠️ No GITHUB_TOKEN found. Skipping real GitHub demo.")  
        return None  
      
    try:  
        # Create real MCP client with GitHub server  
        real_mcp_client = RealMCPClient(["npx", "-y", "@modelcontextprotocol/server-github"])  
          
        # Test real GitHub operations  
        repo_result = real_mcp_client(  
            context_request="Get repository information",  
            tool_name="get_repository",  
            tool_args={"owner": "microsoft", "repo": "vscode"}  
        )  
          
        issues_result = real_mcp_client(  
            context_request="List repository issues",  
            tool_name="list_issues",  
            tool_args={"owner": "microsoft", "repo": "vscode", "state": "open", "limit": 5}  
        )  
          
        print(f"📊 Real GitHub Results:")  
        print(f"Repository Info: {repo_result.tool_result}")  
        print(f"Issues: {issues_result.tool_result}")  
        print(f"Capabilities: {repo_result.capabilities}")  
          
        real_mcp_client.disconnect()  
        return repo_result  
          
    except Exception as e:  
        print(f"❌ Real GitHub demo failed: {e}")  
        return None  
  
def main():  
    print("🚀 Comprehensive MCP Demo with Agentic-DSPy")  
    print("=" * 70)  
      
    # Setup DSPy  
    lm = setup_dspy()  
      
    try:  
        # Demo 1: Python MCP Server  
        python_client = demo_python_mcp_server()  
          
        # Demo 2: Comprehensive Analysis  
        analysis_result = demo_comprehensive_analysis()  
          
        # Demo 3: Multi-Protocol Integration  
        multi_result = demo_multi_protocol_integration()  
          
        # Demo 4: Real GitHub Integration  
        github_result = demo_real_github_integration()  
          
        # Summary  
        print("\n" + "="*70)  
        print("COMPREHENSIVE DEMO SUMMARY")  
        print("="*70)  
          
        print("✅ Python MCP Server demo completed")  
        print("✅ Comprehensive repository analysis completed")  
        print("✅ Multi-protocol integration demonstrated")  
          
        if github_result:  
            print("✅ Real GitHub integration successful")  
        else:  
            print("⚠️ Real GitHub integration skipped")  
          
        print("\n🎯 Key Capabilities Demonstrated:")  
        print("1. 🐍 Python-based MCP server implementation")  
        print("2. 🔍 Comprehensive repository analysis")  
        print("3. 🤖 Multi-protocol agent routing")  
        print("4. 🔗 Real GitHub API integration")  
        print("5. 📊 Advanced DSPy reasoning chains")  
        print("6. 🛡️ Security and quality analysis")  
          
        print("\n📈 Protocol Layer Benefits:")  
        print("- Automatic connection management")  
        print("- Dynamic capability discovery")  
        print("- Standardized error handling")  
        print("- Protocol-agnostic agent design")  
        print("- Seamless DSPy optimization integration")  
          
    except KeyboardInterrupt:  
        print("\n🛑 Demo interrupted by user")  
    except Exception as e:  
        print(f"\n❌ Demo failed with error: {e}")  
    finally:  
        # Cleanup  
        print("\n🧹 Cleaning up resources...")  
        try:  
            if 'python_client' in locals():  
                python_client.disconnect()  
        except:  
            pass  
  
if __name__ == "__main__":  
    main()