"""
GHCP Coding Agent using GitHub Copilot SDK for code generation and hypothesis validation.

This agent uses the github-copilot-sdk to leverage Copilot's agentic runtime
with built-in MCP server support for intelligent code and CLI generation.

Supports two deployment modes:
1. Local Development: Auto-spawns Copilot CLI (requires GitHub Copilot subscription)
2. Azure Production: BYOK with Azure OpenAI (no GitHub auth required)
"""

import asyncio
from typing import Annotated

from pydantic import BaseModel, Field

from src.agents.base import AZURE_MCP_URL, MICROSOFT_LEARN_MCP_URL
from src.config import get_settings
from src.utils.logging import get_logger

# GitHub Copilot SDK imports
try:
    from copilot import CopilotClient, CopilotSession, define_tool, MCPRemoteServerConfig
    COPILOT_SDK_AVAILABLE = True
except ImportError:
    COPILOT_SDK_AVAILABLE = False
    CopilotClient = None
    CopilotSession = None
    define_tool = lambda **kwargs: lambda f: f  # no-op decorator
    MCPRemoteServerConfig = None

# For as_tool() compatibility with agent_framework
from agent_framework import ai_function


logger = get_logger(__name__)


# =============================================================================
# Agent Instructions
# =============================================================================

GHCP_CODING_INSTRUCTIONS = """You are an Azure Hypothesis Validator and Code Generation Expert.

You help validate technical hypotheses about Azure services by:
1. Creating test plans with Azure resources
2. Generating Azure CLI commands for deployment
3. Executing commands (with user approval)
4. Collecting metrics and generating verdicts

## Key Rules

- **NEVER** deploy resources without explicit user approval
- Always estimate costs before proposing deployments
- Clean up ALL resources after testing
- Log all Azure CLI commands for audit purposes
- Provide clear metrics-based verdicts

## Response Format

For test plans:
- State the hypothesis being tested
- List all resources that will be deployed
- Explain the methodology
- Provide cost estimates
- Request explicit approval

For results:
- State the verdict clearly (CONFIRMED, REFUTED, PARTIAL, INCONCLUSIVE)
- Support with collected metrics
- Include confidence level
- Confirm resource cleanup"""


# =============================================================================
# Custom Tools (defined with @define_tool decorator)
# =============================================================================

class CreateTestPlanParams(BaseModel):
    """Parameters for creating a test plan."""
    hypothesis: str = Field(description="The hypothesis to validate (e.g., 'Azure Functions can handle 1000 concurrent requests')")
    max_cost_usd: float = Field(default=50.0, description="Maximum allowed cost for the test in USD")
    max_duration_minutes: int = Field(default=30, description="Maximum duration for the test in minutes")


@define_tool(description="Create a test plan for validating an Azure hypothesis")
async def create_test_plan(params: CreateTestPlanParams) -> str:
    """Create a test plan for validating a hypothesis about Azure services."""
    import uuid
    plan_id = str(uuid.uuid4())[:8]
    
    return f"""## Test Plan Created

**Plan ID**: {plan_id}
**Hypothesis**: {params.hypothesis}

### Budget Constraints
- Maximum Cost: ${params.max_cost_usd:.2f} USD
- Maximum Duration: {params.max_duration_minutes} minutes

### Status
⚠️ **PENDING APPROVAL** - This plan requires explicit approval before execution.

### Next Steps
1. Review the hypothesis and constraints
2. Approve the plan to proceed with resource deployment
3. System will deploy resources, run tests, and clean up automatically

To approve, respond with: "Approved - execute plan {plan_id}" """


class GenerateCLIParams(BaseModel):
    """Parameters for generating Azure CLI commands."""
    resource_type: str = Field(description="Azure resource type (e.g., 'webapp', 'function', 'storage', 'cosmosdb')")
    resource_name: str = Field(description="Name for the resource")
    resource_group: str = Field(description="Resource group name")
    location: str = Field(default="eastus", description="Azure region (e.g., 'eastus', 'westus2', 'westeurope')")


