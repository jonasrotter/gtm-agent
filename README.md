# GTM Agent

AI assistant for Azure Solution Engineers. Research docs, get architecture guidance, generate code — all via a unified API.

## Prerequisites

- **Python 3.11+** (tested with 3.11)
- **Azure OpenAI** resource with a deployed model (e.g., `gpt-4o` or `gpt-5.2`)
- **Azure CLI** (optional, for deployment)

## Quick Start

```bash
# Clone repository
git clone https://github.com/jonasrotter/gtm-agent.git
cd gtm-agent

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Run the application
python -m uvicorn src.api.main:app --port 8000
```

**API Docs:** http://localhost:8000/docs

## Features

| Agent | Capability |
|-------|------------|
| 🔍 **Research** | Search Azure docs with citations (Microsoft Learn MCP) |
| 🏗️ **Architecture** | WAF-aligned guidance (Azure MCP) |
| 💻 **Code** | CLI commands, Bicep, Terraform, SDK samples (GitHub Copilot) |

**Smart Routing** — Queries auto-classify to the optimal processing path:

| Type | Example | Behavior |
|------|---------|----------|
| Factual | "What is Blob Storage?" | Direct answer |
| HowTo | "How do I create a VM?" | Research + code |
| Architecture | "Best practices for AKS?" | WAF guidance |
| Code | "Write CLI to deploy App Service" | Code generation |
| Complex | "Design DR architecture + Terraform" | Multi-step orchestration |

## API

```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"content": "What are the storage tiers for Azure Blob?"}'
```

## MCP Server

Also runs as an MCP server at `/mcp/mcp` for:
- GitHub Copilot Chat (VS Code)
- Microsoft 365 Copilot

## Configuration

Create a `.env` file based on `.env.example`:

```env
# Required: Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-5.2

# Optional: API key authentication (leave empty for Azure AD auth via DefaultAzureCredential)
API_KEY=your-api-key-here

# Optional: Azure AD Service Principal (for non-interactive authentication)
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
```

See [.env.example](.env.example) for all available options.

## Project Structure

```
src/
├── agents/       # Orchestrator, Planner, Researcher, Architect, Coder
├── api/          # FastAPI routes
├── mcp/          # MCP server integration
├── models/       # Data models
├── tools/        # Tool implementations
├── utils/        # Utility functions
└── config.py     # Settings
scripts/
├── deploy.ps1    # Azure deployment (Windows)
└── deploy.sh     # Azure deployment (Linux/macOS)
tests/
├── unit/
├── integration/
└── evaluation/   # Automated quality evaluation
```

## Azure Deployment

Deploy to Azure App Service:

```powershell
# Windows
.\scripts\deploy.ps1 -Environment dev

# Linux/macOS
./scripts/deploy.sh dev
```

This deploys the application to `https://gtm-agent-<env>-app.azurewebsites.net`.

## Development

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Quality evaluation
python -m tests.evaluation.evaluation --save-report
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /agent/query` | Main query endpoint |
| `GET /health` | Health check |
| `GET /docs` | OpenAPI documentation |
| `/mcp/mcp` | MCP server (SSE) |

## License

MIT