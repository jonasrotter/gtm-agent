"""
MCP Server implementation for Solution Engineer Agent.

Exposes the agent's capabilities (research, architecture, code) as MCP tools
using the FastMCP SDK with stateless HTTP transport.

Usage:
    The MCP server is mounted at /mcp in the FastAPI app.
    Full endpoint URL: https://<your-domain>/mcp/mcp
"""

import contextlib
from contextlib import asynccontextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.agents.solution_engineer import SolutionEngineerAgent
from src.lib.logging import get_logger


logger = get_logger(__name__)


# Create FastMCP server with stateless HTTP mode for simple mounting
# Default streamable HTTP endpoint is /mcp, so full path becomes /mcp/mcp
mcp = FastMCP(
    "SolutionEngineerMCP",
    stateless_http=True,
)


# Global agent instance (lazily initialized)
_agent: SolutionEngineerAgent | None = None


def _get_agent() -> SolutionEngineerAgent:
    """Get or create the SolutionEngineerAgent instance."""
    global _agent
    if _agent is None:
        _agent = SolutionEngineerAgent()
        logger.info("MCP: Initialized SolutionEngineerAgent")
    return _agent


@asynccontextmanager
async def mcp_lifespan(app: Any):
    """
    Lifespan context manager to start/stop the MCP session manager with the FastAPI app.
    
    This should be combined with any existing FastAPI lifespan logic.
    
    Args:
        app: The FastAPI application instance.
        
    Yields:
        None - allows the app to run.
    """
    logger.info("MCP: Starting MCP session manager")
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        try:
            yield
        finally:
            # Cleanup agent on shutdown
            global _agent
            if _agent is not None:
                await _agent.close()
                _agent = None
                logger.info("MCP: Cleaned up SolutionEngineerAgent")


# =============================================================================
# MCP Tools - Expose agent capabilities
# =============================================================================


@mcp.tool()
async def research(query: str, session_id: str | None = None) -> dict:
    """
    Search Azure documentation and answer questions with source citations.
    
    Use this tool for questions about Azure services, features, concepts,
    pricing, limits, documentation lookups, or "what is" / "how to" questions.
    
    Args:
        query: The user's question about Azure documentation or concepts.
        session_id: Optional session ID for multi-turn conversation continuity.
            If provided and a session exists, the conversation history is preserved.
            If not provided, a new session is created.
    
    Returns:
        dict containing:
            - content: The answer with source citations
            - session_id: Session ID for follow-up questions
            - turn_count: The current turn number in the conversation
    """
    agent = _get_agent()
    
    # Use the researcher sub-agent directly for focused responses
    # Note: run() returns a string (the text response)
    content = await agent.researcher.run(query)
    
    logger.debug("MCP research tool invoked", query=query[:100])
    
    return {
        "content": content,
        "tool_used": "research",
        "session_id": session_id,
    }


@mcp.tool()
async def architecture(query: str, session_id: str | None = None) -> dict:
    """
    Provide Azure architecture guidance and Well-Architected Framework (WAF) recommendations.
    
    Use this tool for questions about:
    - Architecture design patterns and best practices
    - Azure Well-Architected Framework pillars (reliability, security, cost, operations, performance)
    - Solution design reviews and recommendations
    - Cloud architecture decisions
    
    Args:
        query: The user's architecture question or design request.
        session_id: Optional session ID for multi-turn conversation continuity.
            If provided and a session exists, the conversation history is preserved.
            If not provided, a new session is created.
    
    Returns:
        dict containing:
            - content: Architecture guidance with WAF alignment
            - session_id: Session ID for follow-up questions
            - turn_count: The current turn number in the conversation
    """
    agent = _get_agent()
    
    # Use the architect sub-agent directly for focused responses
    # Note: run() returns a string (the text response)
    content = await agent.architect.run(query)
    
    logger.debug("MCP architecture tool invoked", query=query[:100])
    
    return {
        "content": content,
        "tool_used": "architecture",
        "session_id": session_id,
    }


@mcp.tool()
async def code(query: str, session_id: str | None = None) -> dict:
    """
    Generate code, Azure CLI commands, scripts, Bicep/ARM templates, and test plans.
    
    Use this tool for requests to:
    - Generate Azure CLI or PowerShell commands
    - Create code snippets (Python, C#, JavaScript, etc.)
    - Write Bicep or ARM templates
    - Create deployment scripts
    - Generate test plans for Azure deployments
    
    Args:
        query: The user's code generation request.
        session_id: Optional session ID for multi-turn conversation continuity.
            If provided and a session exists, the conversation history is preserved.
            If not provided, a new session is created.
    
    Returns:
        dict containing:
            - content: Generated code or commands
            - session_id: Session ID for follow-up questions
            - turn_count: The current turn number in the conversation
    """
    agent = _get_agent()
    
    # Use the GHCP coding agent directly for focused responses
    # Note: run() returns a string (the text response)
    content = await agent.ghcp_coding.run(query)
    
    logger.debug("MCP code tool invoked", query=query[:100])
    
    return {
        "content": content,
        "tool_used": "code",
        "session_id": session_id,
    }


@mcp.tool()
async def ask_solution_engineer(query: str, session_id: str | None = None) -> dict:
    """
    Ask the Solution Engineer agent to help with any Azure-related question.
    
    This is the main entry point that intelligently routes your question to the
    most appropriate specialized tool (research, architecture, or code).
    
    Use this when you're not sure which specific tool to use, or when your
    question might span multiple domains.
    
    Args:
        query: Any Azure-related question or request.
        session_id: Optional session ID for multi-turn conversation continuity.
            Provide the session_id from a previous response to continue the conversation.
            If not provided, a new session is created.
    
    Returns:
        dict containing:
            - content: The agent's response
            - agent_used: Which sub-agent handled the request (researcher, architect, or ghcp_coding)
            - session_id: Session ID for follow-up questions
            - turn_count: The current turn number in the conversation
    """
    agent = _get_agent()
    
    # Use the orchestrator to route to the best sub-agent
    result = await agent.run(query, session_id=session_id)
    
    logger.debug(
        "MCP ask_solution_engineer tool invoked",
        query=query[:100],
        agent_used=result.agent_used,
    )
    
    return {
        "content": result.content,
        "agent_used": result.agent_used,
        "session_id": result.session_id,
        "turn_count": result.turn_count,
    }
