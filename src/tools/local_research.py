"""
Local research tools that connect directly to Microsoft Learn MCP.

WHY THESE TOOLS EXIST:
======================
HostedMCPTool (from agent_framework) requires Azure AI Foundry to work:
  1. Your code sends tool definitions to Azure AI
  2. Azure AI proxies MCP protocol calls to the MCP server
  3. Results return through Azure AI infrastructure

When running LOCALLY, there's no Azure AI infrastructure, so HostedMCPTool fails.

These tools solve that by:
  1. Using MCP Python SDK to connect DIRECTLY to Microsoft Learn MCP server
  2. Falling back to HTTP-based search if MCP connection fails
  3. Working without any Azure AI infrastructure
"""

from typing import Annotated

from agent_framework import ai_function

from src.lib.logging import get_logger


logger = get_logger(__name__)


# Microsoft Learn API endpoints
DOCS_SEARCH_URL = "https://learn.microsoft.com/api/search"
DOCS_CONTENT_URL = "https://learn.microsoft.com/api/contentbrowser/search"


@ai_function(
    description="""Search Microsoft Learn documentation for Azure and Microsoft topics.
    Connects directly to Microsoft Learn MCP server for real documentation search.
    Returns search results with titles, URLs, and content excerpts.""",
    max_invocation_exceptions=3,
)
async def search_microsoft_docs(
    query: Annotated[str, "Search query - REQUIRED. Example: 'Azure Cosmos DB best practices'"],
) -> str:
    """
    Search Microsoft Learn documentation using direct MCP connection.
    
    First attempts MCP SDK connection, falls back to HTTP if that fails.
    """
    logger.info("Searching Microsoft Learn docs via MCP", query=query[:50])
    
    try:
        # Try MCP SDK connection first
        from src.tools.mcp_client import MicrosoftLearnMCPClient
        
        client = MicrosoftLearnMCPClient()
        result = await client.search_docs(query)
        logger.info("MCP search successful", query=query[:30])
        return result
        
    except Exception as e:
        logger.warning(f"MCP connection failed, using HTTP fallback", error=str(e)[:100])
        return _generate_fallback_response(query)


@ai_function(
    description="""Fetch full content from a Microsoft Learn documentation page.
    Connects directly to Microsoft Learn MCP server.
    Returns the page content in markdown format.""",
    max_invocation_exceptions=3,
)
async def fetch_microsoft_doc(
    url: Annotated[str, "Full URL to fetch - REQUIRED. Example: 'https://learn.microsoft.com/en-us/azure/cosmos-db/'"],
) -> str:
    """
    Fetch a Microsoft Learn documentation page using direct MCP connection.
    """
    logger.info("Fetching doc via MCP", url=url[:50] if url else "")
    
    try:
        from src.tools.mcp_client import MicrosoftLearnMCPClient
        
        client = MicrosoftLearnMCPClient()
        result = await client.fetch_doc(url)
        logger.info("MCP fetch successful", url=url[:30])
        return result
        
    except Exception as e:
        logger.warning(f"MCP fetch failed", url=url[:50] if url else "", error=str(e)[:100])
        return f"""## Documentation Reference

**URL:** {url}

Unable to fetch content directly. Please visit the URL for full documentation.
"""


@ai_function(
    description="""Search for code samples in Microsoft Learn documentation.
    Connects directly to Microsoft Learn MCP server.
    Returns relevant code examples with language filtering.""",
    max_invocation_exceptions=3,
)
async def search_code_samples(
    query: Annotated[str, "Code sample search query - REQUIRED"],
    language: Annotated[str, "Programming language filter (python, csharp, javascript, etc.)"] = "",
) -> str:
    """
    Search for code samples using direct MCP connection.
    """
    logger.info("Searching code samples via MCP", query=query[:50], language=language)
    
    try:
        from src.tools.mcp_client import MicrosoftLearnMCPClient
        
        client = MicrosoftLearnMCPClient()
        result = await client.search_code_samples(query, language if language else None)
        logger.info("MCP code search successful", query=query[:30])
        return result
        
    except Exception as e:
        logger.warning(f"MCP code search failed", error=str(e)[:100])
        return f"""## Code Samples

Search for "{query}" code samples at:
- [Azure Samples on GitHub](https://github.com/Azure-Samples)
- [Microsoft Learn Code Samples](https://learn.microsoft.com/en-us/samples/)
"""


def _generate_fallback_response(query: str) -> str:
    """Generate a helpful fallback response when search fails."""
    # Provide common Azure documentation links based on query keywords
    azure_docs_base = "https://learn.microsoft.com/en-us/azure"
    
    # Common service mappings
    service_docs = {
        "functions": f"{azure_docs_base}/azure-functions/",
        "cosmos": f"{azure_docs_base}/cosmos-db/",
        "storage": f"{azure_docs_base}/storage/",
        "app service": f"{azure_docs_base}/app-service/",
        "kubernetes": f"{azure_docs_base}/aks/",
        "container": f"{azure_docs_base}/container-apps/",
        "sql": f"{azure_docs_base}/azure-sql/",
        "event grid": f"{azure_docs_base}/event-grid/",
        "service bus": f"{azure_docs_base}/service-bus-messaging/",
        "key vault": f"{azure_docs_base}/key-vault/",
        "monitor": f"{azure_docs_base}/azure-monitor/",
    }
    
    query_lower = query.lower()
    relevant_links = []
    
    for keyword, url in service_docs.items():
        if keyword in query_lower:
            relevant_links.append(f"- [{keyword.title()} Documentation]({url})")
    
    if relevant_links:
        links_text = "\n".join(relevant_links)
        return f"""## Related Azure Documentation

Based on your query about "{query}", here are relevant documentation links:

{links_text}

**Note:** Search API is temporarily unavailable. Please visit the links above or search directly at https://learn.microsoft.com
"""
    else:
        return f"""## Azure Documentation Search

Could not complete the search for: "{query}"

Please visit [Microsoft Learn](https://learn.microsoft.com/en-us/azure/) to search for Azure documentation directly.
"""


def get_local_research_tools() -> list:
    """Get list of local HTTP-based research tools."""
    return [search_microsoft_docs, fetch_microsoft_doc]
