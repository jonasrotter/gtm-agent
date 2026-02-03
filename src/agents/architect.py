"""Architect Agent for Azure architecture best practices.

Uses MCP tools to connect to Azure MCP endpoint
for Well-Architected Framework guidance and best practices.

- Local: MCPStdioTool with environment inheritance (for Azure CLI auth)
- Azure: HostedMCPTool (Azure AI hosted execution)
"""

import os

from agent_framework import ChatAgent, HostedMCPTool, MCPStdioTool

from src.agents.base import create_azure_chat_client, is_azure_deployment
from src.utils.logging import get_logger


logger = get_logger(__name__)


ARCHITECT_INSTRUCTIONS = """You are an Azure Solutions Architect expert.

Use the Azure MCP tool to get best practices aligned with the Well-Architected Framework.

## Well-Architected Framework Pillars

Focus on the five WAF pillars when providing guidance:
1. **Reliability**: Ensure workloads meet availability commitments
2. **Security**: Protect applications and data from threats
3. **Cost Optimization**: Manage costs while maximizing value
4. **Operational Excellence**: Operations processes that keep systems running
5. **Performance Efficiency**: Adapt to changes in demand efficiently

## Guidelines

1. **Reference WAF Pillars**: Map recommendations to specific pillars
2. **Provide Specific Services**: Recommend concrete Azure services
3. **Include Patterns**: Reference relevant architecture patterns
4. **Identify Anti-patterns**: Highlight practices to avoid
5. **Cite Sources**: Include links to Azure Architecture Center
6. **Use Specific Terms**: Include technical terms like authentication, HTTPS, identity, availability, redundancy, regions, cost, optimization, spot, reserved, savings, autoscaler, reliability, resilience, recovery

## Response Format

- Start with the architectural recommendation
- Map to relevant WAF pillar(s)
- Include specific Azure service recommendations
- Note any anti-patterns to avoid
- End with source references

## Scope

You handle ARCHITECTURE queries about Azure solutions.
For documentation research, route to the researcher agent.
For code generation, route to the coding agent.
"""


class ArchitectAgent:
    """
    Architect agent with Azure MCP integration.
    
    Uses environment detection to select the appropriate MCP tool:
    - Local: MCPStreamableHTTPTool (direct HTTP to Azure MCP)
    - Azure: HostedMCPTool (Azure AI hosted execution)
    """
    
    def __init__(self):
        """Initialize ArchitectAgent with environment-appropriate MCP tool."""
        if is_azure_deployment():
            # Azure deployment: use HostedMCPTool (Azure AI handles MCP execution)
            self.mcp_tool = HostedMCPTool(
                name="azure_mcp",
                url="https://api.mcp.github.com/azure",
                description="Get Azure architecture best practices and WAF guidance",
                approval_mode="never_require",
            )
            logger.info("ArchitectAgent using HostedMCPTool (Azure deployment)")
        else:
            # Local development: use MCPStdioTool to run Azure MCP Server locally
            # The Azure MCP Server uses DefaultAzureCredential for auth
            # Pass service principal credentials so EnvironmentCredential is used (not Azure CLI)
            # Note: Azure MCP doesn't support prompts/list, so we disable prompt loading
            mcp_env = {
                # Required for subprocess execution
                "PATH": os.environ.get("PATH", ""),
                "USERPROFILE": os.environ.get("USERPROFILE", ""),
                "HOME": os.environ.get("HOME", os.environ.get("USERPROFILE", "")),
                "TEMP": os.environ.get("TEMP", ""),
                "TMP": os.environ.get("TMP", ""),
                # Service principal credentials for DefaultAzureCredential
                "AZURE_CLIENT_ID": os.environ.get("AZURE_CLIENT_ID", ""),
                "AZURE_TENANT_ID": os.environ.get("AZURE_TENANT_ID", ""),
                "AZURE_CLIENT_SECRET": os.environ.get("AZURE_CLIENT_SECRET", ""),
                # Azure subscription context
                "AZURE_SUBSCRIPTION_ID": os.environ.get("AZURE_SUBSCRIPTION_ID", ""),
            }
            # Only include non-empty values
            mcp_env = {k: v for k, v in mcp_env.items() if v}
            
            self.mcp_tool = MCPStdioTool(
                name="azure_mcp",
                command="npx",
                args=["-y", "@azure/mcp@latest", "server", "start"],
                env=mcp_env,
                load_prompts=False,  # Azure MCP doesn't support prompts/list
            )
            logger.info(
                "ArchitectAgent using MCPStdioTool (local Azure MCP)",
                has_service_principal=bool(os.environ.get("AZURE_CLIENT_ID")),
            )
        
        self.agent = ChatAgent(
            chat_client=create_azure_chat_client(),
            name="architect",
            instructions=ARCHITECT_INSTRUCTIONS,
            tools=self.mcp_tool,
        )
        
        logger.info("ArchitectAgent initialized")
    
    async def run(self, query: str) -> str:
        """
        Process an architecture query.
        
        Args:
            query: User's architecture question about Azure.
            
        Returns:
            Architecture guidance with WAF pillar mappings.
        """
        # MCPStdioTool requires async context to manage the subprocess
        # HostedMCPTool doesn't need this (Azure AI handles it)
        if isinstance(self.mcp_tool, MCPStdioTool):
            async with self.mcp_tool:
                async with self.agent:
                    result = await self.agent.run(query)
                    return result.text
        else:
            async with self.agent:
                result = await self.agent.run(query)
                return result.text
    
    def as_tool(self):
        """
        Return agent as a tool for orchestration.
        
        Used by SolutionEngineerAgent to delegate architecture queries.
        """
        return self.agent.as_tool(
            name="architecture",
            description="Provide Azure architecture guidance and WAF-aligned recommendations",
        )


# =============================================================================
# Factory Function
# =============================================================================

def get_architect_agent() -> ArchitectAgent:
    """Get an ArchitectAgent instance."""
    return ArchitectAgent()
