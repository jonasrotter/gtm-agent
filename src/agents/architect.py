"""
Architect Agent for Azure architecture best practices.

Uses HostedMCPTool to connect directly to Azure MCP endpoint
for Well-Architected Framework guidance and best practices.
"""

from agent_framework import ChatAgent, HostedMCPTool

from src.agents.base import create_azure_chat_client, AZURE_MCP_URL
from src.lib.logging import get_logger


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
    
    Uses HostedMCPTool to connect directly to the Azure MCP endpoint
    for architecture best practices and WAF guidance.
    """
    
    def __init__(self):
        """Initialize ArchitectAgent with HostedMCPTool."""
        self.mcp_tool = HostedMCPTool(
            name="azure_best_practices",
            url=AZURE_MCP_URL,
            description="Get Azure architecture best practices and WAF guidance",
            approval_mode="never_require",  # Auto-approve best practice queries
        )
        
        self.agent = ChatAgent(
            chat_client=create_azure_chat_client(),
            name="architect",
            instructions=ARCHITECT_INSTRUCTIONS,
            tools=self.mcp_tool,
        )
        
        logger.info(
            "ArchitectAgent initialized",
            mcp_url=AZURE_MCP_URL,
        )
    
    async def run(self, query: str) -> str:
        """
        Process an architecture query.
        
        Args:
            query: User's architecture question about Azure.
            
        Returns:
            Architecture guidance with WAF pillar mappings.
        """
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
