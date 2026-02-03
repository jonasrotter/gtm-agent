"""
Researcher Agent for Azure documentation research.

Uses MCP tools to connect to Microsoft Learn MCP endpoint
for searching and retrieving Azure documentation.

- Local: MCPStreamableHTTPTool (direct HTTP connection)
- Azure: HostedMCPTool (Azure AI hosted execution)
"""

from agent_framework import ChatAgent, HostedMCPTool, MCPStreamableHTTPTool

from src.agents.base import create_azure_chat_client, MICROSOFT_LEARN_MCP_URL, is_azure_deployment
from src.utils.logging import get_logger


logger = get_logger(__name__)


RESEARCHER_INSTRUCTIONS = """You are an expert Azure documentation researcher.

Use the Microsoft Learn MCP tool to search and fetch Azure documentation.
Always cite your sources with URLs.

## Available MCP Tools

- **microsoft_docs_search**: Search documentation for topics
- **microsoft_docs_fetch**: Fetch full page content from a URL
- **microsoft_code_sample_search**: Find code examples by query

## Guidelines

1. **Search First**: Use search to find relevant documentation
2. **Fetch Details**: Use fetch to get full content when needed
3. **Find Code**: Use code sample search for implementation examples
4. **Cite Sources**: Always include source URLs in your response
5. **Feature Status**: Note whether features are GA, Preview, or Deprecated
6. **Be Comprehensive**: Include specific technical terms (e.g., for storage: Hot/Cool/Cold/Archive tiers; for monitoring: connection string, telemetry; for deployment: workflow, yaml)

## Response Format

- Start with a direct answer to the question
- Include relevant details and context
- Add code samples if applicable
- End with source citations (URLs)

## Scope

You handle RESEARCH queries about Azure services and technologies.
For architecture reviews, route to the architect agent.
For code generation, route to the coding agent.
"""


class ResearcherAgent:
    """
    Researcher agent with Microsoft Learn MCP integration.
    
    Uses environment detection to select the appropriate MCP tool:
    - Local: MCPStreamableHTTPTool (direct HTTP to Microsoft Learn)
    - Azure: HostedMCPTool (Azure AI hosted execution)
    """
    
    def __init__(self):
        """Initialize ResearcherAgent with environment-appropriate MCP tool."""
        if is_azure_deployment():
            # Azure deployment: use HostedMCPTool (Azure AI handles MCP execution)
            self.mcp_tool = HostedMCPTool(
                name="microsoft_learn",
                url=MICROSOFT_LEARN_MCP_URL,
                description="Search and fetch Azure documentation from Microsoft Learn",
                approval_mode="never_require",
            )
            logger.info("ResearcherAgent using HostedMCPTool (Azure deployment)", mcp_url=MICROSOFT_LEARN_MCP_URL)
        else:
            # Local development: use MCPStreamableHTTPTool (direct HTTP connection)
            self.mcp_tool = MCPStreamableHTTPTool(
                name="microsoft_learn",
                url=MICROSOFT_LEARN_MCP_URL,
            )
            logger.info("ResearcherAgent using MCPStreamableHTTPTool (local)", mcp_url=MICROSOFT_LEARN_MCP_URL)
        
        self.agent = ChatAgent(
            chat_client=create_azure_chat_client(),
            name="researcher",
            instructions=RESEARCHER_INSTRUCTIONS,
            tools=self.mcp_tool,
        )
        
        logger.info("ResearcherAgent initialized")
    
    async def run(self, query: str) -> str:
        """
        Process a research query.
        
        Args:
            query: User's research question about Azure.
            
        Returns:
            Researched answer with source citations.
        """
        # MCPStreamableHTTPTool requires async context to establish connection
        # HostedMCPTool doesn't need this (Azure AI handles it)
        if isinstance(self.mcp_tool, MCPStreamableHTTPTool):
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
        
        Used by SolutionEngineerAgent to delegate research queries.
        """
        return self.agent.as_tool(
            name="research",
            description="Research Azure documentation and answer questions with source citations",
        )


# =============================================================================
# Factory Function
# =============================================================================

def get_researcher_agent() -> ResearcherAgent:
    """Get a ResearcherAgent instance."""
    return ResearcherAgent()
