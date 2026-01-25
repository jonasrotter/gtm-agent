"""
MCP (Model Context Protocol) Server module.

Exposes the Solution Engineer Agent as an MCP server for integration with:
- Microsoft 365 Copilot Chat
- GitHub Copilot Chat (Agent mode)
- Copilot Studio
- Any MCP-compatible client
"""

from src.mcp.mcp_server import mcp, mcp_lifespan

__all__ = ["mcp", "mcp_lifespan"]
