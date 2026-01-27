# GTM Agent - Solution Engineering Agent

A multi-agentic AI assistant for Solution Engineers: research Azure docs, get architecture guidance, and generate code/CLI commands.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

| Agent | Capability |
|-------|------------|
| 🔍 **ResearcherAgent** | Search Azure docs with citations via Microsoft Learn MCP |
| 🏗️ **ArchitectAgent** | WAF-aligned architecture guidance via Azure MCP |
| 💻 **GHCPCodingAgent** | Generate code, CLI commands, test plans via GitHub Copilot SDK |

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FastAPI /agent/query                       │
├──────────────────────────────────────────────────────────────┤
│              SolutionEngineerAgent (Orchestrator)             │
│     Routes queries to specialized agents based on intent      │
├────────────────┬─────────────────┬───────────────────────────┤
│ ResearcherAgent│  ArchitectAgent │     GHCPCodingAgent       │
│ +McpServerTool │  +McpServerTool │     +CopilotSDK           │
├────────────────┴─────────────────┴───────────────────────────┤
│                     MCP Servers                               │
│  • Microsoft Learn: learn.microsoft.com/api/mcp              │
│  • Azure MCP: api.mcp.github.com                             │
└──────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Clone and setup
git clone https://github.com/jonasrotter/gtm-agent.git && cd gtm-agent
python -m venv .venv && .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure and run
cp .env.example .env  # Edit with your Azure OpenAI settings
uvicorn src.api:app --reload
```

**Access:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Prerequisites

- Python 3.11+
- Azure OpenAI deployment with GPT-4o

## API Usage

**POST /agent/query** - Unified endpoint with automatic routing

```bash
curl -X POST http://localhost:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"content": "What are Azure Cosmos DB scaling limits?"}'
```

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/agent/query" -Method Post `
  -ContentType "application/json" -Body '{"content": "What are Azure Cosmos DB scaling limits?"}'
```

## MCP Server Mode

The agent also acts as an MCP Server at `/mcp/mcp` for integration with:
- GitHub Copilot Chat (VS Code Agent mode)
- Microsoft 365 Copilot (via Agents Toolkit or Copilot Studio)

**Tools:** `research`, `architecture`, `code`, `ask_solution_engineer`

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | ✅ |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name | Default: `gpt-4o` |
| `API_KEY` | API authentication key | Optional |

<details>
<summary>GitHub Copilot SDK Settings (for code generation)</summary>

| Variable | Description |
|----------|-------------|
| `COPILOT_USE_AZURE_OPENAI` | Use Azure OpenAI as LLM provider (BYOK) |
| `COPILOT_AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint for BYOK |
| `COPILOT_AZURE_OPENAI_API_KEY` | API key for BYOK mode |

</details>

## Project Structure

```
src/
├── agents/          # ResearcherAgent, ArchitectAgent, GHCPCodingAgent
├── api/             # FastAPI routes and middleware
├── mcp/             # MCP server implementation
├── models/          # Pydantic data models
└── config.py        # Settings
infra/               # Azure Bicep templates
tests/               # Unit, integration, contract tests
```

## Development

```bash
pytest                          # Run tests
pytest --cov=src               # With coverage
ruff check src tests           # Linting
```

## Azure Deployment

```powershell
.\scripts\deploy.ps1 -AzureOpenAiEndpoint "https://your-openai.openai.azure.com"
```

```bash
./scripts/deploy.sh --endpoint "https://your-openai.openai.azure.com"
```

Deploys: App Service (Linux) + Application Insights + Log Analytics

## License

MIT License - see [LICENSE](LICENSE)

---

Built with [FastAPI](https://fastapi.tiangolo.com/), [semantic-kernel](https://pypi.org/project/semantic-kernel/), and [github-copilot-sdk](https://pypi.org/project/github-copilot-sdk/)