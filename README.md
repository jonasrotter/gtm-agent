# GTM Agent - Solution Engineering Agent

A multi-agentic AI assistant that helps Solution Engineers by researching Azure documentation, sharing architecture best practices, and validating hypotheses through Azure deployments.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-118%20passed-brightgreen.svg)]()

## Features

### 🔍 Research Capability 
- Search Azure documentation with source citations via Microsoft Learn MCP
- Distinguish between GA, Preview, and Deprecated features
- Compare Azure services with detailed analysis
- Access Microsoft Learn, Azure Architecture Center, and official docs

### 🏗️ Architecture Guidance 
- Azure Well-Architected Framework (WAF) aligned recommendations via Azure MCP
- Architecture best practices and recommendations
- Pillar-specific guidance (Reliability, Security, Cost, Operational Excellence, Performance)

### 💻 Code & CLI Generation 
- Generate Azure CLI commands with best practices via GitHub Copilot SDK
- Create test plans for hypothesis validation
- Intelligent code generation with MCP-powered context

## Agentic Architecture

The GTM Agent uses a **simplified single-layer architecture** powered by [agent-framework](https://pypi.org/project/agent-framework/) and [github-copilot-sdk](https://pypi.org/project/github-copilot-sdk/). Each specialized agent uses `ChatAgent` with `HostedMCPTool` for direct MCP server integration.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FastAPI Application                                  │
│                            /agent/query                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                      SolutionEngineerAgent                                   │
│                        (Orchestrator)                                        │
│    ┌─────────────────────────────────────────────────────────────────┐      │
│    │  ChatAgent with sub-agents as tools via .as_tool() pattern      │      │
│    │  • Query classification (research/architecture/code)            │      │
│    │  • Azure-scope validation (rejects non-Azure queries)           │      │
│    │  • Intelligent routing to specialized sub-agents                │      │
│    └─────────────────────────────────────────────────────────────────┘      │
│                              │                                               │
│         ┌────────────────────┼────────────────────┐                         │
│         ▼                    ▼                    ▼                          │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                    │
│  │ Researcher  │     │  Architect  │     │GHCPCoding   │                    │
│  │   Agent     │     │    Agent    │     │   Agent     │                    │
│  │             │     │             │     │             │                    │
│  │ ChatAgent + │     │ ChatAgent + │     │ CopilotSDK  │                    │
│  │HostedMCPTool│     │HostedMCPTool│     │ @define_tool│                    │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘                    │
│         │                   │                   │                            │
│         ▼                   ▼                   ▼                            │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                    MCP Servers (Direct Integration)              │        │
│  │  • Microsoft Learn MCP (https://learn.microsoft.com/api/mcp)    │        │
│  │  • Azure MCP (https://api.mcp.github.com)                       │        │
│  │  • GitHub Copilot SDK with custom @define_tool functions        │        │
│  └─────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### How the Agents Work Together

1. **Query Intake**: User submits a query to `/agent/query`
2. **Orchestration**: `SolutionEngineerAgent` classifies the query using its `ChatAgent`
3. **Tool Routing**: Query is routed via `.as_tool()` to the appropriate sub-agent:
   - `research` tool → `ResearcherAgent` (Microsoft Learn MCP)
   - `architecture` tool → `ArchitectAgent` (Azure MCP)
   - `code` tool → `GHCPCodingAgent` (GitHub Copilot SDK)
4. **MCP Execution**: Sub-agents use `HostedMCPTool` or Copilot SDK for direct MCP integration
5. **Response**: Results are returned with sources, recommendations, or generated code

## MCP Server Integration

The GTM Agent can also act as an **MCP Server**, allowing integration with:
- **Microsoft 365 Copilot Chat** (via Copilot Studio or Agents Toolkit)
- **GitHub Copilot Chat** (Agent mode in VS Code)
- Any MCP-compatible client

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `research` | Search Azure documentation with source citations |
| `architecture` | Azure architecture guidance and WAF recommendations |
| `code` | Generate code, CLI commands, Bicep templates |
| `ask_solution_engineer` | Main entry point with intelligent routing |

### MCP Endpoint

```
http://localhost:8000/mcp/mcp
```

### Using with GitHub Copilot Chat (VS Code)

1. Start the server: `uvicorn src.api:app --reload`
2. Open VS Code with Copilot Chat
3. In Agent mode, add MCP server with URL: `http://localhost:8000/mcp/mcp`
4. Ask questions like "Use solution-engineer to explain Azure Functions"

### Using with M365 Copilot

See the [M365 Copilot Integration Guide](#m365-copilot-integration) below.

## Quick Start

### Prerequisites

- Python 3.11+
- Azure CLI (optional, for CLI execution)
- Azure subscription (optional, for resource deployment)
- Azure OpenAI deployment with GPT-4o model

> **Note**: The agents use MCP (Model Context Protocol) servers for real-time access to Azure documentation and best practices:
> - **Microsoft Learn MCP**: `https://learn.microsoft.com/api/mcp`
> - **Azure MCP**: `https://api.mcp.github.com`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jonasrotter/gtm-agent.git
   cd gtm-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
   # For development
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure configuration
   ```

5. **Run the server**
   ```bash
   uvicorn src.api:app --reload
   ```

6. **Access the API**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## API Endpoints

### Agent Query (Primary Endpoint)
```bash
POST /agent/query
```
Unified endpoint for all query types. The `SolutionEngineerAgent` automatically routes queries to the appropriate sub-agent based on intent:
- **Research queries** → `ResearcherAgent` (documentation, "how to", "what is")
- **Architecture queries** → `ArchitectAgent` (best practices, design, WAF)
- **Code/CLI queries** → `GHCPCodingAgent` (generate code, CLI commands, test plans)

**Request:**
```json
{
  "content": "Your question about Azure...",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "content": "Agent response...",
  "processing_time_ms": 1234,
  "session_id": "optional-session-id"
}
```

### Health Check
```bash
GET /health           # Application health
GET /agent/health     # Agent-specific health
```

## Usage Examples

### 🔍 ResearcherAgent - Documentation & Knowledge

The ResearcherAgent helps you find accurate, sourced information from official Azure documentation. It uses `HostedMCPTool` to directly integrate with the Microsoft Learn MCP server:

- `microsoft_docs_search` - Search Microsoft Learn and Azure docs
- `microsoft_docs_fetch` - Retrieve full document content  
- `microsoft_code_sample_search` - Find code examples

**Agentic Workflow:**
```
User Query → SolutionEngineerAgent → routes to research tool
                                           ↓
                              ResearcherAgent.run(query)
                                           ↓
                              HostedMCPTool calls Microsoft Learn MCP
                                           ↓
                              Synthesizes response with sources
```

**Example - Research Query:**

*Linux/macOS (bash):*
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"content": "What are the scaling limits for Azure Cosmos DB and when should I use provisioned vs serverless?"}'
```

*Windows (PowerShell):*
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/agent/query" -Method Post `
  -ContentType "application/json" `
  -Body '{"content": "What are the scaling limits for Azure Cosmos DB and when should I use provisioned vs serverless?"}'
```

**Response includes:**
- Direct answer with specific limits (RU/s, storage, etc.)
- Feature status (GA, Preview, Deprecated)
- Source citations from Microsoft Learn
- Comparison table for provisioned vs serverless

---

### 🏗️ ArchitectAgent - Best Practices & Reviews

The ArchitectAgent provides architecture guidance aligned with Azure Well-Architected Framework. It uses `HostedMCPTool` to directly integrate with the Azure MCP server for best practices and recommendations.

**WAF Pillars Focus:**
- Reliability
- Security  
- Cost Optimization
- Operational Excellence
- Performance Efficiency

**Agentic Workflow:**
```
User Query → SolutionEngineerAgent → routes to architecture tool
                                           ↓
                              ArchitectAgent.run(query)
                                           ↓
                              HostedMCPTool calls Azure MCP
                                           ↓
                              Generates WAF-aligned recommendations
```

**Example - Architecture Review:**

*Linux/macOS (bash):*
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"content": "Review my architecture: Azure App Service frontend, Azure Functions for APIs, Cosmos DB for data, and Blob Storage for files. We expect 50,000 daily active users."}'
```

*Windows (PowerShell):*
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/agent/query" -Method Post `
  -ContentType "application/json" `
  -Body '{"content": "Review my architecture: Azure App Service frontend, Azure Functions for APIs, Cosmos DB for data, and Blob Storage for files. We expect 50,000 daily active users."}'
```

**Response includes:**
- WAF pillar alignment and recommendations
- Architecture best practices for your scenario
- Specific guidance for each Azure service
- Links to Azure Architecture Center patterns

---

### 💻 GHCPCodingAgent - Code & CLI Generation

The GHCPCodingAgent generates code, Azure CLI commands, and test plans using the GitHub Copilot SDK. It uses custom tools defined with `@define_tool`:

- `create_test_plan` - Create comprehensive test plans for hypothesis validation
- `generate_cli_command` - Generate Azure CLI commands with best practices
- `execute_cli_command` - Execute CLI commands with safety checks

**Agentic Workflow:**
```
User Request → SolutionEngineerAgent → routes to code tool
                                            ↓
                              GHCPCodingAgent.run(query)
                                            ↓
                              CopilotSession with MCP servers:
                                • Azure MCP for best practices
                                • Microsoft Learn MCP for documentation
                                            ↓
                              Custom @define_tool functions execute
                                            ↓
                              Returns generated code/CLI/test plan
```

**Example - Code Generation:**

*Linux/macOS (bash):*
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"content": "Generate Azure CLI commands to create a Function App with Premium plan and Application Insights"}'
```

*Windows (PowerShell):*
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/agent/query" -Method Post `
  -ContentType "application/json" `
  -Body '{"content": "Generate Azure CLI commands to create a Function App with Premium plan and Application Insights"}'
```

**Response:**
```json
{
  "content": "## Azure CLI Commands\n\n```bash\n# Create resource group\naz group create --name myapp-rg --location eastus\n\n# Create Application Insights\naz monitor app-insights component create \\\n  --app myapp-insights \\\n  --location eastus \\\n  --resource-group myapp-rg\n\n# Create storage account (required for Functions)\naz storage account create \\\n  --name myappstore \\\n  --resource-group myapp-rg \\\n  --sku Standard_LRS\n\n# Create Function App with Premium plan\naz functionapp plan create \\\n  --name myapp-plan \\\n  --resource-group myapp-rg \\\n  --sku EP1 \\\n  --is-linux\n\naz functionapp create \\\n  --name myapp-func \\\n  --resource-group myapp-rg \\\n  --plan myapp-plan \\\n  --storage-account myappstore \\\n  --runtime python \\\n  --app-insights myapp-insights\n```\n\n**Best Practices Applied:**\n- Premium plan (EP1) for production workloads\n- Application Insights for monitoring\n- Separate resource group for organization",
  "processing_time_ms": 2341
}
```

**Example - Test Plan Creation:**

*Linux/macOS (bash):*
```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"content": "Create a test plan to validate that Azure Functions Premium can handle 1000 concurrent requests with P95 latency under 200ms"}'
```

*Windows (PowerShell):*
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/agent/query" -Method Post `
  -ContentType "application/json" `
  -Body '{"content": "Create a test plan to validate that Azure Functions Premium can handle 1000 concurrent requests with P95 latency under 200ms"}'
```

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models_hypothesis.py -v
```

### Code Quality
```bash
# Linting
ruff check src tests