@define_tool(description="Generate Azure CLI command for deploying a resource")
async def generate_cli_command(params: GenerateCLIParams) -> str:
    """Generate Azure CLI command for deploying an Azure resource."""
    templates = {
        "webapp": f"az webapp create --name {params.resource_name} --resource-group {params.resource_group} --location {params.location} --sku B1",
        "function": f"az functionapp create --name {params.resource_name} --resource-group {params.resource_group} --consumption-plan-location {params.location} --runtime python --runtime-version 3.11 --functions-version 4 --storage-account {params.resource_name}st",
        "storage": f"az storage account create --name {params.resource_name} --resource-group {params.resource_group} --location {params.location} --sku Standard_LRS",
        "cosmosdb": f"az cosmosdb create --name {params.resource_name} --resource-group {params.resource_group} --locations regionName={params.location} failoverPriority=0",
        "container-app": f"az containerapp create --name {params.resource_name} --resource-group {params.resource_group} --environment {params.resource_name}-env --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest",
        "aks": f"az aks create --name {params.resource_name} --resource-group {params.resource_group} --location {params.location} --node-count 1 --node-vm-size Standard_DS2_v2 --generate-ssh-keys",
    }
    
    command = templates.get(
        params.resource_type.lower(),
        f"az {params.resource_type} create --name {params.resource_name} --resource-group {params.resource_group} --location {params.location}"
    )
    
    return f"""## Azure CLI Command

```bash
# Create resource group (if needed)
az group create --name {params.resource_group} --location {params.location}

# Create {params.resource_type}
{command}
```

### Cleanup Command
```bash
az group delete --name {params.resource_group} --yes --no-wait
```

⚠️ **Note**: Review and approve before executing these commands."""


class ExecuteCommandParams(BaseModel):
    """Parameters for executing an approved CLI command."""
    command: str = Field(description="The Azure CLI command to execute")
    approval_confirmed: bool = Field(description="Whether the user has explicitly approved this command")


@define_tool(description="Execute an approved Azure CLI command (requires explicit approval)")
async def execute_cli_command(params: ExecuteCommandParams) -> str:
    """Execute an Azure CLI command after user approval."""
    if not params.approval_confirmed:
        return "❌ **Execution Blocked**: This command requires explicit user approval. Please confirm before proceeding."
    
    # In production, this would execute the command via subprocess
    # For now, return a placeholder showing the command would be executed
    return f"""✅ **Command Approved for Execution**

```bash
{params.command}
```

⏳ Execution would begin here in production mode.
📊 Metrics would be collected and reported upon completion."""


# =============================================================================
# GHCPCodingAgent Class
# =============================================================================

