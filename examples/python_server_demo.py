#!/usr/bin/env python3
"""Python MCP server demonstration."""

import asyncio
import threading
import time
from agenspy.servers import GitHubMCPServer

def start_server():
    """Start the Python MCP server."""
    server = GitHubMCPServer(port=8081)

    # Add custom tools
    async def custom_analysis(code: str, language: str = "python"):
        """Custom code analysis tool."""
        return f"Analysis of {language} code: {len(code)} characters, looks good!"

    server.register_tool(
        "custom_analysis",
        "Analyze code quality",
        {"code": "string", "language": "string"},
        custom_analysis
    )

    print("🚀 Starting Python MCP server on port 8081...")
    server.start()

def main():
    print("🐍 Python MCP Server Demo")
    print("=" * 30)

    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Give server time to start
    time.sleep(2)

    print("✅ Python MCP server is running!")
    print("🔗 Connect to: ws://localhost:8081/mcp")
    print("📋 Available tools: search_repositories, get_repository, get_file_contents, list_issues, custom_analysis")

    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")

if __name__ == "__main__":
    main()