# Formatting
ruff format src tests

# Type checking
mypy src
```

### Project Structure
```
gtm-agent/
├── src/
│   ├── agents/           # AI agents with direct MCP integration
│   │   ├── __init__.py   # Agent exports
│   │   ├── base.py       # Helpers: create_azure_chat_client(), MCP URLs
│   │   ├── researcher.py # ResearcherAgent with HostedMCPTool (Microsoft Learn)
│   │   ├── architect.py  # ArchitectAgent with HostedMCPTool (Azure MCP)
│   │   ├── ghcp_coding_agent.py  # GHCPCodingAgent with GitHub Copilot SDK
│   │   └── solution_engineer.py  # Orchestrator using .as_tool() pattern
│   ├── api/              # FastAPI application
│   │   ├── main.py       # Application factory
│   │   ├── middleware.py # Request logging, error handling
│   │   ├── dependencies.py # Dependency injection
│   │   └── routes/       # API endpoint handlers
│   │       └── agent.py  # /agent/query endpoint
│   ├── lib/              # Shared utilities
│   │   ├── agent_client.py  # AzureOpenAIChatClient implementation
│   │   ├── logging.py    # Structured logging
│   │   └── errors.py     # Custom exception classes
│   └── models/           # Pydantic data models
├── tests/
│   ├── unit/             # Unit tests for agents and models
│   ├── integration/      # Integration tests
│   └── contract/         # API contract tests
├── specs/                # Specification documents
└── .github/              # CI/CD workflows
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Required |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name | `gpt-4o` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-02-15-preview` |
| `API_KEY` | API authentication key | None (disabled) |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FORMAT` | Log format (`json` or `console`) | `json` |
| `AZURE_SUBSCRIPTION_ID` | For hypothesis validation | Optional |

