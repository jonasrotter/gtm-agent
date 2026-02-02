"""
Base agent configuration for agent_framework ChatAgent.

Simplified base module providing:
- Azure OpenAI chat client factory
- MCP endpoint constants
- Common imports for agents

This replaces the previous complex BaseAgentWrapper with direct ChatAgent usage.
"""

import os

from agent_framework import ChatAgent, HostedMCPTool, MCPStreamableHTTPTool, ai_function
from azure.identity import DefaultAzureCredential

from src.utils.agent_client import AzureOpenAIChatClient
from src.utils.logging import get_logger


logger = get_logger(__name__)


# =============================================================================
# Environment Detection
# =============================================================================

def is_azure_deployment() -> bool:
    """
    Detect if running in Azure deployment environment.
    
    Checks for Azure-specific environment variables that indicate
    the app is running in Azure App Service, Container Apps, or Functions.
    
    Returns:
        True if running in Azure, False if running locally.
    """
    # Explicit override via environment variable
    explicit = os.environ.get("AZURE_DEPLOYMENT", "").lower()
    if explicit == "true":
        return True
    if explicit == "false":
        return False
    
    # Auto-detect Azure App Service
    if os.environ.get("WEBSITE_INSTANCE_ID"):
        return True
    
    # Auto-detect Azure Container Apps
    if os.environ.get("CONTAINER_APP_NAME"):
        return True
    
    # Auto-detect Azure Functions
    if os.environ.get("FUNCTIONS_WORKER_RUNTIME"):
        return True
    
    return False


# =============================================================================
# MCP Endpoints
# =============================================================================

MICROSOFT_LEARN_MCP_URL = "https://learn.microsoft.com/api/mcp"
"""Microsoft Learn documentation MCP endpoint (HTTP Streamable)."""

AZURE_MCP_URL = "https://api.mcp.github.com"
"""Azure best practices MCP endpoint (HTTP Gallery)."""


# =============================================================================
# Azure OpenAI Client Factory
# =============================================================================

def create_azure_chat_client() -> AzureOpenAIChatClient:
    """
    Create Azure OpenAI chat client from environment variables.
    
    Required environment variables:
    - AZURE_OPENAI_ENDPOINT: Azure OpenAI endpoint URL
    - AZURE_OPENAI_DEPLOYMENT (or AZURE_OPENAI_CHAT_DEPLOYMENT_NAME): Model deployment name
    
    Returns:
        Configured AzureOpenAIChatClient instance.
    
    Raises:
        ValueError: If required environment variables are missing.
    """
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT") or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    
    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
    if not deployment:
        raise ValueError("AZURE_OPENAI_DEPLOYMENT or AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable is required")
    
    logger.info(
        "Creating Azure OpenAI chat client",
        endpoint=endpoint[:50] + "..." if len(endpoint) > 50 else endpoint,
        deployment=deployment,
    )
    
    return AzureOpenAIChatClient(
        endpoint=endpoint,
        deployment=deployment,
    )


# =============================================================================
# Re-exports for convenience
# =============================================================================

__all__ = [
    # MCP endpoints
    "MICROSOFT_LEARN_MCP_URL",
    "AZURE_MCP_URL",
    # Environment detection
    "is_azure_deployment",
    # Factory
    "create_azure_chat_client",
    # Re-exports from agent_framework
    "ChatAgent",
    "HostedMCPTool",
    "MCPStreamableHTTPTool",
    "ai_function",
    # Azure
    "AzureOpenAIChatClient",
    "DefaultAzureCredential",
    # Logging
    "logger",
]
