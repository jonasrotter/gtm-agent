# GTM Agent - Solution Engineering Agent

A multi-agentic AI assistant for Solution Engineers: research Azure docs, get architecture guidance, and generate code/CLI commands. Powered by the **Plan-Execute-Verify (PEV)** pattern with intelligent query classification and parallel execution.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

### Specialized Agents

| Agent | Capability |
|-------|------------|
| 🔍 **ResearcherAgent** | Search Azure docs with citations via Microsoft Learn MCP |
| 🏗️ **ArchitectAgent** | WAF-aligned architecture guidance via Azure MCP |
| 💻 **GHCPCodingAgent** | Generate code, CLI commands, test plans via GitHub Copilot SDK |

### Intelligent Query Classification

| Category | Example | Processing |
|----------|---------|------------|
| **FACTUAL** | "What is Azure Blob Storage?" | Fast path (skip PEV) |
| **HOWTO** | "How do I create a storage account?" | Lite PEV (1 iteration) |
| **ARCHITECTURE** | "Best practices for App Service security" | Standard PEV (2 iterations) |
| **CODE** | "Write Azure CLI to create RG" | Lite PEV (1 iteration) |
| **COMPLEX** | "Design architecture and generate Bicep" | Full PEV (4 iterations) |

### Performance Optimizations

- ⚡ **Query Classification**: Routes simple queries directly to agents, bypassing planning overhead
- 🔀 **Parallel Execution**: Independent plan steps run concurrently via `asyncio.gather()`
- 🎯 **Adaptive Verification**: Threshold-based quality scoring (0.8 acceptance threshold)

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FastAPI /agent/query                       │
├──────────────────────────────────────────────────────────────┤
│                    OrchestratorAgent                          │
│           Plan-Execute-Verify (PEV) Pattern                   │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │ Classifier  │→ │   Planner   │→ │      Executor       │   │
│  │ (routing)   │  │ (planning)  │  │ (parallel exec)     │   │
│  └─────────────┘  └─────────────┘  └──────────┬──────────┘   │
│                                               ↓              │
│                                    ┌─────────────────────┐   │
│                          ←─────────│     Verifier        │   │
│                          (retry)   │ (quality scoring)   │   │
│                                    └─────────────────────┘   │
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
- Azure OpenAI deployment with GPT-5.2

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
├── agents/          # Agent implementations
│   ├── orchestrator.py    # PEV workflow coordinator
│   ├── classifier.py      # Query classification
│   ├── planner.py         # Execution plan generation
│   ├── executor.py        # Parallel step execution
│   ├── verifier.py        # Quality scoring & feedback
│   ├── researcher.py      # Azure docs research
│   ├── architect.py       # Architecture guidance
│   ├── ghcp_coding_agent.py  # Code generation
│   └── solution_engineer.py  # Legacy orchestrator
├── api/             # FastAPI routes and middleware
├── mcp/             # MCP server implementation
├── models/          # Pydantic data models
├── tools/           # Local tool implementations
├── utils/           # Logging, client utilities
└── config.py        # Settings
infra/               # Azure Bicep templates
tests/
├── unit/            # Unit tests
├── integration/     # Integration tests
└── contract/        # Contract tests
```

## Development

```bash
pytest                          # Run tests
pytest --cov=src               # With coverage
pytest tests/unit/             # Unit tests only
ruff check src tests           # Linting
```

### Running Integration Tests

```bash
# Start the server
uvicorn src.api:app --reload

# Run integration tests (in another terminal)
python tests/integration/test_scenarios.py
```

## Azure Deployment

```powershell
.\scripts\deploy.ps1 -AzureOpenAiEndpoint "https://your-openai.openai.azure.com"
```

```bash
./scripts/deploy.sh --endpoint "https://your-openai.openai.azure.com"
```

Deploys: App Service (Linux) + Application Insights + Log Analytics

## How It Works

### Plan-Execute-Verify (PEV) Pattern

1. **Classify**: Analyze query complexity to determine optimal processing path
2. **Plan**: Break down complex queries into discrete, actionable steps
3. **Execute**: Run steps in parallel where dependencies allow
4. **Verify**: Score results against quality dimensions (correctness, completeness, consistency)
5. **Iterate**: If score < 0.8, refine plan and re-execute (up to 4 iterations)

### Query Flow Example

```
User: "Design a high-availability architecture for a web app and generate the Bicep template"

→ Classifier: COMPLEX (multi-part query)
→ Planner: Creates 3 steps:
    1. architecture: "HA design patterns for web apps"
    2. architecture: "WAF recommendations for availability"  
    3. code: "Generate Bicep template implementing the design"
→ Executor: Runs steps 1 & 2 in parallel, then step 3
→ Verifier: Score 0.85 → Accept
→ Response: Architecture guidance + Bicep code
```

## License

MIT License - see [LICENSE](LICENSE)

---

Built with [FastAPI](https://fastapi.tiangolo.com/), [agent-framework](https://pypi.org/project/agent-framework/), and [github-copilot-sdk](https://pypi.org/project/github-copilot-sdk/)