## Framework Integration

This project uses two key frameworks:

### agent-framework (PyPI)
- `ChatAgent` - LLM-powered agent with tool calling capabilities
- `HostedMCPTool` - Direct integration with MCP servers (no custom adapters needed)
- `@ai_function` - Decorator to create tools from Python functions
- `BaseChatClient` - Protocol for custom LLM clients (Azure OpenAI)

### github-copilot-sdk (PyPI)
- `CopilotClient` - Manages Copilot CLI process lifecycle
- `CopilotSession` - Interactive sessions with MCP server configuration
- `@define_tool` - Decorator for creating custom tools with Pydantic models
- `MCPRemoteServerConfig` - Configure remote MCP servers for sessions
- Used by `GHCPCodingAgent` for intelligent code and CLI generation

## Key Design Principles

- **Single-layer architecture**: Agents directly integrate with MCP servers via `HostedMCPTool`
- **Sub-agents as tools**: Orchestrator uses `.as_tool()` pattern for clean routing
- **Direct MCP integration**: No intermediate service or tool layers
- **Type-safe custom tools**: `@define_tool` with Pydantic models for GitHub Copilot SDK
- **SC-007**: Non-Azure query rejection with helpful messaging

## Azure Deployment

Deploy the GTM Agent to Azure App Service for production use. The deployment includes:
- **Azure App Service** (Linux, Python 3.11)
- **Application Insights** for monitoring
- **Log Analytics** for centralized logging
- **Managed Identity** for secure authentication

