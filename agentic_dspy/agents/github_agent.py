"""GitHub PR Review Agent using MCP protocol."""  
  
import dspy  
import os  
from typing import Optional  
from ..protocols.mcp.client import MCPClient, RealMCPClient  
  
class GitHubPRReviewAgent(dspy.Module):  
    """Agent that reviews GitHub PRs using MCP protocol."""  
      
    def __init__(self, mcp_server_url: str, use_real_mcp: bool = False, github_token: Optional[str] = None):  
        super().__init__()  
          
        if use_real_mcp:  
            # Real GitHub MCP server command  
            github_mcp_command = ["npx", "-y", "@modelcontextprotocol/server-github"]  
            if github_token:  
                os.environ['GITHUB_TOKEN'] = github_token  
            self.mcp_client = RealMCPClient(github_mcp_command)  
        else:  
            # Mock MCP client for demo  
            self.mcp_client = MCPClient(mcp_server_url)  
          
        # DSPy modules for reasoning  
        self.analyze_pr = dspy.ChainOfThought(  
            "pr_context: str, file_changes: str -> analysis: str, suggestions: list[str]"  
        )  
          
        self.generate_review = dspy.ChainOfThought(  
            "analysis: str, suggestions: list[str] -> review_comment: str, approval_status: str"  
        )  
      
    def forward(self, pr_url: str, review_focus: str = "code_quality"):  
        """Review a GitHub PR."""  
        print(f"\n🔍 Reviewing PR: {pr_url}")  
        print(f"📋 Focus: {review_focus}")  
        print("-" * 50)  
          
        # Use protocol layer to get PR context  
        pr_context = self.mcp_client(  
            context_request=f"Get PR details for {pr_url}",  
            tool_name="github_search"  
        )  
          
        # Get file changes through MCP  
        file_changes = self.mcp_client(  
            context_request=f"Get file changes for {pr_url}",  
            tool_name="file_reader"  
        )  
          
        # Analyze using DSPy reasoning  
        print("🧠 Analyzing PR content...")  
        analysis = self.analyze_pr(  
            pr_context=pr_context.context_data,  
            file_changes=file_changes.context_data  
        )  
          
        # Generate final review  
        print("📝 Generating review...")  
        review = self.generate_review(  
            analysis=analysis.analysis,  
            suggestions=analysis.suggestions  
        )  
          
        return dspy.Prediction(  
            review_comment=review.review_comment,  
            approval_status=review.approval_status,  
            protocol_capabilities=pr_context.capabilities,  
            mcp_tools_used=["github_search", "file_reader"],  
            protocol_info=pr_context.protocol_info  
        )  
      
    def cleanup(self):  
        """Clean up resources."""  
        if self.mcp_client:  
            self.mcp_client.disconnect()