class GHCPCodingAgent:
    """
    GHCP Coding Agent using GitHub Copilot SDK for intelligent code and CLI generation.
    
    Features:
    - Copilot CLI runtime handles planning and tool invocation
    - MCP servers for Azure best practices (Azure MCP, Microsoft Learn MCP)
    - Custom tools via @define_tool decorator
    - Streaming responses
    
    Deployment Modes:
    1. Local Development (default):
       - Auto-spawns Copilot CLI process
       - Requires GitHub Copilot subscription
       - Set: COPILOT_USE_AZURE_OPENAI=false (default)
    
    2. Azure Production (BYOK):
       - Uses Azure OpenAI as LLM provider
       - No GitHub authentication required
       - Set: COPILOT_USE_AZURE_OPENAI=true
       - Requires: COPILOT_AZURE_OPENAI_ENDPOINT, COPILOT_AZURE_OPENAI_API_KEY
    
    3. External CLI Server:
       - Connects to pre-running Copilot CLI server
       - Set: COPILOT_CLI_URL=localhost:4321

    Prerequisites:
    - Copilot CLI must be installed: npm install -g @github/copilot
    - Install SDK: pip install github-copilot-sdk
    """
    
    def __init__(self):
        """Initialize GHCPCodingAgent with configuration from settings."""
        self._client: "CopilotClient | None" = None
        self._session: "CopilotSession | None" = None
        self._started = False
        
        # Load configuration
        self._settings = get_settings()
        
        if not COPILOT_SDK_AVAILABLE:
            logger.warning(
                "github-copilot-sdk not installed. "
                "Install with: pip install github-copilot-sdk"
            )
        
        # Log deployment mode
        if self._settings.copilot_use_azure_openai:
            logger.info(
                "GHCPCodingAgent configured for Azure OpenAI BYOK mode",
                endpoint=self._settings.copilot_azure_openai_endpoint[:50] + "..." 
                if self._settings.copilot_azure_openai_endpoint else "NOT SET",
            )
        elif self._settings.copilot_cli_url:
            logger.info(
                "GHCPCodingAgent configured for external CLI server",
                cli_url=self._settings.copilot_cli_url,
            )
        else:
            logger.info("GHCPCodingAgent configured for local CLI (auto-spawn)")

    async def start(self):
        """Start the Copilot client and create a session."""
        if not COPILOT_SDK_AVAILABLE:
            logger.error("github-copilot-sdk not available")
            raise RuntimeError(
                "github-copilot-sdk is not installed. "
                "Install with: pip install github-copilot-sdk"
            )
        
        if self._started:
            logger.debug("GHCPCodingAgent already started, skipping")
            return

        logger.info("GHCPCodingAgent starting Copilot client...")

        # Build client options based on configuration
        client_options = {}
        if self._settings.copilot_cli_url:
            client_options["cli_url"] = self._settings.copilot_cli_url
            logger.info(
                "Connecting to external CLI server",
                cli_url=self._settings.copilot_cli_url,
            )

        try:
            logger.debug("Creating CopilotClient", options=client_options or "default")
            self._client = CopilotClient(client_options) if client_options else CopilotClient()
            
            logger.debug("Starting CopilotClient...")
            await self._client.start()
            logger.info("CopilotClient started successfully")
            
        except FileNotFoundError as e:
            logger.error(
                "Copilot CLI not found",
                error=str(e),
            )
            raise RuntimeError(
                "Copilot CLI not found. Please install it with: npm install -g @github/copilot\n"
                f"Original error: {e}"
            ) from e
        except Exception as e:
            logger.error(
                "Failed to start CopilotClient",
                error=str(e),
                error_type=type(e).__name__,
            )
            if "WinError 2" in str(e) or "No such file" in str(e):
                raise RuntimeError(
                    "Copilot CLI not found. Please install it with: npm install -g @github/copilot\n"
                    f"Original error: {e}"
                ) from e
            raise

        # Build session configuration
        session_config = {
            "model": self._settings.copilot_model,
            "streaming": True,
            "tools": [create_test_plan, generate_cli_command, execute_cli_command],
            "mcp_servers": {
                # Azure MCP for best practices
                "azure": MCPRemoteServerConfig(
                    type="http",
                    url=AZURE_MCP_URL,
                    tools=["*"],  # All tools
                ),
                # Microsoft Learn MCP for documentation
                "microsoft-learn": MCPRemoteServerConfig(
                    type="http",
                    url=MICROSOFT_LEARN_MCP_URL,
                    tools=["*"],
                ),
            },
            "system_message": {
                "mode": "append",
                "content": GHCP_CODING_INSTRUCTIONS,
            },
        }

        # Add Azure OpenAI provider configuration if BYOK mode is enabled
        if self._settings.copilot_use_azure_openai:
            if not self._settings.copilot_has_azure_byok_config:
                raise RuntimeError(
                    "Azure OpenAI BYOK mode is enabled but configuration is incomplete. "
                    "Please set COPILOT_AZURE_OPENAI_ENDPOINT and COPILOT_AZURE_OPENAI_API_KEY."
                )
            
            session_config["provider"] = {
                "type": "azure",
                "base_url": self._settings.copilot_azure_openai_endpoint,
                "api_key": self._settings.copilot_azure_openai_api_key,
                "azure": {
                    "api_version": self._settings.copilot_azure_openai_api_version,
                },
            }
            logger.info(
                "Using Azure OpenAI BYOK provider",
                endpoint=self._settings.copilot_azure_openai_endpoint[:50] + "...",
                model=self._settings.copilot_model,
            )

        # Create session with custom tools and MCP servers
        self._session = await self._client.create_session(session_config)
        
        self._started = True
        logger.info(
            "GHCPCodingAgent session created",
            mcp_servers=["azure", "microsoft-learn"],
            model=self._settings.copilot_model,
            byok_mode=self._settings.copilot_use_azure_openai,
        )

    async def run(self, query: str) -> str:
        """
        Process a coding/validation query.

        Args:
            query: User's request for code generation or hypothesis validation.

        Returns:
            Generated response with code, CLI commands, or test plans.
        """
        logger.info(
            "GHCPCodingAgent.run started",
            query_length=len(query),
            query_preview=query[:100] if query else "",
        )
        
        if not self._started:
            logger.debug("GHCPCodingAgent not started, initializing...")
            try:
                await self.start()
            except Exception as e:
                logger.error(
                    "GHCPCodingAgent failed to start",
                    error=str(e),
                    error_type=type(e).__name__,
                )
                raise
        
        if not self._session:
            logger.error("GHCPCodingAgent session is None after start")
            raise RuntimeError("Session not initialized")
        
        # Collect response
        response_parts: list[str] = []
        done = asyncio.Event()
        error_occurred: Exception | None = None
        events_received: list[str] = []
        
        def on_event(event):
            nonlocal error_occurred
            event_type = getattr(event.type, 'value', str(event.type))
            events_received.append(event_type)
            
            logger.debug(
                "GHCPCodingAgent received event",
                event_type=event_type,
            )
            
            if event_type == "assistant.message":
                content = getattr(event.data, 'content', '')
                if content:
                    response_parts.append(content)
                    logger.debug(
                        "GHCPCodingAgent message received",
                        content_length=len(content),
                    )
            elif event_type == "assistant.message_delta":
                # Handle streaming deltas
                content = getattr(event.data, 'content', '')
                if content:
                    response_parts.append(content)
            elif event_type == "session.idle":
                logger.debug("GHCPCodingAgent session idle, completing")
                done.set()
            elif event_type == "error":
                # Capture error events
                error_data = getattr(event, 'data', None)
                error_msg = str(error_data) if error_data else "Unknown error"
                logger.error(
                    "GHCPCodingAgent received error event",
                    error=error_msg,
                )
                error_occurred = RuntimeError(f"Copilot error: {error_msg}")
                done.set()
        
        self._session.on(on_event)
        
        try:
            logger.debug("GHCPCodingAgent sending prompt to session")
            await self._session.send({"prompt": query})
            
            logger.debug("GHCPCodingAgent waiting for response (timeout=120s)")
            await asyncio.wait_for(done.wait(), timeout=120.0)
            
            logger.info(
                "GHCPCodingAgent response completed",
                events_received=len(events_received),
                response_parts=len(response_parts),
                total_length=sum(len(p) for p in response_parts),
            )
            
        except asyncio.TimeoutError:
            logger.warning(
                "GHCPCodingAgent session timed out",
                timeout_seconds=120,
                events_received=events_received,
                response_parts_collected=len(response_parts),
            )
        except Exception as e:
            logger.error(
                "GHCPCodingAgent session error",
                error=str(e),
                error_type=type(e).__name__,
                events_received=events_received,
            )
            raise
        
        # Check for error that occurred during event handling
        if error_occurred:
            logger.error(
                "GHCPCodingAgent error during processing",
                error=str(error_occurred),
            )
            raise error_occurred
        
        result = "".join(response_parts) if response_parts else "No response generated."
        
        if result == "No response generated.":
            logger.warning(
                "GHCPCodingAgent produced empty response",
                events_received=events_received,
                query_preview=query[:100],
            )
        else:
            logger.info(
                "GHCPCodingAgent.run completed successfully",
                response_length=len(result),
            )
        
        return result
    
    async def close(self):
        """Clean up resources."""
        if self._session:
            try:
                await self._session.destroy()
            except Exception as e:
                logger.warning(f"Error destroying session: {e}")
            self._session = None
        
        if self._client:
            try:
                await self._client.stop()
            except Exception as e:
                logger.warning(f"Error stopping client: {e}")
            self._client = None
        
        self._started = False
        logger.info("GHCPCodingAgent closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    def as_tool(self):
        """
        Return agent as a tool for orchestration.
        
        Used by SolutionEngineerAgent to delegate coding queries.
        Note: For Copilot SDK agents, we wrap the run() method.
        """
        agent = self
        
        @ai_function
        async def code(
            query: Annotated[str, "Code generation, CLI command, or hypothesis validation query"]
        ) -> str:
            """Generate code, Azure CLI commands, and validate hypotheses through test deployments."""
            return await agent.run(query)
        
        return code


# =============================================================================
# Factory Function
# =============================================================================

def get_ghcp_coding_agent() -> GHCPCodingAgent:
    """Get a GHCPCodingAgent instance."""
    return GHCPCodingAgent()