### Prerequisites

- Azure CLI installed and logged in (`az login`)
- Azure subscription with Contributor access
- Azure OpenAI resource with GPT-4o deployment
- Python 3.11+ installed locally (for creating deployment packages)

### Important: ZIP Package Format

When deploying from Windows, the deployment scripts use Python to create ZIP files with Unix-style path separators (forward slashes). This is required because Azure App Service runs on Linux and expects Unix paths in the archive.

### Quick Deploy (PowerShell)

```powershell
# Deploy to development environment
.\scripts\deploy.ps1 -AzureOpenAiEndpoint "https://your-openai.openai.azure.com"

# Deploy to production with higher SKU
.\scripts\deploy.ps1 -Environment prod -Sku P1V3 -AzureOpenAiEndpoint "https://your-openai.openai.azure.com"
```

### Quick Deploy (Bash)

```bash
# Deploy to development environment
./scripts/deploy.sh --endpoint "https://your-openai.openai.azure.com"

# Deploy to production with higher SKU
./scripts/deploy.sh --environment prod --sku P1V3 --endpoint "https://your-openai.openai.azure.com"
```

### GitHub Actions CI/CD

For automated deployments, configure GitHub Actions:

1. **Create Service Principal**:
   ```bash
   az ad sp create-for-rbac --name "gtm-agent-deploy" --role contributor \
     --scopes /subscriptions/{subscription-id} --sdk-auth
   ```

