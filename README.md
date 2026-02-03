# GTM Agent

AI assistant for Azure Solution Engineers. Research docs, get architecture guidance, generate code — all via a unified API.

## Quick Start

```bash
git clone https://github.com/jonasrotter/gtm-agent.git && cd gtm-agent
pip install -r requirements.txt
cp .env.example .env  # Configure Azure OpenAI
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

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
API_KEY=optional-api-key
```

## Project Structure

```
src/
├── agents/       # Orchestrator, Planner, Researcher, Architect, Coder
├── api/          # FastAPI routes
├── mcp/          # MCP server
└── config.py     # Settings
tests/
├── unit/
├── integration/
└── evaluation/   # Automated quality evaluation
```

## Development

```bash
pytest                    # Run tests
python -m tests.evaluation.evaluation --save-report  # Quality eval
```

## License

MIT