2. **Add GitHub Secrets**:
   | Secret | Description |
   |--------|-------------|
   | `AZURE_CREDENTIALS` | JSON output from step 1 |
   | `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID |
   | `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL |
   | `API_KEY` | (Optional) API key for authentication |

3. **Trigger Deployment**:
   - Push to `main` branch for automatic deployment
   - Use workflow dispatch for manual deployment with environment selection

### Infrastructure Files

| File | Description |
|------|-------------|
| `infra/main.bicep` | Main Bicep template |
| `infra/modules/appservice.bicep` | App Service configuration |
| `infra/modules/monitoring.bicep` | Application Insights + Log Analytics |
| `infra/parameters.json` | Default parameter values |
| `app.py` | Entry point that sets up PYTHONPATH for Oryx |
| `gunicorn.conf.py` | Gunicorn configuration |

### Deployment Architecture

The deployment uses Azure App Service with Oryx build system:

1. **Build Phase**: Oryx detects Python from `requirements.txt` and creates a virtual environment
2. **Runtime**: Oryx extracts the compressed app to a temp directory (`/tmp/xxxx`)
3. **Startup**: `app.py` dynamically adds the extraction directory to `sys.path` so `src` module can be imported
4. **Server**: Gunicorn starts with Uvicorn workers for async FastAPI support

### Endpoints After Deployment

| Endpoint | URL |
|----------|-----|
| Web App | `https://gtm-agent-{env}-app.azurewebsites.net` |
| MCP Server | `https://gtm-agent-{env}-app.azurewebsites.net/mcp/mcp` |
| Health Check | `https://gtm-agent-{env}-app.azurewebsites.net/health` |
| API Docs | `https://gtm-agent-{env}-app.azurewebsites.net/docs` |

### View Logs

```bash
az webapp log tail --resource-group rg-gtm-agent-dev --name gtm-agent-dev-app
```

## M365 Copilot Integration

The Solution Engineer Agent can be integrated with Microsoft 365 Copilot Chat through several options:

### Option 1: Microsoft 365 Agents Toolkit (Recommended)

For direct integration with M365 Copilot Chat in Teams/Outlook:

1. **Prerequisites**: VS Code + M365 Agents Toolkit 6.3+, M365 Developer License
2. **Deploy** the GTM Agent to Azure (App Service, Container Apps, or Functions)
3. **Create** a declarative agent using Agents Toolkit pointing to your MCP endpoint
4. **Sideload/Deploy** to M365 Copilot

### Option 2: Copilot Studio + Power Apps Custom Connector

For enterprise governance via Copilot Studio:

1. **Deploy** to Azure with HTTPS endpoint
2. **Create** Entra App Registrations (Client + Server) for OAuth 2.0
3. **Configure** Power Apps Custom Connector with MCP swagger schema:
   ```yaml
   paths:
     /:
       post:
         x-ms-agentic-protocol: mcp-streamable-1.0
   ```
4. **Add** connector as tool in Copilot Studio agent

### Option 3: Azure Functions Self-Hosted

For serverless hosting with pay-per-use billing:

1. **Add** Azure Functions configuration files to the project
2. **Deploy** to Flex Consumption plan
3. **Connect** via Copilot Studio or Agents Toolkit

### MCP Server Configuration

The MCP server exposes the Streamable HTTP endpoint at `/mcp/mcp`. Key features:

- **Transport**: Streamable HTTP (SSE deprecated after Aug 2025)
- **Tools**: 4 tools (research, architecture, code, ask_solution_engineer)
- **Multi-turn**: Supports session continuity via `session_id` parameter
- **Auth**: Configure API Key or OAuth 2.0 based on hosting option

For detailed Microsoft documentation, see:
- [Build plugins from an MCP server for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/build-mcp-plugins)
- [Deploy remote MCP Server for Copilot Studio](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/how-to/deploy-remote-mcp-server-copilot-studio)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Jonas Rotter**

---

Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), and [Azure AI](https://azure.microsoft.com/en-us/products/ai-services/)